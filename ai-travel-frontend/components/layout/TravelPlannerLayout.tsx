"use client";

import ChatWindow from "../chat/ChatWindow";
import TripSummary from "../cards/TripSummary";

export default function TravelPlannerLayout() {
  return (
    <div className="h-screen bg-[#0B0B0F] text-white flex flex-col">
      <header className="h-16 border-b border-zinc-800 flex items-center justify-between px-6">
        <h1 className="text-xl font-semibold">✈️ AI Travel Planner</h1>

        {/* <button className="rounded-lg border border-zinc-700 px-4 py-2 text-sm hover:bg-zinc-900 transition">
          + New Chat
        </button> */}
      </header>

      <div className="flex flex-1 overflow-hidden">
        <div className="w-[50%] overflow-hidden">
          <ChatWindow />
        </div>

        <div className="w-[50%] overflow-y-auto border-l border-zinc-800">
          <TripSummary />
        </div>
      </div>
    </div>
  );
}