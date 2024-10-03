# analyze-weight-training-data

This project is designed to analyze weight training data.

## Project Structure

- `analyse.py`: Analyzes training data and generates charts
- `clean.py`: Cleans and processes raw data
- `export.py`: Exports data from SQLite database to CSV file
- `export.sql`: SQL query for exporting data
- `import.py`: Imports training data from workout log Markdown files into SQLite database
- `parse.py`: Parses workout log Markdown files

## Features

1. Parse and import data from Markdown-formatted workout logs
2. Clean and process raw data
3. Store data in SQLite database
4. Analyze training data and generate daily training volume chart
5. Export data to CSV format

## Usage

1. Place training log Markdown files in the `workout_logs` folder
2. Run `import.py` to import data into the SQLite database
3. Run `analyse.py` to generate the training volume chart
4. (Optional) Run `export.py` to export data to a CSV file

## Dependencies

- pandas
- matplotlib
- sqlite3

## Notes

- Ensure the `workout_logs` folder contains correctly formatted training log Markdown files
- The SQLite database file is named `training.db`
- The exported CSV file is named `training.csv`
