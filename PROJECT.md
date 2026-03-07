# Proyecto: What to Watch

## Objetivo
Web que recomienda películas personalizadas para evitar el scroll infinito de Netflix.
Debe ser rápida, simple y pensada para conversión a "ver ahora".

## Público objetivo
- Personas que no saben qué película ver
- Parejas buscando una película para ver juntos
- Cinéfilos ocasionales que buscan recomendaciones rápidas y confiables

NO está dirigido a críticos de cine ni a usuarios avanzados de plataformas como Letterboxd.

## Flujo principal
1. El usuario interactúa con un chatbot y describe sus preferencias, por ejemplo: "Quiero algo como Interstellar pero menos denso".
2. El sistema utiliza el LLM para generar recomendaciones en tiempo real.
3. Se realiza una búsqueda en una base de datos vectorial para encontrar coincidencias.
4. Se muestran entre 3 y 5 recomendaciones de películas, cada una con una breve explicación.
5. Cada recomendación incluye un botón: VER AHORA.

## Monetización
- Principal: Afiliados de plataformas de streaming.
- Secundario: Suscripción premium para recomendaciones ilimitadas y personalizadas.

## Consideraciones técnicas
- Minimizar las llamadas al modelo de lenguaje (LLM) para optimizar costos.
- Implementar un sistema de caché para almacenar resultados y mejorar la velocidad de respuesta.