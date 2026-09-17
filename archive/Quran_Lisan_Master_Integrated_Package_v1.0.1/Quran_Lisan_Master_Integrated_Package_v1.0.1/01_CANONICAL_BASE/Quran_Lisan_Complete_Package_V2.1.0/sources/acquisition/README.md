# اقتناء النص المرجعي

الحزمة لا توزع نص Tanzil نفسه. يستخدم `scripts/acquire_tanzil.py` للتنزيل إلى staging (منطقة مؤقتة)، ثم يتحقق `scripts/validate_tanzil.py` من الاسم والحجم وSHA-256 وعدد الأسطر قبل السماح بنقله إلى مجلد بيانات المشروع.

المصدر الرسمي: https://tanzil.net/download/  
الإصدار المقيد: Uthmani 1.1 / Hafs an Asim.  
لا يطبق Unicode normalization أو أي تعديل على bytes المرجعية.
