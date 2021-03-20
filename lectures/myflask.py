from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello Flask world!'

@app.route('/user/<username>')
def show_user_profile(username):
    return 'User {}'.format(username)

@app.route('/template/<username>')
def show_template(username):
    return render_template('hello.html', name=username)


if __name__ == '__main__':
    app.debug = True
    app.run(port=8000)

#hello.html
"""
<!doctype html>
<title>Hello from Flask</title>
{% if name %}
  <h1>Hello {{ name }}!</h1>
{% else %}
  <h1>Hello World!</h1>
{% endif %}
"""