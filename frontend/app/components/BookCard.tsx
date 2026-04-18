"use client";

import Link from "next/link";

export default function BookCard({ book }: any) {
  if (!book) return null;

  return (
    <div className="bg-white rounded-2xl shadow-md p-5 hover:shadow-xl transition duration-300 border border-gray-100">
      
      <h2 className="text-lg font-semibold text-gray-800 mb-1">
        <Link href={`/book/${book.id}`} className="hover:text-blue-600">
          {book.title}
        </Link>
      </h2>

      <p className="text-sm text-yellow-600 font-medium mb-2">
        ⭐ {book.rating}
      </p>

      <p className="text-sm text-gray-600 line-clamp-3">
        {book.description}
      </p>

      <div className="mt-4 flex justify-between items-center">
        <Link
          href={`/book/${book.id}`}
          className="text-sm text-blue-600 font-medium hover:underline"
        >
          View Details →
        </Link>

        <a
          href={book.link}
          target="_blank"
          className="text-sm text-green-600 font-medium hover:underline"
        >
          Open ↗
        </a>
      </div>
    </div>
  );
}