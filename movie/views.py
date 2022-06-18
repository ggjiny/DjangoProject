from django.shortcuts import render
import requests
import json

from .forms import SearchForm

my_id = '53d4fa0a5436efd4f6755367e50b9b8f'

def home(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        searchword = request.POST.get('search')
        if form.is_valid():
            url = 'https://api.themoviedb.org/3/search/movie?api_key='+my_id+'&query='+searchword
            response = requests.get(url)
            resdata = response.text
            obj = json.loads(resdata)
            obj = obj['results']
            return render(request, 'movie/search.html', {'obj':obj, 'word':searchword})
    else:
        form = SearchForm()
        url = 'https://api.themoviedb.org/3/trending/movie/week?api_key='+my_id
        response = requests.get(url)
        resdata = response.text
        obj = json.loads(resdata)
        obj = obj['results']
    return render(request, 'movie/index.html', {'obj':obj, 'form':form})

def detail(request, movie_id):
    url = 'https://api.themoviedb.org/3/movie/' + movie_id +'?api_key='+my_id
    response = requests.get(url)
    resdata = response.text
    resdata = json.loads(resdata)
    return render(request, 'movie/detail.html', {"resdata":resdata})

def genre(request):
    url = 'https://api.themoviedb.org/3/genre/movie/list?api_key='+my_id+'&language=ko-KR'
    response = requests.get(url)
    resdata = response.text
    obj = json.loads(resdata)
    obj = obj['genres']
    return render(request, 'movie/genre.html', {"obj": obj})

def detail_genre(request, genre_id, genre):
    url = 'https://api.themoviedb.org/3/discover/movie?api_key=' + my_id + '&with_genres=' + genre_id
    response = requests.get(url)
    resdata = response.text
    obj2= json.loads(resdata)
    obj = obj2['results']
    return render(request, 'movie/genre_detail.html', {'obj': obj, 'genre':genre})

def about(request):
    return render(request, 'movie/about.html')
