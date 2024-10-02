import re


def clean_position(s: str) -> str:
    """
    Clean up the position name to match the database
    """
    valid_positions = ["胸", "背", "腿", "肩", "手", "核心"]
    if s.startswith('## '):
            position = s.strip('# ')  # Position 句子
            if position[0:1] in valid_positions:
                position = position[0:1]  # Position 第一個字
            elif position[0:2] in valid_positions:
                position = position[0:2]  # Position 前兩個字，例如核心
            else:
                position = 'Unknown'
    return position


def clean_exercise(s: str) -> str:
    """
    Clean up the exercise name to match the database
    """
    position = s.strip()

    # Replace 'Leg Crul' with 'Leg Curl'
    if 'Leg Crul' in position:
        position = position.replace('Leg Crul', 'Leg Curl')

    return position


def clean_weight(s: str) -> float:
    """
    Clean up the weight to match the database
    """
    weight_match = re.search(r'(\d+(?:\.\d+)?)\s*kg', s)
    weight = round(float(weight_match.group(1)), 1)  # Weight
    if 'x2' in s:  # Single-hand exercise
        return round(weight * 2, 1)
    else:
        return weight


def clean_reps(s: str) -> int:
    """
    Clean up the reps to match the database
    """
    reps_match = re.search(r'(\d+)\s*下', s)
    reps = int(reps_match.group(1))  # Reps
    return reps


def clean_sets(s: str) -> int:
    """
    Clean up the sets to match the database
    """
    sets_match = re.search(r'(\d+)\s*組', s)
    sets = int(sets_match.group(1))  # Sets
    return sets