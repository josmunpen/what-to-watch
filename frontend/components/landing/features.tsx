const features = [
  {
    icon: "\u{1F4AC}",
    title: "Conversación natural",
    description:
      'Dile lo que te apetece como se lo dirías a un amigo. "Algo ligero para ver en pareja" funciona perfectamente.',
  },
  {
    icon: "\u{1F3AF}",
    title: "Recomendaciones precisas",
    description:
      "Nada de listas genéricas. Cada sugerencia está pensada para lo que tú buscas en ese momento.",
  },
  {
    icon: "\u{1F37F}",
    title: "De la charla al sofá",
    description:
      "Cada recomendación incluye dónde verla. Un click y estás viendo la peli.",
  },
];

export function Features() {
  return (
    <section
      id="features"
      className="mx-auto grid max-w-4xl gap-5 px-6 pb-16 md:grid-cols-3"
    >
      {features.map((f) => (
        <div
          key={f.title}
          className="rounded-xl border border-border bg-bg-card p-6"
        >
          <div className="mb-3 text-3xl">{f.icon}</div>
          <h3 className="mb-2 font-semibold">{f.title}</h3>
          <p className="text-sm text-text-secondary">{f.description}</p>
        </div>
      ))}
    </section>
  );
}
