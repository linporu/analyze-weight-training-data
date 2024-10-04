import sqlite3
import csv


def main():
    conn = sqlite3.connect("training.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM training")
    rows = cursor.fetchall()
    with open("training.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([i[0] for i in cursor.description])
        writer.writerows(rows)
    print("Data exported to training.csv")


if __name__ == "__main__":
    main()
