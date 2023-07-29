from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, FileResponse
from .models import documents as documentModel, usersCerts as usersCertsModel
from users.models import User
from documents.buisnesLogic.test import search
from django.views.decorators.csrf import csrf_exempt
from django import forms
from django.contrib import messages
from django.urls import reverse
from django.shortcuts import render, HttpResponseRedirect
import json
import zipfile
import os
import mimetypes

@csrf_exempt
def validate(request):
    response_data = {'message':'ok'}
    return JsonResponse(response_data)
    # if request.method == 'POST':
    #     try:
    #         file = request.FILES.get('file')
    #         if file:
    #             file_id = documentModel.objects.all().last().id
    #             file = documentModel.objects.get(id=file_id)
    #             file_path = str(file.doc_sign.path)
    #             with zipfile.ZipFile(file_path, 'r') as my_get_zip:
    #                 zip_list = my_get_zip.namelist()
    #                 for i in zip_list:
    #                     if i.endswith('.sig'):
    #                         with zipfile.ZipFile(file_path, 'r') as my_get_zip:
    #                             my_get_zip.extract(i, path='files/sigs')
    #                             get_sig_path = str('files/sigs/' + i)
    #                             command_to_verify = str("cd ..; /opt/cprocsp/bin/amd64; cryptcp -verify " + get_sig_path)
    #                             exit_code = os.system(command_to_verify)
    #                             if exit_code == 0: 
    #                                 response_data = {'message':'ok'}
    #                             else: 
    #                                 response_data = {'error': exit_code}
    #                             return JsonResponse(response_data)
    #     except:
    #         return JsonResponse({'error':'method is not POST'})



@csrf_exempt
def get_file(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        docPath = data.get('pathDoc')
        docName = docPath.replace('files/', '')

        with zipfile.ZipFile('tmp/archive.zip', 'w', zipfile.ZIP_DEFLATED) as zipf:
            zipf.write(docPath, docName)

        response = FileResponse(open('tmp/archive.zip', 'rb'))
        response['Content-Disposition'] = 'attachment; filename="archive.zip"'
        
        return response
    else:
        context = {'error': "Method is not POST"}
        return JsonResponse(context)


def download_file(request):
    if request.method == 'POST':
        filename = request.POST.get('filename')
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        filepath = BASE_DIR + '/' + filename
        path = open(filepath, 'rb')
        mime_type, _ = mimetypes.guess_type(filepath)
        response = HttpResponse(path, content_type=mime_type)
        response['Content-Disposition'] = "attachment; filename=%s" % filename
        return response
    else:
        context = {'error': "Method is not POST"}
        return JsonResponse(context)

def index(request):
    return render(request, 'documents/index.html')

def mydocsnull(request):
    return render(request, 'documents/mydocsnull.html')

def my_cert_null(request):
    return render(request, 'documents/my_cert_null.html')

def cert_option(request):
    userId = request.user.id
    filtered_values = usersCertsModel.objects.filter(user = userId)
    if filtered_values:
        owner = []
        for value in filtered_values:
            owner.append(value.owner)
        context = {'mycerts': owner}
        return JsonResponse(context) 
    else:
        context = {'error': "Certificates not found in the user's personal account"}
        return JsonResponse(context) 

@csrf_exempt
def my_cert(request):

    userId = request.user.id
    if (usersCertsModel.objects.filter(user = userId)):
        context = {'mycerts': usersCertsModel.objects.filter(user = userId)}
        return render(request, 'documents/my_cert.html', context=context)

    else:
        return render(request, 'documents/my_cert_null.html')


@csrf_exempt
def choose_cert(request):

    userINN = str(request.user.INN)
    if request.method=="POST":
        try:
            data = json.loads(request.body)
            INNget = data.get('value')
            indexNum = []
            counter = 0
            for i in range(len(INNget)):
                if (userINN == INNget[i]):
                    counter += 1
                    indexNum.append(i)
                else:
                    pass
            if counter == 0:
                message = str('Сертификаты с ИНН ' + userINN + ' не найдены')
                response_data = {'messageNotFound': message}
                return JsonResponse(response_data)
            else:
                response_data = {'message': counter, 'indexNum': indexNum}
                return JsonResponse(response_data)
        except:
            return JsonResponse({'error':'method is not POST'})
    return render(request, 'documents/choose_cert.html')


@csrf_exempt 
def write_cert(request): 
    
    certData = json.loads(request.POST.get('certData'))  
    
    usersCerts = usersCertsModel() 
    user = str(request.user.id) 
    emptyFilter = usersCertsModel.objects.filter(user = user)

    if not emptyFilter.exists():
        usersCerts.user = request.user
        usersCerts.serialNumber = certData.get('serial')
        usersCerts.validFromDate = certData.get('fromDate')
        usersCerts.validToDate = certData.get('toDate')
        usersCerts.issuerName = certData.get("issuerName")
        usersCerts.owner = certData.get("subjectName") 
        usersCerts.save()
    else:
        usersCertsUpdate = usersCertsModel.objects.get(user = user)
        usersCertsUpdate.serialNumber = certData.get('serial')
        usersCertsUpdate.validFromDate = certData.get('fromDate')
        usersCertsUpdate.validToDate = certData.get('toDate')
        usersCertsUpdate.issuerName = certData.get("issuerName")
        usersCertsUpdate.owner = certData.get("subjectName") 
        usersCertsUpdate.save(update_fields=["serialNumber", "validFromDate", "validToDate", "issuerName", "owner"])

    return JsonResponse({ 'status': 'success' })
               
    

def status(request, doc_id):

    status = documentModel.objects.get(id = doc_id).status
    if status == 'Подписан':

        context = { 'name': documentModel.objects.get(id = doc_id).name, 
                'number': documentModel.objects.get(id = doc_id).number,
                'date_document': documentModel.objects.get(id = doc_id).date_document,
                'date_send': documentModel.objects.get(id = doc_id).date_send,
                'inboxer': documentModel.objects.get(id = doc_id).inboxer,
                'sender': documentModel.objects.get(id = doc_id).sender,
                'status': documentModel.objects.get(id = doc_id).status,
                'doc': documentModel.objects.get(id = doc_id).doc,
                'doc_sign': documentModel.objects.get(id = doc_id).doc_sign} 
        
        return render(request, 'documents/status_sign.html', context=context)

    else:
        context = { 'name': documentModel.objects.get(id = doc_id).name, 
                'number': documentModel.objects.get(id = doc_id).number,
                'date_document': documentModel.objects.get(id = doc_id).date_document,
                'date_send': documentModel.objects.get(id = doc_id).date_send,
                'inboxer': documentModel.objects.get(id = doc_id).inboxer,
                'sender': documentModel.objects.get(id = doc_id).sender,
                'status': documentModel.objects.get(id = doc_id).status,
                'doc': documentModel.objects.get(id = doc_id).doc,
                'id' : doc_id}
        return render(request, 'documents/status.html', context=context)
    

@csrf_exempt

def mypodpis(request): 
    if request.method == "POST": 
        documentsModel = documentModel() 
        idDoc = request.POST.get('idDoc')

        emptyFilter = documentModel.objects.filter(id = idDoc)

        if not emptyFilter.exists():
            if request.POST.get('submitMethod') == 'single':
                documentsModel.name = request.POST.get("name") 
                documentsModel.number = request.POST.get("number") 
                documentsModel.date_document = request.POST.get("date_document") 
                documentsModel.status = request.POST.get("status")
                documentsModel.doc = request.FILES['doc']  
                documentsModel.sender = request.user 
                documentsModel.inboxer = User.objects.get(id=request.POST.get('inboxer'))
                documentsModel.save() 
            else: 
                documentsModel.name = request.POST.get("name") 
                documentsModel.number = request.POST.get("number") 
                documentsModel.date_document = request.POST.get("date_document") 
                documentsModel.status = request.POST.get("status")
                documentsModel.doc = request.FILES['doc']  
                documentsModel.doc_sign = request.FILES['doc_sign']      
                documentsModel.sender = request.user 
                documentsModel.inboxer = User.objects.get(id=request.POST.get('inboxer')) 
                documentsModel.save()

        else:
            documentsModelUpdate = documentModel.objects.get(id = idDoc)
            documentsModelUpdate.status = request.POST.get("status")
            documentsModelUpdate.doc_sign = request.FILES['doc_sign']
            documentsModelUpdate.save(update_fields=["status", "doc_sign"])


        messages.success(request, 'Форма отправлена')

        return JsonResponse({'status': 'success'})

    else:
        context = {'users' : User.objects.all(),}       
        return render(request, 'documents/podpis.html', context=context)
    

def mydocs(request):

    userId = request.user.id

    if (documentModel.objects.filter(sender = userId)) or (documentModel.objects.filter(inboxer = userId)):
        context = {'docsSend': documentModel.objects.filter(sender = userId), 
                   'docsInbox': documentModel.objects.filter(inboxer = userId)}
        return render(request, 'documents/mydocs.html', context=context)

    else:
        return render(request, 'documents/mydocsnull.html')