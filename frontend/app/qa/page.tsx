"use client";

import { useState } from "react";
import axios from "axios";
import Navbar from "../components/Navbar";

export default function QA() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const askQuestion = async () => {
    if (!question) return;

    setLoading(true);

    try {
      const res = await axios.post(
        "http://127.0.0.1:8000/ask-question/",
        { question }
      );

      setAnswer(res.data);

    } catch (err) {
      console.error(err);
    }

    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />

      <div className="max-w-3xl mx-auto p-6">

        <h1 className="text-2xl font-bold mb-4 text-gray-800">
          🤖 Ask About Books
        </h1>

        <input
          className="border rounded-lg p-3 w-full focus:outline-none focus:ring-2 focus:ring-blue-500"
          placeholder="Ask a question..."
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
        />

        <button
          onClick={askQuestion}
          disabled={loading}
          className="mt-3 bg-blue-600 hover:bg-blue-700 text-white px-5 py-2 rounded-lg disabled:opacity-50"
        >
          {loading ? "Thinking..." : "Ask"}
        </button>

        {!answer && !loading && (
          <p className="text-gray-400 mt-4">
            Ask something about books
          </p>
        )}

        {answer && (
          <div className="mt-6 bg-white p-5 rounded-2xl shadow-md">
            <p className="text-gray-800">
              <strong>Answer:</strong> {answer.answer}
            </p>

            <div className="mt-4">
              <strong>Sources:</strong>

              <ul className="list-disc ml-5 text-gray-600">
                {answer.sources.map((s: any, i: number) => (
                  <li key={i}>
                    <strong>{s.title}</strong>
                    <div className="text-sm">
                      {s.snippet}...
                    </div>
                  </li>
                ))}
              </ul>

            </div>
          </div>
        )}

      </div>
    </div>
  );
}