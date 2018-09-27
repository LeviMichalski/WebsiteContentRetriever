import csv


def get_website_references(csv_file_name):
    with open(csv_file_name, 'r') as csv_file:
        reader = csv.reader(csv_file)
        csv_rows = list(reader)

        # remove the title row
        csv_rows.pop(0)

    return csv_rows
