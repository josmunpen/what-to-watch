const plans = [
  {
    name: "Gratis",
    price: "0€",
    period: "para siempre",
    features: [
      "5 consultas al día",
      "Recomendaciones básicas",
      "Historial de la sesión",
    ],
    cta: "Empezar gratis",
    href: "/chat",
    highlighted: false,
  },
  {
    name: "Pro",
    price: "4,99€",
    period: "/mes",
    features: [
      "Consultas ilimitadas",
      "Recomendaciones avanzadas",
      "Historial guardado",
      "Personajes exclusivos",
    ],
    cta: "Próximamente",
    href: "#",
    highlighted: true,
  },
];

export default function PricingPage() {
  return (
    <div className="mx-auto max-w-3xl px-6 py-20 text-center">
      <h1 className="text-3xl font-bold md:text-4xl">Precios</h1>
      <p className="mt-3 text-text-secondary">
        Elige el plan que mejor se adapte a ti.
      </p>

      <div className="mt-12 grid gap-6 md:grid-cols-2">
        {plans.map((plan) => (
          <div
            key={plan.name}
            className={`rounded-xl border p-8 text-left ${
              plan.highlighted
                ? "border-accent bg-bg-card"
                : "border-border bg-bg-card"
            }`}
          >
            <h3 className="text-lg font-semibold">{plan.name}</h3>
            <div className="mt-2">
              <span className="text-3xl font-bold">{plan.price}</span>
              <span className="text-sm text-text-secondary">
                {" "}
                {plan.period}
              </span>
            </div>
            <ul className="mt-6 space-y-3">
              {plan.features.map((f) => (
                <li key={f} className="flex items-center gap-2 text-sm">
                  <span className="text-accent">✓</span>
                  {f}
                </li>
              ))}
            </ul>
            {plan.highlighted ? (
              <button
                disabled
                className="mt-8 w-full rounded-lg border border-border px-4 py-2.5 text-sm font-semibold text-text-secondary"
              >
                {plan.cta}
              </button>
            ) : (
              <a
                href={plan.href}
                className="mt-8 block w-full rounded-lg bg-accent px-4 py-2.5 text-center text-sm font-semibold text-bg-dark transition-colors hover:bg-accent-hover"
              >
                {plan.cta}
              </a>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
