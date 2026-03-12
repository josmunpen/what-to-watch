# TODO Frontend — Fase 1 (MVP)

Ref: [FRONTEND_PLAN.md](FRONTEND_PLAN.md) | Mockup visual: `mockup.html`

## Tareas

### 1. Inicializar proyecto ✅
- [x] Crear proyecto Next.js (App Router) dentro de `frontend/`
- [x] Instalar y configurar Tailwind CSS
- [x] Instalar y configurar shadcn/ui
- [x] Añadir fuente DM Sans (Google Fonts via `next/font`)

### 2. Configurar tema y paleta ✅
- [x] Definir colores custom en `tailwind.config.ts` (bg-dark, bg-card, accent, etc.)
- [x] Configurar shadcn/ui para dark mode fijo con la paleta del plan
- [x] Crear layout global (`app/layout.tsx`) con fuente, fondo y estructura base

### 3. Componentes compartidos ✅
- [x] Navbar (logo "what-to-watch", links, botón CTA)
- [x] Footer

### 4. Landing page (`/`) ✅
- [x] Hero: título, subtítulo, botones CTA
- [x] Feature cards (3 tarjetas: conversación natural, recomendaciones, de la charla al sofá)
- [x] Sección CTA final

### 5. Página de chat (`/chat`) ✅
- [x] Layout del chat: header con avatar, área de mensajes, input abajo
- [x] Componente ChatMessage (burbujas usuario vs asistente)
- [x] Componente MovieCard (título, año, duración, descripción, botón "Ver ahora")
- [x] Estado local: lista de mensajes, input controlado
- [x] Conectar con backend: POST a `/chat` y renderizar respuesta
- [x] Cliente HTTP (`lib/api.ts`) con `NEXT_PUBLIC_API_URL`

### 6. Página de precios (`/pricing`) — mock ✅
- [x] Dos tarjetas: plan gratuito y plan pro
- [x] Contenido placeholder (límites, precio)
- [x] Botón de suscripción deshabilitado o con tooltip "Próximamente"

### 7. CORS en backend ✅
- [x] Añadir middleware CORS en FastAPI permitiendo `localhost:3000` y dominio Vercel

### 8. Deploy
- [ ] Verificar que el proyecto arranca con `npm run dev`
- [ ] Push a GitHub
- [ ] Conectar repo en Vercel y hacer primer deploy
- [ ] Configurar variable `NEXT_PUBLIC_API_URL` en Vercel
