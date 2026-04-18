from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse
from .models import Book
from .serializers import BookSerializer
from .rag import load_books_into_db, query_books, model, collection
import requests

cache = {}


def home(request):
    return HttpResponse("AI Book API is running 🚀")


def load_rag(request):
    books = Book.objects.all()
    load_books_into_db(books)
    return HttpResponse("RAG data loaded successfully")


def build_prompt(context, question):
    return f"""
Answer the question using ONLY this context.

Context:
{context}

Question: {question}

Answer in 2-3 sentences.
"""


@api_view(['GET', 'POST'])
def books(request):
    if request.method == 'GET':
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = BookSerializer(data=request.data)

        if serializer.is_valid():
            book = serializer.save()
            load_books_into_db([book])
            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)


@api_view(['POST'])
def upload_book(request):
    serializer = BookSerializer(data=request.data)

    if serializer.is_valid():
        book = serializer.save()

        load_books_into_db([book])

        return Response({
            "message": "Book uploaded & processed",
            "data": serializer.data
        }, status=201)

    return Response(serializer.errors, status=400)


@api_view(['GET', 'PUT'])
def book_detail(request, id):
    book = get_object_or_404(Book, id=id)

    if request.method == 'GET':
        serializer = BookSerializer(book)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = BookSerializer(book, data=request.data)

        if serializer.is_valid():
            updated_book = serializer.save()
            load_books_into_db([updated_book])
            return Response(serializer.data)

        return Response(serializer.errors, status=400)


@api_view(['GET'])
def recommend_books(request, id):
    book = get_object_or_404(Book, id=id)

    query_embedding = model.encode(book.description or "").tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=6
    )

    metadatas = results.get("metadatas", [[]])
    metadatas = metadatas[0] if metadatas else []

    recommended_titles = list(set([
        meta.get("title")
        for meta in metadatas
        if meta.get("title")
    ]))

    recommendations = Book.objects.filter(
        title__in=recommended_titles
    ).exclude(id=id)[:5]

    serializer = BookSerializer(recommendations, many=True)

    return Response(serializer.data)


@api_view(['POST'])
def ask_question(request):
    question = request.data.get("question")

    if not question:
        return Response(
            {"error": "Question is required"},
            status=400
        )

    if question in cache:
        return Response(cache[question])

    results = query_books(question)

    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]

    context = "\n".join(documents[:2])

    sources = [
        {
            "title": meta.get("title"),
            "snippet": doc[:120]
        }
        for meta, doc in zip(metadatas, documents[:2])
    ]

    prompt = build_prompt(context, question)

    try:
        response = requests.post(
            "http://localhost:1234/v1/chat/completions",
            json={
                "model": "phi-3-mini-4k-instruct",
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "temperature": 0.7,
                "max_tokens": 100
            }
        )

        data = response.json()

        answer = data.get(
            "choices",
            [{}]
        )[0].get(
            "message",
            {}
        ).get(
            "content",
            ""
        )

        if not answer:
            answer = "No response generated"

    except Exception:
        answer = "Error generating response"

    result = {
        "question": question,
        "answer": answer,
        "sources": sources
    }

    cache[question] = result

    return Response(result)


print("CHROMA COUNT:", collection.count())