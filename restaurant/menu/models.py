from django.db import models
from django.contrib.auth.models import User

class Seller(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name
    
class Menu(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    CATEGORY_CHOICES = [
        ('อาหารคาว', 'อาหารคาว'),
        ('ของหวาน', 'ของหวาน'),
        ('เครื่องดื่ม', 'เครื่องดื่ม'),
    ]
    
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='อาหารคาว')
    image = models.ImageField(upload_to='menu_images/')
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=[('เปิด', 'เปิด'), ('ปิด', 'ปิด')], default='เปิด')

    def __str__(self):
        return self.name

class Orders(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    order_date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # คำนวณยอดรวมราคาจากจำนวนและราคาของเมนู
        self.total_price = self.menu.price * self.quantity
        super().save(*args, **kwargs)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
  

    def __str__(self):
        return self.user.username

class Sale(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    amount = models.IntegerField()
    sale_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.menu.name} - {self.amount}"
    
from django.db import models

class Table(models.Model):
    table_number = models.PositiveIntegerField(unique=True)
    is_reserved = models.BooleanField(default=False)

    def __str__(self):
        return f"โต๊ะ {self.table_number}"

class TableReservation(models.Model):
    table = models.OneToOneField(Table, on_delete=models.CASCADE, default=1)  # ใช้ 1 เป็นค่าเริ่มต้น
    customer_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    reservation_date = models.DateField()
    reservation_time = models.TimeField()
    number_of_people = models.PositiveIntegerField()

    def __str__(self):
        return f"โต๊ะที่ {self.table.table_number} - {'จองแล้ว' if self.table.is_reserved else 'ว่าง'}"