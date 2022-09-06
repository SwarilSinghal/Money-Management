import json
import urllib
from PIL import Image
# from urllib import request
import requests
import bcrypt
import pymongo
import random
from string import digits, ascii_uppercase
from click import echo
from flask import Flask, session, redirect, url_for, render_template, request, Response, jsonify, session
from flask_session import Session
import datetime
from pymongo import auth
import cv2
import pytz

app: Flask = Flask(__name__)
app.secret_key = "testing"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
mongo_uri = "mongodb://swaril:" + urllib.parse.quote(
    "$w@R!1") + "@ac-ymz3eon-shard-00-00.iympypo.mongodb.net:27017,ac-ymz3eon-shard-00-01.iympypo.mongodb.net:27017,ac-ymz3eon-shard-00-02.iympypo.mongodb.net:27017/?ssl=true&replicaSet=atlas-y20jq1-shard-0&authSource=admin&retryWrites=true&w=majority"
client = pymongo.MongoClient(
    mongo_uri)
db = client.User
records = db.cashManagement
# video_stream = VideoCamera()

# db = client.get_database('total_records')
# records = db.register
@app.route("/scanQRdebit")
def scanQRdebit():
    print("HOME session:", session)
    if "username" not in session or session['username'] == None:
        return render_template("login.html")
    return render_template('scanQRDebit.html')



@app.route("/")
def menu():
    print("HOME session:", session)
    if "username" not in session or session['username'] == None:
        return render_template("login.html")
    # print("USER TYPE MENU:", session['type'])
    return render_template('menu.html', logged_in='true', type=session['type'])



@app.route("/scanQRcredit")
def scanQRcredit():
    print("HOME session:", session)
    if "username" not in session or session['username'] == None:
        return render_template("login.html")
    return render_template('scanQRcredit.html')



# @app.route("/lastDebitTransactions", methods=['POST'])
# def lastDebitTransactions():
#     print("TEST")
#     if request.method == "POST":
#         json_req = request.get_json()
#         print(json_req)
#         cursor = readTransactions('debitTransactions', {"cid": str(json_req['code'])})
#         print(cursor)
#
#         if(cursor['status'] and cursor['status'] == 'error'):
#             return cursor
#         return list(cursor)
#         return render_template('login.html', transactions=list(cursor))



# def readTransactions(collection, condition):
#     try:
#         mongo_uri = "mongodb://swaril:" + urllib.parse.quote(
#         "$w@R!1") + "@ac-ymz3eon-shard-00-00.iympypo.mongodb.net:27017,ac-ymz3eon-shard-00-01.iympypo.mongodb.net:27017,ac-ymz3eon-shard-00-02.iympypo.mongodb.net:27017/?ssl=true&replicaSet=atlas-y20jq1-shard-0&authSource=admin&retryWrites=true&w=majority"
#         client = pymongo.MongoClient(
#             mongo_uri)
#         db = client.cashManagement
#         print(db)
#         collection = 'Customers'
#         records = db[collection]
#         print(records)
#         cursors = records.find_one(condition)
#         print(cursors)
#         return cursors
#     except:
#         return {'status':'error'}



def readDb(collection, condition):
    try:
        mongo_uri = "mongodb://swaril:" + urllib.parse.quote(
            "$w@R!1") + "@ac-ymz3eon-shard-00-00.iympypo.mongodb.net:27017,ac-ymz3eon-shard-00-01.iympypo.mongodb.net:27017,ac-ymz3eon-shard-00-02.iympypo.mongodb.net:27017/?ssl=true&replicaSet=atlas-y20jq1-shard-0&authSource=admin&retryWrites=true&w=majority"
        client = pymongo.MongoClient(
            mongo_uri)
        db = client.cashManagement
        records = db[collection]
        cursor = records.find_one(condition)
        return cursor
    except:
        return {'status':'error'}



@app.route("/login", methods=["POST", "GET"])
def login(records=None):
    message = 'Please login to your account'
    if "username" in session and session['username'] != None:
        return redirect('/')
    # return render_template('login.html', message=message)
    if hasattr(request, 'method') and request.method == "POST":
        print("inside request")
        username = request.form.get("username")
        password = request.form.get("password")
        # mongo_uri = "mongodb://swaril:" + urllib.parse.quote(
        #     "$w@R!1") + "@ac-ymz3eon-shard-00-00.iympypo.mongodb.net:27017,ac-ymz3eon-shard-00-01.iympypo.mongodb.net:27017,ac-ymz3eon-shard-00-02.iympypo.mongodb.net:27017/?ssl=true&replicaSet=atlas-y20jq1-shard-0&authSource=admin&retryWrites=true&w=majority"
        # client = pymongo.MongoClient(
        #     mongo_uri)
        # db = client.User
        # records = db.cashManagement
        user_found = readDb( "Users" , {"username": username})
        # print("user Found" + email_found)
        if user_found:
            username = user_found['username']
            passwordcheck = user_found['password']

            # if bcrypt.checkpw(password.encode('utf-8'), passwordcheck):
            if passwordcheck == password:
                print(username)
                session["username"] = username
                session['type'] = user_found['type']
                session['amount'] = user_found['amount']
                return redirect('/')
            else:
                message = 'Wrong password'
                return render_template('login.html', message=message)
        else:
            message = 'Email not found'
            return render_template('login.html', message=message)
    return render_template('login.html', message=message)


# @app.route("/logged_in")
# def menu():
#     if "username" in session and sesion['username'] != None:
#         return render_template("menu.html")
#     return render_template("login.html")


@app.route("/logout")
def logout():
    session["username"] = None
    return redirect("/")


@app.route("/debit", methods=["POST", "GET"])
def debit():
    if "username" not in session or session['username'] == None:
        return render_template("login.html")
    if request.method == "POST":
        json_req = request.get_json()
        print(json_req)
        cursor = readDb('Customers', {"cid": str(json_req['code'])})
        print('checking paraments',json_req['code'], json_req['amount'])
        # isIntegar = isinstance(json_req['amount'], int)
        # if not isIntegar:
        #     return {'status' : 'error', 'message': 'Invalid Amount'}
        print("Read DB:", cursor)
        final_balance = int(cursor['balance']) - int(json_req['amount'])
        if (final_balance < 0):
            return {'status': 'error', 'message': 'Insufficient Balance'}
        user = readDb('Users', {'username': session['username']})
        if(user) :
            amount_collected = int(user['amount']) + int(json_req['balance'])
        else:
            return {'status': 'error', 'message': "DB issues, try Again!"}
        resp = update_db('Users', {'amount': amount_collected}, {'username' : session['username']})
        print(resp)
        document = {'amount': json_req['amount'], 'cid' : json_req['code'] }
        receipt = generate_debit_receipt(document)

        print("final Balance:", final_balance)
        resp = update_db("Customers", {'balance': final_balance}, {'cid' : str(json_req['code'])})
        print(resp)
        return {'status':'success', 'balance':final_balance, 'amount':json_req['amount'] }
    return {'status': 'error', 'message' : 'Try Again'}

def rand_string(length = 8):
    legals = digits + ascii_uppercase
    return ''.join( random.choice(legals) for _ in range(length) )


def generate_debit_receipt(document):
    document['user'] = session['username']
    document['txn_id'] = 'CT' + rand_string()
    document['time'] = datetime.datetime.now(pytz.timezone('Asia/Kolkata'))
    mongo_uri = "mongodb://swaril:" + urllib.parse.quote(
        "$w@R!1") + "@ac-ymz3eon-shard-00-00.iympypo.mongodb.net:27017,ac-ymz3eon-shard-00-01.iympypo.mongodb.net:27017,ac-ymz3eon-shard-00-02.iympypo.mongodb.net:27017/?ssl=true&replicaSet=atlas-y20jq1-shard-0&authSource=admin&retryWrites=true&w=majority"
    client = pymongo.MongoClient(
        mongo_uri)

    mydb = client["cashManagement"]
    mycol = mydb["debitTransactions"]
    x = mycol.insert_one(document)
    return x;




@app.route("/credit", methods=["POST", "GET"])
def credit():
    if "username" not in session or session['username'] == None:
        return render_template("login.html")
    if request.method == "POST":
        json_req = request.get_json()
        print(json_req)
        cursor = readDb('Customers', {"cid": str(json_req['code'])})
        print('checking paraments',json_req['code'], json_req['amount'])
        # isIntegar = isinstance(json_req['amount'], int)
        # if not isIntegar:
        #     return {'status' : 'error', 'message': 'Invalid Amount'}
        print("Read DB:", cursor)
        final_balance = int(cursor['balance']) + int(json_req['amount'])
        # if( final_balance < 0):
        #     return {'status' : 'error', 'message': 'Insufficient Balance'}
        document = {'balance': final_balance, 'name': json_req['name'], 'phone_number': json_req['phone_number']}
        print("final Balance:", final_balance)
        resp = update_db("Customers", document, {'cid' : str(json_req['code'])})
        print(resp)
        document['status'] = 'success'
        return document
    return {'status': 'error'}

def update_db(collection, document, condition):
    mongo_uri = "mongodb://swaril:" + urllib.parse.quote(
        "$w@R!1") + "@ac-ymz3eon-shard-00-00.iympypo.mongodb.net:27017,ac-ymz3eon-shard-00-01.iympypo.mongodb.net:27017,ac-ymz3eon-shard-00-02.iympypo.mongodb.net:27017/?ssl=true&replicaSet=atlas-y20jq1-shard-0&authSource=admin&retryWrites=true&w=majority"
    client = pymongo.MongoClient(
        mongo_uri)
    db = client.cashManagement
    records = db[collection]
    document = { "$set" : document}
    resp = records.update_one(condition, document)
    print(resp)
    cursor = readDb(collection, condition)
    return cursor




@app.route("/viewBalance", methods=["POST", "GET"])
def viewBalance():
    print('viewBalance username:', session['username'], session)
    code = request.args.get('code')
    print(code)
    cursor = readDb('Customers', {"cid": code})
    print(cursor)
    print("END viewBalance")
    if "username" in session and session['username'] != None:
        logged_in = "true"
    return render_template("viewBalance.html", Username=cursor['name'], Balance=cursor['balance'], code=code, logged_in=logged_in, MoneyCollected=session['amount'])


@app.route("/viewBalanceCredit", methods=["POST", "GET"])
def viewBalanceCredit():
    print('viewBalance username:', session['username'], session)
    code = request.args.get('code')
    print(code)
    cursor = readDb('Customers', {"cid": code})
    # Username = cursor['name']?cursor['name']:''
    print(cursor)
    print("END viewBalance")
    if "username" in session and session['username'] != None:
        logged_in = "true"
    return render_template("viewBalanceCredit.html", Username=cursor['name'], Balance=cursor['balance'], code=code, logged_in=logged_in, phone_number = cursor['phone_number'], MoneyCollected=session['amount'], MoneyDeposited=session['amount_credit'])




@app.route("/scanQR", methods=["POST", "GET"])
def scanQR():
    if "username" not in session or session['username'] == None:
        return render_template("login.html")
    return render_template("scanQR.html")


# def stopCamera():



# def gen():
#     cap = cv2.VideoCapture(0)
#     # initialize the cv2 QRCode detector
#     detector = cv2.QRCodeDetector()
#     while True:
#         _, img = cap.read()
#         data, bbox, _ = detector.detectAndDecode(img)
#         if bbox is not None:
#             if data:
#                 print("[+] QR Code detected, data:", data)
#                 cap.release()
#                 dictToSend = {'data' : data}
#                 # res = requests.post('http://localhost:5000/viewBalance', json=dictToSend)
#                 # print(res)
#                 # return res
#                 with app.app_context():
#                     return redirect(url_for('viewBalance'))
#
#                 break
#
#         ret, jpeg = cv2.imencode('.jpg', img)
#
#         frame =  jpeg.tobytes()
#         # frame = frame.toByte
#         yield (b'--frame\r\n'
#                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
#         if cv2.waitKey(1) == ord("q"):
#             break

    # cap.release()

    # n=1
    # while n<20:
    #     frame = camera.get_frame()
    #     # frame = Image.fromarray(frame, "RGB")
    #     detector = cv2.QRCodeDetector()
    #     # print("IMENCODE RET:" + str(jpeg))
    #     data, vertices_array, binary_qrcode = detector.detectAndDecode(frame)
    #     # detector = cv2.wechat_qrcode_WeChatQRCode(detector_prototxt_path="detect.prototxt",
    #     #                                           detector_caffe_model_path="detect.caffemodel",
    #     #                                           super_resolution_prototxt_path="sr.prototxt",
    #     #                                           super_resolution_caffe_model_path="sr.caffemodel")
    #     # detect and decode
    #     # data, vertices_array = detector.detectAndDecode(frame)
    #     print("QRCode data:")
    #     print(data)
    #     n = n+1



# @app.route('/video_feed')
# def video_feed():
#     return Response(gen(),
#                     mimetype='multipart/x-mixed-replace; boundary=frame',)
#     return redirect(url_for('viewBalance'))


# @app.route("/result", methods=["POST"])
# def result():
#     # data = json.loads(request.json)
#     # print(data)
#     if True:  # Only if data has been posted
#         result = request.form  # Get the data
#         email = result["email"]
#         password = result["pass"]
#         try:
#             # Try signing in the user with the given information
#             user = auth.sign_in_with_email_and_password(email, password)
#             # Insert the user data in the global person
#             global person
#             person["is_logged_in"] = True
#             person["email"] = user["email"]
#             person["uid"] = user["localId"]
#             # Get the name of the user
#             data = db.child("users").get()
#             person["name"] = data.val()[person["uid"]]["name"]
#             # Redirect to welcome page
#             return redirect(url_for('welcome'))
#         except:
#             # If there is any error, redirect back to login
#             return redirect(url_for('login'))
#     else:
#         # if person["is_logged_in"] == True:
#         #     return redirect(url_for('welcome'))
#         # else:
#         return redirect(url_for('login'))
#

app.run()
