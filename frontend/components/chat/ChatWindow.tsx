"use client";

import ChatInput from "./ChatInput";
import WelcomeCard from "@/components/dashboard/WelcomeCard";
import Message from "./Message";
import { useChatStore } from "@/store/chatStore";

export default function ChatWindow() {
  const messages = useChatStore((s) => s.messages);

  return (
    <div className="flex h-full flex-col">
      <div className="flex-1 overflow-y-auto">
        <div className="mx-auto max-w-4xl px-8 py-8">
          {messages.length === 0 ? (
            <WelcomeCard />
          ) : (
            <div className="space-y-6">
              {messages.map((m) => (
                <Message
                  key={m.id}
                  role={m.role}
                  content={m.content}
                />
              ))}
            </div>
          )}
        </div>
      </div>

      <ChatInput />
    </div>
  );
}