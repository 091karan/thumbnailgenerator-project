from django.shortcuts import render,redirect,get_object_or_404
from .models import Thumb
import cv2
import numpy as np
import os
from PIL import Image

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATH = os.path.join(BASE_DIR,'thumbnail/media')

def home(request):
    if request.method=="POST":
        thumb = Thumb()
        thumb.media = request.FILES['file']
        thumb.type = request.POST['filetype']
        thumb.save()
        if request.POST['filetype']=="video":
            vidcap = cv2.VideoCapture(PATH + '/' + request.FILES['file'].name)
            vidcap.set(cv2.CAP_PROP_POS_MSEC,2000)
            success,image = vidcap.read()
            count = 0
            while success:
                cv2.imwrite(PATH + "/frame%d.jpg" % count, image)     # save frame as JPEG file
                success,image = vidcap.read()
                print('Read a new frame: ', success)
                count += 1
                break

            images = np.array(Image.open(PATH + "/frame0.jpg"))

        elif request.POST['filetype']=="image":
            images = np.array(Image.open(PATH + "/" + request.FILES['file'].name))

        elif request.POST['filetype']=="audio":
            images = np.array(Image.open(PATH + "/audio.jpg"))

        else:
            images = np.array(Image.open(PATH + "/text.jpg"))

        resized_image = cv2.resize(images, (200, 200), interpolation = cv2.INTER_AREA)
        img = Image.fromarray(resized_image)
        img.show()
        return redirect('created')


    else:
        return render(request,'thumbnail/home.html')

def created(request):
    return render(request,'thumbnail/created.html')
