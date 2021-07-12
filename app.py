from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient  

# from bson.objectid import ObjectId

app = Flask(__name__)

client = MongoClient('localhost', 27017) 
db = client.dbsparta  

@app.route('/')
def home():
   return render_template('index.html')


@app.route('/memo', methods=['POST'])
def post_article():
   title_receive = request.form['title_give']  
   comment_receive = request.form['comment_give'] 

   article = {'title': title_receive, 'comment': comment_receive}

   db.articles.insert_one(article)

   return jsonify({'result': 'success'})


@app.route('/memo/list', methods=['GET'])
def read_articles():
   result = list(db.articles.find({}, {'_id': 0})) 
   #2 _id -> string 변경 후 json 전달 필요
   return jsonify({'result': 'success', 'articles': result})


@app.route('/memo/check', methods=['POST'])
def check_article():
   title_receive = request.form['title_give']

   article = db.articles.find_one({'title': title_receive})
   global id_receive #3 임시 전역변수. read_article에서 pk _id 넘기고 삭제 예정
   id_receive = article['_id']

   return jsonify({'result': 'success'})

@app.route('/memo/modify', methods=['POST'])
def modify_article():
   title_receive = request.form['title_give']
   comment_receive = request.form['comment_give']

   db.articles.update({'_id': id_receive}, {'$set': {'title': title_receive, 'comment': comment_receive}})

   return jsonify({'result': 'success'})


@app.route('/memo/delete', methods=['POST'])
def delete_article():
   title_receive = request.form['title_give']
   
   db.articles.delete_one({'title': title_receive}) #4 pk값 _id로 변경해야함
   
   return jsonify({'result': 'success'})

if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)