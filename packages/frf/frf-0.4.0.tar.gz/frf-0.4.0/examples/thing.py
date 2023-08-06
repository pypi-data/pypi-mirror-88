import uvicorn
from frf import Resource
from frf import get_asgi_application


class Thing(Resource):

    async def retrieve(self, resource_id: int):
        return {
            "thing_id": resource_id,
            "message": "Hello world!"
        }

    async def list(self):
        return [
            {"message": "First item in a list of Thing!"},
            {"message": "Second item in a list of Thing!"},
        ]


if __name__ == '__main__':
    app = get_asgi_application(allowed_hosts=['*'])
    app.add_resource(Thing)
    uvicorn.run(app, host="127.0.0.1", port=8000)
