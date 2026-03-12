import Link from "next/link";

export function Hero() {
  return (
    <section className="mx-auto max-w-2xl px-6 pb-12 pt-20 text-center md:pt-28">
      <h1 className="text-4xl font-bold leading-tight md:text-5xl">
        Deja de hacer scroll.
        <br />
        <span className="text-accent">Encuentra tu peli.</span>
      </h1>
      <p className="mx-auto mt-5 max-w-md text-lg text-text-secondary">
        Chatea con un asistente que entiende lo que te apetece ver esta noche.
        Sin algoritmos opacos, sin perder media hora eligiendo.
      </p>
      <div className="mt-8 flex justify-center gap-4">
        <Link
          href="/chat"
          className="rounded-lg bg-accent px-6 py-3 font-semibold text-bg-dark transition-colors hover:bg-accent-hover"
        >
          Pruébalo gratis
        </Link>
        <a
          href="#features"
          className="rounded-lg border border-border px-6 py-3 font-medium transition-colors hover:border-text-secondary"
        >
          Ver cómo funciona
        </a>
      </div>
    </section>
  );
}
