import re
import os
import sqlite3
from datetime import datetime


FOLDER_PATH = './workout_logs'


def main():
   
    # Step 1: Open workout log .md files in the folder
    md_files = [f for f in os.listdir(FOLDER_PATH) if f.endswith('.md')]

    # Step 2: Read .md files
    for md_file in md_files:
        file_name, content = read_md_file(md_file)

        # Step 3: Parse content
        exercises = parse_workout_log(file_name, content)
        
        # Step 4: Insert data into training.db
        record_data(exercises)
        

def read_md_file(md_file):
    file_path = os.path.join(FOLDER_PATH, md_file)
    file_name = os.path.basename(file_path)
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        return file_name, content


def parse_workout_log(file_name, content):

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
                exercise = exercise_data[0].strip()  # Exercise
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


def record_data(exercises):

    # Connect to SQLite database
    conn = sqlite3.connect('training.db')
    cursor = conn.cursor()

    # Record data
    for exercise in exercises:
        cursor.execute('''INSERT INTO training 
                            (date, position, exercise, weight, reps, sets, volume) 
                            VALUES (?, ?, ?, ?, ?, ?, ?)''', 
                        (exercise['date'], exercise['position'], exercise['exercise'], exercise['weight'], 
                            exercise['reps'], exercise['sets'], exercise['volume']))
        print(f"Recorded: {exercise['date']}, {exercise['position']}, {exercise['exercise']}, {exercise['weight']}, {exercise['reps']}, {exercise['sets']}, {exercise['volume']}")

    # Commit changes and close connection
    conn.commit()
    conn.close()


def clean_position(line):
    valid_positions = ["胸", "背", "腿", "肩", "手", "核心"]
    if line.startswith('## '):
            position = line.strip('# ')  # Position 句子
            if position[0:1] in valid_positions:
                position = position[0:1]  # Position 第一個字
            elif position[0:2] in valid_positions:
                position = position[0:2]  # Position 前兩個字，例如核心
            else:
                position = 'Unknown'
    return position



if __name__ == "__main__":
    main()
