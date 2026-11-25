"""Mamdani fuzzy inference (min-AND, min-implication, max-aggregation, centroid)."""
import numpy as np
import skfuzzy as fuzz

UNI = {"temp": np.linspace(0, 40, 401), "hum": np.linspace(0, 100, 501), "cool": np.linspace(0, 100, 501)}
MFS = {
    "temp": {"Cold": ("trap", [0, 0, 12, 20]), "Moderate": ("tri", [15, 23, 30]), "Hot": ("trap", [25, 32, 40, 40])},
    "hum": {"Dry": ("trap", [0, 0, 25, 40]), "Normal": ("tri", [30, 50, 70]), "Humid": ("trap", [60, 75, 100, 100])},
    "cool": {"Low": ("trap", [0, 0, 20, 40]), "Medium": ("tri", [25, 50, 75]), "High": ("trap", [60, 80, 100, 100])},
}
RULES = [
    ("Cold", "Dry", "Low"), ("Cold", "Normal", "Low"), ("Cold", "Humid", "Low"),
    ("Moderate", "Dry", "Medium"), ("Moderate", "Normal", "Medium"), ("Moderate", "Humid", "High"),
    ("Hot", "Dry", "High"), ("Hot", "Normal", "High"), ("Hot", "Humid", "High")]


def _m(mfs):
    return MFS if mfs is None else mfs


def curve(var, name, x=None, mfs=None):
    kind, p = _m(mfs)[var][name]
    x = UNI[var] if x is None else x
    return fuzz.trapmf(x, p) if kind == "trap" else fuzz.trimf(x, p)


def check(mfs=None):
    """Return a list of human-readable problems (empty list = configuration is valid)."""
    mfs, errs = _m(mfs), []
    for var, d in mfs.items():
        lo, hi, ok = UNI[var][0], UNI[var][-1], True
        for n, (k, p) in d.items():
            p, need = list(p), (4 if k == "trap" else 3)
            if len(p) != need:
                errs.append(f"{var}/{n}: needs {need} points"); ok = False
            elif p != sorted(p):
                errs.append(f"{var}/{n}: points must be in ascending order (a ≤ b ≤ c ≤ d)"); ok = False
            elif min(p) < lo or max(p) > hi:
                errs.append(f"{var}/{n}: points must stay inside the universe [{lo:g}, {hi:g}]"); ok = False
            elif p[0] == p[-1]:
                errs.append(f"{var}/{n}: degenerate function (all points equal)"); ok = False
        if ok:
            cov = np.max([curve(var, n, mfs=mfs) for n in d], axis=0)
            gap = UNI[var][cov <= 0]
            if gap.size:
                errs.append(f"{var}: no fuzzy set covers {gap[0]:.1f} (first gap) — widen or overlap the sets")
    return errs


def validate(mfs=None):
    errs = check(mfs)
    assert not errs, errs


def fuzzify(var, x, mfs=None):
    x = float(np.clip(x, UNI[var][0], UNI[var][-1]))
    return {n: float(fuzz.interp_membership(UNI[var], curve(var, n, mfs=mfs), x)) for n in _m(mfs)[var]}


def infer(t, h, mfs=None):
    ft, fh = fuzzify("temp", t, mfs), fuzzify("hum", h, mfs)
    acts = [min(ft[a], fh[b]) for a, b, _ in RULES]
    agg = np.zeros_like(UNI["cool"])
    for (a, b, c), w in zip(RULES, acts):
        agg = np.fmax(agg, np.fmin(w, curve("cool", c, mfs=mfs)))
    out = float(fuzz.defuzz(UNI["cool"], agg, "centroid"))
    out_deg = {n: float(fuzz.interp_membership(UNI["cool"], curve("cool", n, mfs=mfs), out)) for n in _m(mfs)["cool"]}
    label = max(out_deg, key=out_deg.get)
    return {"temp_mu": ft, "hum_mu": fh, "activations": acts, "aggregated": agg, "output": out,
            "out_mu": out_deg, "label": label, "n_active": sum(a > 0 for a in acts)}


def surface(nt=41, nh=51, mfs=None):
    ts, hs = np.linspace(0, 40, nt), np.linspace(0, 100, nh)
    z = np.array([[infer(t, h, mfs)["output"] for t in ts] for h in hs])
    return ts, hs, z
