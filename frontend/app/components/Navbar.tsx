"use client";

import Link from "next/link";

export default function Navbar() {
  return (
    <nav className="bg-white shadow-sm border-b px-6 py-4 flex justify-between items-center">
      
      <h1 className="text-xl font-bold text-gray-800">
        📚 AI Book Platform
      </h1>

      <div className="space-x-6">
        <Link href="/" className="text-gray-600 hover:text-blue-600">
          Home
        </Link>
        <Link href="/qa" className="text-gray-600 hover:text-blue-600">
          Q&A
        </Link>
      </div>
    </nav>
  );
}