import requests
from bs4 import BeautifulSoup
import pandas as pd

# Your imbd ratings url
URL = 'https://www.imdb.com/user/ur73628355/ratings?ref_=nv_usr_rt_4'

html = requests.get(URL).content
soup = BeautifulSoup(html,"html.parser")


movies = soup.find_all("div",{"class":"lister-item mode-detail"})


#Lists
movie_title_arr     = []
movie_year_arr      = []
movie_time_arr      = []
movie_synopsys_arr  = []
movie_genre_arr     = []
movie_watchdate_arr = []
movie_rate_arr      = []
movie_imdb_arr      = []
movie_img_arr       = []

def getMovieTitle(header):
    try:
        return header.find("h3",{"class": "lister-item-header"}).find("a").text
    except:
        return 'NA'

def getMovieYear(header):
    try:
        return header.find("h3",{"class": "lister-item-header"}).find("span",{"class":"lister-item-year text-muted unbold"}).text
    except:
        return 'NA'

def getMovieTime(header):
    try:
        return header.find("p",{"class":"text-muted text-small"}).find("span",{"class": "runtime"}).text
    except:
        return 'NA'

def getMovieSynopsys(header):
    try:
        return header.find("div",{"class":"lister-item-content"}).find_all("p")[2].text
    except:
        return 'NA'

def getMovieGenre(header):
    try:
        return header.find("p",{"class":"text-muted text-small"}).find("span",{"class": "genre"}).text
    except:
        return 'NA'

def getMovieWatch(header):
    try:
        return header.find("div",{"class":"lister-item-content"}).find_all("p")[1].text.split("on ")[1]
    except:
        return 'NA'

def getMovieRate(header):
    try:
        return header.find_all("span",{"class":"ipl-rating-star__rating"})[1].text
    except:
        return 'NA'

def getMovieİmdb(header):
    try:
        return header.find_all("span",{"class":"ipl-rating-star__rating"})[0].text
    except:
        return 'NA'

def getMovieImg(header):
    try:
        return str(header.find_all("img")).split('loadlate="')[1].split('"')[0]
    except:
        return 'NA'


for i in movies:
    movie_title_arr.append(getMovieTitle(i))
    movie_year_arr.append(getMovieYear(i))
    movie_time_arr.append(getMovieTime(i))
    movie_synopsys_arr.append((getMovieSynopsys(i)))
    movie_genre_arr.append(getMovieGenre(i))
    movie_watchdate_arr.append(getMovieWatch(i))
    movie_rate_arr.append(getMovieRate(i))
    movie_imdb_arr.append(getMovieİmdb(i))
    movie_img_arr.append(getMovieImg(i))
    
    

movieDf = pd.DataFrame({
    "Title"         : movie_title_arr,
    "Release_Year"  : movie_year_arr,
    "Duration"      : movie_time_arr,
    "Synopsis"      : movie_synopsys_arr,
    "Genre"         : movie_genre_arr,
    "Watch_Date"    : movie_watchdate_arr,
    "Rate"          : movie_rate_arr,
    "Imbb_Rate"     : movie_imdb_arr,
    "image_id"      : movie_img_arr
})

user = soup.find("div",{"class":"article listo"})
user_name = user.find("h1",{"class":"header"}).text.replace(' ','_')

movieDf.to_csv('{}.csv'.format(user_name))
print("------- CSV Downloaded -------")