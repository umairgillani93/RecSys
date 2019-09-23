from flask import Flask
from flask import render_template
from main import Recommendations


app = Flask(__name__)

@app.route('/movies')
def show_response():
    rec = Recommendations()
    return render_template('home.html', rec = rec)

if __name__ == '__main__':
    app.run(debug = True)
