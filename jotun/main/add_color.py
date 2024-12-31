import os
import django
import csv

# تحديد إعدادات Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "jotun.settings")

# تهيئة Django
django.setup()

# استيراد نموذج Color بعد تهيئة Django
from main.models import Color

# تحديد مسار الملف CSV
csv_file_path = r'C:\Users\rf\Desktop\python\Jotun\576_exterior_colours_with_hex.csv'

# فتح الملف وقراءته
with open(csv_file_path, mode='r', newline='', encoding='utf-8') as file:
    csv_reader = csv.DictReader(file)
    
    # المرور عبر كل سطر في الملف وإضافة الألوان إلى قاعدة البيانات
    for row in csv_reader:
        # إنشاء أو تحديث السجل في قاعدة البيانات
        color, created = Color.objects.get_or_create(
            number=row['Colour Number'], 
            name=row['Colour Name'], 
            hex_value=row['Hex']
        )
        if created:
            print(f"تم إضافة اللون: {row['Colour Name']} ({row['Colour Number']})")
        else:
            print(f"اللون {row['Colour Name']} موجود بالفعل.")
