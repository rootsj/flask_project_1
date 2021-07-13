from bson import ObjectId
from flask.json import JSONEncoder

class MongoJSONEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        else:
            return super().default(o)



'''
#참고
import json
from bson import ObjectId

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

JSONEncoder().encode(analytics)


#mongoflask.py
from datetime import datetime, date

import isodate as iso
from bson import ObjectId
from flask.json import JSONEncoder
from werkzeug.routing import BaseConverter


class MongoJSONEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, (datetime, date)):
            return iso.datetime_isoformat(o)
        if isinstance(o, ObjectId):
            return str(o)
        else:
            return super().default(o)


class ObjectIdConverter(BaseConverter):
    def to_python(self, value):
        return ObjectId(value)

    def to_url(self, value):
        return str(value)


#app.py
from .mongoflask import MongoJSONEncoder, ObjectIdConverter

def create_app():
    app = Flask(__name__)
    app.json_encoder = MongoJSONEncoder
    app.url_map.converters['objectid'] = ObjectIdConverter

    # Client sends their string, we interpret it as an ObjectId
    @app.route('/users/<objectid:user_id>')
    def show_user(user_id):
        # setup not shown, pretend this gets us a pymongo db object
        db = get_db()

        # user_id is a bson.ObjectId ready to use with pymongo!
        result = db.users.find_one({'_id': user_id})

        # And jsonify returns normal looking json!
        # {"_id": "5b6b6959828619572d48a9da",
        #  "name": "Will",
        #  "birthday": "1990-03-17T00:00:00Z"}
        return jsonify(result)


    return app
'''