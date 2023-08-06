from typing import List
from .SecurityPolicyEnum import SecurityPolicyEnum
from .MethodsEnum import MethodsEnum


class Path:
    def __init__(
        self,
        url: str,
        methods: List[MethodsEnum] = [MethodsEnum.ALL],
        policy: SecurityPolicyEnum = SecurityPolicyEnum.ANNONYMOUS
    ):
        self.__url = url
        self.__policy = policy
        self.__methods = methods

    def getUrl(self) -> str:
        return self.__url

    def getPolicy(self) -> SecurityPolicyEnum:
        return self.__policy

    def getMethods(self) -> List[MethodsEnum]:
        return self.__methods
