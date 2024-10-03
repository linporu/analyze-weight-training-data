import sqlite3
from typing import List, Dict
from clean import clean_position, clean_exercise, clean_weight, clean_reps, clean_sets
import re
import os
from datetime import datetime

class Workout:
    def __init__(self, date: str=None, position: str=None, exercise: str=None, weight: float=None, reps: int=None, sets: int=None, volume: float=None):
        self.date = date
        self.position = position
        self.exercise = exercise
        self.weight = weight
        self.reps = reps
        self.sets = sets
        self.volume = volume

    def __str__(self):
        return f"{self.date} {self.position} {self.exercise} {self.weight} {self.reps} {self.sets} {self.volume}"

    @classmethod
    def from_dict(cls, data: Dict) -> 'Workout':
        return cls(
            date=data['date'],
            position=data['position'],
            exercise=data['exercise'],
            weight=data['weight'],
            reps=data['reps'],
            sets=data['sets'],
            volume=data['volume']
        )

    def to_dict(self) -> Dict:
        return {
            'date': self.date,
            'position': self.position,
            'exercise': self.exercise,
            'weight': self.weight,
            'reps': self.reps,
            'sets': self.sets,
            'volume': self.volume
        }

    @staticmethod
    def parse_md_files(file_paths: List[str]) -> List['Workout']:
        workouts = []
        for file_path in file_paths:
            file_name: str = os.path.basename(file_path)
            with open(file_path, 'r', encoding='utf-8') as file:
                content: list[str] = file.readlines()
                content: list[str] = [line.strip() for line in content]

                # Parse date
                date_match = re.search(r'(\d{6})', file_name)
                if date_match:
                    date_str = date_match.group(1)
                    date = datetime.strptime(date_str, '%y%m%d').strftime('%Y-%m-%d')
                else:
                    date = None

                exercises = []
                position = None
                for line in content:
                    if line.startswith('## '):
                        position = clean_position(line)
                    elif line.startswith('- [x] '):
                        exercise_data = line[6:].strip()

                        exercise = clean_exercise(exercise_data)
                        weight = clean_weight(exercise_data, exercise)
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
                
                workouts.append(Workout(date=date, exercises=exercises))
        return workouts

    @staticmethod
    def save_to_db(workouts: List['Workout'], db_path: str):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 創建表格（如果不存在）
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS training
            (date TEXT, position TEXT, exercise TEXT, weight REAL, reps INTEGER, sets INTEGER, volume REAL)
        ''')

        # 插入數據
        for workout in workouts:
            cursor.execute('''
                INSERT INTO training (date, position, exercise, weight, reps, sets, volume)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (workout.date, workout.position, workout.exercise, workout.weight, workout.reps, workout.sets, workout.volume))

        conn.commit()
        conn.close()


