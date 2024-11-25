from my_dashboard.wsgi import *
from django.template.loader import get_template
from weasyprint import HTML

def printTicjet():
    template = get_template('index.html')
    html_template = template.render()
    HTML(string=html_template).write_pdf(target='mypdf.pdf')