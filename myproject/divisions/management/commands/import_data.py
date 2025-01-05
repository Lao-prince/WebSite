import json
from django.core.management.base import BaseCommand
from divisions.models import Division, Employee
from datetime import datetime

class Command(BaseCommand):
    help = 'Импортирует данные для разделов и сотрудников'

    def handle(self, *args, **kwargs):
        # Загрузка данных для разделов
        with open('divisions.json', 'r', encoding='utf-8') as f:
            divisions_data = json.load(f)

        # Загрузка данных для сотрудников
        with open('employees.json', 'r', encoding='utf-8') as f:
            employees_data = json.load(f)

        # Очистка текущих данных и добавление новых
        Division.objects.all().delete()  # Удалим все текущие записи, если нужно

        # Добавление данных для подразделений
        for division in divisions_data:
            parent = Division.objects.filter(id=division['parent_id']).first() if division['parent_id'] else None
            Division.objects.create(
                id=division['id'],
                name=division['name'],
                parent=parent
            )

        # Добавление данных для сотрудников
        for employee in employees_data:
            division = Division.objects.get(id=employee['division_id'])
            Employee.objects.create(
                id=employee['id'],
                full_name=employee['full_name'],
                position=employee['position'],
                birth_date=datetime.strptime(employee['birth_date'], '%Y-%m-%d').date(),
                start_date=datetime.strptime(employee['start_date'], '%Y-%m-%d').date(),
                photo=employee['photo'],
                division=division
            )

        self.stdout.write(self.style.SUCCESS('Данные успешно загружены в базу данных!'))
