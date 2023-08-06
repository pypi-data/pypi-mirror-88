from typing import Type

from django.db import models
from rest_framework import serializers

__all__ = (
    "PkModelFieldDoesNotExist",
    "PkModelFieldIsNotForRead",
    "PkModelField",
)


class PkModelFieldDoesNotExist(Exception):
    def __init__(self, model, pk):
        self.model = model
        self.msg = '"{model_class}"에서 pk={pk}인 인스턴스를 찾을 수 없습니다'.format(
            model_class=model.__class__.__name__, pk=pk
        )

    def __str__(self):
        return self.msg


class PkModelFieldIsNotForRead(Exception):
    def __str__(self):
        return "PkModelField는 생성시에만 사용할 수 있습니다"


class PkModelField(serializers.Field):
    """
    특정 Model의 instance를 나타내는 Field
    주어지는 데이터가
        dict
            {'pk': 1} 또는 {'id': 1}
        literal (pk가 될 수 있는 숫자/문자 등의 고정 값)
            1, '1'
    과 같은 여러 형태일 때 전부 처리해주도록 한다

    * 생성시에만 사용한다
    """

    def __init__(self, model: Type[models.Model], *args, **kwargs):
        """
        :param model: Model class
        :param kwargs:
        """
        if not issubclass(model, models.Model):
            raise ValueError('PkModelField의 "model"인수에는 Django Model의 자식클래스가 전달되어야합니다')

        self.model = model
        super().__init__(*args, **kwargs)

    def to_internal_value(self, data):
        if not isinstance(data, self.model):
            if hasattr(data, "get"):
                pk = (
                    data.get("id")
                    or data.get("pk")
                    or data.get(self.model._meta.pk.attname, data)
                )
            else:
                pk = data

            try:
                return self.model.objects.get(pk=pk)
            except self.model.DoesNotExist:
                raise PkModelFieldDoesNotExist(self.model, pk)
        return data

    def to_representation(self, value):
        raise PkModelFieldIsNotForRead()
