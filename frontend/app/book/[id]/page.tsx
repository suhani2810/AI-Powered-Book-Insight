"use client";

import { useEffect, useState } from "react";
import axios from "axios";
import Navbar from "../../components/Navbar";
import { useParams } from "next/navigation";
import Link from "next/link";

export default function BookDetail() {
  const { id } = useParams();

  const [book, setBook] = useState<any>(null);
  const [recommendations, setRecommendations] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!id) return;

    axios.get(`http://127.0.0.1:8000/books/${id}/`)
      .then(res => setBook(res.data));

    axios.get(`http://127.0.0.1:8000/books/${id}/recommend/`)
      .then(res => setRecommendations(res.data))
      .finally(() => setLoading(false));

  }, [id]);

  if (loading) return <p className="p-6">Loading...</p>;
  if (!book) return <p className="p-6">Book not found</p>;

  return (
    <div className="min-h-screen bg-gray-50">
  <Navbar />

  <div className="max-w-4xl mx-auto p-6 bg-white mt-6 rounded-2xl shadow-md">

    <h1 className="text-3xl font-bold text-gray-800 mb-2">
      {book.title}
    </h1>

    <p className="text-yellow-600 font-medium mb-4">
      ⭐ {book.rating}
    </p>

    <p className="text-gray-700 mb-6">
      {book.description}
    </p>

    <div className="mb-6">
      <h2 className="font-semibold text-lg mb-1">🧠 Summary</h2>
      <p className="text-gray-600">{book.summary}</p>
    </div>

    <div className="mb-6">
      <h2 className="font-semibold text-lg mb-1">🎯 Genre</h2>
      <p className="text-gray-600">{book.genre}</p>
    </div>

    <a
      href={book.link}
      target="_blank"
      className="text-blue-600 hover:underline"
    >
      🔗 View Original Book
    </a>

    <div className="mt-8">
      <h2 className="font-semibold text-lg mb-3">📚 Recommendations</h2>

      <ul className="space-y-2">
        {recommendations.map((rec) => (
          <li key={rec.id}>
            <Link
              href={`/book/${rec.id}`}
              className="text-blue-600 hover:underline"
            >
              {rec.title}
            </Link>
          </li>
        ))}
      </ul>
    </div>
  </div>
</div>
);
}