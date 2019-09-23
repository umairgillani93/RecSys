from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

name_list = []

class Names(Resource):
    def get(self, name):
        for existing_name in name_list:
            if existing_name['name'] == name:
                return name
        return {'name': None}

    def post(self, name):
        add_name = {'name': name}
        name_list.append(add_name)

        return name_list

    def delete(self, name):
        for index, existing_name in enumerate(name_list):
            if existing_name['name'] == name:
                deleted_name = name_list.pop(index)
                return  {'Note': 'Delete success!'}

        print ({'Response': "Here's your updated list:"})
        return name_list

class AllNames(Resource):
    def get(self):
        return {'Names': name_list}

# adding resources and binding them to urls
api.add_resource(Names, '/showname/<string:name>')
api.add_resource(AllNames, '/names')

# running the server
if __name__ == '__main__':
    app.run(debug = True)
