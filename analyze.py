import re
import os
import sqlite3
from datetime import datetime


def main():
   
    # Step 1: Open .md files in the folder
    folder_path = "."  # Assume .md files are in the current folder
    md_files = [f for f in os.listdir(folder_path) if f.endswith('.md')]

    # Connect to SQLite database
    conn = sqlite3.connect('training.db')
    cursor = conn.cursor()

    # Step 2 and 3: Read .md files and parse content
    for md_file in md_files:
        file_path = os.path.join(folder_path, md_file)
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        date, position, exercise, weight, reps, sets, volume = parse(content)

    # Step 4: Insert data into training.db
    cursor.execute('''INSERT INTO training_data 
                        (date, position, exercise, weight, reps, sets, volume) 
                        VALUES (?, ?, ?, ?, ?, ?, ?)''', 
                    (date.strftime('%Y-%m-%d'), position, exercise, weight, reps, sets, volume))

    # Commit changes and close connection
    conn.commit()
    conn.close()

    print("Data has been successfully inserted into training.db")



def parse(content):
    # Here we need to implement the logic to parse content
    # Assume we have a simple format: date|position|exercise|weight|reps|sets
   
    parts = content.strip().split('|')
    date = datetime.strptime(parts[0], '%Y-%m-%d')
    position, exercise = parts[1], parts[2]
    weight, reps, sets = map(int, parts[3:6])

    
    volume = weight * reps * sets
    return date, position, exercise, weight, reps, sets, volume









if __name__ == "__main__":
    main()
