import requests
from django.shortcuts import render,redirect
from django.views.generic import TemplateView
from django.core.files.storage import FileSystemStorage
import os
from django.core.exceptions import ValidationError
import csv
from smart_open import open

from .convertor import convert_pdf_to_txt
#from django.http import HttpResponse
from .tasks import extractemail, extractname, extractphone, extractlinkedin, extractlinesandchar
from .createcsv import data
# Create your views here.

csvurl=""

def home(request):
    #return HttpResponse('<h1>Home Page</h1>')
    return render (request,'app1/index.html')


def uploadpage(request):
    #return HttpResponse('<h1>Home Page</h1>')
    return render(request, 'app1/upload.html')


def uploadnow(request):  
    if request.method == 'POST' and request.FILES['document']:
            myfile = request.FILES['document']
            print(myfile.name)
            fs = FileSystemStorage()
            ext = os.path.splitext(myfile.name)[1]
            valid_extensions = ['.pdf', '.doc', '.docx']
            if not ext in valid_extensions:
                raise ValidationError(u'File not supported!')

            filename = fs.save(myfile.name, myfile)
            uploaded_file_url = fs.url(filename)
            print(uploaded_file_url)
            text = convert_pdf_to_txt(uploaded_file_url)
            if(len(text)):
                e= extractemail(text)
                n = extractname(text)
                p = extractphone(text)
                l = extractlinkedin(text)
                t, tc = extractlinesandchar(uploaded_file_url)
                csvurl=data(uploaded_file_url,n,e,l,p,t,tc)
                print (csvurl)
            else:
                print("Empty file")
            return render(request, 'app1/upload.html', {'uploaded_file_url': uploaded_file_url,'csvurl':csvurl})

    return render(request, 'app1/upload.html')


def success(request):
    csvurl = '/media/csvfiles/out.csv'
    return render(request, 'app1/success.html', {'csvurl': csvurl})
