from parse import parse_workout_log
import os
import sqlite3
from workout import Workout


FOLDER_PATH = './workout_logs'


def main():
   
    # Step 1: Open workout log .md files in the folder
    md_files = [f for f in os.listdir(FOLDER_PATH) if f.endswith('.md')]
    md_files.sort()

    # Step 2: Save .md files into Workout objects
    workouts = Workout.parse_md_files(md_files)

    # Step 3: Insert data into training.db
    Workout.save_to_db(workouts, "training.db")

   
def read_md_file(md_file: str) -> tuple:
    file_path = os.path.join(FOLDER_PATH, md_file)
    file_name: str = os.path.basename(file_path)
    with open(file_path, 'r', encoding='utf-8') as file:
        content: list[str] = file.readlines()
        content: list[str] = [line.strip() for line in content]
        return file_name, content


if __name__ == "__main__":
    main()
