from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient  

from bson import json_util
from mongoengine_jsonencoder import MongoJSONEncoder
# ObjectId -> str 변경

from bson.objectid import ObjectId #str -> ObjectId 변경


app = Flask(__name__)
app.json_encoder = MongoJSONEncoder # json 타입 적용

client = MongoClient('localhost', 27017) 
db = client.dbtest  
#MongoDB dbtest 생성

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
   # result = list(db.articles.find({}, {'_id': 0})) # id를 제외하고 검색
   result = list(db.articles.find({})) 

   return jsonify({'result': 'success', 'articles': result})


@app.route('/memo/modify', methods=['POST'])
def modify_article():
   id_receive = request.form['id_give']
   title_receive = request.form['title_give']
   comment_receive = request.form['comment_give']

   bson_id = ObjectId(id_receive) # str -> objectID 변경

   db.articles.update_one({'_id': bson_id}, {'$set': {'title': title_receive, 'comment': comment_receive}})

   return jsonify({'result': 'success'})


@app.route('/memo/delete', methods=['POST'])
def delete_article():
   id_receive = request.form['id_give']

   bson_id = ObjectId(id_receive) # str -> objectID 변경

   db.articles.delete_one({'_id': bson_id}) #_id로 삭제
   
   return jsonify({'result': 'success'})

if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)