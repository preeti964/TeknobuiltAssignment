import pandas as pd
from bs4 import BeautifulSoup
import requests
from tqdm import tqdm
import re
import os


def download_imdb_top250():
    main_url = "https://www.imdb.com"
    top250_url = "https://www.imdb.com/chart/top"
    response = requests.get(top250_url)
    bSoup = BeautifulSoup(response.text, 'lxml')

    links = [a.attrs.get('href') for a in bSoup.select('td.titleColumn a')]

    column_list = ["ranking", "movieTitle", "movieYear", "rating", "voteCount", "censorRating", "movieLength",
                   "runtime",
                   "genre", "releaseDate", "summary", "starList",
                   "writerList", "director", "country", "language", "budget", "gross_worldwide", "production", "url"]

    df = pd.DataFrame(columns=column_list)

    for i in tqdm(range(0, len(links))):
        links[i] = main_url + links[i]

        resp = requests.get(links[i])
        soup = BeautifulSoup(resp.text, 'lxml')

        url = links[i]
        ranking = i + 1
        movieTitle = (soup.find("div", {"class": "title_wrapper"}).find("h1")).get_text(strip=True).split('(')[0]
        movieYear = ((soup.find(id='titleYear').get_text(strip=True)).split('(')[1]).split(')')[0]
        rating = soup.find("span", {"itemprop": "ratingValue"}).text
        voteCount = soup.find("span", {"itemprop": "ratingCount"}).text

        subtext = soup.find("div", {"class": "subtext"}).get_text(strip=True).split('|')
        if len(subtext) < 4:
            # Setting values when the movie is unrated
            censorRating = "No rating"
            movieLength = subtext[0]
            genre = subtext[1]
            releaseDate = (subtext[2].split('('))[0]
        else:
            censorRating = subtext[0]
            movieLength = subtext[1]
            genre = subtext[2]
            releaseDate = (subtext[3].split('('))[0]

        summary = soup.find("div", {"class": "summary_text"}).get_text(strip=True).strip()

        creditSummary = []
        for item in soup.find_all("div", {"class": "credit_summary_item"}):
            creditSummary.append(re.split(',|:|\|', item.get_text(strip=True)))

        stars = creditSummary.pop()[1:4]
        starList = ""
        for i in range(0, len(stars)):
            starList = starList + stars[i]
            if i + 1 != len(stars):
                starList = starList + ","
        # print(starList)

        writers = creditSummary.pop()[1:3]
        writerList = ""
        for i in range(0, len(writers)):
            fWriter = writers[i].split('(')[0]
            writerList = writerList + fWriter
            if i + 1 != len(writers):
                writerList = writerList + ","
        # print(writerList)

        director = (creditSummary.pop()[1:])[0]

        box_office_details = []
        box_office_dictionary = {'Country': '', 'Language': '', 'Budget': '',
                                 'Cumulative Worldwide Gross': '', 'Production Co': '', 'Runtime': ''}

        for details in soup.find_all("div", {"class": "txt-block"}):
            detail = details.get_text(strip=True).split(':')
            if detail[0] in box_office_dictionary:
                box_office_details.append(detail)

        for detail in box_office_details:
            if detail[0] in box_office_dictionary:
                box_office_dictionary.update({detail[0]: detail[1]})

        country = (box_office_dictionary['Country'].split("|"))[0]
        language = (box_office_dictionary['Language'].split("|"))[0]
        budget = box_office_dictionary['Budget'].split('(')[0]
        gross_worldwide = box_office_dictionary['Cumulative Worldwide Gross'].split(' ')[0]
        runtime = (box_office_dictionary['Runtime'].split("|")[0]).split('(')[0].split(' ')[0]

        production_list = box_office_dictionary['Production Co'].split('See more')[0]
        production = production_list.split(',')[0]

        movie_dict = {'ranking': ranking,
                      'movieTitle': movieTitle,
                      'movieYear': movieYear,
                      'rating': rating,
                      'voteCount': voteCount,
                      'censorRating': censorRating,
                      'movieLength': movieLength,
                      'runtime': runtime,
                      'genre': genre,
                      'releaseDate': releaseDate,
                      'summary': summary,
                      'starList': starList,
                      'writerList': writerList,
                      'director': director,
                      'country': country,
                      'language': language,
                      'budget': budget,
                      'gross_worldwide': gross_worldwide,
                      'production': production,
                      'url': url
                      }

        df = df.append(pd.DataFrame.from_records([movie_dict], columns=movie_dict.keys()))

    df = df[column_list]
    df = df.set_index(['ranking'], drop=False)
    df.to_csv("IMDBTop250.csv")
    return df


########################################################################################################################

def display_title_bar():
    # Clears the terminal screen, and displays a title bar.
    os.system('clear')
    print("\t**********************************************")
    print("\t****       Greeter - Hello friends!       ****")
    print("\t**********************************************")


def get_user_choice():
    print("\n[1] Filter movies by 1 field")
    print("[2] Filter movies by 2 fields")
    print("[q] Quit.")
    return input("What would you like to do? ")


def get_filtering_choice():
    print("\n[1] Genre")
    print("[2] Movie Length")
    print("[3] Actor")
    print("[4] Director")
    print("[q] Quit.")
    return input("Please choose a filtering field? ")


def filtering_by_genre(df):
    print("\nFiltering movies by Genre:\n")
    print("Some Acceptable Genres: Drama/Crime/Action/Biography/Adventure/Western/Romance/Sci-Fi/"
          "\nFantasy/Mystery/Comedy/Thriller/Family/War/Animation/Music/Horror/History/Musical/Sport\n")

    input_genre = input("Please enter a proper genre: ")
    filtered_data = df[df['genre'].str.contains(input_genre)]
    print(filtered_data[['ranking','movieTitle', 'movieYear', 'rating', 'movieLength', 'genre', 'country', 'language',
                         'production']])


def filtering_by_runtime(df):
    print("\nFiltering movies by runtime\n")
    input_runtime = input("Please enter the movie length in minutes: ")
    answer = input("Would you like movies OVER: " + input_runtime + " minutes? y/n: ")
    if answer == 'y':
        print("Looking for movies OVER " + input_runtime + " minutes...")
        filtered_data = df[pd.to_numeric(df['runtime']) >= int(input_runtime)]
        print(filtered_data[['ranking','movieTitle', 'movieYear', 'rating', 'movieLength', 'genre', 'country',
                             'language', 'production']])
    elif answer == 'n':
        print("Looking for movies UNDER " + input_runtime + " minutes...")
        filtered_data = df[pd.to_numeric(df['runtime']) <= int(input_runtime)]
        print(filtered_data[['ranking','movieTitle', 'movieYear', 'rating', 'movieLength', 'genre', 'country',
                             'language', 'production']])
    else:
        print("\nPlease enter a valid option.\n")


def filtering_by_actor(df):
    print("\nFiltering movies by Actor:\n")
    input_actor = input("Please enter actor's fullname: ")
    filtered_data = df[df['starList'].str.contains(input_actor)]
    print(filtered_data[['ranking','movieTitle', 'movieYear', 'rating', 'movieLength', 'genre', 'country', 'language',
                         'production']])


def filtering_by_director(df):
    print("\nFiltering movies by Director:\n")
    input_director = input("Please enter Director's fullname: ")
    filtered_data = df[df['director'].str.contains(input_director)]
    print(filtered_data[['ranking','movieTitle', 'movieYear', 'rating', 'movieLength', 'genre', 'country', 'language',
                         'production']])


def filtering_by_2fields(df):
    print("\nFiltering movies by 2 fields:")
    print("\nFiltering movies by Runtime and Genre fields:\n")
    print("Some Acceptable Genres: Drama/Crime/Action/Biography/Adventure/Western/Romance/Sci-Fi/"
          "\nFantasy/Mystery/Comedy/Thriller/Family/War/Animation/Music/Horror/History/Musical/Sport\n")

    input_genre = input("Please enter a proper genre: ")
    input_runtime = input("Please enter the movie length in minutes: ")
    answer = input("Would you like movies OVER: " + input_runtime + " minutes? y/n: ")
    if answer == 'y':
        print("Looking for movies with genre = " + input_genre + " and OVER " + input_runtime + " minutes...")
        runtime_filter = pd.to_numeric(df['runtime']) >= int(input_runtime)
        genre_filter = df['genre'].str.contains(input_genre)
        all_filter = runtime_filter & genre_filter
        print(df[all_filter][['ranking','movieTitle', 'movieYear', 'rating', 'movieLength', 'genre', 'country',
                              'language', 'production']])
    elif answer == 'n':
        print("Looking for movies with genre = " + input_genre + " and UNDER " + input_runtime + " minutes...")
        runtime_filter = pd.to_numeric(df['runtime']) <= int(input_runtime)
        genre_filter = df['genre'].str.contains(input_genre)
        all_filter = runtime_filter & genre_filter
        print(df[all_filter][['ranking','movieTitle', 'movieYear', 'rating', 'movieLength', 'genre', 'country',
                              'language', 'production']])
    else:
        print("\nPlease enter a valid option.\n")


def filtering_by_1field(df):
    print("\nFiltering movies by 1 field:\n")
    filtering_choice = ''
    while filtering_choice != 'q':
        filtering_choice = get_filtering_choice()
        if filtering_choice == '1':
            filtering_by_genre(df)
        elif filtering_choice == '2':
            filtering_by_runtime(df)
        elif filtering_choice == '3':
            filtering_by_actor(df)
        elif filtering_choice == '4':
            filtering_by_director(df)
        elif filtering_choice == 'q':
            print("\nReturning to main menu.")
        else:
            print("\nI didn't understand that choice.\n")


#######################################################################################################################
choice = ''
display_title_bar()

if os.path.isfile("IMDBTop250.csv"):
    print("\nReading from csv file..")
    imdb = pd.read_csv("IMDBTop250.csv")
else:
    print("\nDownloading IMDB Top 250 movies into a CSV file..")
    imdb = download_imdb_top250()

while choice != 'q':
    choice = get_user_choice()
    # Respond to the user's choice.
    display_title_bar()
    if choice == '1':
        filtering_by_1field(imdb)
    elif choice == '2':
        filtering_by_2fields(imdb)
    elif choice == 'q':
        print("\nThanks for playing. Bye.")
    else:
        print("\nI didn't understand that choice.\n")
