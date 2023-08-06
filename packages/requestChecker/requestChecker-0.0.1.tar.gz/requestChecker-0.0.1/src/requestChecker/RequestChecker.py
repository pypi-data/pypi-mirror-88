from typing import List
from flask_jwt_extended import JWTManager, verify_jwt_in_request
from werkzeug.exceptions import abort
from flask import Flask, request
from flask_restful import Api, Resource
from .MethodsEnum import MethodsEnum
from .SecurityPolicyEnum import SecurityPolicyEnum
from .Path import Path


class RequestChecker:
    def __init__(self, app):
        self.__paths: List[Path] = list()
        if type(app) == Api:
            self.__app: Flask = app.app
            self.__api: Api = app
        elif type(app) == Flask:
            self.__app: Flask = app
            self.__api: Api = None
        else:
            raise Exception("app is not an Api or a Flask object")

        self.__jwtManager = JWTManager(self.__app)

        if self.__app is not None:
            self.__app.before_request(self.__checkPath)

    def __checkPath(self):
        found = False
        policy = None

        url = request.url
        method = request.method

        for path in self.__paths:
            if path.getUrl() in url:
                cond_methodPath = method in path.getMethods()
                cond_methodAll = path.getMethods() == [MethodsEnum.ALL]
                if cond_methodPath or cond_methodAll:
                    found = True
                    policy = path.getPolicy()
                    break

        if found:
            if policy == SecurityPolicyEnum.JWT:
                try:
                    verify_jwt_in_request()
                except Exception as e:
                    print(e)
                    abort(403)
        else:
            abort(404)

    def getApp(self) -> Flask:
        return self.__app

    def getApi(self) -> Api:
        return self.__api

    def getPaths(self) -> List[Path]:
        return self.__paths

    def addPath(self, path: Path, resource: Resource = None):
        if path not in self.__paths:
            self.__paths.append(path)
            if self.__api is not None:
                self.__api.add_resource(resource, path.getUrl())

    def getJwtManager(self) -> JWTManager:
        return self.__jwtManager
