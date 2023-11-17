from flask import Flask, request
from flask_restful import Api, Resource, reqparse
from testGetBD import getRequest, getRequest2

app = Flask(__name__)
api = Api(app)


class HelloWorld(Resource):
    def get(self):
        data = request.args.get('data')
        id = data
        res = getRequest2(id)[0]
        content = res[1]
        return {'message': content}

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True)
        parser.add_argument('age', type=int, required=True)
        args = parser.parse_args()

        name = args['name']
        age = args['age']

        res = name + str(age)
        return res


api.add_resource(HelloWorld, '/hello')

if __name__ == '__main__':
    app.run()

