from flask import Flask
from flask import render_template
from main import Recommendations

app = Flask(__name__)

@app.route('/', methods = ['GET'])
def show_response():
    rec = Recommendations()
    return render_template('home.html', rec = rec)

@app.route('/movies', methods = ['GET'])
def search_movies():
    rec = Recommendations()
    return render_template('search.html', rec = rec)

if __name__ == '__main__':
    app.run(debug = True)
