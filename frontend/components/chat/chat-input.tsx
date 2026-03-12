"use client";

import { useState } from "react";

interface ChatInputProps {
  onSend: (message: string) => void;
  disabled?: boolean;
}

export function ChatInput({ onSend, disabled }: ChatInputProps) {
  const [input, setInput] = useState("");

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    const trimmed = input.trim();
    if (!trimmed || disabled) return;
    onSend(trimmed);
    setInput("");
  }

  return (
    <form
      onSubmit={handleSubmit}
      className="flex gap-3 border-t border-border px-4 py-3"
    >
      <input
        type="text"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder="Cuéntame qué te apetece ver..."
        disabled={disabled}
        className="flex-1 rounded-lg border border-border bg-bg-input px-4 py-2.5 text-sm text-text-primary placeholder:text-text-secondary focus:border-accent focus:outline-none disabled:opacity-50"
      />
      <button
        type="submit"
        disabled={disabled || !input.trim()}
        className="rounded-lg bg-accent px-4 py-2.5 text-lg transition-colors hover:bg-accent-hover disabled:opacity-50"
      >
        ➤
      </button>
    </form>
  );
}
