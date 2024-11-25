import pandas as pd
import matplotlib.pyplot as plt
from django.shortcuts import render, redirect
from django.db import connection
from my_dashboard.forms import LoginForm
from django.contrib.auth import login, logout, authenticate
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from io import BytesIO
import base64
from django.http import JsonResponse
from django.contrib.auth.models import User
from .decorators import admin_only
from django.http import JsonResponse 
import json
from django.contrib.auth.decorators import login_required
from .utils import is_ajax, classify_face
from logs.models import Log
from django.core.files.base import ContentFile
from django.contrib.auth.models import User
from profiles.models import Profile
from django.template.loader import get_template
from weasyprint import HTML
from django.http import HttpResponse
from profiles.models import Profile


def graph_generate_sales_growth_chart(df):
    # Agrupar por año y sumar las ventas
    sales_by_year = df.groupby(df['invoice_date'].dt.year)['quantity'].sum().reset_index()
    sales_by_year.columns = ['Year', 'Total Sales']

    # Calcular crecimiento año a año
    sales_by_year['Growth'] = sales_by_year['Total Sales'].pct_change() * 100  # Crecimiento en porcentaje

    # Crear gráfico
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(sales_by_year['Year'], sales_by_year['Total Sales'], marker='o', label='Ventas Totales', color='#489FB5')
    ax.set_xlabel('Año')
    ax.set_ylabel('Ventas Totales')
    ax.grid()
    plt.xticks(sales_by_year['Year'])
    
    # Guardar la imagen en un buffer
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    
    return base64.b64encode(image_png).decode('utf-8')

def calculate_total_sales(df):
    return df['quantity'].sum()

def calculate_retention_rate(df):
    purchase_counts = df['customer_id'].value_counts()
    total_customers = len(purchase_counts)
    retained_customers = (purchase_counts > 1).sum()
    retention_rate = (retained_customers / total_customers) * 100 if total_customers > 0 else 0
    return retention_rate

def graph_generate_category_distribution_chart(df):
    fig, ax = plt.subplots(figsize=(10, 6))
    df.groupby('category')['quantity'].sum().plot(kind='bar', ax=ax, color='#489FB5', edgecolor='black')
    ax.set_xlabel('Categoría')
    ax.set_ylabel('Cantidad')
    plt.tight_layout()

    # Guardar la imagen en un buffer
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    
    return base64.b64encode(image_png).decode('utf-8')


##########################
def plot_employees_by_department(df):
    # Contar el número de empleados por departamento
    employees_by_department = df['department'].value_counts()

    # Crear el gráfico
    fig, ax = plt.subplots(figsize=(10, 6))
    employees_by_department.plot(kind='bar', color='#489FB5', edgecolor='black')
    ax.set_xlabel('Departamento')
    ax.set_ylabel('Cantidad de Empleados')
    plt.tight_layout()
    
    # Guardar la imagen en un buffer
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    
    return base64.b64encode(image_png).decode('utf-8')

def generate_department_chart(df):
    department_counts = df['department'].value_counts()
    fig, ax = plt.subplots(figsize=(10, 6))
    department_counts.plot(kind='bar', color='#6a95b1', ax=ax)
    ax.set_xlabel('Departamento')
    ax.set_ylabel('Cantidad de Empleados')
    plt.tight_layout()
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    return base64.b64encode(image_png).decode('utf-8')

def generate_recruitment_channel_chart(df):
    # Contar la cantidad de empleados por canal de reclutamiento
    recruitment_channel_counts = df['recruitment_channel'].value_counts()
    fig, ax = plt.subplots(figsize=(10, 6))
    recruitment_channel_counts.plot(kind='pie', autopct='%1.1f%%', startangle=90, colors=['#FF8C00', '#6a95b1', '#b16a95'], ax=ax)
    ax.set_ylabel('')  # Eliminar la etiqueta de la y
    plt.tight_layout()

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    return base64.b64encode(image_png).decode('utf-8')

def length_of_service_chart(df):
    fig, ax = plt.subplots(figsize=(10, 6))
    df['length_of_service'].plot(kind='hist', bins=20, color='#489FB5', edgecolor='black', ax=ax)
    ax.set_xlabel('Años de Servicio')
    ax.set_ylabel('Cantidad de Empleados')
    plt.tight_layout()
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    return base64.b64encode(image_png).decode('utf-8')

def quantity_of_active_employees(df):
    return df['employee_id'].count()

def number_of_trainings(df):
    return df['no_of_trainings'].sum()

#####Finanzas

def generate_income_by_category_chart(df):
    df['income'] = df['quantity'] * df['price']
    income_by_category = df.groupby('category')['income'].sum()
    
    # Crear gráfico
    fig, ax = plt.subplots(figsize=(10, 6))
    income_by_category.plot(kind='bar', color='#6a95b1', ax=ax, edgecolor='black')
    ax.set_xlabel('Categoría')
    ax.set_ylabel('Ingresos Totales ($)')
    plt.tight_layout()

    # Guardar la imagen
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    return base64.b64encode(image_png).decode('utf-8')

def generate_payment_method_chart(df):
    df['income'] = df['quantity'] * df['price']
    income_by_payment = df.groupby('payment_method')['income'].sum()

    # Crear gráfico
    fig, ax = plt.subplots(figsize=(10, 6))
    income_by_payment.plot(kind='pie', autopct='%1.1f%%', startangle=90, ax=ax, colors=['#FF8C00','#008af8' , '#6a95b1'])
    ax.set_ylabel('')  # Eliminar la etiqueta de eje Y
    plt.tight_layout()

    # Guardar la imagen
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    return base64.b64encode(image_png).decode('utf-8')

def generate_monthly_sales_chart(df):
    df['income'] = df['quantity'] * df['price']
    monthly_sales = df.groupby(df['invoice_date'].dt.to_period('M'))['income'].sum()

    # Crear gráfico
    fig, ax = plt.subplots(figsize=(10, 6))
    monthly_sales.plot(kind='line', marker='o', color='#489FB5', ax=ax)
    ax.set_xlabel('Mes')
    ax.set_ylabel('Ingresos Totales ($)')
    ax.grid()
    plt.tight_layout()

    # Guardar la imagen
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    return base64.b64encode(image_png).decode('utf-8')

def find_most_profitable_category(df):
    df['income'] = df['quantity'] * df['price']
    return df.groupby('category')['income'].sum().idxmax()

def extract_data_from_database():
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM invoice;')
        invoices = cursor.fetchall()
    
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM hr_report;')
        hr_report = cursor.fetchall()
    
    
    hr_report_list = [{'department': row[1], 'length_of_service': row[5], 'no_of_trainings': row[3], 'recruitment_channel': row[2],'employee_id': row[2]} for row in hr_report]
    
    # Crear la lista de diccionarios para el DataFrame
    invoice_list = [{'category': row[1], 'quantity': row[2], 'customer_id': row[8], 'invoice_date': row[6], 'price': row[4], 'payment_method': row[5]} for row in invoices]
    
    df_invoice = pd.DataFrame(invoice_list)
    df_hr_report = pd.DataFrame(hr_report_list)
    
    df_invoice['invoice_date'] = pd.to_datetime(df_invoice['invoice_date'])
    
    graph_category_chart = graph_generate_category_distribution_chart(df_invoice)
    graph_sales_per_year = graph_generate_sales_growth_chart(df_invoice)
    retention_rate = calculate_retention_rate(df_invoice)
    retention_rate = round(retention_rate, 4) 
    total_sales = calculate_total_sales(df_invoice)
    total_sales = "{:,}".format(total_sales)
    
    # Recursos Humanos
    
    graph_employee_qty_department = plot_employees_by_department(df_hr_report)
    graph_length_of_service_chart = length_of_service_chart(df_hr_report)
    graph_recruitment_channel_chart = generate_recruitment_channel_chart(df_hr_report)
    
    value_active_employees = quantity_of_active_employees(df_hr_report)
    number_trainings = number_of_trainings(df_hr_report)
    
    # Finanzas
    
    graph_income_by_category = generate_income_by_category_chart(df_invoice)
    graph_payment_method = generate_payment_method_chart(df_invoice)
    graph_monthly_sales = generate_monthly_sales_chart(df_invoice)
    
    most_profitable_category = find_most_profitable_category(df_invoice)
    
    context = {
        'Comercial': {
            'graphics': [
                ('category_chart', graph_category_chart, 'Distribución de Categorías'),
                ('sales_per_year', graph_sales_per_year, 'Crecimiento de Ventas')
                
            ],
            'set_values': [
                ('retention_rate', retention_rate, 'Tasa de Retención', '%'),
                ('total_sales', total_sales, 'Ventas Totales', '$')
            ],
            'title': {
                'name': 'Reporte de Comercial',
                'description': 'Análisis de ventas y retención de clientes'
            }
        },
        'RR.HH': {
            'graphics': [
                ('graph_qty_employee', graph_employee_qty_department, 'Distribución de Empleados por Departamento'),
                ('graph_service_year', graph_length_of_service_chart, 'Distribución de Años de Servicio'),
                ('graph_recruitment_channel_chart', graph_recruitment_channel_chart, 'Distribución por Canal de Reclutamiento')
            ],
            'set_values': [
                ('qty_active_employee', value_active_employees, 'Empleados Activos'),
                ('number_of_trainings', number_trainings, 'Capacitaciones Realizadas')
            ],
            'title': {
                'name': 'Reporte de RR.HH',
                'description': 'Análisis de empleados y capacitaciones'
            }
        },
        'Finanzas': {
            'graphics': [
                ('income_by_category_chart', graph_income_by_category, 'Ingresos por Categoría'),
                ('payment_method_chart', graph_payment_method, 'Distribución de Métodos de Pago'),
                ('monthly_sales_chart', graph_monthly_sales, 'Ventas Mensuales')
            ],
            'set_values': [
                ('total_sales', total_sales, 'Ventas Totales', '$'),
                ('most_profitable_category', most_profitable_category, 'Categoría más Rentable', '')
            ],
            'title': {
                'name': 'Reporte de finanzas',
                'description': 'Análisis de ingresos y gastos'
            }
        }
    }

    
    return df_invoice.to_json(), context

@admin_only
def index(request):
    df_invoice, context = extract_data_from_database()
    try:
        profile = request.user.profile.sector.name_sector
        context_to_send = context[profile]
        context_to_send['profile'] = profile
        return render(request, 'index.html', context_to_send)
    except:
        return render(request, 'index.html', {'error': 'No hay datos disponibles.'})

def pdf_wiewer(request):
    # Cargar la plantilla
    df_invoice, context = extract_data_from_database()
    template = get_template('other.html')
    profile = request.user.profile.sector.name_sector
    context_to_send = context[profile]
    
    html_template = template.render(context_to_send)

    # Generar el PDF
    pdf = HTML(string=html_template, base_url=request.build_absolute_uri()).write_pdf()

    # Devolver el PDF en la respuesta
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="mypdf.pdf"'
    return response

@csrf_exempt
def verify_user(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        if User.objects.filter(username=username).exists():
            return JsonResponse({'found': True})
        else:
            return JsonResponse({'found': False})
    return JsonResponse({'found': False})

def login_succes(request):
    data = {"mesg": "", "form": LoginForm()}
    username = request.GET.get('username', '')
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid:
            username = request.POST.get("username")
            password = request.POST.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    messages.success(request, "Inició sesión correctamente!!! :)")
                    return redirect(to='index')
                else:
                    data["mesg"] = "¡Nombre de usuario o contraseña no son correctos!"
            else:
                data["mesg"] = "¡Nombre de usuario o contraseña no son correctos!"
    return render(request, 'login.html', {'username': username})

def logout_succes(request):
    logout(request)
    messages.success(request, "Cerró sesión correctamente!!!")
    return redirect(to='login')

###########################################################

def get_username(request):
    if request.method == "GET":
        # Aquí puedes implementar la lógica para obtener el nombre de usuario
        username = "benja"  # Sustituir por lógica de obtención real
        user = User.objects.filter(username=username).first()
        if user:
            return JsonResponse({"username": user.username})
        return JsonResponse({"username": None})

def login_view(request):
    return render(request, 'login.html', {})

def logout_view(request):
    logout(request)
    return redirect('scan')

def find_user_view(request):
    if is_ajax(request):
        photo = request.POST.get('photo')
        _, str_img = photo.split(';base64')

        print(photo)
        decoded_file = base64.b64decode(str_img)
        print(decoded_file)

        x = Log()
        x.photo.save('upload.png', ContentFile(decoded_file))
        x.save()

        res = classify_face(x.photo.path)
        if res:
            user_exists = User.objects.filter(username=res).exists()
            if user_exists:
                user = User.objects.get(username=res)
                profile = Profile.objects.get(user=user)
                x.profile = profile
                x.save()

                login(request, user)
                return JsonResponse({'success': True})
        return JsonResponse({'success': False})

def scan(request):
    
    id_request = request.GET.get("unique_id", None) 
    if request.method == 'GET':
        id_user = Profile.objects.filter(id_unique=id_request).first()
        print(id_user)
        if id_user:
            return redirect('login')
    return render(request, 'scan.html')







