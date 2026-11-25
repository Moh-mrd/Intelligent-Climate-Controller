"""Design system: CSS, HTML helpers and Plotly theme for SMART CLIMATE AI."""
import re

PAL = ["#22D3EE", "#3B82F6", "#8B5CF6"]
LEVEL = {"Low": "#22D3EE", "Medium": "#8B5CF6", "High": "#F472B6"}


def H(s):
    """Collapse HTML to one line so Markdown never treats it as a code block."""
    return re.sub(r"\n\s*", "", s).strip()


def rgba(hex_, a):
    h = hex_.lstrip("#")
    return f"rgba({int(h[0:2], 16)},{int(h[2:4], 16)},{int(h[4:6], 16)},{a})"


CSS = """<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500&display=swap');
:root{--line:rgba(255,255,255,.08);--cy:#22D3EE;--bl:#3B82F6;--vi:#8B5CF6;--tx:#E6EAF5;--mut:#8B93A7}
html,body,.stApp,[class*="css"]{font-family:'Inter',sans-serif;color:var(--tx)}
.stApp{background:radial-gradient(900px 520px at 88% -8%,rgba(139,92,246,.20),transparent 60%),radial-gradient(800px 520px at -8% 6%,rgba(34,211,238,.13),transparent 60%),#050816}
#MainMenu,footer,[data-testid="stDecoration"],[data-testid="stMainMenu"],[data-testid="stAppDeployButton"],[data-testid="stToolbarActions"]{display:none!important}
[data-testid="stExpandSidebarButton"],[data-testid="stSidebarCollapsedControl"]{display:flex!important;visibility:visible!important;opacity:1!important;color:#22D3EE!important;background:rgba(34,211,238,.12)!important;border:1px solid rgba(34,211,238,.45)!important;border-radius:10px!important;box-shadow:0 0 18px rgba(34,211,238,.25);transition:all .2s}
[data-testid="stExpandSidebarButton"]:hover,[data-testid="stSidebarCollapsedControl"]:hover{background:rgba(34,211,238,.25)!important;transform:scale(1.08)}
header[data-testid="stHeader"]{background:transparent}
.block-container{padding:2rem 3rem 4rem;max-width:1280px}
h1,h2,h3{letter-spacing:-.02em}
/* sidebar */
section[data-testid="stSidebar"]{background:linear-gradient(180deg,#070B1C,#050816);border-right:1px solid var(--line)}
section[data-testid="stSidebar"] .block-container,section[data-testid="stSidebar"]>div{padding-top:1rem}
.brand{display:flex;gap:12px;align-items:center;padding:6px 4px 18px}
.logo{width:38px;height:38px;border-radius:11px;display:grid;place-items:center;font-size:19px;background:linear-gradient(135deg,#22D3EE,#8B5CF6);box-shadow:0 6px 24px rgba(34,211,238,.35)}
.brand b{font-size:15px;letter-spacing:.06em}.brand small{display:block;color:var(--mut);font-size:11px}
.side-h{font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--mut);margin:22px 4px 6px}
[data-testid="stSidebar"] [role="radiogroup"]{gap:3px}
[data-testid="stSidebar"] [role="radiogroup"] label{width:100%;padding:9px 12px;border-radius:10px;border:1px solid transparent;transition:all .18s ease;cursor:pointer}
[data-testid="stSidebar"] [role="radiogroup"] label>div:first-child{display:none}
[data-testid="stSidebar"] [role="radiogroup"] label:hover{background:rgba(255,255,255,.05);transform:translateX(4px)}
[data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked){background:linear-gradient(90deg,rgba(34,211,238,.16),rgba(139,92,246,.12));border-color:rgba(34,211,238,.35);box-shadow:0 0 24px rgba(34,211,238,.10)}
[data-testid="stSidebar"] [role="radiogroup"] label p{font-size:14px;font-weight:500}
[data-testid="stSlider"] [role="slider"]{background:#22D3EE!important;box-shadow:0 0 0 4px rgba(34,211,238,.22);transition:box-shadow .2s}
[data-testid="stSlider"] [role="slider"]:hover{box-shadow:0 0 0 8px rgba(34,211,238,.25)}
[data-testid="stSlider"] label p{color:var(--mut);font-size:12px}
.side-foot{margin-top:28px;padding:12px;border-radius:12px;border:1px solid var(--line);background:rgba(255,255,255,.03);font-size:12px;color:var(--mut)}
/* surfaces */
div[data-testid="stVerticalBlockBorderWrapper"]{background:linear-gradient(180deg,rgba(255,255,255,.055),rgba(255,255,255,.02));border:1px solid var(--line)!important;border-radius:18px!important;box-shadow:0 10px 40px rgba(0,0,0,.35);backdrop-filter:blur(14px);transition:border-color .25s,transform .25s}
div[data-testid="stVerticalBlockBorderWrapper"]:hover{border-color:rgba(34,211,238,.28)!important}
.glass{background:linear-gradient(180deg,rgba(255,255,255,.055),rgba(255,255,255,.02));border:1px solid var(--line);border-radius:18px;padding:20px 22px;box-shadow:0 10px 40px rgba(0,0,0,.35);backdrop-filter:blur(14px);transition:all .25s ease;height:100%}
.glass:hover{border-color:rgba(34,211,238,.3);transform:translateY(-2px)}
.hero{position:relative;padding:34px 36px;border-radius:24px;margin-bottom:26px;border:1px solid var(--line);overflow:hidden;background:linear-gradient(135deg,rgba(34,211,238,.10),rgba(139,92,246,.12) 55%,rgba(59,130,246,.06))}
.hero:after{content:"";position:absolute;right:-80px;top:-80px;width:300px;height:300px;border-radius:50%;background:radial-gradient(circle,rgba(139,92,246,.35),transparent 70%)}
.eyebrow{font-size:12px;letter-spacing:.16em;text-transform:uppercase;color:var(--cy);font-weight:600}
.hero h1,.ph h1{font-size:44px;line-height:1.08;font-weight:800;margin:10px 0 10px;background:linear-gradient(90deg,#fff,#A5F3FC 45%,#C4B5FD);-webkit-background-clip:text;background-clip:text;color:transparent;padding:0}
.ph{margin-bottom:22px}.ph h1{font-size:34px;margin:6px 0 6px}
.sub{color:var(--mut);font-size:15px;max-width:640px;line-height:1.6}
.pill{display:inline-flex;gap:8px;align-items:center;padding:6px 12px;border-radius:99px;font-size:12px;font-weight:600;border:1px solid rgba(16,185,129,.35);background:rgba(16,185,129,.10);color:#6EE7B7;margin-bottom:6px}
.dot{width:8px;height:8px;border-radius:50%;background:#10B981;box-shadow:0 0 0 0 rgba(16,185,129,.6);animation:pulse 2s infinite}
@keyframes pulse{70%{box-shadow:0 0 0 9px rgba(16,185,129,0)}100%{box-shadow:0 0 0 0 rgba(16,185,129,0)}}
.chips{display:flex;gap:10px;flex-wrap:wrap;margin-top:20px;position:relative;z-index:1}
.chip{padding:8px 14px;border-radius:12px;background:rgba(5,8,22,.55);border:1px solid var(--line);font-size:12px;color:var(--mut)}
.chip b{display:block;font-family:'JetBrains Mono',monospace;font-size:17px;color:var(--tx);margin-top:2px}
.sec{font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:var(--mut);margin:26px 2px 12px;font-weight:600}
/* kpi */
.kpi .l{font-size:12px;color:var(--mut);letter-spacing:.06em;text-transform:uppercase}
.kpi .v{font-size:32px;font-weight:700;margin:6px 0 2px;font-family:'JetBrains Mono',monospace}.kpi .s{font-size:12px;color:var(--mut)}
.bar{height:6px;border-radius:9px;background:rgba(255,255,255,.07);overflow:hidden;margin-top:6px}
.bar i{display:block;height:100%;border-radius:9px;animation:grow 1s cubic-bezier(.2,.8,.2,1);transition:width .6s}
@keyframes grow{from{width:0}}
.mu{margin:12px 0}.mu div{display:flex;justify-content:space-between;font-size:13px}.mu span{font-family:'JetBrains Mono',monospace;color:var(--mut)}
.badge{display:inline-block;padding:3px 10px;border-radius:99px;font-size:12px;font-weight:600}
/* gauge */
.gauge{position:relative;max-width:300px;margin:0 auto}.gauge svg{width:100%;filter:drop-shadow(0 0 18px rgba(34,211,238,.25))}
.arc{animation:draw 1.2s cubic-bezier(.2,.8,.2,1)}@keyframes draw{from{stroke-dasharray:0 600}}
.gnum{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;padding-top:6px}
.gnum b{font-size:46px;font-family:'JetBrains Mono',monospace}.gnum span{color:var(--mut);font-size:12px;letter-spacing:.12em;text-transform:uppercase}
.seg{display:flex;gap:6px;margin-top:10px}.seg div{flex:1;text-align:center;padding:7px 0;border-radius:9px;font-size:12px;font-weight:600;border:1px solid var(--line);color:var(--mut);transition:all .3s}
/* rule table */
.rt{width:100%;border-collapse:separate;border-spacing:0 8px}.rt th{font-size:11px;letter-spacing:.12em;text-transform:uppercase;color:var(--mut);text-align:left;padding:0 12px;font-weight:600}
.rt td{padding:13px 12px;background:rgba(255,255,255,.03);font-size:13.5px;border-top:1px solid var(--line);border-bottom:1px solid var(--line);transition:background .2s}
.rt tr:hover td{background:rgba(34,211,238,.07)}.rt td:first-child{border-left:1px solid var(--line);border-radius:12px 0 0 12px;font-family:'JetBrains Mono',monospace;color:var(--cy)}
.rt td:last-child{border-right:1px solid var(--line);border-radius:0 12px 12px 0;min-width:170px}.rt tr.off td{opacity:.45}
.tag{display:inline-block;padding:2px 9px;border-radius:7px;background:rgba(139,92,246,.15);color:#C4B5FD;font-size:12.5px;margin:0 2px}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:14px}
.step{font-family:'JetBrains Mono',monospace;color:var(--cy);font-size:12px}.glass h4{margin:6px 0 6px;font-size:16px}.glass p{color:var(--mut);font-size:13.5px;line-height:1.6;margin:0}
.stButton button,.stDownloadButton button{border-radius:12px;border:1px solid rgba(34,211,238,.4);background:linear-gradient(135deg,rgba(34,211,238,.18),rgba(139,92,246,.18));color:#fff;font-weight:600;transition:all .2s}
.stButton button:hover,.stDownloadButton button:hover{transform:translateY(-2px);box-shadow:0 8px 28px rgba(34,211,238,.25);border-color:#22D3EE}
[data-testid="stDataFrame"]{border-radius:14px;overflow:hidden;border:1px solid var(--line)}
@media(max-width:768px){.block-container{padding:1.2rem 1rem}.hero{padding:22px}.hero h1{font-size:30px}}
</style>"""


def head(eyebrow, title, sub):
    return H(f'<div class="ph"><div class="eyebrow">{eyebrow}</div><h1>{title}</h1><div class="sub">{sub}</div></div>')


def kpi(label, value, sub="", pct=None, color="#22D3EE"):
    bar = f'<div class="bar"><i style="width:{pct*100:.0f}%;background:linear-gradient(90deg,{color},#8B5CF6)"></i></div>' if pct is not None else ""
    return H(f'<div class="glass kpi"><div class="l">{label}</div><div class="v">{value}</div><div class="s">{sub}</div>{bar}</div>')


def badge(label):
    c = LEVEL.get(label, "#22D3EE")
    return f'<span class="badge" style="color:{c};background:{rgba(c, .14)};border:1px solid {rgba(c, .4)}">{label}</span>'


def mu_card(title, d, accent):
    rows = "".join(f'<div class="mu"><div>{k}<span>{v:.3f}</span></div><div class="bar"><i style="width:{v*100:.1f}%;background:linear-gradient(90deg,{accent},{rgba(accent, .45)})"></i></div></div>' for k, v in d.items())
    return H(f'<div class="glass"><div class="kpi"><div class="l">{title}</div></div>{rows}</div>')


def gauge_svg(value, label):
    C = 2 * 3.14159265 * 78
    arc, val = C * .75, C * .75 * max(0, min(value, 100)) / 100
    segs = "".join(
        f'<div style="{"color:%s;background:%s;border-color:%s" % (LEVEL[k], rgba(LEVEL[k], .14), rgba(LEVEL[k], .5)) if k == label else ""}">{k}</div>'
        for k in LEVEL)
    return H(f'''<div class="gauge"><svg viewBox="0 0 200 200"><defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#22D3EE"/><stop offset="1" stop-color="#8B5CF6"/></linearGradient></defs>
    <circle cx="100" cy="100" r="78" fill="none" stroke="rgba(255,255,255,.07)" stroke-width="12" stroke-linecap="round" stroke-dasharray="{arc} {C}" transform="rotate(135 100 100)"/>
    <circle class="arc" cx="100" cy="100" r="78" fill="none" stroke="url(#g)" stroke-width="12" stroke-linecap="round" stroke-dasharray="{val} {C}" transform="rotate(135 100 100)"/></svg>
    <div class="gnum"><b>{value:.1f}%</b><span>Cooling power</span></div></div><div class="seg">{segs}</div>''')


def style(f, h=380, **kw):
    f.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", height=h,
                    font=dict(family="Inter", color="#9AA4BC"), margin=dict(l=8, r=8, t=56, b=8),
                    legend=dict(orientation="h", y=1.14, x=0), title_font=dict(size=15, color="#E6EAF5"),
                    hoverlabel=dict(bgcolor="#0B1020", bordercolor="#22D3EE", font_family="Inter"), **kw)
    f.update_xaxes(gridcolor="rgba(255,255,255,.05)", zeroline=False, linecolor="rgba(255,255,255,.1)")
    f.update_yaxes(gridcolor="rgba(255,255,255,.05)", zeroline=False)
    return f
