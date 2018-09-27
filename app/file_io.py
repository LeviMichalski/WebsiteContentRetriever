# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
# web_io.py
#
# Contains the logic for reading and writing files, particularly CSV files
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
import csv


def get_csv(csv_file_name):
    with open(csv_file_name, 'r') as csv_file:
        reader = csv.reader(csv_file)
        csv_rows = list(reader)

        # remove the title row
        csv_rows.pop(0)

    return csv_rows
