from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from .models import Division, Employee
from .serializers import DivisionSerializer, EmployeeSerializer
import os

def upload_photo(request):
    if request.method == 'POST' and request.FILES.get('photo'):
        photo = request.FILES['photo']
        fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'assets/photos'))
        filename = fs.save(photo.name, photo)
        file_url = fs.url(f'assets/photos/{filename}')
        return JsonResponse({'url': file_url}, status=201)
    return JsonResponse({'error': 'Invalid request'}, status=400)

class DivisionViewSet(viewsets.ModelViewSet):
    queryset = Division.objects.all()
    serializer_class = DivisionSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    parser_classes = (MultiPartParser, FormParser)  # Для обработки файлов

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)  # Частичное обновление
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()
    
    def destroy(self, request, *args, **kwargs):
        """Удаление сотрудника"""
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()