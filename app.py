from flask import Flask, render_template, request, jsonify, redirect, url_for
import jwt
import datetime
import hashlib
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['UPLOAD_FOLDER'] = "./static/profile_pics"

SECRET_KEY = 'SPARTA'

from pymongo import MongoClient
import certifi
from pymongo import MongoClient
import certifi

ca = certifi.where()

client = MongoClient('mongodb+srv://test:sparta@cluster0.gswdo8n.mongodb.net/Cluster0?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.dbsparta
db.devsbook_bestseller.drop()
db.devsbook_front.drop()
db.devsbook_back.drop()

import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
# 베스트 셀러 크롤링
data = requests.get(
    'http://www.kyobobook.co.kr/bestSellerNew/bestseller.laf?mallGb=KOR&linkClass=33&range=0&kind=1&orderClick=DCb',
    headers=headers)
bestseller_soup = BeautifulSoup(data.text, 'html.parser')

bestseller_books = bestseller_soup.select('#main_contents > ul > li')

for bestseller_book in bestseller_books:
    booktitle = bestseller_book.select_one('div.detail > div.title > a > strong').text
    price = bestseller_book.select_one('div.price > strong').text
    image = bestseller_book.select_one('div.cover > a > img')
    doc = {
        'booktitle': booktitle,
        'price': price,
        'image': image['src']
    }
    db.devsbook_bestseller.insert_one(doc)

# 프론트엔드북 크롤링
front_data = requests.get(
    'https://search.kyobobook.co.kr/web/search?vPstrKeyWord=react&searchPcondition=1&searchCategory=%EA%B5%AD%EB%82%B4%EB%8F%84%EC%84%9C@KORBOOK@@%EC%BB%B4%ED%93%A8%ED%84%B0/IT@33&collName=KORBOOK&from_CollName=%EC%A0%84%EC%B2%B4@UNION&vPstrTab=PRODUCT&from_coll=KORBOOK&currentPage=1&orderClick=LIZ',
    headers=headers)
front_soup = BeautifulSoup(front_data.text, 'html.parser')
front_books = front_soup.select('#search_gallery > tr > td')

for front_book in front_books:
    booktitle = front_book.select_one('div > div.title > a > strong').text
    price = front_book.select_one('div > div.price > div.sell_price > strong').text
    image = front_book.select_one('div > div.image > div.cover > a > img')
    doc = {
        'booktitle': booktitle,
        'price': price,
        'image': image['src']
    }
    db.devsbook_front.insert_one(doc)

back_data = requests.get(
    'https://search.kyobobook.co.kr/web/search?vPstrKeyWord=spring&searchPcondition=1&searchCategory=%EA%B5%AD%EB%82%B4%EB%8F%84%EC%84%9C@KORBOOK@@%EC%BB%B4%ED%93%A8%ED%84%B0/IT@33&collName=KORBOOK&from_CollName=%EC%A0%84%EC%B2%B4@UNION&searchOrder=0&vPstrTab=PRODUCT&from_coll=KORBOOK&currentPage=1&orderClick=LIZ',
    headers=headers)
back_soup = BeautifulSoup(back_data.text, 'html.parser')
back_books = back_soup.select('#search_gallery > tr > td')

# 백엔드북 크롤링
for back_book in back_books:
    booktitle = back_book.select_one('div > div.title > a > strong').text
    price = back_book.select_one('div > div.price > div.sell_price > strong').text
    image = back_book.select_one('div > div.image > div.cover > a > img')
    doc = {
        'booktitle': booktitle,
        'price': price,
        'image': image['src']
    }
    db.devsbook_back.insert_one(doc)


@app.route('/')
def home():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])

        return render_template()
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))


@app.route('/login')
def login():
    msg = request.args.get("msg")
    return render_template('login.html', msg=msg)


@app.route('/user/<username>')
def user(username):
    # 각 사용자의 프로필과 글을 모아볼 수 있는 공간
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        status = (username == payload["id"])  # 내 프로필이면 True, 다른 사람 프로필 페이지면 False

        user_info = db.users.find_one({"username": username}, {"_id": False})
        return render_template('user.html', user_info=user_info, status=status)
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("home"))


@app.route('/sign_in', methods=['POST'])
def sign_in():
    # 로그인
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']

    pw_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    result = db.users.find_one({'username': username_receive, 'password': pw_hash})

    if result is not None:
        payload = {
            'id': username_receive,
            'exp': datetime.utcnow() + timedelta(seconds=60 * 60 * 24)  # 로그인 24시간 유지
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256').decode('utf-8')

        return jsonify({'result': 'success', 'token': token})
    # 찾지 못하면
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})


# 회원가입 서버
@app.route('/sign_up/save', methods=['POST'])
def sign_up():
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']
    password_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    doc = {
        "username": username_receive,  # 아이디
        "password": password_hash,  # 비밀번호
        "profile_name": username_receive,  # 프로필 이름 기본값은 아이디
        "profile_pic": "",  # 프로필 사진 파일 이름
        "profile_pic_real": "profile_pics/profile_placeholder.png",  # 프로필 사진 기본 이미지
        "profile_info": ""  # 프로필 한 마디
    }
    db.users.insert_one(doc)
    return jsonify({'result': 'success'})


# 아이디 중복확인
@app.route('/sign_up/check_dup', methods=['POST'])
def check_dup():
    username_receive = request.form['username_give']
    exists = bool(db.users.find_one({"username": username_receive}))
    return jsonify({'result': 'success', 'exists': exists})


@app.route('/update_profile', methods=['POST'])
def save_img():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        # 프로필 업데이트
        return jsonify({"result": "success", 'msg': '프로필을 업데이트했습니다.'})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("home"))


@app.route('/posting', methods=['POST'])
def posting():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        # 포스팅하기
        return jsonify({"result": "success", 'msg': '포스팅 성공'})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("home"))


@app.route("/get_posts", methods=['GET'])
def get_posts():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        # 포스팅 목록 받아오기
        return jsonify({"result": "success", "msg": "포스팅을 가져왔습니다."})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("home"))


@app.route('/update_like', methods=['POST'])
def update_like():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        # 좋아요 수 변경
        return jsonify({"result": "success", 'msg': 'updated'})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("home"))


# 메인페이지, jinja2
@app.route('/main', methods=["GET"])
def main_page():
    bestseller_list = list(db.devsbook_bestseller.find({}, {'_id': False}))
    front_list = list(db.devsbook_front.find({}, {'_id': False}))
    back_list = list(db.devsbook_back.find({}, {'_id': False}))
    return render_template('main_page.html',
                           bestseller_list=bestseller_list, front_list=front_list, back_list=back_list
                           )


# 의견달기
@app.route('/main')
def homework():
    return render_template('main_page.html')


@app.route("/comment", methods=["POST"])
def comment_post():
    comment_receive = request.form['comment_give']

    comment_list = list(db.comment.find({}, {'_id': False}))
    count = len(comment_list) + 1

    doc = {
        'num': count,
        'comment': comment_receive,
        'done': 0
    }

    db.comment.insert_one(doc)

    return jsonify({'msg': '저장 완료!'})


@app.route("/comment/done", methods=["POST"])
def comment_done():
    num_receive = request.form['num_give']
    db.comment.update_one({'num': int(num_receive)}, {'$set': {'done': 1}})
    return jsonify({'msg': '삭제 완료!'})


@app.route("/comment", methods=["GET"])
def comment_get():
    comment_list = list(db.comment.find({}, {'_id': False}))
    return jsonify({'comments': comment_list})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
