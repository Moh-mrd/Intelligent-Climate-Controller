import copy, json
import pandas as pd, plotly.graph_objects as go, streamlit as st
from engine.fuzzy_controller import MFS, RULES, UNI, curve, infer, surface, check
from components.styles import CSS, H, PAL, LEVEL, rgba, head, kpi, badge, mu_card, gauge_svg, style

st.set_page_config(page_title="SMART CLIMATE AI", page_icon="❄️", layout="wide", initial_sidebar_state="expanded")
st.markdown(CSS, unsafe_allow_html=True)
CFG = {"displayModeBar": False}
PAGES = {"Dashboard": "▦", "Membership Functions": "∿", "Rule Engine": "☰", "Simulation Lab": "⚡",
         "Membership Editor": "⚙", "Decision Surface": "◬", "Learn Fuzzy Logic": "✧", "About Project": "ⓘ"}

if "mfs" not in st.session_state:
    st.session_state.mfs = copy.deepcopy(MFS)
MF = st.session_state.mfs  # per-session active (always validated) membership functions

# ---------- sidebar ----------
st.sidebar.markdown(H('<div class="brand"><div class="logo">❄</div><div><b>SMART CLIMATE AI</b><small>Fuzzy control studio</small></div></div>'), unsafe_allow_html=True)
page = st.sidebar.radio("Navigation", list(PAGES), format_func=lambda p: f"{PAGES[p]}   {p}", label_visibility="collapsed")
st.sidebar.markdown('<div class="side-h">Live inputs</div>', unsafe_allow_html=True)
t = st.sidebar.slider("Temperature (°C)", 0.0, 40.0, 25.0, 0.5)
h = st.sidebar.slider("Humidity (%)", 0.0, 100.0, 50.0, 1.0)
R = infer(t, h, MF)
st.sidebar.markdown(H(f'<div class="side-foot"><span class="pill" style="margin:0 0 8px"><span class="dot"></span>Engine online</span><br>Mamdani · min/max · centroid<br>{R["n_active"]}/{len(RULES)} rules active</div>'), unsafe_allow_html=True)


def plot(fig, key=None):
    st.plotly_chart(fig, width="stretch", config=CFG, key=key)


def mf_fig(var, title, xlabel, mark=None):
    f = go.Figure()
    for i, n in enumerate(MF[var]):
        f.add_scatter(x=UNI[var], y=curve(var, n, mfs=MF), name=n, fill="tozeroy", fillcolor=rgba(PAL[i], .10), line=dict(color=PAL[i], width=3))
    if mark is not None:
        f.add_vline(x=mark, line_dash="dot", line_color="#F472B6", annotation_text=f"  {mark:g}", annotation_font_color="#F472B6")
    return style(f, 340, title=title, xaxis_title=xlabel, yaxis_title="Membership μ", yaxis_range=[0, 1.05])


@st.cache_data
def cached_surface(mfs_json):
    return surface(mfs=json.loads(mfs_json))


# ---------- pages ----------
if page == "Dashboard":
    tl, hl = max(R["temp_mu"], key=R["temp_mu"].get), max(R["hum_mu"], key=R["hum_mu"].get)
    st.markdown(H(f'''<div class="hero"><span class="pill"><span class="dot"></span>System live · inference updating in real time</span>
    <h1>Intelligent Climate Controller</h1>
    <div class="sub">A Mamdani fuzzy system that turns vague notions of “hot” and “humid” into a precise cooling decision.</div>
    <div class="chips"><div class="chip">Temperature<b>{t:g} °C</b></div><div class="chip">Humidity<b>{h:g} %</b></div>
    <div class="chip">Cooling output<b>{R["output"]:.1f} %</b></div><div class="chip">Decision<b>{R["label"]}</b></div></div></div>'''), unsafe_allow_html=True)
    c1, c2 = st.columns([1, 1.25], gap="large")
    with c1, st.container(border=True):
        st.markdown(gauge_svg(R["output"], R["label"]), unsafe_allow_html=True)
    with c2:
        st.markdown(H(f'''<div class="glass"><div class="eyebrow">Decision {badge(R["label"])}</div>
        <h3 style="margin:10px 0 8px;font-weight:700">Recommended: {R["label"].lower()} cooling at {R["output"]:.1f}%</h3>
        <p>Temperature of {t:g}°C is mostly <b style="color:#E6EAF5">{tl.lower()}</b> (μ={R["temp_mu"][tl]:.2f}) and humidity of {h:g}% is mostly
        <b style="color:#E6EAF5">{hl.lower()}</b> (μ={R["hum_mu"][hl]:.2f}). {R["n_active"]} of {len(RULES)} rules fired and were aggregated, then defuzzified by centroid.</p></div>'''), unsafe_allow_html=True)
        k1, k2 = st.columns(2)
        k1.markdown(kpi("Active rules", f'{R["n_active"]}/{len(RULES)}', "non-zero activation", R["n_active"] / len(RULES)), unsafe_allow_html=True)
        k2.markdown(kpi("Peak activation", f'{max(R["activations"]):.2f}', "strongest rule", max(R["activations"]), "#8B5CF6"), unsafe_allow_html=True)
    st.markdown('<div class="sec">Membership degrees</div>', unsafe_allow_html=True)
    a, b, c = st.columns(3, gap="medium")
    a.markdown(mu_card("Temperature", R["temp_mu"], PAL[0]), unsafe_allow_html=True)
    b.markdown(mu_card("Humidity", R["hum_mu"], PAL[1]), unsafe_allow_html=True)
    c.markdown(mu_card("Cooling output", R["out_mu"], PAL[2]), unsafe_allow_html=True)
    st.markdown('<div class="sec">Fuzzification & defuzzification</div>', unsafe_allow_html=True)
    d1, d2 = st.columns(2, gap="medium")
    with d1, st.container(border=True):
        fz = go.Figure()
        for nm, d, col in [("Temperature", R["temp_mu"], PAL[0]), ("Humidity", R["hum_mu"], PAL[2])]:
            fz.add_bar(x=list(d), y=list(d.values()), name=nm, marker=dict(color=col, line_width=0))
        plot(style(fz, 340, title="One input, several fuzzy sets", barmode="group", yaxis_range=[0, 1.05], bargap=.35), "fz")
    with d2, st.container(border=True):
        ag = go.Figure()
        ag.add_scatter(x=UNI["cool"], y=R["aggregated"], fill="tozeroy", name="Aggregated output", line=dict(color=PAL[2], width=3), fillcolor=rgba(PAL[2], .25))
        ag.add_vline(x=R["output"], line_color="#F472B6", line_dash="dot", annotation_text=f"  centroid {R['output']:.2f}", annotation_font_color="#F472B6")
        plot(style(ag, 340, title="Aggregated fuzzy set & centroid", xaxis_title="Cooling power (%)", yaxis_title="μ", yaxis_range=[0, 1.05]), "ag")

elif page == "Membership Functions":
    st.markdown(head("Fuzzification", "Membership Functions", "How crisp values map to graded membership. The dotted line marks your current live input."), unsafe_allow_html=True)
    for k, (var, ttl, xl, mk) in enumerate([("temp", "Temperature", "°C", t), ("hum", "Humidity", "%", h), ("cool", "Cooling power", "%", R["output"])]):
        with st.container(border=True):
            plot(mf_fig(var, ttl, xl, mk), f"mf{k}")

elif page == "Rule Engine":
    st.markdown(head("Inference", "Rule Engine", "Each rule’s strength is min(μ_temperature, μ_humidity). Active rules light up with your live inputs."), unsafe_allow_html=True)
    rows = "".join(
        f'<tr class="{"" if w > 0 else "off"}"><td>R{i+1}</td><td>IF <span class="tag">{a}</span> AND <span class="tag">{b}</span></td><td>{badge(c)}</td>'
        f'<td><div class="mu" style="margin:0"><div><span>{w:.3f}</span></div><div class="bar"><i style="width:{w*100:.1f}%;background:linear-gradient(90deg,#22D3EE,#8B5CF6)"></i></div></div></td></tr>'
        for i, ((a, b, c), w) in enumerate(zip(RULES, R["activations"])))
    st.markdown(H(f'<div class="glass"><table class="rt"><tr><th>ID</th><th>Condition (Temp · Humidity)</th><th>Then cooling</th><th>Activation</th></tr>{rows}</table></div>'), unsafe_allow_html=True)
    st.write("")
    with st.container(border=True):
        bar = go.Figure(go.Bar(x=[f"R{i+1}" for i in range(len(RULES))], y=R["activations"], marker=dict(color=R["activations"], colorscale=[[0, "#3B82F6"], [1, "#22D3EE"]], line_width=0)))
        plot(style(bar, 300, title="Rule activation strengths", yaxis_range=[0, 1.05]), "rb")

elif page == "Simulation Lab":
    st.markdown(head("Testing", "Simulation Lab", "Run predefined or custom scenarios through the real fuzzy controller and compare outputs."), unsafe_allow_html=True)
    sc = {"Cold & dry": (5, 15), "Cold & humid": (5, 90), "Moderate & normal": (23, 50), "Hot & dry": (37, 15), "Hot & humid": (37, 90)}
    with st.container(border=True):
        c1, c2, c3 = st.columns([1, 1, 2])
        cust_t = c1.number_input("Custom temperature (°C)", 0.0, 40.0, 28.0)
        cust_h = c2.number_input("Custom humidity (%)", 0.0, 100.0, 60.0)
        sc["Custom"] = (cust_t, cust_h)
        pick = c3.multiselect("Scenarios to run", list(sc), default=list(sc))
    if pick:
        res = {k: infer(*sc[k], MF) for k in pick}
        cards = "".join(f'<div class="glass kpi"><div class="l">{k}</div><div class="v">{r["output"]:.1f}%</div><div class="s">{sc[k][0]:g}°C · {sc[k][1]:g}% RH &nbsp;{badge(r["label"])}</div><div class="bar"><i style="width:{r["output"]:.0f}%;background:linear-gradient(90deg,#22D3EE,#8B5CF6)"></i></div></div>' for k, r in res.items())
        st.markdown(f'<div class="sec">Results</div><div class="grid">{H(cards)}</div>', unsafe_allow_html=True)
        df = pd.DataFrame([{"Scenario": k, "Temperature": sc[k][0], "Humidity": sc[k][1], "Cooling %": round(r["output"], 2), "Class": r["label"]} for k, r in res.items()])
        st.write("")
        l, r_ = st.columns([1.1, 1], gap="medium")
        with l, st.container(border=True):
            fg = go.Figure(go.Bar(x=df["Scenario"], y=df["Cooling %"], marker=dict(color=df["Cooling %"], colorscale=[[0, "#3B82F6"], [.5, "#8B5CF6"], [1, "#F472B6"]], line_width=0)))
            plot(style(fg, 340, title="Cooling output per scenario", yaxis_range=[0, 100]), "sim")
        with r_:
            st.dataframe(df, width="stretch", hide_index=True)
            st.download_button("⬇  Download CSV", df.to_csv(index=False), "results.csv", "text/csv")

elif page == "Membership Editor":
    st.markdown(head("Configuration", "Membership Editor", "Edit every membership function. Invalid configurations are rejected and never reach the inference engine."), unsafe_allow_html=True)
    NAMES = {"temp": ("Temperature", "°C"), "hum": ("Humidity", "%"), "cool": ("Cooling power", "%")}

    def reset_mfs():
        st.session_state.mfs = copy.deepcopy(MFS)
        for v in MFS:
            for n, (_, p) in MFS[v].items():
                for i, x in enumerate(p):
                    st.session_state[f"p_{v}_{n}_{i}"] = float(x)

    cand = {}
    for var in MFS:
        with st.container(border=True):
            st.markdown(f'<div class="eyebrow">{NAMES[var][0]} ({NAMES[var][1]})</div>', unsafe_allow_html=True)
            cand[var] = {}
            for n, (kind, p0) in MFS[var].items():
                cols = st.columns([1.3] + [1] * len(p0))
                cols[0].markdown(f"**{n}** · {'trapezoid' if kind == 'trap' else 'triangle'}")
                vals = [cols[i + 1].number_input("abcd"[i], key=f"p_{var}_{n}_{i}", value=float(MF[var][n][1][i]), step=1.0, min_value=-1000.0, max_value=1000.0) for i in range(len(p0))]
                cand[var][n] = (kind, vals)
    errs = check(cand)
    if errs:
        st.markdown(H('<div class="glass" style="border-color:rgba(244,114,182,.55)"><div class="eyebrow" style="color:#F472B6">Configuration rejected — previous valid setup kept</div>' + "".join(f"<p>⚠ {e}</p>" for e in errs) + "</div>"), unsafe_allow_html=True)
    else:
        if json.dumps(cand) != json.dumps(MF):
            st.session_state.mfs = cand
            st.rerun()
        st.markdown(H('<div class="pill"><span class="dot"></span>Configuration valid and applied across the whole app</div>'), unsafe_allow_html=True)
    st.button("↺  Reset to defaults", on_click=reset_mfs)
    st.markdown('<div class="sec">Live preview</div>', unsafe_allow_html=True)
    for k, (var, ttl, xl, mk) in enumerate([("temp", "Temperature", "°C", t), ("hum", "Humidity", "%", h), ("cool", "Cooling power", "%", R["output"])]):
        with st.container(border=True):
            plot(mf_fig(var, ttl, xl, mk), f"ed{k}")

elif page == "Decision Surface":
    st.markdown(head("Visualization", "Decision Surface", "The full input–output map of the controller, computed point by point by the real inference engine."), unsafe_allow_html=True)
    ts, hs, z = cached_surface(json.dumps(MF))
    with st.container(border=True):
        f = go.Figure(go.Surface(x=ts, y=hs, z=z, colorscale=[[0, "#1E3A8A"], [.35, "#3B82F6"], [.65, "#8B5CF6"], [1, "#F472B6"]], colorbar=dict(title="Cooling %", thickness=12), lighting=dict(ambient=.7)))
        f.add_scatter3d(x=[t], y=[h], z=[R["output"]], mode="markers", marker=dict(size=7, color="#22D3EE", line=dict(color="white", width=2)), name="Current input")
        sc3 = dict(xaxis_title="Temperature (°C)", yaxis_title="Humidity (%)", zaxis_title="Cooling (%)", bgcolor="rgba(0,0,0,0)")
        for ax in ("xaxis", "yaxis", "zaxis"):
            sc3[ax] = dict(gridcolor="rgba(255,255,255,.08)", backgroundcolor="rgba(0,0,0,0)", title=sc3.pop(ax + "_title"))
        plot(style(f, 620, title="Cooling power = f(temperature, humidity)", scene=sc3), "surf")
    if st.toggle("Show 2D contour map"):
        with st.container(border=True):
            ct = go.Figure(go.Contour(x=ts, y=hs, z=z, colorscale=[[0, "#1E3A8A"], [.5, "#8B5CF6"], [1, "#F472B6"]], contours_coloring="heatmap"))
            ct.add_scatter(x=[t], y=[h], mode="markers", marker=dict(size=12, color="#22D3EE", line=dict(color="white", width=2)), name="Current input")
            plot(style(ct, 440, title="Contour map", xaxis_title="Temperature (°C)", yaxis_title="Humidity (%)"), "cont")

elif page == "Learn Fuzzy Logic":
    st.markdown(head("Education", "Learn Fuzzy Logic", "The ideas behind the controller, in the order the data flows through it."), unsafe_allow_html=True)
    steps = [("01", "Crisp inputs", "Exact sensor readings, like 26 °C and 62 % humidity."), ("02", "Fuzzification", "Each reading gets a membership degree in every fuzzy set it touches."),
             ("03", "Rule evaluation", "IF Hot AND Humid THEN High. AND is the minimum of the degrees."), ("04", "Aggregation", "Every rule’s clipped output set is merged with the maximum."),
             ("05", "Defuzzification", "The centroid of the merged shape gives one crisp cooling value."), ("06", "Output", "Cooling power from 0 to 100 %, ready to drive the actuator.")]
    st.markdown('<div class="grid">' + "".join(H(f'<div class="glass"><div class="step">{n}</div><h4>{a}</h4><p>{b}</p></div>') for n, a, b in steps) + "</div>", unsafe_allow_html=True)
    st.markdown('<div class="sec">Classical vs fuzzy</div>', unsafe_allow_html=True)
    x1, x2 = st.columns(2, gap="medium")
    x1.markdown(H('<div class="glass"><div class="step">CLASSICAL</div><h4>True or false</h4><p>“Hot” means above 30 °C. 29.9 °C is not hot, 30.1 °C is. Truth is 0 or 1, so decisions jump abruptly.</p></div>'), unsafe_allow_html=True)
    x2.markdown(H('<div class="glass"><div class="step">FUZZY</div><h4>Degrees of truth</h4><p>28 °C can be partly moderate and partly hot at once. Truth is a value in [0, 1], so decisions change smoothly.</p></div>'), unsafe_allow_html=True)
    st.markdown('<div class="sec">Mathematics</div>', unsafe_allow_html=True)
    with st.container(border=True):
        st.latex(r"\mu_A : X \to [0,1] \qquad w_k=\min\big(\mu_{T_k}(t),\,\mu_{H_k}(h)\big)")
        st.latex(r"\mu'_k(y)=\min\big(w_k,\mu_{C_k}(y)\big) \qquad \mu_{agg}(y)=\max_k \mu'_k(y)")
        st.latex(r"y^*=\frac{\int y\,\mu_{agg}(y)\,dy}{\int \mu_{agg}(y)\,dy}")

else:
    st.markdown(head("Project", "About Project", "Intelligent Climate Controller Using Fuzzy Logic"), unsafe_allow_html=True)
    info = [("Module", "Knowledge Representation and Reasoning (RC)"), ("Chapter", "Chapter 3 – Fuzzy Set Theory"), ("University", "Université de Batna 2"),
            ("Department", "Computer Science"), ("Academic year", "2026/2027"), ("Instructor", "Dr. Baghiani Radouane")]
    st.markdown('<div class="grid">' + "".join(H(f'<div class="glass kpi"><div class="l">{a}</div><div style="font-size:16px;font-weight:600;margin-top:8px">{b}</div></div>') for a, b in info) + "</div>", unsafe_allow_html=True)
    st.markdown('<div class="sec">Educational objectives</div>', unsafe_allow_html=True)
    objs = ["Formal modeling of vague concepts", "Use of AI tools", "Intelligent reasoning with imprecision", "Critical analysis", "Scientific writing"]
    st.markdown('<div class="grid">' + "".join(H(f'<div class="glass"><div class="step">0{i+1}</div><h4>{o}</h4></div>') for i, o in enumerate(objs)) + "</div>", unsafe_allow_html=True)
    st.markdown('<div class="sec">Coverage guarantee</div>', unsafe_allow_html=True)
    st.markdown(H('<div class="glass"><p>The 3×3 rule base covers every (temperature, humidity) pair and each universe is fully covered by its membership functions, so inference is defined everywhere in the domain.</p></div>'), unsafe_allow_html=True)
