"use client";

import { useState, useRef, useEffect } from "react";
import { sendMessage, type ChatMessage as ChatMessageType } from "@/lib/api";
import { ChatMessage } from "@/components/chat/chat-message";
import { ChatInput } from "@/components/chat/chat-input";

export default function ChatPage() {
  const [messages, setMessages] = useState<ChatMessageType[]>([]);
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  async function handleSend(text: string) {
    const userMessage: ChatMessageType = { role: "user", content: text };
    const updatedMessages = [...messages, userMessage];
    setMessages(updatedMessages);
    setLoading(true);

    try {
      const response = await sendMessage(text, messages);
      setMessages([
        ...updatedMessages,
        { role: "assistant", content: response },
      ]);
    } catch {
      setMessages([
        ...updatedMessages,
        {
          role: "assistant",
          content: "Lo siento, ha ocurrido un error. Inténtalo de nuevo.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="mx-auto flex h-[calc(100vh-65px)] max-w-3xl flex-col">
      {/* Header */}
      <div className="flex items-center gap-3 border-b border-border px-4 py-3">
        <div className="flex h-9 w-9 items-center justify-center rounded-full bg-accent text-lg">
          🎬
        </div>
        <div>
          <h2 className="text-sm font-semibold">What to Watch</h2>
          <p className="text-xs text-text-secondary">Tu asistente de pelis</p>
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 space-y-4 overflow-y-auto px-4 py-6">
        {messages.length === 0 && (
          <div className="flex h-full items-center justify-center text-center text-text-secondary">
            <p>
              Cuéntame qué te apetece ver.
              <br />
              <span className="text-sm">
                Un género, un estado de ánimo, una peli que te gustó...
              </span>
            </p>
          </div>
        )}
        {messages.map((msg, i) => (
          <ChatMessage key={i} message={msg} />
        ))}
        {loading && (
          <div className="flex justify-start">
            <div className="rounded-xl border border-border bg-bg-card px-4 py-3 text-sm text-text-secondary">
              Pensando...
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <ChatInput onSend={handleSend} disabled={loading} />
    </div>
  );
}
