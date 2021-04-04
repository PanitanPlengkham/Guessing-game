from flask import Flask, request, jsonify,render_template,redirect
from pymongo import MongoClient
import os, json, redis,pymongo

# App
app = Flask(__name__)
# connect to MongoDB
mongoClient = MongoClient('mongodb://' + os.environ['MONGODB_USERNAME'] + ':' + os.environ['MONGODB_PASSWORD'] + '@' + os.environ['MONGODB_HOSTNAME'] + ':27017/' + os.environ['MONGODB_AUTHDB'])
db = mongoClient[os.environ['MONGODB_DATABASE']]

# connect to Redis
redisClient = redis.Redis(host=os.environ.get("REDIS_HOST", "localhost"), port=os.environ.get("REDIS_PORT", 6379), db=os.environ.get("REDIS_DB", 0))

@app.route('/', methods=['GET'])
def index():
    return render_template("index.html")

@app.route('/start', methods=['POST'])
def start():
    data = {
        "question": {
            "1_ques": "A",
            "2_ques": "B",
            "3_ques": "C",
            "4_ques": "D"
        },
        "stage": 0,
        "answer": {
            "1_ans": "_",
            "2_ans": "_",
            "3_ans": "_",
            "4_ans": "_"
        },
    }
    db.static.insert_one(data)
    static = db.static.find_one(sort=[('_id', pymongo.DESCENDING)])
    return render_template("play.html",static=static)

@app.route('/ques', methods=['POST','GET'])
def ques():
    static = db.static.find_one(sort=[('_id', pymongo.DESCENDING)])
    if request.method == "POST":
        if static['question']['1_ques'] != static['answer']['1_ans']:
            while request.form['alphabet'] != static['question']['1_ques']:
                return redirect('/ques')
            db.static.update_one({"_id": static["_id"]}, {"$set": {"answer.1_ans": static['question']['1_ques']}})
            return redirect('/ques')

        elif static['question']['2_ques'] != static['answer']['2_ans']:
            while request.form['alphabet'] != static['question']['2_ques']:
                return redirect('/ques')
            db.static.update_one({"_id": static["_id"]}, {"$set": {"answer.2_ans":static['question']['2_ques']}})
            return redirect('/ques')

        elif static['question']['3_ques'] != static['answer']['3_ans']:
            while request.form['alphabet'] != static['question']['3_ques']:
                return redirect('/ques')
            db.static.update_one({"_id": static["_id"]}, {"$set": {"answer.3_ans": static['question']['3_ques']}})
            return redirect('/ques')

        elif static['question']['4_ques'] != static['answer']['4_ans']:
            while request.form['alphabet'] != static['question']['4_ques']:
                return redirect('/ques')
            db.static.update_one({"_id": static["_id"]}, {"$set": {"answer.4_ans": static['question']['4_ques']}})
            return redirect('/ques')

    elif request.method == "GET":
        return render_template('play.html', static=static)




if __name__ == "__main__":
    ENVIRONMENT_DEBUG = os.environ.get("FLASK_DEBUG", True)
    ENVIRONMENT_PORT = os.environ.get("FLASK_PORT", 5000)
    app.run(host='0.0.0.0', port=ENVIRONMENT_PORT, debug=ENVIRONMENT_DEBUG)