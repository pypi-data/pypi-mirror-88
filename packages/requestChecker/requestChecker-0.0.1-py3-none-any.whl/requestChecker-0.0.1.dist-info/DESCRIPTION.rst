Request Checker
===============

Flask module allowing to configure and centralize the authorizations on
the routes.

Exemple
-------

::

    from flask import Flask
    from flask_restful import Api, Resource
    from RequestChecker import RequestChecker, Path, SecurityPolicyEnum, MethodsEnum

    app = Flask("test")
    api = Api(app)

    requestChecker = RequestChecker(api)

    def LoginResource(Resource):
        def post(self):
            pass

    def TestResource(Resource):
        def get(self):
            pass

        def post(self):
            pass

    pathLogin = Path('/login', policy=SecurityPolicyEnum.ANNONYMOUS, methods=[MethodsEnum.POST])
    pathTest = Path('/test', policy=SecurityPolicyEnum.JWT, methods=[MethodsEnum.GET, MethodsEnum.POST])

    requestChecker.addPath(pathTest, TestResource)
    requestChecker.addPath(pathLogin, LoginResource)

Dependencies
------------

`Flask <https://github.com/pallets/flask>`__
`flask\_jwt\_extended <https://github.com/vimalloc/flask-jwt-extended>`__
`werkzeug <https://github.com/pallets/werkzeug>`__
`Flask-Restful <https://github.com/flask-restful/flask-restful>`__


