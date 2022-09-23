import csv
from io import TextIOWrapper
from zipfile import ZipFile

# opens file for oscars table.
film_outfile = open("film.csv", 'w', )
film_outwriter = csv.writer(film_outfile, delimiter=",", quoting=csv.QUOTE_NONE)

directed_by_outfile = open("directed_by.csv", 'w', )
directed_by_outwriter = csv.writer(directed_by_outfile, delimiter=",", quoting=csv.QUOTE_NONE)

written_by_outfile = open("written_by.csv", 'w', )
written_by_outwriter = csv.writer(written_by_outfile, delimiter=",", quoting=csv.QUOTE_NONE)

acted_by_outfile = open("acted_by.csv", 'w', )
acted_by_outwriter = csv.writer(acted_by_outfile, delimiter=",", quoting=csv.QUOTE_NONE)

belongs_to_outfile = open("belongs_to.csv", 'w', )
belongs_to_outwriter = csv.writer(belongs_to_outfile, delimiter=",", quoting=csv.QUOTE_NONE)

won_outfile = open("won.csv", 'w', )
won_outwriter = csv.writer(won_outfile, delimiter=",", quoting=csv.QUOTE_NONE)

# lists to keep track of duplicates
films = {}
directed_bys = []
written_bys = []
acted_bys = []
belongs_tos = []
winners = {}



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

                # pre-process : remove all quotation marks from input and turns NA into null value ''.
                row = [v.replace(',', '') for v in row]
                row = [v.replace("'", '') for v in row]
                row = [v.replace('"', '') for v in row]
                row = [v if v != 'NA' else "" for v in row]

                # In the first years of oscars in the database they used "/" for example 1927/28, so we will change these.
                row[2] = row[2].split("/")[0]

                # In 1962 two movies were written as winners, then we change one of them to nominee.
                if row[4] == "Winner" and row[2] == "1962" and row[14] == "8d5317bd-df12-4f24-b34d-e5047ef4665e":
                    row[4] = "Nominee"

                # In 2020 Nomadland won and marked as nominee by mistake.
                if row[2] == "2020" and row[1] == "Nomadland":
                    row[4] = "Winner"

                process_row(row)

    film_outfile.close()
    directed_by_outfile.close()
    written_by_outfile.close()
    acted_by_outfile.close()
    belongs_to_outfile.close()
    won_outfile.close()

# return a list of all the inner values in the given list_value.
# you should use this to handle value in the original table which
# contains an inner list of values.
# DO NOT CHANGE!!!
def split_list_value(list_value):
    return list_value.split("&&")

# process_row should splits row into the different csv table files
def process_row(row):
    row_index = row[0]
    film_name = row[1]
    oscar_year = row[2]
    studio = row[3]
    award = row[4]
    release_year = row[5]
    duration = row[6]
    genres = row[7]
    imdb_rating = row[8]
    imdb_votes = row[9]
    content_rating = row[10]
    directors = row[11]
    authors = row[12]
    actors = row[13]
    film_id = row[14]

    # check for duplicates and write new tuples into appropriate files
    if film_id not in films:
        film_outwriter.writerow([film_id, oscar_year, duration, release_year, film_name, studio, imdb_rating, imdb_votes, content_rating])
        films[film_id] = duration + release_year + film_name + studio + imdb_rating + imdb_votes + content_rating
    elif films.get(film_id) != duration + release_year + film_name + studio + imdb_rating + imdb_votes + content_rating:
            print("problem with film key: " + film_id)

    add_list_value_related_to_film_to_relation_table(directors, film_id, directed_bys, directed_by_outwriter)
    add_list_value_related_to_film_to_relation_table(authors, film_id, written_bys, written_by_outwriter)
    add_list_value_related_to_film_to_relation_table(actors, film_id, acted_bys, acted_by_outwriter)
    add_list_value_related_to_film_to_relation_table(genres, film_id, belongs_tos, belongs_to_outwriter)

    if award == "Winner":
        if oscar_year not in winners:
            won_outwriter.writerow([oscar_year, film_id])
            winners[oscar_year] = film_id
        elif winners.get(oscar_year) != film_id:
            print("problem in won with oscar year key: " + film_id + " year " + oscar_year)
            print("already have " + oscar_year + " " + winners.get(oscar_year))

# This function handles columns with lists values by adding each value combined with the film_id
# to the relation table without duplications.
def add_list_value_related_to_film_to_relation_table(list_value, film_id, relation_duplications_list, relation_out_writer):
    for separate_value in split_list_value(list_value):
        if separate_value != "" and film_id + separate_value not in relation_duplications_list:
            relation_out_writer.writerow([film_id, separate_value])
            relation_duplications_list.append(film_id + separate_value)

# return the list of all tables
def get_names():
    return ["film", "directed_by", "written_by", "acted_by", "belongs_to", "won"]


if __name__ == "__main__":
    process_file()

