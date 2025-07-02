# Maps for depreciation/weightage by range

type1 = {
    (0, 2): 100,
    (3, 5): 95,
    (6, 10): 90,
    (11, 20): 80,
    (21, 30): 70,
    (31, 40): 60,
    (41, 50): 50,
    (51, 60): 40,
    (61, 70): 30,
    (71, 80): 20,
    (81, 90): 10,
    (91, 100): 0,
}

type2 = {
    (0, 2): 100,
    (3, 5): 95,
    (6, 10): 90,
    (11, 20): 75,
    (21, 30): 60,
    (31, 40): 15,
    (41, 50): 30,
    (51, 60): 15,
    (61, 70): 0
}

def calculate_depreciation_rate(year, name):
    from datetime import datetime
    current_year = datetime.now().year
    try:
        year = int(year)
    except (TypeError, ValueError):
        return 0
    year_diff = current_year - year
    type2_names = [
        "झोपडी किंवा मातीची इमारत",
        "दगड विटा मातीची इमारत",
        "जनावरांचा",
        "आर सी सी"
    ]
    type1_names = [
        "दगड सिमेंट चुना अर्ध पक्के घर",
        "आर सी सी पक्के घर",
        "आर सी सी .."
        # Add more as needed
    ]
    if name in type2_names:
        depreciation_map = type2
    elif name in type1_names:
        depreciation_map = type1
    else:
        return 0
    for (start, end), value in depreciation_map.items():
        if start <= year_diff <= end:
            return value
    return 0
