import re
from datetime import datetime
from clean import clean_position, clean_exercise

def parse_workout_log(file_name: str, content: str) -> list:

    # Parse date
    date_match = re.search(r'(\d{6})', file_name)
    if date_match:
        date_str = date_match.group(1)
        date = datetime.strptime(date_str, '%y%m%d').strftime('%Y-%m-%d')
    else:
        date = "Unknown"

    # Parse exercise data
    exercises = []
    for line in content.split('\n'):       
        if line.startswith('## '):
            position = clean_position(line)
        elif line.startswith('- [x] '):
            exercise_data = line[6:].split('｜')
            if len(exercise_data) >= 4:
                exercise = clean_exercise(exercise_data[0])  # Exercise
                weight_match = re.search(r'(\d+(?:\.\d+)?)\s*kg', exercise_data[1])
                reps_match = re.search(r'(\d+)\s*下', exercise_data[2])
                sets_match = re.search(r'(\d+)\s*組', exercise_data[3])

                if weight_match and reps_match and sets_match:
                    weight = round(float(weight_match.group(1)), 1)  # Weight
                    if 'x2' in exercise_data[1]:  # Single-hand exercise
                        weight = round(weight * 2, 1)
                    reps = int(reps_match.group(1))  # Reps
                    sets = int(sets_match.group(1))  # Sets
                    volume = round(weight * reps * sets, 1)  # Training volume

                    exercises.append({'date': date, 'position': position, 'exercise': exercise, 'weight': weight,
                        'reps': reps, 'sets': sets, 'volume': volume})

    return exercises