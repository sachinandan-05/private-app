import os
from datetime import datetime, timedelta
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect
from googleapiclient.http import MediaFileUpload
from rest_framework.decorators import api_view
from rest_framework.response import Response

from Private.Google import Create_Service
from Private.forms import PrivateForm
from Private.models import PrivateModel, Private_SubModel
from Private.serializer import PrivateSerialize
from User.models import Profile
from .utils import encode_id, decode_id


# 404 Page Not Found
def page_not_found_view(request, exception):
    return render(request, '404.html', status=404)


# Logout Every 30 minutes
def some_view(request):
    # Check if session has expired
    login_time = request.session.get('login_time')
    if login_time:
        login_time = datetime.fromtimestamp(login_time)
        if datetime.now() - login_time > timedelta(minutes=30):
            check = 1
        else:
            check = 0
    else:
        check = 1

    return check


# View All/Edit Details
def admin_private_view(request):
    if request.method == 'POST':
        user_id = request.session.get('private_id')
        user_obj = User.objects.get(id=user_id)
        try:
            id = request.POST.get('id')
            jj = PrivateModel.objects.get(id=id)
            if not jj.user.username == user_obj.username:
                return redirect(f'/view/{id}')
            d = PrivateForm(request.POST or None, instance=jj, )
        except:
            d = PrivateForm(request.POST)
        if d.is_valid():
            private_data = d.save(commit=False)
            private_data.user = user_obj
            private_data.save()
            id = private_data.id
            return redirect(f'/view/{id}')
        else:
            return redirect(f'/view/')
    else:
        if 'private_admin' in request.session:
            d = PrivateForm()
            user2 = request.session.get('private_admin')
            user_obj2 = User.objects.get(username=user2)
            b = PrivateModel.objects.filter(user=user_obj2, deleted=False).order_by('-date_name')
            x = {'m': d, 'list': b, 'private_master': 'master', 'private_active': 'private_master', "private_1": 0,
                    "checkcon": 0}
        else:
            messages.success(request, 'Please Login First.')
            return redirect('/login/')
    return render(request, 'private_des.html', x)


# View All Photo, Add Photo 
def private_view(request, id):
    if request.method == 'POST':
        id = request.POST.get("id")
        try:
            user_id = request.session.get('private_id')
            user_obj = User.objects.get(id=user_id)
        except:
            return redirect(f"/view/{id}")

        myfile = request.FILES.getlist("private_img")

        for f in myfile:
            chek = str(f).split('.')[-1]
            if chek == "mp4":
                type_ = "video"
            else:
                type_ = "photo"
            pro_obj = Private_SubModel()
            pri_id = PrivateModel.objects.get(id=decode_id(id))
            if not pri_id.user.username == user_obj.username:
                return redirect(f'/view/{id}')
            pro_obj.private_id = pri_id
            pro_obj.private_img = f
            pro_obj.type = type_
            pro_obj.save()

        return redirect(f"/view/{id}")

    if 'private_admin' in request.session:
        user2 = request.session.get('private_admin')
        try:
            order = PrivateModel.objects.get(id=id, deleted=False)
            if not order.user.username == user2:
                return redirect('/view/')

            pro_list = Private_SubModel.objects.filter(private_id=id, deleted=False)
            for i in pro_list:
                i.name = i.private_img.url.split('/')[-1].split('.')[0]
            d = PrivateForm()
            data = {
                'm': d,
                'private_master': 'master',
                'private_activee': 'private_masterr',
                'lists': pro_list,
                'order': order,
                "private_1": 0,
                "checkcon": 0,
            }

            return render(request, 'private.html', data)
        except:
            return redirect('/view/')

    try:
        obj = PrivateModel.objects.get(id=id, deleted=False, share=True)
    except:
        obj = None

    if obj:
        return redirect(f'/share/{encode_id(id)}')

    messages.success(request, 'Please Login First.')
    return redirect('/login/')


# View All Photo, Add Photo
def private_views(request, hid):
    try:
        obj = PrivateModel.objects.get(id=hid, deleted=False, share=True)
    except:
        obj = None
    if obj:
        if not request.session.get('private_admin') == obj.user.username:
            return redirect(f'/share/{encode_id(hid)}')

    return redirect(f'/view/{encode_id(hid)}')


# View All/Edit Details
def share(request):
    if 'private_admin' in request.session:
        user2 = request.session.get('private_admin')
        user_obj2 = User.objects.get(username=user2)
        b = PrivateModel.objects.filter(user=user_obj2, deleted=False, share=True).order_by('-date_name')
        x = {
            'list': b,
            'private_master': 'master_share',
            'private_active': 'share_private_master',
            "private_1": 0,
            "checkcon": 0
        }

        return render(request, 'private_des_share.html', x)

    messages.success(request, 'Please Login First.')
    return redirect('/login/')


# View All Photo, Add Photo
def share_view(request, id):
    try:
        order = PrivateModel.objects.get(id=id, deleted=False, share=True)

        pro_list = Private_SubModel.objects.filter(private_id=id, deleted=False)
        for i in pro_list:
            i.name = i.private_img.url.split('/')[-1].split('.')[0]
        d = PrivateForm()
        data = {
            'm': d,
            'private_master': 'master_share',
            'private_activee': 'share_private_masterr',
            'lists': pro_list,
            'order': order,
            "private_1": 0,
            "checkcon": 0,
        }

        return render(request, 'private_share.html', data)
    except:
        return redirect('/share/')


# View All Photo, Add Photo
def share_views(request, hid):
    return redirect(f'/share/{encode_id(hid)}')


# Private Detail Function
@api_view(['POST'])
def updatepra(request):
    id = decode_id(request.POST.get('id'))
    get_data = PrivateModel.objects.get(id=id, deleted=False)
    serializer = PrivateSerialize(get_data)
    return Response(serializer.data)


# Delete Detail Fun
def remove_pri(request, hid):
    if 'private_admin' in request.session:
        user2 = request.session.get('private_admin')
        obj = PrivateModel.objects.get(id=decode_id(hid))
        if obj.user.username == user2:
            obj.deleted = True
            obj.save()
            return redirect('/view/')
        else:
            return redirect('/view/')
    else:
        messages.success(request, 'Please Login First.')
        return redirect('/login/')


# Delete Photo Fun
def remove_photo(request, hid):
    if 'private_admin' in request.session:
        user2 = request.session.get('private_admin')
        obj = Private_SubModel.objects.get(id=decode_id(hid))
        if obj.private_id.user.username == user2:
            jj = obj.private_id.id
            obj.deleted = True
            obj.save()
            return redirect(f'/view/{jj}')
        else:
            return redirect('/view/')
    else:
        messages.success(request, 'Please Login First.')
        return redirect('/login/')


# Upload Into Google Drive
def download_data(request):
    if request.method == 'POST':
        condition_check = request.POST.get('check')
        if int(condition_check) == 1:
            id = request.POST.get('id')
            try:
                folder_url = upload(id)
                a = {'url': folder_url, 'status': True}
            except:
                a = {'status': False}
        else:
            vall = request.POST.get('folder_id')
            folder_id = vall.split('/')[-1]
            try:
                delete_drive(folder_id)
                a = {'status': True}
            except:
                a = {'status': False}
        return JsonResponse(a)
    else:
        a = {'status': False}
        return JsonResponse(a)


# Upload Folder, File, Photos/Videos Into Google Drive
def upload(id):
    order = PrivateModel.objects.get(id=id)
    if order.title:
        folder_name = str(f'{order.title} ({order.date_name})')
    else:
        folder_name = str(f'{order.date_name}')

    # Login Process Start# Download From console.cloud.google.com
    service = Create_Service()
    # Login Process End

    main_folder_id = settings.GOOGLE_DRIVE_FOLDER_ID

    request_body = {
        'role': 'reader',
        'type': 'anyone',
    }

    # Create a Folder
    folder_type = 'application/vnd.google-apps.folder'
    folder_metadata = {
        'name': folder_name,
        'mimeType': folder_type,
        'parents': main_folder_id,
    }
    folder = service.files().create(
        body=folder_metadata,
        fields='id'
    ).execute()
    folder_id = folder.get('id')

    # Folder Permission
    permission_folder = service.permissions().create(
        fileId=folder_id,
        body=request_body
    ).execute()

    # Print Sharing URL FOLDER
    response_share_link_folder = service.files().get(
        fileId=folder_id,
        fields='webViewLink'
    ).execute()
    folder_url = response_share_link_folder['webViewLink']

    working_dir = os.getcwd()

    file_pathh = working_dir + '/uploads/text.txt'
    with open(file_pathh, "w") as file:
        file.write(str(order.private_description))

    text_file_type = 'text/plain'
    text_file_metadata = {
        'name': f'text.txt',
        'parents': [folder_id],
    }

    des_content = MediaFileUpload(file_pathh, mimetype=text_file_type)
    filess = service.files().create(
        body=text_file_metadata,
        media_body=des_content,
        fields='id'
    ).execute()
    file_ids = filess["id"]

    # File Permission
    permission_file = service.permissions().create(
        fileId=file_ids,
        body=request_body
    ).execute()

    # Upload a Images
    pro_list = Private_SubModel.objects.filter(private_id=id)
    for i in pro_list:
        file_11 = str(i.private_img)
        file_namee = str(file_11).split('/')[-1]
        chek = str(file_11).split('.')[-1]
        if chek == "mp4":
            img_type = 'video/mp4'
        else:
            if chek == "png":
                img_type = 'image/png'
            else:
                img_type = 'image/jpeg'
        img_metadata = {
            'name': f'{file_namee}',
            'parents': [folder_id],
        }

        img_content = MediaFileUpload(working_dir + '/uploads/' + file_11, mimetype=img_type)
        file = service.files().create(
            body=img_metadata,
            media_body=img_content,
            fields='id'
        ).execute()
        file_id = file["id"]

        # File Permission
        permission_file = service.permissions().create(
            fileId=file_id,
            body=request_body
        ).execute()
    return folder_url


# Delete Google Drive Folder
def delete_drive(folder_id):
    service = Create_Service()
    service.files().delete(fileId=folder_id).execute()
