# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework import exceptions
from rest_framework.decorators import action
from rest_framework.response import Response


class AllMixin(object):
    """
        Not paging Mixin
    """
    LIMIT = 2000
    @action(methods=['get'], detail=False)
    def all(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        if queryset.count() > self.LIMIT:
            raise exceptions.ValidationError('Too much data to get %s data at once. Please do paging for this situation' % self.LIMIT)

        serializer = self.get_serializer(queryset, many=True)

        return Response({'detail': serializer.data})


class CustomSetFieldMixin(object):
    """
    set a filed value
    """
    FIELD_NAME = 'field'
    FIELDS_NAME = 'fields'

    @action(methods=['post'], detail=True)
    def set_field(self, request, *args, **kwargs):
        value = request.data.get(self.ACTIVE_FIELD_NAME)
        instance = self.get_object()
        setattr(instance, self.ACTIVE_FIELD_NAME, value)
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(methods=['post'], detail=True)
    def set_many_field(self, request, *args, **kwargs):
        """
        set many field value exclude pk field
        """
        fields = request.data.get(self.FIELD_NAME)
        if not isinstance(fields, dict):
            raise exceptions.ValidationError('data type error')
        instance = self.get_object()
        for key, value in fields.items():
            if hasattr(instance, key):
                setattr(instance, key, value)
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

