# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
# web_io.py
#
# Contains the logic for reading and writing files, particularly CSV files
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
import re
import csv
import datetime


def get_csv(csv_file_name):
    _clean_txt_file(csv_file_name)

    with open(csv_file_name, 'r') as csv_file:
        reader = csv.reader(csv_file)
        csv_rows = list(reader)

        # remove the title row
        csv_rows.pop(0)

    return csv_rows


def write_new_csv(original_file_name, dictionary_list):
    new_file_name = _create_new_file_name(original_file_name)
    print('Writing results to ' + new_file_name)

    column_headers = _get_dictionary_keys(dictionary_list)
    with open(new_file_name, mode='w') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=column_headers)
        writer.writeheader()
        writer.writerows(dictionary_list)


def clean_txt(raw_txt):
    return re.sub('[^a-zA-Z0-9\n\.\-"\',/|!@#$%^&*()[\]{}:?/+=_\\\]', ' ', raw_txt).strip()


def _clean_txt_file(filename):
    with open(filename, 'r', encoding='latin-1') as txt_file:
        raw_txt = txt_file.read()

    cleaned_txt = clean_txt(raw_txt)

    with open(filename, 'w', encoding='utf-8') as txt_file:
        txt_file.write(cleaned_txt)


def _create_new_file_name(original_file_name):
    # Create a new unique file name for the results. Do not overwrite the original.
    # Example: buzzSumo_Monthly.csv --> buzzSumo_Monthly-meta-20181002-2219.csv
    now = datetime.datetime.now()
    period_index = original_file_name.rfind(".")
    original_name = original_file_name[:period_index]
    original_suffix = original_file_name[period_index:]
    file_date_stamp = str(now.year) + str(now.month) + str(now.day) + '-' + str(now.hour) + str(now.minute)
    return original_name + '_meta-' + file_date_stamp + original_suffix


def _get_dictionary_keys(dictionary_list):
    keys = []
    for dict_item in dictionary_list:
        for key in dict_item.keys():
            if key not in keys:
                keys.append(key)

    return keys
