from wsgiref.util import FileWrapper

from django.http import HttpResponse
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.management import call_command

from freight_terminal.settings import DATABASE_BACKUP_FILENAME


class BackupdDBAPIView(APIView):
    def post(self, request, *args, **kwargs):
        call_command('dumpdata', '-o', DATABASE_BACKUP_FILENAME)
        return Response()


class RestoreDBAPIView(APIView):
    def post(self, request, *args, **kwargs):
        call_command('loaddata', DATABASE_BACKUP_FILENAME)
        return Response()
