from rest_framework import serializers
from .models import Division, Employee

class DivisionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Division
        fields = '__all__'

class EmployeeSerializer(serializers.ModelSerializer):
    division = serializers.PrimaryKeyRelatedField(queryset=Division.objects.all())
    
    class Meta:
        model = Employee
        fields = '__all__'

    def update(self, instance, validated_data):
        # Обработка загрузки фото
        photo = validated_data.pop('photo', None)
        if photo:
            instance.photo.delete(save=False)  # Удаление старого фото, если есть
            instance.photo = photo

        # Обновление остальных полей
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance
