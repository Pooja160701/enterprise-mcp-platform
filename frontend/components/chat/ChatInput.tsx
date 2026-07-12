"use client";

import { Send } from "lucide-react";
import { useState } from "react";
import { useChatStore } from "@/store/chatStore"; 

export default function ChatInput() {
  const [message, setMessage] = useState("");

  const sendMessage = useChatStore((s) => s.sendMessage);

  const buttonClick = async () => {
    if (!message.trim()) return;

    await sendMessage(message);
    setMessage("");
  };

  return (
    <div className="border-t border-zinc-700 bg-zinc-900 p-6">
      <div className="mx-auto flex max-w-4xl gap-4">
        <textarea
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyDown={async (e) => {
            if (e.key === "Enter" && !e.shiftKey) {
              e.preventDefault();
              await buttonClick();
            }
          }}
          placeholder="Ask anything about your infrastructure..."
          className="min-h-[56px] flex-1 resize-none rounded-xl border border-zinc-700 bg-zinc-800 p-4 text-white outline-none focus:border-blue-500"
        />

        <button
          onClick={buttonClick}
          className="rounded-xl bg-blue-600 px-6 text-white hover:bg-blue-700 disabled:opacity-50"
          disabled={!message.trim()}
        >
          <Send />
        </button>
      </div>
    </div>
  );
}