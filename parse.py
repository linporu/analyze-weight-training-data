from clean import clean_position, clean_exercise, clean_weight, clean_reps, clean_sets
import re
from datetime import datetime

def parse_workout_log(file_name: str, content: list[str]) -> list[dict]:
    # Parse date
    date_match = re.search(r'(\d{6})', file_name)
    if date_match:
        date_str = date_match.group(1)
        date = datetime.strptime(date_str, '%y%m%d').strftime('%Y-%m-%d')
    else:
        date = None

    exercises: list[dict] = []
    for line in content:
        if line.startswith('## '):
            position = clean_position(line)
        elif line.startswith('- [x] '):
            exercise_data = line[6:].strip()

            exercise = clean_exercise(exercise_data)
            weight = clean_weight(exercise_data)
            reps = clean_reps(exercise_data)
            sets = clean_sets(exercise_data)
            volume = round(weight * reps * sets, 1) if all([weight, reps, sets]) else None

            exercises.append({
                'date': date,
                'position': position,
                'exercise': exercise,
                'weight': weight,
                'reps': reps,
                'sets': sets,
                'volume': volume
            })

    return exercises