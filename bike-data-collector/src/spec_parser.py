import re

LABELS = {
    "engine_cc": ["engine", "displacement"],
    "power_bhp": ["power"],
    "torque_nm": ["torque"],
    "kerb_weight_kg": ["kerb weight"],
    "mileage_kmpl": ["mileage"]
}

RANGES = {
    "engine_cc": (50, 1300),
    "power_bhp": (3, 220),
    "torque_nm": (5, 200),
    "kerb_weight_kg": (90, 300),
    "mileage_kmpl": (10, 90)
}

def _num(text):
    m = re.search(r"(\d+(\.\d+)?)", text)
    return float(m.group(1)) if m else None

def parse_engine(t):
    n = _num(t)
    return n if n and RANGES["engine_cc"][0] <= n <= RANGES["engine_cc"][1] else None

def parse_power(t):
    n = _num(t)
    if not n:
        return None
    if "ps" in t.lower():
        n *= 0.98632
    if "bhp" not in t.lower() and "hp" not in t.lower():
        return None
    return n if RANGES["power_bhp"][0] <= n <= RANGES["power_bhp"][1] else None

def parse_torque(t):
    n = _num(t)
    if not n:
        return None
    if "kgm" in t.lower():
        n *= 9.80665
    if "nm" not in t.lower():
        return None
    return n if RANGES["torque_nm"][0] <= n <= RANGES["torque_nm"][1] else None

def parse_weight(t):
    n = _num(t)
    if not n or "kg" not in t.lower():
        return None
    return n if RANGES["kerb_weight_kg"][0] <= n <= RANGES["kerb_weight_kg"][1] else None

def parse_mileage(t):
    n = _num(t)
    if not n or "km" not in t.lower():
        return None
    return n if RANGES["mileage_kmpl"][0] <= n <= RANGES["mileage_kmpl"][1] else None

PARSERS = {
    "engine_cc": parse_engine,
    "power_bhp": parse_power,
    "torque_nm": parse_torque,
    "kerb_weight_kg": parse_weight,
    "mileage_kmpl": parse_mileage
}

def extract_specs(rows):
    result = {k: None for k in PARSERS}

    for label, value in rows:
        l = label.lower()
        for field, keys in LABELS.items():
            if result[field] is not None:
                continue
            if any(k in l for k in keys):
                result[field] = PARSERS[field](value)

    return result
