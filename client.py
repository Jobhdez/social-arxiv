import requests
import json

"""
possible endpoints:
     GET papers: http://127.0.0.1:8000/api/
     GET papers with given tag: http://127.0.0.1:8000/api/tag/<tag>/
     GET paper detail: http://127.0.0.1:8000/api/<id>
     POST search: http://127.0.0.1:8000/api/search/ + data where data is {'search': '<whatever>'}
     POST get paper comments: http://127.0.0.1:8000/api/<id>/comment/' where data is {'name': '<x_name>', 'email': '<x_email>', 'body': '<x_body>'} 
"""

URL = 'http://127.0.0.1:8000/api/'

def get_papers():
    re = requests.get(URL)
    return re.json()

def get_tagged_papers(tag):
    link = URL + "tag/" + tag + "/"
    re = requests.get(link)
    return re.json()

def get_detail_paper(id_num):
    link = URL + id_num + "/"
    re = requests.get(link)
    return re.json()

def search_papers(search_term):
    link = URL + 'search/'
    data = {'search': search_term}
    re = requests.post(link, data=data)
    return re.json()

def get_comments(id_num, name, email, body):
    link = URL + id_num + 'comment/'
    data = {'name': name, 'email': email, 'body': body}
    re = requests.post(link, data=data)
    return re.json()

def login(username, password):
    link = URL + 'login/'
    data = {'username': username, 'password': password}
    re = requests.post(link, data=data)
    return re.json()

def register(password, username, first_name, email):
    link = URL + 'register/'
    data = {'password': password, 'password2': password, 'username':username, 'first_name': first_name, 'email': email}
    re = requests.post(link, data=data)
    return re.json()

def get_users(username, password):
    link = URL + 'users/'
    re = requests.post(link, auth=(username, password))
    return re.json()
