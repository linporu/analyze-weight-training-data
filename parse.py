import re
from datetime import datetime
from clean import clean_position, clean_exercise, clean_weight, clean_reps, clean_sets

def parse_workout_log(file_name: str, content: list[str]) -> list[dict]:

    # Parse date
    date_match = re.search(r'(\d{6})', file_name)
    if date_match:
        date_str = date_match.group(1)
        date = datetime.strptime(date_str, '%y%m%d').strftime('%Y-%m-%d')
    else:
        date = "Unknown"

    # Parse exercise data
    exercises: list[dict] = []
    for line in content:
        if line.startswith('## '):
            position = clean_position(line)
        elif line.startswith('- [x] '):
            exercise_data = line[6:].split('｜')
            if len(exercise_data) > 0:
                exercise: str | None = get_value(exercise_data, 0, clean_exercise)
                weight: float | None = get_value(exercise_data, 1, clean_weight)
                reps: int | None = get_value(exercise_data, 2, clean_reps)
                sets: int | None = get_value(exercise_data, 3, clean_sets)

                # Calculate volume, only calculate when all necessary values exist
                if weight is not None and reps is not None and sets is not None:
                    volume: float = round(weight * reps * sets, 1)
                else:
                    volume = None

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


def get_value(data: list[str], index: int, clean_func: callable) -> str | None:
    if index < len(data):
        return clean_func(data[index])
    return None