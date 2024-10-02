from parse import parse_workout_log
import os
import sqlite3


FOLDER_PATH = './workout_logs'


def main():
   
    # Step 1: Open workout log .md files in the folder
    md_files = [f for f in os.listdir(FOLDER_PATH) if f.endswith('.md')]
    md_files.sort()

    # Step 2: Read .md files
    for md_file in md_files:
        file_name, content = read_md_file(md_file)

        # Step 3: Parse content
        exercises = parse_workout_log(file_name, content)
        
        # Step 4: Insert data into training.db
        record_data(exercises)
        

def read_md_file(md_file: str) -> tuple:
    file_path = os.path.join(FOLDER_PATH, md_file)
    file_name: str = os.path.basename(file_path)
    with open(file_path, 'r', encoding='utf-8') as file:
        content: list[str] = file.readlines()
        content: list[str] = [line.strip() for line in content]
        return file_name, content


def record_data(exercises: list[dict]):

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


if __name__ == "__main__":
    main()
