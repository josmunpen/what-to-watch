import { cn } from "@/lib/utils";
import type { ChatMessage as ChatMessageType } from "@/lib/api";
import { MovieCard } from "./movie-card";

// Simple regex to detect movie cards in assistant responses
// Expected format: **Title** (Year · Duration) — Description
const MOVIE_REGEX =
  /\*\*(.+?)\*\*\s*\((\d{4})\s*·\s*(.+?)\)\s*(?:—|–|-)\s*(.+)/g;

interface ParsedMovie {
  title: string;
  year: string;
  duration: string;
  description: string;
}

function parseMovies(text: string): {
  movies: ParsedMovie[];
  textWithoutMovies: string;
} {
  const movies: ParsedMovie[] = [];
  const textWithoutMovies = text.replace(MOVIE_REGEX, (_, title, year, duration, description) => {
    movies.push({ title, year, duration, description: description.trim() });
    return "";
  });
  return { movies, textWithoutMovies: textWithoutMovies.trim() };
}

export function ChatMessage({ message }: { message: ChatMessageType }) {
  const isUser = message.role === "user";

  if (isUser) {
    return (
      <div className="flex justify-end">
        <div className="max-w-[80%] rounded-xl border border-border bg-bg-input px-4 py-3 text-sm">
          {message.content}
        </div>
      </div>
    );
  }

  const { movies, textWithoutMovies } = parseMovies(message.content);

  return (
    <div className="flex justify-start">
      <div className="max-w-[80%] space-y-3 rounded-xl border border-border bg-bg-card px-4 py-3 text-sm leading-relaxed">
        {textWithoutMovies && <p>{textWithoutMovies}</p>}
        {movies.map((movie) => (
          <MovieCard key={movie.title} {...movie} />
        ))}
      </div>
    </div>
  );
}
