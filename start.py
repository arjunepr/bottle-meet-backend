from bottle import Bottle, run, response, request, template
from json import dumps as jdumps
from db import DatabaseConnection
import atexit

app = Bottle()

DBConn=DatabaseConnection('db');

def cleanup():
    conn=DBConn.get_conn()
    if conn:
        conn.close()

atexit.register(cleanup)

@app.route('/hello-world')
def hello():
    response.content_type='application/json'
    ret_val=jdumps({ 'message': "Hello World" })
    return ret_val

@app.route('/hello/<name>')
def greet(name='Stranger'):
    response.content_type='application/json'
    ret_message='Hellllllow {name}'.format(name=name)
    return jdumps({ 'visitor':name, 'message': ret_message })
    # return template("Helloww {{name}}, how are you?", name=name)

@app.get('/login')
def login():
    file=open("login_form.html")
    form_string=file.read()
    file.close()
    return form_string

@app.post('/register')
def do_register():
    username=request.forms.get('username')
    password=request.forms.get('password')
    password_confirm=request.forms.get('password_confirm')


# @app.post('/post')
# def login

if __name__ == "__main__":
    run(app, host='localhost', port=8080, debug=True, reloader=True)
