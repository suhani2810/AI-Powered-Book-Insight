**📚 AI-Powered Book Intelligence Platform**

**🚀 Overview**

This project is a full-stack AI-powered document intelligence system that scrapes book data, stores it in a structured database, and enables intelligent question answering using a RAG (Retrieval-Augmented Generation) pipeline.

**💻 Live Demo (How it works)**

1. Scrape books using Selenium  
2. Books stored in backend database  
3. AI generates summaries  
4. User asks a question  
5. System retrieves relevant books (ChromaDB)  
6. LLM generates contextual answer  

➡️ Example Query:
"What is Sapiens about?"

➡️ Output:
"Provides a historical narrative of human evolution..."

Users can:
Browse books
View detailed book information
Ask natural language questions about books
Get AI-generated answers with sources
Receive book recommendations

**🧠 Design Decisions**

- Used LM Studio instead of OpenAI to avoid API costs and ensure offline capability
- Implemented RAG instead of simple keyword search for better contextual answers
- Used ChromaDB for fast semantic similarity search
- Added caching to reduce repeated LLM calls

**🧠 Key Features**

📖 Automated book scraping using Selenium
🗄️ Book metadata storage in Django + MySQL/SQLite
🔎 Semantic search using embeddings (Sentence Transformers)
🧠 RAG pipeline using ChromaDB vector database
🤖 AI-powered answers using local LLM (LM Studio)
📌 Book recommendations based on similarity search
⚡ Response caching for faster repeated queries
🎨 Responsive frontend built with Next.js + Tailwind CSS

**🏗️ Tech Stack**

*🔧 Backend*
Django
Django REST Framework
Python
SQLite / MySQL
Requests

*🧠 AI / RAG Pipeline*
SentenceTransformers (all-MiniLM-L6-v2)
ChromaDB (Vector Database)
LM Studio (Local LLM - Mistral / Phi-3)
Retrieval-Augmented Generation (RAG)

*🕷️ Automation*
Selenium (Web scraping)
ChromeDriver

*🎨 Frontend*
Next.js (React)
TypeScript
Tailwind CSS
Axios

**🧩 System Architecture**

Scraper (Selenium)
        ↓
Django Backend (API Layer)
        ↓
Database (Books Metadata)
        ↓
Embeddings (Sentence Transformers)
        ↓
Vector DB (ChromaDB)
        ↓
RAG Retrieval System
        ↓
LM Studio LLM (Answer Generation)
        ↓
Frontend (Next.js UI)

**📡 API Endpoints**

📘 Books
Method	Endpoint	Description
GET	/books/	Get all books
POST	/books/	Add new book
GET	/books/<id>/	Get book details
PUT	/books/<id>/	Update book

🤖 AI / RAG
Method	Endpoint	Description
POST	/ask-question/	Ask AI question
GET	/books/<id>/recommend/	Get similar books
GET	/load-rag/	Load embeddings into vector DB
POST	/upload-book/	Upload + process book

**🧪 Sample Questions**
What is this book about?
Recommend books similar to mystery genre
Summarize the book description
Which books are best for fiction lovers?

**⚙️ Setup Instructions**

*1️⃣ Clone Repository*
git clone https://github.com/your-username/AI-Powered-Book-Insight.git
cd AI-Powered-Book-Insight

*2️⃣ Start LM Studio (IMPORTANT FIRST)*
Open LM Studio
Load model:
phi-3-mini-4k-instruct (recommended)
Start local server:
http://localhost:1234

*3️⃣ Backend Setup*
cd ai_book_project
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

Run migrations:
python manage.py makemigrations
python manage.py migrate

Start server:

python manage.py runserver

*4️⃣ Load RAG Data*
GET http://127.0.0.1:8000/load-rag/

👉 This step:
Generates embeddings
Stores data in ChromaDB

*5️⃣ Run Scraper*
python scraper.py

*6️⃣ Frontend Setup*
cd frontend
npm install
npm run dev

Frontend runs at:
http://localhost:3000

*7️⃣ Verify Everything Works*
Open frontend
Ask:
"What is Sapiens about?"

**📊 Example Flow**
User asks:
"Recommend me books like mystery novels"

System:
Converts query → embedding
Searches ChromaDB
Retrieves relevant book chunks
Sends context to LLM

Output:
AI-generated answer
Source books shown

**💡 Key Improvements Implemented**
Overlapping chunking for better retrieval
Embedding-based semantic search
Cached responses for faster queries
Structured prompt engineering
Clean REST API design
Responsive frontend UI

**📷 Screenshots**

Dashboard
<img width="1919" height="1126" alt="Screenshot 2026-04-18 164927" src="https://github.com/user-attachments/assets/9904c382-5c96-4b4f-9f27-008ea8dd3b45" />

Book Detail Page
<img width="1919" height="1125" alt="Screenshot 2026-04-18 165015" src="https://github.com/user-attachments/assets/726bf09c-7c98-4d05-bdce-f8816e9a4b16" />

Q&A Interface
<img width="1919" height="1127" alt="Screenshot 2026-04-18 164906" src="https://github.com/user-attachments/assets/c599927a-49d5-483b-a49a-3e433dc621e8" />

**⚠️ Challenges Faced**

1. Slow AI response time  
   → Solved using caching + limited batch processing  

2. ChromeDriver compatibility issues  
   → Fixed by matching browser version  

3. Large context handling in RAG  
   → Used chunking strategy with overlap  

4. API failures during scraping  
   → Added error handling and retries

**🚀 Future Improvements**

- Async processing using Celery
- Deploy using Docker
- Add authentication system
- Improve RAG with hybrid search (BM25 + embeddings)

**⚠️ Notes**
Ensure LM Studio is running before asking questions
First RAG load may take time (/load-rag/)
ChromeDriver version must match Chrome browser

**👨‍💻 Author**
Built as part of Frontend/Backend AI Internship Assignment

⭐ If you like this project

Give it a star ⭐ on GitHub

