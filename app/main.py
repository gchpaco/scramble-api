from flask import Flask, render_template, request
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
import random
import collections

admin_users = {
    'admin': generate_password_hash('admin')
}

request_logs = collections.deque([], 10)
Request = collections.namedtuple("Request", ['api', 'input', 'output'])

app = Flask(__name__)
auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(username, password):
    if username in admin_users and check_password_hash(admin_users.get(username), password):
        return username
    else:
        return None

def do_scramble(s):
    as_list = list(s)
    random.shuffle(as_list)
    return ''.join(as_list)

@app.route("/")
def top():
    return render_template('main.html')

@app.get("/v1/scramble")
def scramble_get():
    return top()

@app.post("/v1/scramble")
def scramble():
    input = request.form['scramble']
    output = do_scramble(input)
    request_logs.append(Request('/v1/scramble', input, output))
    return render_template('scrambled.html', scramble=output)

@app.get("/v1/audit")
@auth.login_required
def audit_logs():
    result = render_template('audit_logs.html', logs=request_logs)
    request_logs.append(Request('/v1/audit', None, None))
    return result

if __name__ == "__main__":
    app.run(host='0.0.0.0')
