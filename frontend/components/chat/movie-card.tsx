interface MovieCardProps {
  title: string;
  year: string;
  duration: string;
  description: string;
}

export function MovieCard({ title, year, duration, description }: MovieCardProps) {
  return (
    <div className="flex items-center justify-between rounded-lg border border-border bg-bg-dark px-4 py-3">
      <div>
        <div className="font-semibold">{title}</div>
        <div className="text-xs text-text-secondary">
          {year} · {duration} — {description}
        </div>
      </div>
      <button className="ml-4 shrink-0 rounded-md bg-accent px-3 py-1.5 text-xs font-semibold text-bg-dark transition-colors hover:bg-accent-hover">
        Ver ahora
      </button>
    </div>
  );
}
