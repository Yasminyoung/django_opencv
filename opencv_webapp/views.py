from django.shortcuts import render
from .forms import SimpleUploadForm, ImageUploadForm
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from  .cv_functions import cv_detect_face


# Create your views here.
def first_view(request):
    return render(request, 'opencv_webapp/first_view.html', {})


def simple_upload(request):

    # print(request.method) # 'POST'

    if request.method == 'POST':

        # request.POST # 'title'
        # request.FILES # 'image'

        form = SimpleUploadForm(request.POST, request.FILES)

        if form.is_valid():
            myfile = request.FILES['image'] # 메모리에 업로드되어있는 유저 업로드 이미지

            fs = FileSystemStorage()
            # fs.save('파일 저장 시 활용할 이름', 파일 객체 자체)
            filename = fs.save(myfile.name, myfile) # 저장이 끝난 물리적인 파일의 이름
            uploaded_file_url = fs.url(filename) # 저장이 끝난 물리적인 파일로 접근 가능한 URL
            # fs.save() / fs.url() / fs.delete()

            context = {'form':form, 'uploaded_file_url':uploaded_file_url}

            return render(request, 'opencv_webapp/simple_upload.html', context)


    else:
        form = SimpleUploadForm()
        context = {'form':form}
        return render(request, 'opencv_webapp/simple_upload.html', context)


# Detect face with OpenCV
def detect_face(request):

    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)

        if form.is_valid():
            post = form.save(commit=False) # post == ImageUploadModel's variable
            # post.description = papago.translate(post.description)
            form.save() # DB record 추가 & 이미지 파일 저장 종료

            # document : ImageUploadModel Class에 선언되어 있는 “document”에 해당
            imageURL = settings.MEDIA_URL + form.instance.document.name
            # == form.instance.document.url
            # == post.document.url
            # == '/media/images/2021/10/29/ses_XQAftn4.jpg'
            # print(form.instance, form.instance.document.name, form.instance.document.url)
            cv_detect_face(settings.MEDIA_ROOT_URL + imageURL) # 추후 구현 예정

            # saved_models/cnn_basic.h5
            # saved_models/main_data.xlsx

            # import tensorflow as tf
            # loaded_model = tf.keras.models.load_model('./saved_models/cnn_basic.h5')
            #
            # import pandas as pd
            # df = pd.read_excel('./saved_models/main_data.xlsx')


            return render(request, 'opencv_webapp/detect_face.html', {'form':form, 'post':post})


    else:
        # GET 요청 처리
        form = ImageUploadForm()
        return render(request, 'opencv_webapp/detect_face.html', {'form':form})
