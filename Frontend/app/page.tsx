"use client";

import React, { useState } from "react";
import axios from "axios";

export default function Home() {
  const [prompt, setPrompt] = useState<string>("");
  const [model, setModel] = useState<string>("chatbot"); // match your backend deployment name
  const [response, setResponse] = useState<string>("");
  const [loading, setLoading] = useState<boolean>(false);

  const handleSubmit = async () => {
    if (!prompt.trim()) {
      setResponse("Please enter a prompt.");
      return;
    }
    setLoading(true);
    setResponse("");
    try {
      const res = await axios.post("http://localhost:8000/api/run", {
        prompt,
        model,
      });
      setResponse(res.data.output);
    } catch (error) {
      console.error("Error:", error);
      setResponse("Something went wrong. Please try again.");
    }
    setLoading(false);
  };

  return (
    <div className="p-6 max-w-xl mx-auto">
      <h1 className="text-2xl font-bold mb-6">AI Assistant</h1>

      <textarea
        className="w-full p-3 border rounded resize-none"
        rows={6}
        placeholder="Enter your prompt here..."
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
        disabled={loading}
      />

      <select
        className="mt-4 p-3 border rounded w-full"
        value={model}
        onChange={(e) => setModel(e.target.value)}
        disabled={loading}
      >
        <option value="chatbot">Azure GPT-4 (chatbot)</option>
        <option value="openai-gpt4" disabled>
          OpenAI GPT-4 (coming soon)
        </option>
        <option value="huggingface-bart" disabled>
          HuggingFace BART (coming soon)
        </option>
      </select>

      <button
        onClick={handleSubmit}
        disabled={loading}
        className="mt-6 w-full bg-blue-600 text-white px-4 py-3 rounded hover:bg-blue-700 disabled:bg-blue-400"
      >
        {loading ? "Running..." : "Run AI"}
      </button>

      <div className="mt-6 bg-gray-100 p-4 rounded min-h-[120px] whitespace-pre-wrap">
        <strong>Response:</strong>
        <p className="mt-2">{response}</p>
      </div>
    </div>
  );
}
