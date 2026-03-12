# TODO Frontend — Fase 1 (MVP)

Ref: [FRONTEND_PLAN.md](FRONTEND_PLAN.md) | Mockup visual: `mockup.html`

## Tareas

### 1. Inicializar proyecto
- [ ] Crear proyecto Next.js (App Router) dentro de `frontend/`
- [ ] Instalar y configurar Tailwind CSS
- [ ] Instalar y configurar shadcn/ui
- [ ] Añadir fuente DM Sans (Google Fonts via `next/font`)

### 2. Configurar tema y paleta
- [ ] Definir colores custom en `tailwind.config.ts` (bg-dark, bg-card, accent, etc.)
- [ ] Configurar shadcn/ui para dark mode fijo con la paleta del plan
- [ ] Crear layout global (`app/layout.tsx`) con fuente, fondo y estructura base

### 3. Componentes compartidos
- [ ] Navbar (logo "what-to-watch", links, botón CTA)
- [ ] Footer

### 4. Landing page (`/`)
- [ ] Hero: título, subtítulo, botones CTA
- [ ] Feature cards (3 tarjetas: conversación natural, recomendaciones, de la charla al sofá)
- [ ] Sección CTA final

### 5. Página de chat (`/chat`)
- [ ] Layout del chat: header con avatar, área de mensajes, input abajo
- [ ] Componente ChatMessage (burbujas usuario vs asistente)
- [ ] Componente MovieCard (título, año, duración, descripción, botón "Ver ahora")
- [ ] Estado local: lista de mensajes, input controlado
- [ ] Conectar con backend: POST a `/chat` y renderizar respuesta
- [ ] Cliente HTTP (`lib/api.ts`) con `NEXT_PUBLIC_API_URL`

### 6. Página de precios (`/pricing`) — mock
- [ ] Dos tarjetas: plan gratuito y plan pro
- [ ] Contenido placeholder (límites, precio)
- [ ] Botón de suscripción deshabilitado o con tooltip "Próximamente"

### 7. CORS en backend
- [ ] Añadir middleware CORS en FastAPI permitiendo `localhost:3000` y dominio Vercel

### 8. Deploy
- [ ] Verificar que el proyecto arranca con `npm run dev`
- [ ] Push a GitHub
- [ ] Conectar repo en Vercel y hacer primer deploy
- [ ] Configurar variable `NEXT_PUBLIC_API_URL` en Vercel
