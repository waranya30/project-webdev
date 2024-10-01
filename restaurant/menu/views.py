
from django.shortcuts import render, redirect
from .models import Menu,  Profile, Sale
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Menu, Profile
from .models import Sale, Menu
from django.db.models import Sum
from django.utils import timezone
import calendar
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth import views as auth_views
from .forms import CustomLoginForm
from .forms import OrderForm, TableReservationForm
from django.shortcuts import render, redirect, get_object_or_404
from .models import TableReservation, Table

def order_and_reserve(request):
    order_form = OrderForm()
    reservation_form = TableReservationForm()

    if request.method == 'POST':
        if 'order' in request.POST:
            order_form = OrderForm(request.POST)
            if order_form.is_valid():
                order_form.save()
                messages.success(request, 'สั่งอาหารเรียบร้อยแล้ว!')
                return redirect('order_and_reserve')
        elif 'reserve' in request.POST:
            reservation_form = TableReservationForm(request.POST)
            if reservation_form.is_valid():
                reservation = reservation_form.save()
                # อัปเดตสถานะโต๊ะให้เป็นจองแล้ว
                table = reservation.table
                table.is_reserved = True
                table.save()
                messages.success(request, 'จองโต๊ะเรียบร้อยแล้ว!')
                return redirect('reservation_detail', reservation_id=reservation.id)

    # ดึงข้อมูลเมนูและโต๊ะทั้งหมด
    menus = Menu.objects.filter(status='เปิด')
    tables = Table.objects.all()
    return render(request, 'order_and_reserve.html', {
        'order_form': order_form,
        'reservation_form': reservation_form,
        'menus': menus,
        'tables': tables,
    })
def reservation_detail(request, reservation_id):
    reservation = get_object_or_404(TableReservation, id=reservation_id)
    return render(request, 'reservation_detail.html', {'reservation': reservation})

def reserve_table(request):
    if request.method == 'POST':
        form = TableReservationForm(request.POST)
        if form.is_valid():
            # บันทึกข้อมูลการจอง
            reservation = form.save()
            messages.success(request, 'จองโต๊ะเรียบร้อยแล้ว!')
            # รีไดเร็กไปยังหน้ารายละเอียดการจอง โดยใช้ reservation.id
            return redirect('reservation_detail', reservation_id=reservation.id)
    else:
        form = TableReservationForm()

    return render(request, 'reserve_table.html', {'form': form})

def reservation_detail(request, reservation_id):
    # ดึงข้อมูลการจองจากฐานข้อมูล
    reservation = get_object_or_404(TableReservation, id=reservation_id)
    return render(request, 'reservation_detail.html', {'reservation': reservation})


def order_food(request):
    order_form = OrderForm()

    if request.method == 'POST':
        order_form = OrderForm(request.POST)
        if order_form.is_valid():
            order_form.save()
            messages.success(request, 'สั่งอาหารเรียบร้อยแล้ว')
            return redirect('order_food')

    # ดึงข้อมูลเมนูที่เปิดอยู่เพื่อแสดงผลในหน้าเว็บ
    menus = Menu.objects.filter(status='เปิด')
    return render(request, 'order_food.html', {
        'order_form': order_form,
        'menus': menus,
    })
class CustomLoginView(auth_views.LoginView):
    form_class = CustomLoginForm
    template_name = 'registration/login.html'

def login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"ยินดีต้อนรับ {username}")
                return redirect('home')  # เปลี่ยนเป็น URL ของหน้าหลักที่คุณต้องการให้ผู้ใช้เข้า
            else:
                messages.error(request, "ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง")
        else:
            messages.error(request, "กรุณากรอกข้อมูลให้ถูกต้อง")
    else:
        form = CustomLoginForm()

    return render(request, 'registration/login.html', {'form': form})
class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        label="ชื่อผู้ใช้",
        help_text="กรุณากรอกชื่อผู้ใช้ที่มีไม่เกิน 150 ตัวอักษร และสามารถใช้ตัวอักษร, ตัวเลข และเครื่องหมาย @/./+/-/_",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password1 = forms.CharField(
        label="รหัสผ่าน",
        help_text="""
            <ul>
                <li>รหัสผ่านต้องไม่เหมือนกับข้อมูลส่วนตัวของคุณ</li>
                <li>รหัสผ่านต้องมีอย่างน้อย 8 ตัวอักษร</li>
                <li>รหัสผ่านต้องไม่เป็นรหัสที่ใช้งานทั่วไป</li>
                <li>รหัสผ่านต้องไม่ประกอบด้วยตัวเลขทั้งหมด</li>
            </ul>
        """,
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    password2 = forms.CharField(
        label="ยืนยันรหัสผ่าน",
        help_text="กรุณากรอกรหัสผ่านอีกครั้งเพื่อยืนยัน",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

@login_required
def my_sales(request):
    current_year = timezone.now().year
    current_month = timezone.now().month
    current_month_name = calendar.month_name[current_month]  # ใช้เพื่อแปลงเดือนเป็นชื่อเต็มภาษาอังกฤษ
    # หากต้องการแสดงผลเป็นภาษาไทย
    month_names_th = ["", "มกราคม", "กุมภาพันธ์", "มีนาคม", "เมษายน", "พฤษภาคม", "มิถุนายน", "กรกฎาคม", "สิงหาคม", "กันยายน", "ตุลาคม", "พฤศจิกายน", "ธันวาคม"]
    current_month_name = month_names_th[current_month]

    menus = Menu.objects.all()

    # เตรียมข้อมูลยอดขายของเดือนปัจจุบัน
    monthly_sales_data = {'labels': [], 'data': []}
    for menu in menus:
        # ดึงยอดขายเฉพาะเดือนปัจจุบัน
        sales = Sale.objects.filter(menu=menu, sale_date__year=current_year, sale_date__month=current_month).aggregate(total=Sum('amount'))['total'] or 0
        monthly_sales_data['labels'].append(menu.name)
        monthly_sales_data['data'].append(float(sales))

    # เตรียมข้อมูลสำหรับแสดงในตารางยอดขายรวม
    sales_data = []
    for menu in menus:
        total_sales = Sale.objects.filter(menu=menu).aggregate(total_sales=Sum('amount'))['total_sales'] or 0
        sales_data.append({'menu': menu, 'total_sales': total_sales})

    return render(request, 'my_sales.html', {
        'monthly_sales_data': monthly_sales_data,
        'sales_data': sales_data,
        'year': current_year,
        'month': current_month_name
    })


def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)  # สร้างโปรไฟล์ให้ผู้ใช้ใหม่
            messages.success(request, 'สมัครสมาชิกเรียบร้อยแล้ว')
            return redirect('menu_list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

@login_required
def add_menu(request):
    print("Current User: ", request.user)  # แสดงผู้ใช้ที่ล็อกอินอยู่
    if request.method == 'POST':
        name = request.POST.get('menu_name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        category = request.POST.get('category')
        image = request.FILES.get('image')  # ตรวจสอบว่ามีการอัปโหลดไฟล์รูปภาพหรือไม่
        seller = request.user  # ใช้ผู้ใช้ที่ล็อกอินเป็นผู้ขาย

        # ตรวจสอบว่าเมนูมีข้อมูลครบถ้วน
        if not name or not price or not category:
            messages.error(request, 'กรุณากรอกข้อมูลให้ครบถ้วน')
            return render(request, 'add_menu.html')  # คืนค่ากลับไปที่ฟอร์ม

        # สร้างเมนูใหม่
        Menu.objects.create(
            name=name,
            description=description,
            price=price,
            category=category,
            image=image,
            seller=seller  # ค่าที่จะถูกบันทึกที่นี่
        )

        messages.success(request, 'เพิ่มเมนูเรียบร้อยแล้ว')
        return redirect('menu_list')  # เปลี่ยนเส้นทางไปยังหน้าดูรายการเมนู

    return render(request, 'add_menu.html')

   

@login_required
def menu_list(request):
    menus = Menu.objects.all()  # ดึงข้อมูลเมนูทั้งหมดจากฐานข้อมูล
    return render(request, 'menu_list.html', {'menus': menus})

@login_required
def edit_menu(request, menu_id):
    try:
        menu = Menu.objects.get(id=menu_id)
    except Menu.DoesNotExist:
        messages.error(request, 'ไม่พบเมนูที่ต้องการแก้ไข')
        return redirect('menu_list')

    if request.method == 'POST':
        menu.name = request.POST['name']
        menu.description = request.POST['description']
        menu.price = request.POST['price']
        menu.category = request.POST['category']
        
        if 'image' in request.FILES:
            menu.image = request.FILES['image']
        
        menu.save()
        messages.success(request, 'แก้ไขเมนูเรียบร้อยแล้ว')
        return redirect('menu_list')

    return render(request, 'edit_menu.html', {'menu': menu})


@login_required
def delete_menu(request, menu_id):
    try:
        menu = Menu.objects.get(id=menu_id)
        menu.delete()
        messages.success(request, 'เมนูถูกลบเรียบร้อยแล้ว')
    except Menu.DoesNotExist:
        messages.error(request, 'ไม่พบเมนูที่ต้องการลบ')
    return redirect('menu_list')





def home(request):
    menus = Menu.objects.all()  # ดึงเมนูทั้งหมดจากฐานข้อมูล
    return render(request, 'home.html', {'menus': menus})

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username']


@login_required
def profile(request):
    if request.method == 'POST':
        new_username = request.POST.get('username')
        if new_username:
            request.user.username = new_username
            request.user.save()
            return redirect('profile')  # เปลี่ยนเป็น URL ของหน้าโปรไฟล์

    return render(request, 'profile.html')

@login_required
def edit_profile(request):
    if request.method == 'POST':
        new_username = request.POST.get('username')

        # ตรวจสอบว่าชื่อผู้ใช้มีการเปลี่ยนแปลงและไม่ซ้ำกับผู้ใช้คนอื่น
        if new_username and request.user.username != new_username:
            if User.objects.filter(username=new_username).exists():
                messages.error(request, 'ชื่อผู้ใช้นี้ถูกใช้แล้ว')
            else:
                request.user.username = new_username
                request.user.save()
                messages.success(request, 'อัปเดตโปรไฟล์เรียบร้อยแล้ว')
                return redirect('profile')

    return render(request, 'edit_profile.html')
