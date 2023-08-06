import json

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render

from .models import AnnotationImageModel, YoloClassModel, ImageDetectionModel

file_supported = ['png', 'PNG', 'jpg', 'jpeg', 'JPG', 'JPEG']


def upload(request):
    context = {}
    table = YoloClassModel.objects.all().values('name')
    context['class_table'] = list(table)
    annotate = request.POST.get('annotate-files', '')
    print(annotate)
    if request.method == 'POST':
        print(request.FILES)
        context['msg_class'] = 'is-primary'
        print(request.POST.keys())
        for i in request.POST.keys():
            print(request.POST.get(i))
        for field in request.FILES.keys():
            print(field)
            for formfile in request.FILES.getlist(field):
                # check if file is supported
                print(formfile)
                if str(formfile.name).split(".")[1] not in file_supported:
                    context['msg_class'] = 'is-danger'
                    context['message'] = 'File extension not supported!'
                    return render(request, 'upload.html', context=context)

                img = AnnotationImageModel(image=formfile)
                img.save()
                # create annotation file
                annotate = request.POST.get('annotate-files', '')
                annotate_path = settings.MEDIA_ROOT + '/' + str(img.image).replace(str(img.image).split('.')[1], 'txt')
                f = open(annotate_path, 'w+')
                f.write(json.loads(annotate))

                img.annotate = annotate_path
                img.save()

                f.close()

        context['message'] = 'File uploaded!'
    return render(request, 'upload.html', context=context)


def home(request):
    print(request.META.get("REMOTE_ADDR"))
    return render(request, 'home.html')


def analysis(request):
    return render(request, 'analysis.html')


def stat(request):
    context = {}
    context['card'] =[{
        'name': 'CLASS',
        'value': YoloClassModel.objects.count(),
    }, {
        'name': 'Images',
        'value': AnnotationImageModel.objects.count(),
    }, {
        'name': 'Response Time',
        'value': str(2.5) + 'ms',
    }]
    return render(request, 'stat.html', context=context)


def yolo_class(request):
    context = {}
    table = YoloClassModel.objects.all().values()
    context['class_table'] = table
    print(table)
    return render(request, 'class.html', context=context)


def detection_image(request):
    if request.FILES:
        image = request.FILES['image']
        model = ImageDetectionModel(image=image)
        return JsonResponse({
            "status": True,

        })
    return JsonResponse({
        "status": False,
    })


def model(request):
    context = {}
    context['log'] = read_file(settings.MEDIA_ROOT + '/darknet/log.txt')
    return render(request, "model.html", context=context)


def model_settings(request):
    context = {}
    main_path = settings.MEDIA_ROOT + '/config/'
    # create class file
    f = open(main_path + 'classes.name', 'w+')
    class_model = YoloClassModel.objects.all()
    total_classes = YoloClassModel.objects.count()
    for c in class_model:
        f.write(c.name + "\n")
    f.close()
    context['classes'] = read_file(main_path + 'classes.name')
    context['total_class'] = total_classes
    # configure data file
    f = open(main_path + 'darknet.data', 'w')
    f.write('classes = ' + str(total_classes) + '\n')
    f.write('train = ' + main_path + 'train.txt\n')
    f.write('valid = ' + main_path + 'test.txt\n')
    f.write('names = ' + main_path + 'classes.names\n')
    f.write('backup = ' + settings.MEDIA_ROOT + '/weights/\n')
    f.close()

    # yolo configuration file
    context['image_width'] = ''
    context['image_height'] = ''
    with open(settings.MEDIA_ROOT + '/darknet/cfg/yolov3.cfg', 'r') as fp:
        for line in fp:
            print(line)
            context['image_width'] = line.replace("width=", "") if line.__contains__("width=") else context['image_width']
            context['image_height'] = line.replace("height=", "") if line.__contains__("height=") else context['image_height']
    return render(request, "settings.html", context=context)


def train(request):
    return JsonResponse({
        "status": True
    })
