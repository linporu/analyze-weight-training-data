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
    s = s.strip()

    # Replace 'Leg Crul' with 'Leg Curl'
    if 'Leg Crul' in s:
        s = s.replace('Leg Crul', 'Leg Curl')

    return s