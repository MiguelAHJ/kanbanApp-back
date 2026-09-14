"""
Genera los artboards (.dc.html) del canvas de diseño de IssueFlow.
Cada pantalla es un archivo independiente; este script solo evita duplicar
a mano el CSS base y los iconos. Ejecutar: python build_artboards.py
"""
from pathlib import Path

OUT = Path(__file__).parent

# ---------------------------------------------------------------- iconos SVG
ICON_PATHS = {
    "home": '<path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/>',
    "mic": '<path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"/><path d="M19 10v2a7 7 0 0 1-14 0v-2"/><line x1="12" y1="19" x2="12" y2="23"/><line x1="8" y1="23" x2="16" y2="23"/>',
    "kanban": '<rect x="3" y="3" width="5" height="18" rx="1.5"/><rect x="10" y="3" width="5" height="12" rx="1.5"/><rect x="17" y="3" width="4" height="8" rx="1.5"/>',
    "chart": '<line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/>',
    "sliders": '<line x1="4" y1="21" x2="4" y2="14"/><line x1="4" y1="10" x2="4" y2="3"/><line x1="12" y1="21" x2="12" y2="12"/><line x1="12" y1="8" x2="12" y2="3"/><line x1="20" y1="21" x2="20" y2="16"/><line x1="20" y1="12" x2="20" y2="3"/><line x1="1" y1="14" x2="7" y2="14"/><line x1="9" y1="8" x2="15" y2="8"/><line x1="17" y1="16" x2="23" y2="16"/>',
    "plus": '<line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/>',
    "search": '<circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/>',
    "bell": '<path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.73 21a2 2 0 0 1-3.46 0"/>',
    "camera": '<path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"/><circle cx="12" cy="13" r="4"/>',
    "pen": '<path d="M12 20h9"/><path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"/>',
    "check": '<polyline points="20 6 9 17 4 12"/>',
    "arrow-left": '<line x1="19" y1="12" x2="5" y2="12"/><polyline points="12 19 5 12 12 5"/>',
    "arrow-right": '<line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/>',
    "zap": '<polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/>',
    "clock": '<circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>',
    "calendar": '<rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/>',
    "users": '<path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>',
    "stop": '<rect x="6" y="6" width="12" height="12" rx="2"/>',
    "x": '<line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>',
    "chevron-down": '<polyline points="6 9 12 15 18 9"/>',
    "file": '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/>',
    "download": '<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/>',
    "lock": '<rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/>',
    "mail": '<path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/>',
    "alert": '<path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/>',
    "sparkle": '<path d="M12 3l1.8 5.2L19 10l-5.2 1.8L12 17l-1.8-5.2L5 10l5.2-1.8z"/><path d="M19 17l.8 2.2L22 20l-2.2.8L19 23l-.8-2.2L16 20l2.2-.8z"/>',
    "more": '<circle cx="12" cy="12" r="1"/><circle cx="19" cy="12" r="1"/><circle cx="5" cy="12" r="1"/>',
    "branch": '<line x1="6" y1="3" x2="6" y2="15"/><circle cx="18" cy="6" r="3"/><circle cx="6" cy="18" r="3"/><path d="M18 9a9 9 0 0 1-9 9"/>',
    "image": '<rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="8.5" cy="8.5" r="1.5"/><polyline points="21 15 16 10 5 21"/>',
    "eye": '<path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/>',
    "grip": '<circle cx="9" cy="6" r="1"/><circle cx="15" cy="6" r="1"/><circle cx="9" cy="12" r="1"/><circle cx="15" cy="12" r="1"/><circle cx="9" cy="18" r="1"/><circle cx="15" cy="18" r="1"/>',
}


def icon(name, size=20, stroke="currentColor", width=1.8, extra_style=""):
    return (
        f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{stroke}" '
        f'stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round" '
        f'style="flex-shrink: 0; {extra_style}">{ICON_PATHS[name]}</svg>'
    )


LOGO = (
    '<svg width="34" height="34" viewBox="0 0 32 32" style="flex-shrink: 0;">'
    '<rect x="2" y="2" width="28" height="28" rx="9" fill="#F7907F"/>'
    '<path d="M9 16h3.5l2-5.5 3 11 2-5.5H23" stroke="#15171c" stroke-width="2.4" fill="none" '
    'stroke-linecap="round" stroke-linejoin="round"/></svg>'
)

# ---------------------------------------------------------------- tokens
DARK = """
      :root {
        --bg: #0e1014; --surface: #161920; --surface-2: #1d212a; --surface-3: #262b36;
        --line: rgba(255,255,255,0.07); --line-strong: rgba(255,255,255,0.14);
        --ink: #f3f4f6; --ink-2: #a3a9b6; --ink-3: #6b7280;
        --coral: #F7907F; --amber: #F3C56B; --lavender: #BDA9F7; --mint: #8EDBB9; --sky: #8CC8F2;
        --on-tile: #15171c;
        --shadow: 0 24px 60px rgba(0,0,0,0.45);
      }
"""

LIGHT = """
      :root {
        --bg: #F6F2EC; --surface: #FFFFFF; --surface-2: #F3EEE7; --surface-3: #EAE3DA;
        --line: rgba(20,18,16,0.08); --line-strong: rgba(20,18,16,0.16);
        --ink: #17181c; --ink-2: #5f6470; --ink-3: #8a8f9a;
        --coral: #F7907F; --amber: #F3C56B; --lavender: #BDA9F7; --mint: #8EDBB9; --sky: #8CC8F2;
        --on-tile: #15171c;
        --shadow: 0 24px 60px rgba(40,30,20,0.14);
      }
"""

BASE_CSS = """
      body { margin: 0; background: var(--bg); color: var(--ink); font-family: 'DM Sans', 'Segoe UI', system-ui, sans-serif; font-size: 14px; line-height: 1.45; -webkit-font-smoothing: antialiased; }
      a { color: var(--coral); text-decoration: none; } a:hover { color: var(--amber); }
      h1, h2, h3, .display { font-family: 'Sora', 'Segoe UI', system-ui, sans-serif; letter-spacing: -0.02em; margin: 0; }
      * { box-sizing: border-box; }
      .rail-btn { width: 48px; height: 48px; border-radius: 16px; display: flex; align-items: center; justify-content: center; color: var(--ink-3); }
      .rail-btn.active { background: var(--ink); color: var(--bg); }
      .card { background: var(--surface); border: 1px solid var(--line); border-radius: 22px; }
      .chip { display: inline-flex; align-items: center; gap: 6px; padding: 5px 10px; border-radius: 999px; font-size: 12px; font-weight: 500; background: var(--surface-2); color: var(--ink-2); border: 1px solid var(--line); white-space: nowrap; }
      .btn { display: inline-flex; align-items: center; gap: 8px; height: 44px; padding: 0 18px; border-radius: 14px; font-weight: 600; font-size: 14px; border: 1px solid transparent; white-space: nowrap; }
      .btn-primary { background: var(--coral); color: var(--on-tile); }
      .btn-ghost { background: transparent; color: var(--ink-2); border-color: var(--line-strong); }
      .btn-ink { background: var(--ink); color: var(--bg); }
      .avatar { width: 30px; height: 30px; border-radius: 999px; display: flex; align-items: center; justify-content: center; font-size: 11px; font-weight: 600; color: var(--on-tile); border: 2px solid var(--surface); }
      .dot { width: 8px; height: 8px; border-radius: 999px; flex-shrink: 0; }
      .muted { color: var(--ink-2); } .faint { color: var(--ink-3); }
      .eyebrow { font-size: 11px; font-weight: 600; letter-spacing: 0.08em; text-transform: uppercase; color: var(--ink-3); }
      @keyframes rise { from { opacity: 0; transform: translateY(14px); } to { opacity: 1; transform: none; } }
      .reveal { animation: rise 0.7s cubic-bezier(0.2, 0.7, 0.2, 1) both; }
      .d1 { animation-delay: 0.05s; } .d2 { animation-delay: 0.12s; } .d3 { animation-delay: 0.19s; } .d4 { animation-delay: 0.26s; } .d5 { animation-delay: 0.33s; } .d6 { animation-delay: 0.4s; }
      @keyframes wave { 0%, 100% { transform: scaleY(0.35); } 50% { transform: scaleY(1); } }
      .wave-bar { flex: 1; min-width: 3px; max-width: 6px; border-radius: 4px; background: var(--on-tile); transform-origin: center; animation: wave 1.1s ease-in-out infinite; }
      @keyframes pulse { 0% { box-shadow: 0 0 0 0 rgba(247,144,127,0.45); } 100% { box-shadow: 0 0 0 18px rgba(247,144,127,0); } }
      .pulse { animation: pulse 1.6s ease-out infinite; }
      @keyframes blink { 50% { opacity: 0; } }
      .caret { display: inline-block; width: 2px; height: 16px; background: var(--coral); vertical-align: -3px; margin-left: 2px; animation: blink 1s step-end infinite; }
"""

FONTS = '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Sora:wght@500;600;700&family=DM+Sans:wght@400;500;600&display=swap">'


def rail(active):
    items = [("home", "Inicio"), ("mic", "Reuniones"), ("kanban", "Tablero"), ("chart", "Reportes")]
    nav = ""
    for key, label in items:
        cls = "rail-btn active" if key == active else "rail-btn"
        nav += f'<div class="{cls}" title="{label}">{icon(key, 22)}</div>'
    return f'''
  <aside style="width: 84px; height: 100%; display: flex; flex-direction: column; align-items: center; padding: 22px 0; gap: 10px; border-right: 1px solid var(--line); background: var(--surface); flex-shrink: 0;">
    <div style="margin-bottom: 18px;">{LOGO}</div>
    <div style="display: flex; flex-direction: column; gap: 8px; align-items: center;">{nav}</div>
    <div style="flex-grow: 1;"></div>
    <div class="rail-btn" title="Ajustes">{icon("sliders", 22)}</div>
    <div class="avatar" style="width: 40px; height: 40px; background: var(--lavender); font-size: 13px; margin-top: 6px;">MH</div>
  </aside>'''


def page(title, body, tokens=DARK, width=1440, height=900, extra_css=""):
    return f'''<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <script src="./support.js"></script>
</head>
<body>
<x-dc>
<helmet>
  {FONTS}
  <style>
{tokens}
{BASE_CSS}
{extra_css}
  </style>
</helmet>
<div style="width: {width}px; height: {height}px; display: flex; overflow: hidden; background: var(--bg); color: var(--ink); font-family: 'DM Sans', 'Segoe UI', system-ui, sans-serif;">
{body}
</div>
</x-dc>
</body>
</html>
'''


def avatar(initials, color):
    return f'<div class="avatar" style="background: var(--{color});">{initials}</div>'


def topbar(title, subtitle="", right=""):
    sub = f'<div class="muted" style="font-size: 15px; margin-top: 6px;">{subtitle}</div>' if subtitle else ""
    return f'''
    <div style="display: flex; align-items: flex-start; justify-content: space-between; gap: 24px;">
      <div>
        <h1 style="font-size: 38px; font-weight: 600; line-height: 1.1;">{title}</h1>
        {sub}
      </div>
      <div style="display: flex; align-items: center; gap: 10px;">{right}</div>
    </div>'''


SEARCH = f'''<div style="display: flex; align-items: center; gap: 10px; height: 44px; padding: 0 16px; border-radius: 14px; background: var(--surface); border: 1px solid var(--line); color: var(--ink-3); width: 290px; white-space: nowrap;">{icon("search", 18)}<span>Buscar issues, reuniones…</span><span style="margin-left: auto; font-size: 11px; padding: 2px 6px; border-radius: 6px; border: 1px solid var(--line-strong);">⌘K</span></div>'''
BELL = f'<div class="rail-btn" style="background: var(--surface); border: 1px solid var(--line); width: 44px; height: 44px; border-radius: 14px; color: var(--ink-2);">{icon("bell", 20)}</div>'


# ================================================================ INICIO
def dashboard_body():
    tile = lambda color, ic, t, s, d: f'''
        <div class="reveal {d}" style="background: var(--{color}); color: var(--on-tile); border-radius: 24px; padding: 22px; height: 168px; display: flex; flex-direction: column; justify-content: space-between;">
          <div style="width: 44px; height: 44px; border-radius: 14px; background: rgba(21,23,28,0.12); display: flex; align-items: center; justify-content: center;">{icon(ic, 22, "#15171c", 2)}</div>
          <div>
            <div class="display" style="font-size: 20px; font-weight: 600;">{t}</div>
            <div style="font-size: 13px; opacity: 0.72; margin-top: 4px;">{s}</div>
          </div>
        </div>'''

    meeting = lambda t, proj, when, status, color: f'''
          <div style="display: flex; align-items: center; gap: 16px; padding: 14px 0; border-bottom: 1px solid var(--line);">
            <div style="width: 40px; height: 40px; border-radius: 12px; background: var(--surface-2); display: flex; align-items: center; justify-content: center; color: var(--ink-2);">{icon("mic", 18)}</div>
            <div style="flex-grow: 1; min-width: 0;">
              <div style="font-weight: 600; font-size: 15px;">{t}</div>
              <div class="faint" style="font-size: 12.5px; margin-top: 2px;">{proj} · {when}</div>
            </div>
            <span class="chip"><span class="dot" style="background: var(--{color});"></span>{status}</span>
          </div>'''

    pending = lambda t, tipo, color: f'''
          <div style="display: flex; align-items: flex-start; gap: 12px; padding: 12px 0; border-bottom: 1px solid var(--line);">
            <div style="width: 20px; height: 20px; border-radius: 6px; border: 1.5px solid var(--line-strong); margin-top: 2px; flex-shrink: 0;"></div>
            <div style="flex-grow: 1; min-width: 0;">
              <div style="font-weight: 500; font-size: 14px; line-height: 1.35;">{t}</div>
              <div style="display: flex; gap: 8px; margin-top: 6px; align-items: center;"><span class="chip" style="padding: 3px 8px;"><span class="dot" style="background: var(--{color});"></span>{tipo}</span><span class="faint" style="font-size: 12px;">origen: minuta</span></div>
            </div>
          </div>'''

    bars = ""
    for h, hi in [(38, 0), (52, 0), (30, 0), (64, 0), (72, 1), (24, 0), (12, 0)]:
        bg = "var(--mint)" if hi else "var(--surface-3)"
        bars += f'<div style="flex: 1; height: {h}px; background: {bg}; border-radius: 4px 4px 0 0;"></div>'

    return f'''
{rail("home")}
  <main style="flex-grow: 1; padding: 34px 40px; display: flex; flex-direction: column; gap: 26px; min-width: 0;">
    {topbar("Buenos días, Miguel", "Viernes 11 de septiembre · 3 reuniones esta semana · 4 candidatos por revisar", SEARCH + BELL + f'<div class="btn btn-primary">{icon("zap", 18, "#15171c", 2)}Issue rápido</div>')}

    <div style="display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 16px;">
      {tile("coral", "mic", "Nueva reunión", "Audio, fotos o notas — lo que haya", "d1")}
      {tile("amber", "zap", "Issue rápido", "Sin reunión, en 10 segundos", "d2")}
      {tile("lavender", "kanban", "Tablero", "18 issues activos en 3 proyectos", "d3")}
      {tile("mint", "chart", "Reportes", "Diario, semanal o por rango", "d4")}
    </div>

    <div style="display: grid; grid-template-columns: 1.35fr 1fr 0.85fr; gap: 16px; flex-grow: 1; min-height: 0;">
      <div class="card reveal d4" style="padding: 24px; display: flex; flex-direction: column;">
        <div style="display: flex; align-items: center; justify-content: space-between;">
          <h2 style="font-size: 18px; font-weight: 600;">Reuniones recientes</h2>
          <a style="font-size: 13px; font-weight: 500;">Ver todas</a>
        </div>
        <div style="margin-top: 8px;">
          {meeting("Sync semanal — Plataforma de pagos", "pagos-core", "hoy, 10:00", "3 issues creados", "mint")}
          {meeting("Revisión de pipeline CI/CD", "infra-ci", "ayer", "Minuta pendiente", "amber")}
          {meeting("Kickoff app móvil", "app-mobile", "lun 8 sep", "Minuta lista", "sky")}
        </div>
        <div style="flex-grow: 1;"></div>
        <div style="display: flex; align-items: center; gap: 12px; padding: 14px 16px; border-radius: 16px; background: var(--surface-2); margin-top: 10px;">
          {icon("sparkle", 18, "var(--amber)", 1.8)}
          <span class="muted" style="font-size: 13px;">La minuta de <b style="color: var(--ink);">Revisión de pipeline CI/CD</b> está lista para revisar.</span>
          <a style="margin-left: auto; font-size: 13px; font-weight: 600;">Abrir</a>
        </div>
      </div>

      <div class="card reveal d5" style="padding: 24px; display: flex; flex-direction: column;">
        <div style="display: flex; align-items: center; justify-content: space-between;">
          <h2 style="font-size: 18px; font-weight: 600;">Por revisar</h2>
          <span class="chip" style="background: var(--coral); color: var(--on-tile); border-color: transparent;">4</span>
        </div>
        <div style="margin-top: 8px;">
          {pending("Mover runners de staging a los nodos nuevos", "tarea", "sky")}
          {pending("El job de deploy no falla cuando la migración rompe", "bug", "coral")}
          {pending("Cachear dependencias de Flutter en el pipeline", "mejora", "lavender")}
          {pending("Documentar variables de entorno del release", "tarea", "sky")}
        </div>
        <div style="flex-grow: 1;"></div>
        <div class="btn btn-ink" style="justify-content: center; margin-top: 12px;">Revisar y crear en GitLab</div>
      </div>

      <div style="display: flex; flex-direction: column; gap: 16px; min-height: 0;">
        <div class="card reveal d5" style="padding: 22px; flex-grow: 1; display: flex; flex-direction: column;">
          <div class="eyebrow">Esta semana</div>
          <div style="display: flex; align-items: baseline; gap: 10px; margin-top: 10px;">
            <div style="font-size: 48px; font-weight: 600; line-height: 1;">12</div>
            <div class="muted" style="font-size: 13px;">issues cerrados</div>
          </div>
          <div style="font-size: 13px; margin-top: 6px;"><span style="color: var(--mint); font-weight: 600;">+3</span> <span class="faint">vs. semana pasada</span></div>
          <div style="display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 10px; margin-top: 18px; padding-top: 14px; border-top: 1px solid var(--line);">
            <div><div style="font-size: 20px; font-weight: 600;">9</div><div class="faint" style="font-size: 11.5px;">creados</div></div>
            <div><div style="font-size: 20px; font-weight: 600;">3</div><div class="faint" style="font-size: 11.5px;">reuniones</div></div>
          </div>
          <div style="flex-grow: 1;"></div>
          <div style="display: flex; align-items: flex-end; gap: 6px; height: 76px; margin-top: 14px;">{bars}</div>
          <div style="display: flex; justify-content: space-between; font-size: 11px; color: var(--ink-3); margin-top: 8px;"><span>L</span><span>M</span><span>M</span><span>J</span><span>V</span><span>S</span><span>D</span></div>
        </div>
        <div class="card reveal d6" style="padding: 22px;">
          <div class="eyebrow">Tablero</div>
          <div style="display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 8px; margin-top: 12px;">
            <div style="text-align: center;"><div style="font-size: 22px; font-weight: 600;">5</div><div class="faint" style="font-size: 11px;">Por hacer</div></div>
            <div style="text-align: center;"><div style="font-size: 22px; font-weight: 600;">3</div><div class="faint" style="font-size: 11px;">En curso</div></div>
            <div style="text-align: center;"><div style="font-size: 22px; font-weight: 600;">2</div><div class="faint" style="font-size: 11px;">Revisión</div></div>
            <div style="text-align: center;"><div style="font-size: 22px; font-weight: 600;">8</div><div class="faint" style="font-size: 11px;">Hecho</div></div>
          </div>
        </div>
      </div>
    </div>
  </main>'''


# ================================================================ NUEVA REUNIÓN
def meeting_body():
    waves = "".join(f'<div class="wave-bar" style="height: {h}px; animation-delay: {i * 0.09:.2f}s;"></div>' for i, h in enumerate([18, 30, 44, 26, 52, 34, 20, 40, 56, 30, 22, 46, 28, 38, 18, 32, 48, 24]))
    thumb = lambda name: f'''<div style="border-radius: 14px; background: var(--surface-3); height: 96px; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 6px; color: var(--ink-3); border: 1px solid var(--line);">{icon("image", 22)}<span style="font-size: 11px;">{name}</span></div>'''
    return f'''
{rail("mic")}
  <main style="flex-grow: 1; padding: 34px 40px; display: flex; flex-direction: column; gap: 22px; min-width: 0;">
    <div style="display: flex; align-items: center; gap: 14px;">
      <div class="rail-btn" style="width: 40px; height: 40px; border-radius: 12px; background: var(--surface); border: 1px solid var(--line); color: var(--ink-2);">{icon("arrow-left", 18)}</div>
      <span class="faint" style="font-size: 13px;">Reuniones / Nueva reunión</span>
      <div style="flex-grow: 1;"></div>
      <span class="chip"><span class="dot pulse" style="background: var(--coral);"></span>Grabando · 12:34</span>
    </div>

    <div style="display: flex; align-items: flex-end; justify-content: space-between; gap: 24px;">
      <div style="flex-grow: 1;">
        <div class="eyebrow">Título de la reunión</div>
        <h1 style="font-size: 36px; font-weight: 600; line-height: 1.1; margin-top: 8px; border-bottom: 2px solid var(--line-strong); padding-bottom: 8px; display: inline-block; min-width: 620px;">Sync semanal — Plataforma de pagos<span class="caret"></span></h1>
      </div>
      <div style="display: flex; gap: 10px; align-items: center;">
        <span class="chip" style="height: 40px; padding: 0 14px; font-size: 13px;">{icon("branch", 16)}pagos-core{icon("chevron-down", 14)}</span>
        <div style="display: flex; align-items: center;">{avatar("MH", "lavender")}<span style="margin-left: -8px;">{avatar("AR", "mint")}</span><span style="margin-left: -8px;">{avatar("LP", "amber")}</span><span class="chip" style="margin-left: 6px; height: 30px;">{icon("plus", 14)}</span></div>
      </div>
    </div>

    <div style="display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 16px; flex-grow: 1; min-height: 0;">

      <div class="card reveal d1" style="padding: 0; display: flex; flex-direction: column; overflow: hidden;">
        <div style="background: var(--coral); color: var(--on-tile); padding: 22px; display: flex; flex-direction: column; gap: 16px;">
          <div style="display: flex; align-items: center; justify-content: space-between;">
            <div style="display: flex; align-items: center; gap: 10px; font-weight: 600; font-size: 15px;">{icon("mic", 18, "#15171c", 2)}Audio</div>
            <span style="font-size: 11px; font-weight: 600; letter-spacing: 0.06em; opacity: 0.7;">OPCIONAL</span>
          </div>
          <div style="display: flex; align-items: center; gap: 5px; height: 60px;">{waves}</div>
          <div style="display: flex; align-items: center; gap: 12px;">
            <div style="width: 52px; height: 52px; border-radius: 999px; background: var(--on-tile); display: flex; align-items: center; justify-content: center;">{icon("stop", 20, "#F7907F", 2)}</div>
            <div><div class="display" style="font-size: 24px; font-weight: 600; letter-spacing: 0;">12:34</div><div style="font-size: 12px; opacity: 0.72;">Micrófono de la sala</div></div>
          </div>
        </div>
        <div style="padding: 20px 22px; display: flex; flex-direction: column; gap: 10px; flex-grow: 1; min-height: 0;">
          <div class="eyebrow" style="display: flex; align-items: center; gap: 8px;">{icon("sparkle", 14)}Transcripción en vivo</div>
          <p class="muted" style="margin: 0; font-size: 13.5px; line-height: 1.6;">…entonces el pipeline de staging debería correr en los runners nuevos a partir del lunes. Andrea revisa que las variables de entorno del release estén documentadas.</p>
          <p style="margin: 0; font-size: 13.5px; line-height: 1.6;">Y el bug del deploy: cuando la migración falla, el job sigue en verde y nadie se entera<span class="caret"></span></p>
        </div>
      </div>

      <div class="card reveal d2" style="padding: 22px; display: flex; flex-direction: column; gap: 14px;">
        <div style="display: flex; align-items: center; justify-content: space-between;">
          <div style="display: flex; align-items: center; gap: 10px; font-weight: 600; font-size: 15px;">{icon("camera", 18)}Fotos de notas</div>
          <span class="eyebrow">Opcional</span>
        </div>
        <div style="border: 1.5px dashed var(--line-strong); border-radius: 18px; padding: 26px 16px; display: flex; flex-direction: column; align-items: center; gap: 8px; color: var(--ink-3); text-align: center;">
          <div style="width: 44px; height: 44px; border-radius: 14px; background: var(--surface-2); display: flex; align-items: center; justify-content: center;">{icon("plus", 20)}</div>
          <div style="font-size: 13px;">Arrastra fotos aquí o <a>elige archivos</a></div>
          <div style="font-size: 12px;">La IA lee la letra a mano y la cruza con el audio</div>
        </div>
        <div style="display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 10px;">{thumb("notas-1.jpg")}{thumb("notas-2.jpg")}</div>
        <div style="display: flex; align-items: center; gap: 8px; font-size: 13px; color: var(--ink-2);">{icon("check", 16, "var(--mint)", 2.2)}2 fotos leídas · 0 partes ilegibles</div>
      </div>

      <div class="card reveal d3" style="padding: 22px; display: flex; flex-direction: column; gap: 14px;">
        <div style="display: flex; align-items: center; justify-content: space-between;">
          <div style="display: flex; align-items: center; gap: 10px; font-weight: 600; font-size: 15px;">{icon("pen", 18)}Notas escritas</div>
          <span class="eyebrow">Opcional</span>
        </div>
        <div style="flex-grow: 1; border-radius: 18px; background: var(--surface-2); border: 1px solid var(--line); padding: 16px; font-size: 14px; line-height: 1.6; color: var(--ink);">
          <div>- Migrar runners de staging → lunes</div>
          <div>- Andrea documenta variables del release</div>
          <div>- Revisar por qué el deploy no falla con migraciones rotas</div>
          <div class="faint">- <span class="caret"></span></div>
        </div>
        <div class="faint" style="font-size: 12.5px; line-height: 1.5;">Si nadie grabó ni tomó fotos, escribe aquí los puntos tratados. También sirve para complementar lo demás.</div>
      </div>
    </div>

    <div style="display: flex; align-items: center; gap: 12px; padding-top: 4px;">
      <span class="faint" style="font-size: 13px;">Cualquier combinación sirve: audio, fotos, texto — o ninguno.</span>
      <div style="flex-grow: 1;"></div>
      <div class="btn btn-ghost">Guardar borrador</div>
      <div class="btn btn-primary">Cerrar reunión y generar minuta{icon("arrow-right", 18, "#15171c", 2)}</div>
    </div>
  </main>'''


# ================================================================ MINUTA
def minuta_body():
    li = lambda t: f'<div style="display: flex; gap: 12px; padding: 9px 12px; border-radius: 12px; line-height: 1.5;"><span class="dot" style="background: var(--ink-3); margin-top: 8px;"></span><span>{t}</span></div>'
    cand = lambda t, tipo, color, checked, who, wc: f'''
        <div style="border-radius: 18px; border: 1px solid {"var(--line-strong)" if checked else "var(--line)"}; background: var(--surface); padding: 16px; display: flex; gap: 14px; {"" if checked else "opacity: 0.55;"}">
          <div style="width: 22px; height: 22px; border-radius: 7px; flex-shrink: 0; margin-top: 1px; {"background: var(--coral); display: flex; align-items: center; justify-content: center;" if checked else "border: 1.5px solid var(--line-strong);"}">{icon("check", 14, "#15171c", 2.6) if checked else ""}</div>
          <div style="flex-grow: 1; min-width: 0; display: flex; flex-direction: column; gap: 10px;">
            <div style="font-weight: 600; font-size: 15px; line-height: 1.35;">{t}</div>
            <div style="display: flex; gap: 8px; flex-wrap: wrap; align-items: center;">
              <span class="chip"><span class="dot" style="background: var(--{color});"></span>{tipo}{icon("chevron-down", 12)}</span>
              <span class="chip">{icon("branch", 13)}pagos-core{icon("chevron-down", 12)}</span>
              <span class="chip" style="padding-left: 4px;">{avatar(who, wc).replace('class="avatar"', 'class="avatar" ').replace("width: 30px; height: 30px", "width: 22px; height: 22px")}Asignar</span>
            </div>
          </div>
        </div>'''
    return f'''
{rail("mic")}
  <main style="flex-grow: 1; padding: 34px 40px; display: flex; flex-direction: column; gap: 22px; min-width: 0;">
    <div style="display: flex; align-items: center; gap: 14px;">
      <div class="rail-btn" style="width: 40px; height: 40px; border-radius: 12px; background: var(--surface); border: 1px solid var(--line); color: var(--ink-2);">{icon("arrow-left", 18)}</div>
      <span class="faint" style="font-size: 13px;">Reuniones / Sync semanal — Plataforma de pagos / Minuta</span>
    </div>

    <div style="display: flex; align-items: flex-end; justify-content: space-between; gap: 24px;">
      <div>
        <h1 style="font-size: 34px; font-weight: 600; line-height: 1.1;">Minuta lista para revisar</h1>
        <div style="display: flex; gap: 8px; margin-top: 12px; align-items: center;">
          <span class="chip">{icon("mic", 13)}Audio 12:34</span>
          <span class="chip">{icon("camera", 13)}2 fotos</span>
          <span class="chip">{icon("pen", 13)}Notas</span>
          <span class="chip" style="background: transparent; border-style: dashed;">{icon("sparkle", 13)}Borrador generado por IA — nada se publica sin tu OK</span>
        </div>
      </div>
      <div style="display: flex; gap: 10px;">
        <div class="btn btn-ghost">{icon("download", 18)}Exportar minuta</div>
      </div>
    </div>

    <div style="display: grid; grid-template-columns: 1.3fr 1fr; gap: 16px; flex-grow: 1; min-height: 0;">
      <div class="card reveal d1" style="padding: 28px 30px; display: flex; flex-direction: column; gap: 22px; overflow: hidden;">
        <div>
          <div class="eyebrow" style="display: flex; align-items: center; justify-content: space-between;"><span>Temas tratados</span><span style="display: flex; align-items: center; gap: 6px; text-transform: none; letter-spacing: 0; font-weight: 500;">{icon("pen", 13)}Editable</span></div>
          <div style="margin-top: 8px; margin-left: -12px;">
            {li("Migración del pipeline de staging a los runners nuevos.")}
            {li("Comportamiento del job de deploy cuando falla una migración de base de datos.")}
            {li("Documentación de variables de entorno del release.")}
          </div>
        </div>
        <div>
          <div class="eyebrow">Decisiones</div>
          <div style="margin-top: 8px; margin-left: -12px;">
            {li("Los runners nuevos entran en staging a partir del lunes; producción una semana después si no hay incidentes.")}
            {li("Andrea documenta las variables del release antes del próximo sync.")}
          </div>
        </div>
        <div style="flex-grow: 1;"></div>
        <div style="border-radius: 18px; background: rgba(243,197,107,0.12); border: 1px solid rgba(243,197,107,0.35); padding: 16px 18px; display: flex; gap: 12px;">
          {icon("alert", 18, "var(--amber)", 1.8, "margin-top: 1px;")}
          <div style="font-size: 13.5px; line-height: 1.55;">
            <div style="font-weight: 600; margin-bottom: 4px;">2 cosas que conviene confirmar</div>
            <div class="muted">En el audio se dice “lunes” pero en las notas a mano aparece “martes” para la migración de runners.</div>
            <div class="muted">Una línea de las notas quedó cortada por el borde de la foto.</div>
          </div>
        </div>
      </div>

      <div style="display: flex; flex-direction: column; gap: 12px; min-height: 0;">
        <div style="display: flex; align-items: center; justify-content: space-between; padding: 0 4px;">
          <h2 style="font-size: 18px; font-weight: 600;">Candidatos a issue</h2>
          <span class="muted" style="font-size: 13px;">2 de 3 seleccionados</span>
        </div>
        <div class="reveal d2" style="display: flex; flex-direction: column; gap: 10px;">
          {cand("Mover runners de staging a los nodos nuevos", "tarea", "sky", True, "MH", "lavender")}
          {cand("El job de deploy no falla cuando la migración rompe", "bug", "coral", True, "AR", "mint")}
          {cand("Documentar variables de entorno del release", "tarea", "sky", False, "LP", "amber")}
          <div style="border: 1.5px dashed var(--line-strong); border-radius: 18px; padding: 14px; display: flex; align-items: center; justify-content: center; gap: 8px; color: var(--ink-3); font-size: 13.5px;">{icon("plus", 16)}Agregar un issue que la IA no detectó</div>
        </div>
        <div style="flex-grow: 1;"></div>
        <div class="card" style="padding: 16px; display: flex; align-items: center; gap: 12px; background: var(--surface-2);">
          <div style="font-size: 13px; line-height: 1.45;" class="muted">Cada issue guarda el enlace a esta minuta como origen.</div>
          <div class="btn btn-primary" style="margin-left: auto;">Crear 2 issues en GitLab{icon("arrow-right", 18, "#15171c", 2)}</div>
        </div>
      </div>
    </div>
  </main>'''


# ================================================================ TABLERO
def board_body():
    def card(t, labels, origin, who, wc, days, lifted=False):
        lab = "".join(f'<span class="chip" style="padding: 3px 8px; font-size: 11px;"><span class="dot" style="background: var(--{c}); width: 6px; height: 6px;"></span>{l}</span>' for l, c in labels)
        oi = "mic" if origin.startswith("Reunión") else "zap"
        style = "transform: rotate(-1.5deg) translateY(-4px); box-shadow: var(--shadow); border-color: var(--line-strong);" if lifted else ""
        return f'''
          <div class="card" style="padding: 14px 16px; display: flex; flex-direction: column; gap: 10px; {style}">
            <div style="font-weight: 600; font-size: 14px; line-height: 1.4;">{t}</div>
            <div style="display: flex; gap: 6px; flex-wrap: wrap;">{lab}</div>
            <div style="display: flex; align-items: center; gap: 8px; margin-top: 2px;">
              <span class="faint" style="display: inline-flex; align-items: center; gap: 5px; font-size: 11.5px;">{icon(oi, 12)}{origin}</span>
              <div style="flex-grow: 1;"></div>
              <span class="faint" style="font-size: 11.5px;">{days}</span>
              {avatar(who, wc).replace("width: 30px; height: 30px", "width: 24px; height: 24px").replace("font-size: 11px", "font-size: 9.5px")}
            </div>
          </div>'''

    def col(title, n, wip, cards, color):
        w = f'<span class="faint" style="font-size: 12px;">WIP {wip}</span>' if wip else ""
        return f'''
        <div style="display: flex; flex-direction: column; gap: 12px; min-width: 0;">
          <div style="display: flex; align-items: center; gap: 10px; padding: 0 6px;">
            <span class="dot" style="background: var(--{color});"></span>
            <span style="font-weight: 600; font-size: 14px;">{title}</span>
            <span class="chip" style="padding: 2px 8px; font-size: 11.5px;">{n}</span>
            <div style="flex-grow: 1;"></div>{w}
            {icon("plus", 16, "var(--ink-3)")}
          </div>
          <div style="display: flex; flex-direction: column; gap: 10px; padding: 10px; border-radius: 22px; background: var(--surface-2); border: 1px solid var(--line); flex-grow: 1; min-height: 0;">{cards}</div>
        </div>'''

    c1 = col("Por hacer", 4, None, "".join([
        card("Cachear dependencias de Flutter en el pipeline", [("mejora", "lavender"), ("infra-ci", "sky")], "Reunión 11 sep", "MH", "lavender", "hoy"),
        card("Documentar variables de entorno del release", [("tarea", "sky")], "Reunión 11 sep", "LP", "amber", "hoy"),
        card("Alerta cuando un runner se queda sin disco", [("mejora", "lavender")], "Rápido", "AR", "mint", "2d"),
        card("Revisar permisos del token de deploy", [("tarea", "sky"), ("seguridad", "coral")], "Rápido", "MH", "lavender", "3d"),
    ]), "ink-3")
    c2 = col("En progreso", 3, 4, "".join([
        card("Mover runners de staging a los nodos nuevos", [("tarea", "sky"), ("infra-ci", "sky")], "Reunión 11 sep", "MH", "lavender", "1d", lifted=True),
        card("Pantalla de login de la app móvil", [("feature", "mint"), ("app-mobile", "lavender")], "Reunión 8 sep", "AR", "mint", "4d"),
        card("Migrar secretos a variables protegidas", [("seguridad", "coral")], "Rápido", "LP", "amber", "2d"),
    ]), "amber")
    c3 = col("En revisión", 2, None, "".join([
        card("El job de deploy no falla cuando la migración rompe", [("bug", "coral"), ("pagos-core", "sky")], "Reunión 11 sep", "AR", "mint", "6h"),
        card("Limpiar imágenes viejas del registry", [("mejora", "lavender")], "Rápido", "MH", "lavender", "1d"),
    ]), "sky")
    c4 = col("Hecho", 8, None, "".join([
        card("Pipeline de release con aprobación manual", [("feature", "mint"), ("infra-ci", "sky")], "Reunión 1 sep", "MH", "lavender", "cerrado ayer"),
        card("Notificar a Slack cuando falla main", [("mejora", "lavender")], "Rápido", "LP", "amber", "cerrado mar"),
    ]) + '<div class="faint" style="text-align: center; font-size: 12.5px; padding: 8px;">+ 6 más esta semana</div>', "mint")

    filters = "".join(f'<span class="chip" style="height: 36px; padding: 0 14px; font-size: 13px; {"background: var(--ink); color: var(--bg); border-color: transparent;" if a else ""}">{t}</span>' for t, a in [("Todos", True), ("pagos-core", False), ("infra-ci", False), ("app-mobile", False)])
    return f'''
{rail("kanban")}
  <main style="flex-grow: 1; padding: 34px 40px; display: flex; flex-direction: column; gap: 22px; min-width: 0;">
    {topbar("Tablero", "", SEARCH + f'<div class="btn btn-primary">{icon("plus", 18, "#15171c", 2)}Nuevo issue</div>')}
    <div style="display: flex; align-items: center; gap: 8px;">
      {filters}
      <div style="flex-grow: 1;"></div>
      <span class="chip" style="height: 36px; padding: 0 14px;">{icon("users", 14)}Todos{icon("chevron-down", 12)}</span>
      <span class="chip" style="height: 36px; padding: 0 14px;">Sincronizado con GitLab · hace 1 min</span>
    </div>
    <div class="reveal d1" style="display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 14px; flex-grow: 1; min-height: 0;">
      {c1}{c2}{c3}{c4}
    </div>
  </main>'''


# ================================================================ ISSUE RÁPIDO (popup)
def quick_body():
    return f'''
  <div style="width: 100%; height: 100%; display: flex; align-items: center; justify-content: center; background: radial-gradient(120% 90% at 20% 0%, rgba(247,144,127,0.16), transparent 60%), radial-gradient(90% 70% at 100% 100%, rgba(189,169,247,0.16), transparent 60%), var(--bg);">
    <div class="card reveal" style="width: 520px; padding: 24px; display: flex; flex-direction: column; gap: 16px; box-shadow: var(--shadow); border-radius: 26px;">
      <div style="display: flex; align-items: center; gap: 12px;">
        <div style="width: 40px; height: 40px; border-radius: 13px; background: var(--amber); display: flex; align-items: center; justify-content: center;">{icon("zap", 20, "#15171c", 2)}</div>
        <div><div class="display" style="font-size: 18px; font-weight: 600;">Issue rápido</div><div class="faint" style="font-size: 12px;">Sin reunión · va a la cola de revisión</div></div>
        <div style="flex-grow: 1;"></div>
        <span class="chip" style="font-size: 11px;">Ctrl + Shift + I</span>
        {icon("x", 18, "var(--ink-3)")}
      </div>
      <div style="border-radius: 18px; background: var(--surface-2); border: 1px solid var(--line); padding: 16px; min-height: 120px; font-size: 15px; line-height: 1.55;">
        Luis pide que el reporte semanal se pueda exportar a PDF directo desde el tablero, sin pasar por reportes<span class="caret"></span>
      </div>
      <div style="display: flex; gap: 8px; flex-wrap: wrap; align-items: center;">
        <span class="chip">{icon("branch", 13)}app-desktop{icon("chevron-down", 12)}</span>
        <span class="chip" style="background: var(--ink); color: var(--bg); border-color: transparent;"><span class="dot" style="background: var(--lavender);"></span>mejora</span>
        <span class="chip"><span class="dot" style="background: var(--coral);"></span>bug</span>
        <span class="chip"><span class="dot" style="background: var(--sky);"></span>tarea</span>
        <div style="flex-grow: 1;"></div>
        <div class="pulse" style="width: 44px; height: 44px; border-radius: 999px; background: var(--coral); display: flex; align-items: center; justify-content: center;" title="Dictar">{icon("mic", 18, "#15171c", 2)}</div>
      </div>
      <div style="display: flex; align-items: center; gap: 12px; padding-top: 4px; border-top: 1px solid var(--line);">
        <span class="faint" style="font-size: 12.5px; line-height: 1.4;">No se publica en GitLab hasta que lo apruebes en “Por revisar”.</span>
        <div style="flex-grow: 1;"></div>
        <div class="btn btn-primary" style="height: 42px;">Enviar a revisión{icon("arrow-right", 16, "#15171c", 2)}</div>
      </div>
    </div>
  </div>'''


# ================================================================ REPORTES
def reports_body():
    kpi = lambda label, val, delta, good, d: f'''
      <div class="card reveal {d}" style="padding: 20px 22px; display: flex; flex-direction: column; gap: 8px;">
        <div class="eyebrow">{label}</div>
        <div style="font-size: 34px; font-weight: 600; line-height: 1;">{val}</div>
        <div style="font-size: 12.5px;"><span style="font-weight: 600; color: var(--{"mint" if good else "coral"});">{delta}</span> <span class="faint">vs. periodo anterior</span></div>
      </div>'''
    vals = [2, 4, 1, 3, 5, 0, 0, 3, 2, 4, 3]
    days = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11"]
    mx = max(vals)
    bars = ""
    for v, dname in zip(vals, days):
        h = int(v / mx * 280)
        label = f'<div style="font-size: 12px; font-weight: 600; margin-bottom: 6px;">{v}</div>' if v == mx else '<div style="height: 22px;"></div>'
        bars += f'''<div style="flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: flex-end; height: 100%;">{label}<div style="width: 22px; height: {max(h, 2)}px; background: var(--mint); border-radius: 4px 4px 0 0;"></div></div>'''
    labels = "".join(f'<div class="faint" style="flex: 1; text-align: center; font-size: 11px;">{d}</div>' for d in days)
    person = lambda who, wc, name, closed, prog, pct: f'''
        <div style="display: flex; align-items: center; gap: 12px; padding: 11px 0; border-bottom: 1px solid var(--line);">
          {avatar(who, wc)}
          <div style="width: 150px; font-weight: 500;">{name}</div>
          <div style="flex-grow: 1; height: 8px; border-radius: 4px; background: var(--surface-3); overflow: hidden;"><div style="width: {pct}%; height: 100%; background: var(--mint); border-radius: 4px;"></div></div>
          <div style="width: 84px; text-align: right; white-space: nowrap;"><b>{closed}</b> <span class="faint">cerrados</span></div>
          <div style="width: 84px; text-align: right; white-space: nowrap;"><b>{prog}</b> <span class="faint">en curso</span></div>
        </div>'''
    seg = "".join(f'<span style="padding: 8px 14px; border-radius: 10px; font-size: 13px; font-weight: 500; {"background: var(--ink); color: var(--bg);" if a else "color: var(--ink-2);"}">{t}</span>' for t, a in [("Hoy", False), ("Semana", True), ("Mes", False), ("Rango", False)])
    return f'''
{rail("chart")}
  <main style="flex-grow: 1; padding: 34px 40px; display: flex; flex-direction: column; gap: 22px; min-width: 0;">
    {topbar("Reportes", "Qué se hizo, quién lo hizo y de dónde salió", f'<div style="display: flex; gap: 2px; padding: 4px; border-radius: 14px; background: var(--surface); border: 1px solid var(--line);">{seg}</div><span class="chip" style="height: 44px; padding: 0 14px; font-size: 13px;">{icon("calendar", 15)}1 – 11 sep 2026</span><div class="btn btn-ink">{icon("download", 18)}Exportar</div>')}

    <div style="display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 14px;">
      {kpi("Issues cerrados", "27", "+6", True, "d1")}
      {kpi("Issues creados", "34", "+9", True, "d2")}
      {kpi("Tiempo medio en progreso", "2.3 d", "−0.6 d", True, "d3")}
      {kpi("Reuniones con minuta", "6", "+2", True, "d4")}
    </div>

    <div style="display: grid; grid-template-columns: 1.2fr 1fr; gap: 14px; flex-grow: 1; min-height: 0;">
      <div class="card reveal d4" style="padding: 24px; display: flex; flex-direction: column; gap: 10px;">
        <div style="display: flex; align-items: center; justify-content: space-between;">
          <h2 style="font-size: 17px; font-weight: 600;">Issues cerrados por día</h2>
          <span class="faint" style="font-size: 12.5px;">septiembre</span>
        </div>
        <div style="display: flex; gap: 22px; margin-top: 4px; font-size: 13px;" class="muted"><span><b style="color: var(--ink);">2.5</b> por día en promedio</span><span>Mejor día: <b style="color: var(--ink);">5 sep</b></span><span>Sin cierres: <b style="color: var(--ink);">fin de semana</b></span></div>
        <div style="flex-grow: 1;"></div>
        <div style="display: flex; align-items: stretch; gap: 8px; border-bottom: 1px solid var(--line-strong); height: 340px;">{bars}</div>
        <div style="display: flex; gap: 8px; margin-top: 8px;">{labels}</div>
      </div>
      <div style="display: flex; flex-direction: column; gap: 14px; min-height: 0;">
        <div class="card reveal d5" style="padding: 22px 24px; flex-grow: 1;">
          <h2 style="font-size: 17px; font-weight: 600;">Por persona</h2>
          <div style="margin-top: 6px;">
            {person("MH", "lavender", "Miguel Hernández", 11, 2, 100)}
            {person("AR", "mint", "Andrea Rojas", 9, 3, 82)}
            {person("LP", "amber", "Luis Pérez", 7, 1, 64)}
          </div>
          <h2 style="font-size: 17px; font-weight: 600; margin-top: 22px;">Por proyecto</h2>
          <div style="display: flex; flex-direction: column; gap: 10px; margin-top: 12px;">
            <div style="display: flex; align-items: center; gap: 12px;"><span class="chip">{icon("branch", 13)}infra-ci</span><div style="flex-grow: 1; height: 8px; border-radius: 4px; background: var(--surface-3); overflow: hidden;"><div style="width: 100%; height: 100%; background: var(--mint); border-radius: 4px;"></div></div><span style="width: 84px; text-align: right; white-space: nowrap;"><b>14</b> <span class="faint">cerrados</span></span></div>
            <div style="display: flex; align-items: center; gap: 12px;"><span class="chip">{icon("branch", 13)}pagos-core</span><div style="flex-grow: 1; height: 8px; border-radius: 4px; background: var(--surface-3); overflow: hidden;"><div style="width: 64%; height: 100%; background: var(--mint); border-radius: 4px;"></div></div><span style="width: 84px; text-align: right; white-space: nowrap;"><b>9</b> <span class="faint">cerrados</span></span></div>
            <div style="display: flex; align-items: center; gap: 12px;"><span class="chip">{icon("branch", 13)}app-mobile</span><div style="flex-grow: 1; height: 8px; border-radius: 4px; background: var(--surface-3); overflow: hidden;"><div style="width: 29%; height: 100%; background: var(--mint); border-radius: 4px;"></div></div><span style="width: 84px; text-align: right; white-space: nowrap;"><b>4</b> <span class="faint">cerrados</span></span></div>
          </div>
        </div>
        <div class="card reveal d6" style="padding: 22px 24px; display: flex; gap: 14px; align-items: center;">
          <div style="flex-grow: 1;">
            <div class="eyebrow">Origen de los issues</div>
            <div style="display: flex; gap: 14px; margin-top: 10px; font-size: 13px;">
              <span style="display: inline-flex; align-items: center; gap: 6px;"><span class="dot" style="background: var(--coral);"></span>Reunión <b>21</b></span>
              <span style="display: inline-flex; align-items: center; gap: 6px;"><span class="dot" style="background: var(--amber);"></span>Rápido <b>13</b></span>
            </div>
          </div>
          <div style="display: flex; width: 160px; height: 10px; border-radius: 5px; overflow: hidden; gap: 2px;"><div style="width: 62%; background: var(--coral);"></div><div style="flex-grow: 1; background: var(--amber);"></div></div>
        </div>
      </div>
    </div>
  </main>'''


# ================================================================ LOGIN
def login_body():
    field = lambda ic, label, val, pw=False: f'''
        <div style="display: flex; flex-direction: column; gap: 6px;">
          <label style="font-size: 12.5px; font-weight: 500; color: var(--ink-2);">{label}</label>
          <div style="display: flex; align-items: center; gap: 10px; height: 48px; padding: 0 14px; border-radius: 14px; background: var(--surface-2); border: 1px solid var(--line-strong); color: var(--ink);">{icon(ic, 17, "var(--ink-3)")}<span style="font-size: 14px; {"letter-spacing: 0.25em;" if pw else ""}">{val}</span></div>
        </div>'''
    return f'''
  <div style="width: 100%; height: 100%; display: grid; grid-template-columns: 1.1fr 1fr;">
    <div style="position: relative; overflow: hidden; background: var(--surface); border-right: 1px solid var(--line); padding: 48px; display: flex; flex-direction: column;">
      <div style="position: absolute; width: 520px; height: 520px; border-radius: 999px; background: var(--coral); right: -160px; top: -200px;"></div>
      <div style="position: absolute; width: 440px; height: 440px; border-radius: 999px; background: var(--lavender); right: -230px; bottom: -280px;"></div>
      <div style="position: absolute; width: 170px; height: 170px; border-radius: 52px; background: var(--amber); right: 150px; top: 330px; transform: rotate(18deg);"></div>
      <div style="position: absolute; width: 120px; height: 120px; border-radius: 999px; background: var(--mint); right: 40px; top: 400px;"></div>
      <div style="position: relative; display: flex; align-items: center; gap: 12px;">{LOGO}<span class="display" style="font-size: 18px; font-weight: 600;">IssueFlow</span></div>
      <div style="flex-grow: 1;"></div>
      <h1 class="reveal d1" style="position: relative; font-size: 58px; font-weight: 600; line-height: 1.02; max-width: 470px; text-wrap: pretty;">De la reunión al issue, sin fricción.</h1>
      <p class="reveal d2 muted" style="position: relative; font-size: 16px; max-width: 400px; margin: 18px 0 0; line-height: 1.55;">Graba, fotografía o escribe. IssueFlow arma la minuta, propone los issues y los crea en GitLab cuando tú digas.</p>
    </div>
    <div style="display: flex; align-items: center; justify-content: center; padding: 48px;">
      <div class="reveal d2" style="width: 400px; display: flex; flex-direction: column; gap: 22px;">
        <div>
          <h2 style="font-size: 28px; font-weight: 600;">Inicia sesión</h2>
          <div class="muted" style="margin-top: 6px; font-size: 14px;">Usa la cuenta que te asignó tu equipo.</div>
        </div>
        {field("mail", "Correo", "miguel@empresa.com")}
        {field("lock", "Contraseña", "••••••••••", True)}
        <div style="display: flex; align-items: center; justify-content: space-between; font-size: 13px;">
          <span style="display: inline-flex; align-items: center; gap: 8px;" class="muted"><span style="width: 18px; height: 18px; border-radius: 6px; background: var(--coral); display: inline-flex; align-items: center; justify-content: center;">{icon("check", 12, "#15171c", 3)}</span>Recordarme en este equipo</span>
          <a>¿Olvidaste la contraseña?</a>
        </div>
        <div class="btn btn-primary" style="justify-content: center; height: 50px; font-size: 15px;">Entrar{icon("arrow-right", 18, "#15171c", 2)}</div>
        <div style="display: flex; align-items: center; gap: 12px; color: var(--ink-3); font-size: 12px;"><div style="flex-grow: 1; height: 1px; background: var(--line);"></div>o<div style="flex-grow: 1; height: 1px; background: var(--line);"></div></div>
        <div class="btn btn-ghost" style="justify-content: center; height: 50px;">{icon("branch", 18)}Continuar con GitLab</div>
        <div class="faint" style="font-size: 12px; text-align: center; line-height: 1.5;">Conexión cifrada · Sesión ligada a este equipo</div>
      </div>
    </div>
  </div>'''


# ================================================================ escribir archivos
files = {
    "Main.dc.html": page("Inicio", dashboard_body()),
    "Reunion.dc.html": page("Nueva reunión", meeting_body()),
    "Minuta.dc.html": page("Minuta", minuta_body()),
    "Tablero.dc.html": page("Tablero", board_body()),
    "Reportes.dc.html": page("Reportes", reports_body()),
    "Login.dc.html": page("Login", login_body()),
    "IssueRapido.dc.html": page("Issue rápido", quick_body(), width=760, height=560),
    "InicioClaro.dc.html": page("Inicio (claro)", dashboard_body(), tokens=LIGHT),
}
for name, html in files.items():
    (OUT / name).write_text(html, encoding="utf-8")
    print("ok", name, len(html))
