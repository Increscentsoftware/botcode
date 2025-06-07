"use client";
import React, { useState } from 'react';
import axios from 'axios';

export default function Home() {
  const [prompt, setPrompt] = useState('');
  const [model, setModel] = useState('azure-gpt4');
  const [response, setResponse] = useState('');

  const handleSubmit = async () => {
    try {
      const res = await axios.post("http://localhost:8000/api/run", {
        prompt,
        model
      });
      setResponse(res.data.output);
    } catch (error) {
      console.error("Error:", error);
      setResponse("Something went wrong.");
    }
  };

  return (
    <div className="p-6">
      <h1 className="text-xl font-bold mb-4">AI Assistant</h1>
      <textarea
        className="w-full p-2 border rounded"
        rows={4}
        placeholder="Enter your prompt here..."
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
      />
      <select
        className="mt-2 p-2 border rounded"
        value={model}
        onChange={(e) => setModel(e.target.value)}
      >
        <option value="azure-gpt4">Azure GPT-4</option>
        <option value="openai-gpt4">OpenAI GPT-4</option>
        <option value="huggingface-bart">HuggingFace BART</option>
      </select>
      <button
        onClick={handleSubmit}
        className="mt-4 bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
      >
        Run AI
      </button>
      <div className="mt-4 bg-gray-100 p-4 rounded">
        <strong>Response:</strong>
        <pre>{response}</pre>
      </div>
    </div>
  );
}
