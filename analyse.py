import pandas as pd
import matplotlib.pyplot as plt
import sqlite3
from matplotlib.dates import DateFormatter, date2num

# CONSTANTS
SIG_FIGS = 1


def main():
    # Step 1: get data from training.db
    conn = sqlite3.connect("training.db")
    df = pd.read_sql_query("SELECT * FROM training", conn)
    conn.close()

    # Step 2: calculate volume
    df["volume"] = round(df["weight"] * df["sets"] * df["reps"], SIG_FIGS)
    df["date"] = pd.to_datetime(df["date"])

    daily_volume = df.groupby("date")["volume"].sum().reset_index()

    # Step 3: plot line chart
    plt.figure(figsize=(12, 6))
    plt.plot(date2num(daily_volume["date"]), daily_volume["volume"])
    plt.title("Daily training volume")
    plt.xlabel("Date")
    plt.ylabel("Volume")

    # 使用 Matplotlib 的 DateFormatter 來格式化日期
    date_formatter = DateFormatter("%Y-%m-%d")
    plt.gca().xaxis.set_major_formatter(date_formatter)

    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.show()


if __name__ == "__main__":
    main()
