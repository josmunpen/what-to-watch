import Link from "next/link";

export function CTA() {
  return (
    <section className="border-t border-border py-16 text-center">
      <h2 className="text-2xl font-bold md:text-3xl">
        ¿Listo para dejar de hacer scroll?
      </h2>
      <p className="mt-3 text-text-secondary">
        Empieza gratis. Sin tarjeta. Sin compromiso.
      </p>
      <Link
        href="/chat"
        className="mt-6 inline-block rounded-lg bg-accent px-6 py-3 font-semibold text-bg-dark transition-colors hover:bg-accent-hover"
      >
        Empieza ahora
      </Link>
    </section>
  );
}
