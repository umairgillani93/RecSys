from flask import Flask
from flask_restful import Resource, Api
from RecPackage import recsys1
from flask import render_template

app = Flask(__name__)
api = Api(app)

class Recommendations(Resource):
    def get(self):
        try:
            myfunc = recsys1.MovieChoice('Penitentiary (1979)')
            myfunc = myfunc.to_dict('list')

            return myfunc
        except:
            return {'Note': 'Movie Not Found!'}

api.add_resource(Recommendations, '/')

if __name__ == '__main__':
    app.run(debug = True)
