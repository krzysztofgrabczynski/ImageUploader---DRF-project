from abc import ABC, abstractstaticmethod
from rest_framework import status
from rest_framework.response import Response


class BaseTierClass(ABC):
    """
    Abstract class representing a tiers.
    Abstract static method `get_response` needs to be overridden by subclasses.
    Method `class_name` gives tier name as permission gropu names.
    """

    @abstractstaticmethod
    def get_response(serializer):
        pass

    @classmethod
    def class_name(cls):
        return cls.__name__.replace("Tier", "")


class BasicTier(BaseTierClass):
    @staticmethod
    def get_response(serializer):
        return Response("basic", status=status.HTTP_201_CREATED)


class PremiumTier(BaseTierClass):
    @staticmethod
    def get_response(serializer):
        return Response("premium", status=status.HTTP_201_CREATED)


class EnterpriseTier(BaseTierClass):
    @staticmethod
    def get_response(serializer):
        return Response("enteprise", status=status.HTTP_201_CREATED)
