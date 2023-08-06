# -*- coding:utf-8 -*-
from __future__ import division, unicode_literals
from xyz_restful.mixins import UserApiMixin
from xyz_util.statutils import do_rest_stat_action, using_stats_db
from rest_framework.response import Response

__author__ = 'denishuang'

from . import models, serializers
from rest_framework import viewsets, decorators, status
from xyz_restful.decorators import register, register_raw


@register()
class ProjectViewSet(viewsets.ModelViewSet):
    queryset = models.Project.objects.all()
    serializer_class = serializers.ProjectSerializer
    filter_fields = {
        'id': ['in', 'exact'],
    }
    search_fields = ('name',)


@register()
class SubjectViewSet(viewsets.ModelViewSet):
    queryset = models.Subject.objects.all()
    serializer_class = serializers.SubjectSerializer
    filter_fields = {
        'id': ['in', 'exact'],
    }
    search_fields = ('name',)


@register()
class SessionViewSet(viewsets.ModelViewSet):
    queryset = models.Session.objects.all()
    serializer_class = serializers.SessionSerializer
    filter_fields = {
        'id': ['in', 'exact'],
    }
    search_fields = ('name',)


@register()
class CategoryViewSet(UserApiMixin, viewsets.ModelViewSet):
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer
    filter_fields = {
        'id': ['in', 'exact'],
        'project': ['exact'],
        'name': ['exact']
    }
    search_fields = ('name',)

    @decorators.detail_route(['GET'])
    def rank(self, request, pk):
        category = self.get_object()
        points = self.paginate_queryset(category.points.filter(session=category.project.sessions.last()).order_by('-value'))
        return Response(dict(
            category=serializers.CategorySerializer(category).data,
            points=serializers.PointSerializer(points, many=True).data
        ))

@register()
class PointViewSet(UserApiMixin, viewsets.ModelViewSet):
    queryset = models.Point.objects.all()
    serializer_class = serializers.PointSerializer
    filter_fields = {
        'id': ['in', 'exact'],
        'user': ['in']
    }

@register()
class ItemViewSet(UserApiMixin, viewsets.ModelViewSet):
    queryset = models.Item.objects.all()
    serializer_class = serializers.ItemSerializer
    filter_fields = {
        'id': ['in', 'exact'],
        'user': ['in']
    }

