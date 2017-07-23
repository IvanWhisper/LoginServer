from flask import Flask
from flask import request
import base64
import time
import random

app = Flask(__name__)

# user info
user = {
    'liuchunming': ['12345']
}


# generate token
def gen_token(uid):
    token = base64.b64encode(':'.join([str(uid),str(random.random()),str(time.time() + 7200)]).encode(encoding="utf-8"))
    user[uid]=[user[uid],token]
    print(user)
    return token

#verify token
def verify_token(token):
    _token = base64.b64decode(token.encode(encoding='utf-8')).decode()
    print(_token)
    print(user.get(_token.split(':')[0])[-1])
    print(user.get(_token.split(':')[0])[-1].decode())
    print(token)
    if not user.get(_token.split(':')[0])[-1].decode() == token:
        return -1
    if float(_token.split(':')[-1]) >= time.time():
        return 1
    else:
        return 0

#if login success,return a token to user
@app.route('/login', methods=['POST','GET'])
def login():
    print(base64.b64decode(request.headers['Authorization'].encode(encoding='utf8')))
    print(base64.b64decode(request.headers['Authorization'].encode(encoding='utf8')).decode())
    uid,password = base64.b64decode(request.headers['Authorization'].encode(encoding='utf8')).decode().split(':')
    print(uid)
    print(password)
    if user.get(uid)[0] == password:

        return gen_token(uid)
    else:
        return 'error'

#create a test route for verify login success or not
@app.route('/testlogin',methods=['POST','GET'])
def test():

    token = request.args.get('token')
    print(token)
    if verify_token(token) == 1:
        return 'login_success'
    else:
        return 'login_error'


if __name__ == '__main__':
    app.run(debug=True)


