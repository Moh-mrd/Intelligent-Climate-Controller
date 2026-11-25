import sys, pathlib, itertools
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import numpy as np, pytest
from engine.fuzzy_controller import infer, fuzzify, validate, surface, MFS, curve

def test_mf_valid():
    validate()
    for v in MFS:
        for n in MFS[v]:
            c = curve(v, n); assert c.min() >= 0 and c.max() <= 1

@pytest.mark.parametrize("t,h", list(itertools.product([0, 40], [0, 100])))
def test_extremes(t, h):
    r = infer(t, h); assert 0 <= r["output"] <= 100 and np.isfinite(r["output"])

def test_full_domain():
    for t in np.linspace(0, 40, 21):
        for h in np.linspace(0, 100, 21):
            assert 0 <= infer(t, h)["output"] <= 100

def test_typical():
    assert infer(5, 50)["label"] == "Low"
    assert infer(23, 50)["label"] == "Medium"
    assert infer(38, 80)["label"] == "High"

def test_monotone_temp():
    outs = [infer(t, 50)["output"] for t in range(0, 41, 5)]
    assert all(b >= a - 1e-6 for a, b in zip(outs, outs[1:]))

def test_out_of_range_clipped():
    assert fuzzify("temp", -5) == fuzzify("temp", 0)

def test_surface_shape():
    ts, hs, z = surface(5, 5); assert z.shape == (5, 5) and z.min() >= 0 and z.max() <= 100

import copy
from engine.fuzzy_controller import check

def test_check_default_ok():
    assert check() == []

def test_check_rejects_unsorted():
    m = copy.deepcopy(MFS); m["temp"]["Hot"] = ("trap", [30, 10, 20, 40])
    assert check(m)

def test_check_rejects_out_of_range():
    m = copy.deepcopy(MFS); m["temp"]["Hot"] = ("trap", [25, 32, 40, 50])
    assert check(m)

def test_check_rejects_gap():
    m = copy.deepcopy(MFS); m["temp"]["Cold"] = ("trap", [0, 0, 5, 8]); m["temp"]["Moderate"] = ("tri", [15, 23, 30])
    assert any("covers" in x for x in check(m))

def test_custom_mfs_still_valid_output():
    m = copy.deepcopy(MFS); m["temp"]["Hot"] = ("trap", [20, 28, 40, 40]); assert check(m) == []
    assert 0 <= infer(30, 50, m)["output"] <= 100
