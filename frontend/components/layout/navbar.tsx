import Link from "next/link";

export function Navbar() {
  return (
    <nav className="flex items-center justify-between border-b border-border px-6 py-4 md:px-16">
      <Link href="/" className="text-xl font-bold text-accent">
        what-to-<span className="text-text-primary">watch</span>
      </Link>
      <div className="flex items-center gap-6">
        <Link
          href="/pricing"
          className="text-sm text-text-secondary transition-colors hover:text-text-primary"
        >
          Precios
        </Link>
        <Link
          href="/chat"
          className="rounded-lg bg-accent px-4 py-2 text-sm font-semibold text-bg-dark transition-colors hover:bg-accent-hover"
        >
          Empezar gratis
        </Link>
      </div>
    </nav>
  );
}
