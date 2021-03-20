#sudo pip install bottle 
from bottle import route, run, template

@route('/hello')
def hello():
    return "Hello World!"

@route('/')
@route('/hello/<name>')
def greet(name='Stranger'):
    return template('Hello {{name}}, how are you?', name=name)

if __name__ == '__main__':
    run(host='localhost', port=8000, debug=True)