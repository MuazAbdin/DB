import csv
from functools import reduce
from io import TextIOWrapper
from zipfile import ZipFile
import numpy as np

# opens file for oscars table.
# CHANGE!
outfile = open("oscars.csv", 'w', )
outwriter = csv.writer(outfile, delimiter=",", quoting=csv.QUOTE_NONE)


# return the list of all tables
def get_names() -> list:
    return ["Movie_person", "Producer", "Actor", "Director", "Author",
            "Film", "Winner", "Nominee", "Oscar", "Content_rating", "Genre"]


out_files = [open(f"{name}.csv", 'w', ) for name in get_names()]
out_writers = [csv.writer(out_file, delimiter=",", quoting=csv.QUOTE_NONE)
               for out_file in out_files]
attr_indices = [[3, 11, 12, 13], [3], [13], [11], [12],
                [1, 2, 5, 6, 8, 9, 14], [14], [14], [2], [10], [7]]
seen = [set() for i in range(len(get_names()))]


def setup():
    attributes = [["pname"], ["prname"], ["aname"], ["dname"], ["auname"],
                  ["film_name", "osyear", "release_year", "duration", "imdb_rating",
                   "imdb_votes", "film_id"], ["film_id"], ["film_id"], ["oyear"],
                  ["rating"], ["genre_type"]]
    for idx in range(len(out_writers)):
        out_writers[idx].writerow(attributes[idx])


def cleanup():
    for file in out_files:
        file.close()


def write_attributes(table, row):
    # process Film, Winner, Nominee, Oscar tables (have neither && nor NULL)
    if table in [5, 6, 7, 8]:
        attr_values = row[attr_indices[table]]
        if tuple(attr_values) in seen[table]:
            return
        seen[table].add(tuple(attr_values))
        out_writers[table].writerow(attr_values)
    # process other tables which may have && or NULL
    else:
        attr_values = row[attr_indices[table]]
        attr_values[attr_values == ''] = 'NULL'
        attr_values = np.char.split(attr_values, sep='&&')
        attr_values = np.array([np.array(lst) for lst in attr_values])
        attr_values = reduce(np.union1d, attr_values)

        for value in attr_values:
            value = value.strip()
            if value in seen[table]:
                continue
            seen[table].add(value)
            out_writers[table].writerow([value])


INITIAL_ROW = ['', 'Film', 'Oscar Year', 'Film Studio/Producer(s)', 'Award', 'Year of Release',
               'Movie Time', 'Movie Genre', 'IMDB Rating', 'IMDB Votes', 'Content Rating',
               'Directors', 'Authors', 'Actors', 'Film ID']


# process_row should splits row into the different csv table files
# CHANGE!!!
def process_row(row):
    row = np.array(row)
    if np.all(row == INITIAL_ROW):
        outwriter.writerow(row)
        return

    for table in range(len(get_names())):
        write_attributes(table, row)

    outwriter.writerow(row)


# process_file goes over all rows in original csv file, and sends each row to process_row()
# DO NOT CHANGE!!!
def process_file():
    with ZipFile('archive.zip') as zf:
        with zf.open('oscars_df.csv', 'r') as infile:
            reader = csv.reader(TextIOWrapper(infile, 'utf-8'))
            for row in reader:
                # remove some of the columns
                chosen_indices = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 13, 14, 15, 16, 29]
                row = [row[index] for index in chosen_indices]

                # change "," into && in list values
                lists_values_indices = [7, 11, 12, 13]
                for list_value_index in lists_values_indices:
                    row[list_value_index] = row[list_value_index].replace(',', '&&')

                # pre-process : remove all quotation marks from input and turns NA into null
                # value ''.
                row = [v.replace(',', '') for v in row]
                row = [v.replace("'", '') for v in row]
                row = [v.replace('"', '') for v in row]
                row = [v if v != 'NA' else "" for v in row]

                # In the first years of oscars in the database they used "/" for example 1927/28,
                # so we will change these.
                row[2] = row[2].split("/")[0]

                # In 1962 two movies were written as winners, then we change one of them to nominee.
                if row[4] == "Winner" and row[2] == "1962" and row[
                    14] == "8d5317bd-df12-4f24-b34d-e5047ef4665e":
                    row[4] = "Nominee"

                # In 2020 Nomadland won and marked as nominee by mistake.
                if row[2] == "2020" and row[1] == "Nomadland":
                    row[4] = "Winner"

                process_row(row)

    # flush and close the file. close all of your files.
    outfile.close()


# return a list of all the inner values in the given list_value.
# you should use this to handle value in the original table which
# contains an inner list of values.
# DO NOT CHANGE!!!
def split_list_value(list_value):
    return list_value.split("&&")


if __name__ == "__main__":
    setup()
    process_file()
    cleanup()

