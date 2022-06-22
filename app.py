from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('mongodb+srv://test:sparta@cluster0.gswdo8n.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbsparta

@app.route('/')
def home():
    try:
        devsbook = db.devsbook.find_one({"title": booktitle}, {"_id": False})
        return render_template('detail.html', devsbook=devsbook)


    # API - DB 데이터 가져오기(상세페이지-식물 detail) : jinja2로 detail.html에서 나타냈음
    @app.route('/detail/', methods=['GET'])
    def get_details():
        detail_box = list(db.detail.find({}, {'_id': False}))
        return jsonify({'detail_box': detail_box})

import requests
from bs4 import BeautifulSoup
headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}

data = requests.get('https://search.kyobobook.co.kr/web/search?vPstrKeyWord=spring&searchPcondition=1&searchCategory=%EA%B5%AD%EB%82%B4%EB%8F%84%EC%84%9C@KORBOOK@@%EC%BB%B4%ED%93%A8%ED%84%B0/IT@33&collName=KORBOOK&from_CollName=%EC%A0%84%EC%B2%B4@UNION&searchOrder=0&vPstrTab=PRODUCT&from_coll=KORBOOK&currentPage=1&orderClick=LIZ',headers=headers)

soup = BeautifulSoup(data.text, 'html.parser')

main_list = soup.select('#plants_list > ul > div')

for bestseller_book in bestseller_book:
    image = bestseller_book.select_one('div.cover > a > img')
    booktitle = bestseller_book.select_one('div.detail > div.title > a > strong').text

    doc = {
    'image': image['src'],
    'booktitle': booktitle,
    'desc' : desc
    }
db.devsbook.insert_one(doc)

if __name__ == '__main__':
   app.run('0.0.0.0',port=5000,debug=True)