from django.shortcuts import render,redirect,get_object_or_404
from .models import Thumb
import cv2
import numpy as np
import os
from PIL import Image
import pdb

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATH = os.path.join(BASE_DIR,"thumbnail")


def home(request):
    if request.method=="POST":
        thumb = Thumb()
        thumb.media = request.FILES['file']
        thumb.type = request.POST['filetype']
        thumb.save()
        if request.POST['filetype']=="video":

            vidcap = cv2.VideoCapture(os.path.join(PATH,request.FILES['file'].name))
            #pdb.set_trace()
            print(PATH + "\\" + request.FILES['file'].name)

            vidcap.set(cv2.CAP_PROP_POS_MSEC,2000)
            success,image = vidcap.read()
            count = 0
            print(success)
            while success:
                cv2.imwrite(PATH + "/%s.jpg" % request.FILES['file'].name, image)     # save frame as JPEG file
                success,image = vidcap.read()
                print('Read a new frame: ', success)
                count += 1
                break

            images = np.array(Image.open(PATH + "/%s.jpg" % request.FILES['file'].name))


        elif request.POST['filetype']=="image":
            images = np.array(Image.open(PATH + "/" + request.FILES['file'].name))

        elif request.POST['filetype']=="audio":
            images = np.array(Image.open(PATH + "/audio.jpg"))

        else:
            images = np.array(Image.open(PATH + "/text.jpg"))

        resized_image = cv2.resize(images, (200, 200), interpolation = cv2.INTER_AREA)
        img = Image.fromarray(resized_image)
        img.show()
        #img.save('thumbnail/templates/thumbnail/out.png')
        #urllib.urlretrieve("http://127.0.0.1:8000/%2Fcreated/out.png", "out.png")
        if(0xFF==("q") and cv2.waitKey(1)):
            sys.exit()

        return redirect('created')


    else:
        return render(request,'thumbnail/home.html')

def created(request):
    thumb = Thumb.objects
    return render(request,'thumbnail/created.html',{'thumb':thumb})
