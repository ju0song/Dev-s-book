from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('mongodb+srv://test:sparta@cluster0.gswdo8n.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbsparta

import requests
from bs4 import BeautifulSoup
headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('http://www.kyobobook.co.kr/bestSellerNew/bestseller.laf?mallGb=KOR&linkClass=33&range=0&kind=1&orderClick=DCb', headers=headers)
soup = BeautifulSoup(data.text, 'html.parser')

@app.route('/')
def main_page():
    return render_template('main_page.html')

@app.route('/Front_page')
def Front_page():
    return render_template('Front_page.html')

@app.route('/back_page')
def back_page():
    return render_template('back_page.html')

if __name__ == '__main__':
   app.run('0.0.0.0',port=5000,debug=True)

books = soup.select('#main_contents > ul > li')

for book in books:
    b = book.select_one('div.detail > div.title > a > strong').text
    booktitle = b
    price = book.select_one('div.price > strong').text
    image = book.select_one('div.cover > a > img')
    doc = {
        'booktitle': booktitle,
        'price': price,
        'image': image['src']
    }
    db.devsbook.insert_one(doc)

@app.route('/booklist', methods=['GET'])
def books ():
    book_list = list(db.devsbook.find({}, {'_id': False}))
    return jsonify({'devsbook': book_list})
