from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('mongodb+srv://WhiteIndigo:rhdtneh123@cluster0.o6pkllk.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta


@app.route('/')
def home():
    return render_template('index.html')


@app.route("/comment", methods=["POST"])
def comment_post():
    comment_receive = request.form['comment_give']
    comment_list = list(db.comment.find({}, {'_id': False}))
    count = len(comment_list) + 1

    doc = {
        'num':count,
        'comment':comment_receive,
        'done':0
    }

    db.comment.insert_one(doc)

    return jsonify({'msg': '등록 완료!'})


@app.route("/comment/delete", methods=["POST"])
def comment_delete():
    num_receive = request.form['num_give']
    db.comment.delete_one({'num': int(num_receive)})
    return jsonify({'msg': '삭제 완료!'})

@app.route("/comment", methods=["GET"])

def comment_get():
    comment_list = list(db.comment.find({}, {'_id': False}))

    return jsonify({'comments': comment_list})




if __name__ == '__main__':
        app.run('0.0.0.0', port=4000, debug=True)
