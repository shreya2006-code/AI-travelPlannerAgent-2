"use client";

import { useState } from "react";
import MessageBubble from "./MessageBubble";
import { sendMessage } from "@/lib/api";
import { useTrip } from "@/context/TripContext";

export default function ChatWindow() {
  const [messages, setMessages] = useState<
    { role: "user" | "assistant"; message: string }[]
>([]);
  const { setTrip, clearTrip } = useTrip();
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const handleNewChat = () => {
    setMessages([]);
    setInput("");
    clearTrip();
  };

  const handleSend = async () => {
    if (!input.trim()) return;

    const userMessage = input;

    setMessages((prev) => [
      ...prev,
      {
        role: "user",
        message: userMessage,
      },
    ]);

    setInput("");
    setLoading(true);

    try {
      const result = await sendMessage(userMessage);
      console.log(result);
      console.log(result.trip);
      console.log("TRIP FROM BACKEND:", result.trip);

      setTrip(result.trip);
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          message: result.chat_response,
        },
      ]);
      setLoading(false);
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          message: "⚠️ Couldn't connect to the backend.",
        },
      ]);
      setLoading(false);
    }
  };

  return (
    <div className="flex h-full flex-col">

      {/* Header */}
      <div className="flex items-center justify-between border-b border-zinc-800 px-6 py-4">
        <div>
          <h2 className="text-lg font-semibold">AI Travel Planner</h2>
          <p className="text-sm text-zinc-500">
            Plan, modify and explore trips naturally.
          </p>
        </div>

        <button
          disabled={loading}
          onClick={handleNewChat}
          className="rounded-lg border border-zinc-700 px-4 py-2 text-sm hover:bg-zinc-900 transition"
        >
          + New Chat
        </button>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto min-h-0 space-y-5 p-6">
        {messages.length === 0 ? (
          <div className="flex h-full items-center justify-center">
            <div className="max-w-2xl text-center">
              <div className="mb-6 text-6xl">🌍</div>

              <h2 className="text-5xl font-bold">
                Where should we travel today?
              </h2>

              <p className="mt-6 text-lg text-zinc-400">
                Plan trips, modify itineraries, estimate budgets, and explore
                your next adventure.
              </p>
            </div>
          </div>
        ) : (
          <div className="space-y-5">
            {messages.map((msg, index) => (
              <MessageBubble
                key={index}
                role={msg.role}
                message={msg.message}
              />
            ))}

            {loading && (
              <MessageBubble
                role="assistant"
                message="✈️ Planning your perfect trip..."
              />
            )}
          </div>
        )}
      </div>

      {/* Input */}
      <div className="shrink-0 border-t border-zinc-800 bg-[#0B0B0F] p-5">
        <div className="mx-auto flex w-full max-w-4xl items-center rounded-2xl border border-zinc-700 bg-zinc-900 px-3 py-3 shadow-xl">
          <input
            disabled={loading}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter") {
                handleSend();
              }
            }}
            className="flex-1 bg-transparent px-4 text-white placeholder:text-zinc-500 outline-none"
            placeholder="Plan a trip to Goa under ₹30,000..."
          />

          <button
            disabled={loading}
            onClick={handleSend}
            className={`flex h-12 w-12 items-center justify-center rounded-full text-lg transition ${
              loading
                ? "bg-zinc-700 cursor-not-allowed"
                : "bg-blue-600 hover:bg-blue-700"
            }`}
          >
            ➜
          </button>
        </div>
      </div>

    </div>
  );
}