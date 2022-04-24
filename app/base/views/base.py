from __future__ import annotations

from typing import Type

from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from rest_framework import exceptions, serializers
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import set_rollback

from app.base.exceptions import *
from app.base.permissions.base import BasePermission
from app.base.schemas.mixins import SerializerSchemaMixin, ViewSchemaMixin
from app.base.serializers.base import EmptySerializer
from app.base.utils.common import status_by_method
from app.base.utils.schema import extend_schema

__all__ = ['BaseView']

_TypeSerializer = Type[serializers.Serializer]
_TypePermission = Type[BasePermission]


def _exception_handler(exception):
    try:
        set_rollback()
        if settings.DEBUG and isinstance(exception, MethodNotAllowed):
            return Response(str(exception))
        try:
            raise exception
        except APIWarning as e:
            api_error = e
        except ClientError as e:
            api_error = e
        except CriticalError as e:
            api_error = e
        except tuple(APIWarning.EXCEPTION__CAST.keys()) as exception_to_cast:
            api_error = APIWarning.cast_exception(exception_to_cast)
        except tuple(ClientError.EXCEPTION__CAST.keys()) as exception_to_cast:
            api_error = ClientError.cast_exception(exception_to_cast)
        except tuple(CriticalError.EXCEPTION__CAST.keys()) as exception_to_cast:
            api_error = CriticalError.cast_exception(exception_to_cast)
        
        error = api_error
    
    except Exception as e:
        error = CriticalError(str(e))
    
    error.log()
    return error.to_response()


class BaseView(GenericAPIView):
    lookup_field = 'id'
    ordering = 'id'
    serializer_class = EmptySerializer
    serializer_class_map: dict[str, tuple[int, _TypeSerializer] | _TypeSerializer] = {}
    permission_classes_map: dict[str, list[_TypePermission] | tuple[_TypePermission]] = {}
    
    @property
    def method(self) -> str:
        return self.request.method.lower()
    
    @classmethod
    def _extract_serializer_class_with_status(
        cls, method_name: str
    ) -> tuple[int, _TypeSerializer] | None:
        serializer_class = cls.serializer_class_map.get(method_name)
        if serializer_class and issubclass(serializer_class, serializers.Serializer):
            status = status_by_method(method_name)
            return status, serializer_class
        return serializer_class
    
    def get_serializer_class(self):
        serializer_class = self._extract_serializer_class_with_status(self.method)
        if serializer_class is None:
            return self.serializer_class
        return serializer_class[1]
    
    def get_permissions(self):
        permission_classes = self.permission_classes_map.get(self.method)
        if permission_classes is None:
            return super().get_permissions()
        if isinstance(permission_classes, list):
            permission_classes = self.permission_classes + permission_classes
        return [p() for p in permission_classes]
    
    @classmethod
    def _to_schema(cls) -> None:
        for method_name in cls.http_method_names:
            try:
                method = getattr(cls, method_name)
            except AttributeError:
                continue
            responses = {}
            
            extracted = cls._extract_serializer_class_with_status(method_name)
            if extracted:
                serializer_class = extracted[1]
                if issubclass(serializer_class, SerializerSchemaMixin):
                    responses |= serializer_class.to_schema(extracted[0])
            
            if issubclass(cls, ViewSchemaMixin):
                responses |= cls.to_schema()
            
            setattr(cls, method_name, extend_schema(responses=responses)(method))
    
    @classmethod
    def as_view(cls, **initkwargs):
        cls._to_schema()
        return csrf_exempt(super().as_view(**initkwargs))
    
    def handle_exception(self, exception):
        return _exception_handler(exception)
    
    def permission_denied(self, request, message=None, code=None):
        if request.authenticators and not request.successful_authenticator:
            getattr(request, 'on_auth_fail', lambda: None)()
            raise exceptions.NotAuthenticated()
        raise exceptions.PermissionDenied(detail=message, code=code)
