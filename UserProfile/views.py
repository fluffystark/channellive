# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import viewsets
from UserProfile.models import Business
from UserProfile.serializers import BusinessSerializer


class BusinessViewSet(viewsets.ModelViewSet):
    queryset = Business.objects.all()
    serializer_class = BusinessSerializer
