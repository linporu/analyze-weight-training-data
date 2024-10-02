import re


# PATTERNS
WEIGHT_PATTERN = r'(\d+(?:\.\d+)?)\s*kg ?(?: x2)?'
REPS_PATTERN = r'(\d+)\s*下'
SETS_PATTERN = r'(\d+)\s*組'


# CONSTANTS
BODY_WEIGHT = 60


def clean_position(s: str) -> str:
    valid_positions = ["胸", "背", "腿", "肩", "手", "核心"]
    if s.startswith('## '):
        position = s.strip('# ')  # Position 句子
        if position[0:1] in valid_positions:
            position = position[0:1]  # Position 第一個字
        elif position[0:2] in valid_positions:
            position = position[0:2]  # Position 前兩個字，例如核心
        else:
            position = None
    return position


def clean_exercise(s: str) -> str | None:
    if '｜' not in s:
        return None
    
    exercise = s.split('｜')[0].strip()

    # Replace 'Leg Crul' with 'Leg Curl'
    if 'Leg Crul' in exercise:
        exercise = exercise.replace('Leg Crul', 'Leg Curl')

    return exercise if exercise else None


def clean_weight(s: str, exercise: str) -> float | None:
    if s is None:
        return None
    
    if "引體向上" in exercise:
        return BODY_WEIGHT
    elif "伏地挺身" in exercise:
        return round(BODY_WEIGHT * 0.75, 1)
    
    weight_match = re.search(WEIGHT_PATTERN, s)
    if weight_match:
        weight = round(float(weight_match.group(1)), 1)
        return weight if not 'x2' in s else round(weight * 2, 1)  # single-hand exercise
    return None


def clean_reps(s: str) -> int | None:
    if s is None:
        return None
    reps_match = re.search(REPS_PATTERN, s)
    return int(reps_match.group(1)) if reps_match else None


def clean_sets(s: str) -> int | None:
    if s is None:
        return None
    sets_match = re.search(SETS_PATTERN, s)
    return int(sets_match.group(1)) if sets_match else None