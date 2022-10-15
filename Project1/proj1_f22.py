#########################################
##### Name:        Ziyi Liu         #####
##### Uniqname:       ziyiliu       #####
#########################################

import json
import requests
import webbrowser

class Media:

    def __init__(self, title="No Title", author="No Author", release_year = "No Release Year", url = "No URL", json = None):
        self.json = json
        if json == None:
            self.title = title
            self.author = author
            self.release_year = release_year
            self.url = url
        else:
            try: 
                self.title = json["collectionName"]
            except: 
                self.title = json["trackName"]
            self.author = json["artistName"]
            self.release_year = json["releaseDate"][0:4]
            try: 
                self.url=json["collectionViewUrl"]
            except:
                self.url = json["trackViewUrl"]

    def info(self):
        return f"{self.title} by {self.author} ({self.release_year})"

    def length(self):
        return 0



class Song(Media):
    def __init__(self, title="No Title", author="No Author", release_year = "No Release Year", url = "No URL", album = "No Album", genre = "No Genre", track_length = 0, json = None):
        self.json = json
        super().__init__(title, author, release_year, url, json)
        if json ==None:
            self.album = album
            self.genre = genre
            self.track_length = track_length
        else:
            self.title = json["trackName"]
            self.album = json["collectionName"]
            self.genre = json["primaryGenreName"]
            self.track_length = json["trackTimeMillis"]
    
    def info(self):
        return f"{super().info()} [{self.genre}]"

    def length(self):
        return round(float(self.track_length) / 1000)

class Movie(Media):
    def __init__(self, title="No Title", author="No Author", release_year="No Release Year", url="No URL", rating = "No Rating", movie_length = 0, json=None):
        self.json = json
        super().__init__(title, author, release_year, url, json)
        if json == None:
            self.rating = rating
            self.movie_length = movie_length
        else: 
            self.title = json["trackName"]
            self.track_length = json["trackTimeMillis"]
            self.rating = json["contentAdvisoryRating"]
            self.movie_length = json["trackTimeMillis"]
    
    def info(self):
        return f"{super().info()} [{self.rating}]"

    def length(self):
        return round(float(self.movie_length) / 60000)
        

def itunes_API(param):
    url = 'https://itunes.apple.com/search'
    dict = {'term':param}
    resp = requests.get(url, dict)
    list = json.loads(resp.text)['results']
    return list

def itunes_response(param):
    songs = []
    movies = []
    medias = []
    itunes_list = []
    num = 0
    for result in itunes_API(param):
        if 'kind' in result:
            if result['kind'] == 'song':
                songs.append(Song(json=result))       
            elif result['kind'] =='feature-movie':
                movies.append(Movie(json=result))
            else:
                medias.append(Media(json=result))
    print ('SONGS')
    for song in songs:
        itunes_list.append(song.url)
        num += 1
        print (str(num)+ ' ' + song.info())

    print ('MOVIES')
    for movie in movies:
        itunes_list.append(movie.url)
        num += 1
        print (str(num)+ ' ' + movie.info())

    print ('OTHER MEDIA')
    for media in medias:
        itunes_list.append(media.url)
        num += 1
        print (str(num)+ ' ' + media.info())
         
    return itunes_list

if __name__ == "__main__":
    # your control code for Part 4 (interactive search) should go here
    user_input = input('Enter a search term or exit: ')
    if user_input == 'exit':
        print('Exit.')
        exit()
    result = itunes_response(user_input)
    while(1):
        userinput_search = input('Enter a number to preview, or enter another search term, or exit: ')
        if userinput_search.isnumeric() and int(userinput_search) < len(result): 
            url = result[int(userinput_search)-1]
            print('Launching ')
            print(url)
            print('in web browser...')
            webbrowser.open(url)
        elif userinput_search.isnumeric() and int(userinput_search) > len(result): 
            print('Please input valid index')
            
        elif userinput_search == 'exit':
            print('Exit.')
            exit()
        else:
            result = itunes_response(userinput_search)

