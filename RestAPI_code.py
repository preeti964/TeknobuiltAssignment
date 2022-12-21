import mysql.connector as connector


class Movie:
    def __init__(self, name, rating, release_date, duration, description, date_and_time):
        self.__name = name
        self.__rating = rating
        self.__release_date = release_date
        self.__duration = duration
        self.__description = description
        self.__date_and_time = date_and_time

    def get_name(self):
        return self.__name

    def get_rating(self):
        return self.__rating

    def get_release_date(self):
        return self.__release_date

    def get_duration(self):
        return self.__duration

    def get_descriptoin(self):
        return self.__description

    def get_data_and_time(self):
        return self.__date_and_time


class DataBase:
    def __init__(self):
        # self.__connection = "" # Have the necessary code in place
        self.__connection = connector.connect(host='localhost', user='root', password='123456', database='tekno_movie')
        self.cursor = self.__connection.cursor()

    def get_instance(self):
        return self.__connection

    def execute_query(self, query):
        # Have the code which executes the query and returns the data
        # print(query)  # placeholder

        self.cursor.execute(query)
        myresult = self.cursor.fetchall()
        print(myresult)
        return myresult
class MovieService:
    def __init__(self, database: DataBase):
        # self.__movie = []
        self.__database = database

    def fetch_movie_details(self):
        self.__movie =[]
        # TODO: Check how can we paginate a query in MYSQL
        self.__data = self.__database.execute_query("SELECT * from imdbtop250")

        # Offset needs to be hooked to this query
        # print(self.__data)
        for movie in self.__data:
            movie_detail = {}
            movie_detail["name"] = movie[1]
            movie_detail["year"] = movie[2]
            movie_detail["rating"] = movie[3]
            movie_detail["duration"] = movie[5]
            movie_detail['description'] = movie[8]
            self.__movie.append(movie_detail)
        return self.__movie

    def sort_movie_details(self):
        self.__movie = []
        # TODO: Check how can we paginate a query in MYSQL
        self.__data = self.__database.execute_query("SELECT * from imdbtop250 order by movieTitle, rating,movieYear, runTime ")

        # Offset needs to be hooked to this query
        # print(self.__data)
        for movie in self.__data:
            movie_detail = {}
            movie_detail["name"] = movie[1]
            movie_detail["year"] = movie[2]
            movie_detail["rating"] = movie[3]
            movie_detail["duration"] = movie[5]
            movie_detail['description'] = movie[8]
            self.__movie.append(movie_detail)
        return self.__movie

    def search_movie_details(self,name):
        print('search_movie_details')
        print(name)
        movies = []
        # TODO: Check how can we paginate a query in MYSQL
        # self.__data = self.__database.execute_query("SELECT * from imdbtop250 where movieTitle = "+name)
        self.__data = self.__database.execute_query("select * from imdbtop250 where movieTitle = '"+name+"' ")
        # Offset needs to be hooked to this query
        print("select * from imdbtop250 where movieTitle = ' " + name + " ' ")
        for movie in self.__data:
            movie_detail = {}
            movie_detail["name"] = movie[1]
            movie_detail["year"] = movie[2]
            movie_detail["rating"] = movie[3]
            movie_detail["duration"] = movie[5]
            movie_detail['description'] = movie[8]
            movies.append(movie_detail)
        return movies

from flask import Flask, jsonify
app = Flask(__name__)


@app.route("/get_movie")  # Assuming we need all the movie present in the database
def get_movie():
    database = DataBase()
    print(database)
    movieService = MovieService(database)
    print(movieService)
    movie = movieService.fetch_movie_details()
    return jsonify(movie)

@app.route("/get_movie_bysort")  # Assuming we need all the movie present in the database
def get_movie_bysort():
    database = DataBase()
    print(database)
    movieService = MovieService(database)
    print(movieService)
    movie = movieService.sort_movie_details()
    return jsonify(movie)

@app.route("/search_movie_byname/<name>")  # Assuming we need all the movie present in the database
def get_movie_bysearch(name):
    database = DataBase()
    print(database)
    movieService = MovieService(database)
    print(movieService)
    movie = movieService.search_movie_details(name)
    return jsonify(movie)

if __name__ == "__main__":
    app.run()
