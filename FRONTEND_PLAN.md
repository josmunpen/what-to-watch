# Frontend Plan — What to Watch

## Decisiones tomadas

| Aspecto | Decisión |
|---|---|
| Framework | **Next.js** (App Router) |
| Componentes UI | **shadcn/ui** + Tailwind CSS |
| Tipografía | DM Sans |
| Despliegue | **Vercel** (conectado a GitHub, deploy automático) |
| Auth | **Clerk** (fase 2, no en la primera versión) |
| Pagos | **Stripe** con modelo freemium (mockeado hasta definirlo) |
| Modo visual | Dark mode fijo |

## Paleta de colores

| Token | Valor | Uso |
|---|---|---|
| `bg-dark` | `#1A1614` | Fondo principal |
| `bg-card` | `#241F1C` | Tarjetas, paneles |
| `bg-input` | `#2E2724` | Inputs, campos |
| `accent` | `#E09145` | CTAs, links, elementos destacados |
| `accent-hover` | `#C97D35` | Hover de accent |
| `text-primary` | `#F5E6D3` | Texto principal (crema) |
| `text-secondary` | `#A89585` | Texto secundario |
| `border` | `#3A3230` | Bordes y separadores |

## Referencia visual

Ver `mockup.html` en la raíz del proyecto para la dirección estética aprobada.

## Páginas

### 1. Landing (`/`)
- Hero: título + subtítulo + CTA "Empieza gratis"
- 3 feature cards (conversación natural, recomendaciones precisas, de la charla al sofá)
- CTA final de cierre

### 2. Chat (`/chat`)
- Interfaz tipo ChatGPT: mensajes en burbujas, input abajo
- Mensajes del asistente con tarjetas de películas (título, año, duración, descripción corta)
- Botón "Ver ahora" en cada tarjeta
- Conectado al backend FastAPI via POST /chat

### 3. Precios (`/pricing`) — mockeado
- Plan gratuito vs plan pro (placeholder)
- Botón de suscripción deshabilitado o mockeado

## Fases de implementación

### Fase 1 — MVP (sin auth, sin pagos reales)
1. Inicializar proyecto Next.js con Tailwind + shadcn/ui
2. Configurar paleta de colores y tema en Tailwind
3. Landing page
4. Página de chat conectada al backend FastAPI
5. Página de precios mockeada
6. Deploy en Vercel

### Fase 2 — Auth
1. Integrar Clerk (registro, login, login con Google)
2. Proteger ruta `/chat` (solo usuarios logueados)
3. Pasar user ID al backend en las peticiones

### Fase 3 — Pagos
1. Integrar Stripe (suscripciones)
2. Modelo freemium: X consultas gratis/día, ilimitado con plan pro
3. Webhook de Stripe para actualizar estado de suscripción

### Fase 4 — Personajes (futuro)
1. Selector de "personalidad" del asistente antes de chatear
2. Cada personaje con su propio color de acento y estilo de respuesta
3. Personajes: el pedante, la mainstream, el cinéfilo indie, etc.

## Conexión frontend ↔ backend

- El frontend (Vercel) llama al backend (FastAPI) via HTTP
- Endpoint principal: `POST /chat` con body `{ message, history }`
- En desarrollo: backend en `localhost:8000`, frontend en `localhost:3000`
- En producción: variable de entorno `NEXT_PUBLIC_API_URL` apuntando al backend desplegado
- CORS configurado en FastAPI para permitir el dominio de Vercel

## Estructura de carpetas esperada

```
frontend/
├── app/
│   ├── layout.tsx          # Layout global (fuente, tema)
│   ├── page.tsx            # Landing
│   ├── chat/
│   │   └── page.tsx        # Chat
│   └── pricing/
│       └── page.tsx        # Precios (mock)
├── components/
│   ├── ui/                 # shadcn/ui components
│   ├── landing/            # Hero, FeatureCard, CTA
│   ├── chat/               # ChatMessage, ChatInput, MovieCard
│   └── layout/             # Navbar, Footer
├── lib/
│   └── api.ts              # Cliente HTTP para el backend
├── tailwind.config.ts
└── .env.local              # NEXT_PUBLIC_API_URL
```
