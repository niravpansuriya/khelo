import json
import math
import pickle

import cv2
import matplotlib.pyplot as plt
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
import subprocess, re
from django.conf import settings
import os

init_Dict = dict()
exec_Dict = dict()

gifList = {'1': "ffd.gif"}


class Home(TemplateView):
    template_name = 'home.html'


class Temp(TemplateView):
    template_name = 'temp.html'


class Image(TemplateView):
    template_name = 'image.html'


class uploadCustom(TemplateView):
    template_name = 'videoUploadPage.html'


def submitQuery(request):
    if request.method == 'POST':
        shotId = request.POST['shotId']
        useType = int(request.POST['useType'])
        gif = "gif/" + gifList[shotId]
        context = {'shotId': shotId, "gif": gif}

        if useType == 0:
            return render_to_response('battingPageWebcam.html', context)
        else:
            return render_to_response("videoUploadPage.html", context)

    else:
        return HttpResponse("Request method is not a POST")


@csrf_exempt
def sendBattingDataWebcam(request):
    if request.method == 'POST':
        posesNorm = request.POST.get('upPoses')
        if posesNorm is not None:
            poses = json.loads(request.POST['upPoses'])
            # poseId = request.POST['poseId']   #choose which posture of batting
            # print(poseId)
            print(poses)
            return HttpResponse("Working !!")
        else:
            return HttpResponse("Null")
    else:
        return HttpResponse("Error")


@csrf_exempt
def upload_batting_video(request):
    file = request.FILES['video']
    name = file.name.split(".")
    extension = name[-1]
    fs = FileSystemStorage()
    filename = fs.save('temp.' + extension, file)
    file_url = fs.url(filename)
    context = {'file': file_url, 'gif': request.POST['gif'], 'shotId': request.POST['shotId']}
    return render_to_response('sampleVideo.html', context)


@csrf_exempt
def sendBattingDataVideo(request):
    if request.method == 'POST':
        posesNorm = request.POST.get('upPoses')
        if posesNorm is not None:
            poses = json.loads(request.POST['upPoses'])
            # poseId = request.POST['poseId']   #choose which posture of batting
            # print(poseId)
            print(poses)
            return HttpResponse("Working !!")
        else:
            return HttpResponse("Null")
    else:
        return HttpResponse("Error")


@csrf_exempt
def getImageData(request):
    if request.method == 'POST':
        poses = json.loads(request.POST['upPoses'])
        # print("Left Ankle Co-ordinates : (" + poses.pose.keypoints[15].position.x + "," + poses[0].pose.keypoints[15].position.y+")")
        # print("Right Ankle Co-ordinates : (" + poses.pose.keypoints[16].position.x + "," + poses[0].pose.keypoints[16].position.y+")")
        print("Right Ankle : " + str(poses[0]['pose']['keypoints'][16]))
        print("Left Ankle : " + str(poses[0]['pose']['keypoints'][15]))
        rankleX = poses[0]['pose']['keypoints'][16]['position']['x']
        rankleY = poses[0]['pose']['keypoints'][16]['position']['y']
        lankleX = poses[0]['pose']['keypoints'][15]['position']['x']
        lankleY = poses[0]['pose']['keypoints'][15]['position']['y']

        print(calculateDistance(rankleX, rankleY, lankleX, lankleY))
        print(calculateSlope(rankleX, rankleY, lankleX, lankleY))

        p = poses[0]['pose']['keypoints']
        l = len(p)
        points = dict()
        for i in range(l):
            d = p[i]
            if d['score'] > 0.4:
                x, y = d['position']['x'], -d['position']['y']
                points[p[i]['part']] = [x, y]

        if 'leftEar' in points.keys():
            points.pop('leftEar')

        if 'rightEar' in points.keys():
            points.pop('rightEar')

        print(points.keys())
        graph = make_Graph(points)
        for i in range(len(graph)):
            print(graph[i])
        print('\n')
        for i in range(len(graph)):
            plt.plot([graph[i][0][0], graph[i][1][0]], [graph[i][0][1], graph[i][1][1]])
            print([graph[i][0][0], graph[i][1][0]], [graph[i][0][1], graph[i][1][1]])

        plt.savefig('img.png')

        # plt.show()
        return HttpResponse("Working !!")
    else:
        return HttpResponse("Error")


@csrf_exempt
def uploadGymVideoCustom(request):
    file = request.FILES['video']
    name = file.name.split(".")
    extension = name[-1]
    fs = FileSystemStorage()
    filename = fs.save('tempy.' + extension, file)
    file_url = fs.url(filename)
    cap = cv2.VideoCapture("media/tempy.mp4")
    fps = int(cap.get(cv2.CAP_PROP_FPS))

    total_frame = cv2.CAP_PROP_FRAME_COUNT
    length = total_frame / fps

    s_t = 0
    s_e = 10

    i = 0
    while (cap.isOpened()):
        print(i, s_t * fps, s_e * fps)
        if i < s_t * fps:
            ret, frame = cap.read()
            if ret == False:
                print(False)
                break
            i += 1
            frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
            if i % 3 == 0:
                cv2.imwrite('media/image' + str(i) + '.jpg', frame)
            continue
        else:
            print(fps)
            ret, frame = cap.read()
            if ret == False:
                print(False)
                break
            frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
            if i % 3 == 0:
                cv2.imwrite('media/image' + str(i) + '.jpg', frame)
        i += 1

    cap.release()
    context = {'file': file_url, 'img_frag': i}
    # os.remove('media/tempy.mp4')
    return render_to_response('sampleVideo.html', context)


def make_Graph(points):
    graph = []
    keys = points.keys()
    if 'leftEye' in keys and 'nose' in keys:
        graph += [[points['nose'], points['leftEye']]]
    if 'rightEye' in keys and 'nose' in keys:
        graph += [[points['nose'], points['rightEye']]]
    if 'leftShoulder' in keys and 'nose' in keys:
        graph += [[points['nose'], points['leftShoulder']]]
    if 'rightShoulder' in keys and 'nose' in keys:
        graph += [[points['nose'], points['rightShoulder']]]
    if 'rightShoulder' in keys and 'rightElbow' in keys:
        graph += [[points['rightElbow'], points['rightShoulder']]]
    if 'leftShoulder' in keys and 'leftElbow' in keys:
        graph += [[points['leftElbow'], points['leftShoulder']]]
    if 'leftWrist' in keys and 'leftElbow' in keys:
        graph += [[points['leftElbow'], points['leftWrist']]]
    if 'rightWrist' in keys and 'rightElbow' in keys:
        graph += [[points['rightElbow'], points['rightWrist']]]
    if 'leftHip' in keys and 'leftShoulder' in keys:
        graph += [[points['leftHip'], points['leftShoulder']]]
    if 'rightHip' in keys and 'rightShoulder' in keys:
        graph += [[points['rightHip'], points['rightShoulder']]]
    if 'leftHip' in keys and 'leftKnee' in keys:
        graph += [[points['leftHip'], points['leftKnee']]]
    if 'rightHip' in keys and 'rightKnee' in keys:
        graph += [[points['rightHip'], points['rightKnee']]]
    if 'leftAnkle' in keys and 'leftKnee' in keys:
        graph += [[points['leftAnkle'], points['leftKnee']]]
    if 'rightAnkle' in keys and 'rightKnee' in keys:
        graph += [[points['rightAnkle'], points['rightKnee']]]
    return graph


def calculateDistance(x1, y1, x2, y2):
    dist = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return dist


def calculateSlope(x1, y1, x2, y2):
    dist = (y2 - y1) / (x2 - x1)
    return dist


@csrf_exempt
def sendLooperData(request):
    if request.method == 'POST':
        poses = json.loads(request.POST['upPoses'])
        no = request.POST['imageNo']
        print("-----------------------------------------------------------------")
        print("NO: " + no)
        # print("Left Ankle Co-ordinates : (" + poses.pose.keypoints[15].position.x + "," + poses[0].pose.keypoints[15].position.y+")")
        # print("Right Ankle Co-ordinates : (" + poses.pose.keypoints[16].position.x + "," + poses[0].pose.keypoints[16].position.y+")")
        p = poses[0]['pose']['keypoints']
        l = len(p)
        points = dict()
        for i in range(l):
            d = p[i]
            if d['score'] > 0:
                x, y, c = d['position']['x'], -d['position']['y'], d['score']
                points[p[i]['part']] = [x, y, c]

        user_slopes = user_slope(points)
        with open('ideal_init.pickle', 'rb') as input:
            ideal_init_slopes = pickle.load(input)
        with open('ideal_exec.pickle', 'rb') as input:
            ideal_exec_slopes = pickle.load(input)
            #  print(user_slopes,ideal_init_slopes,ideal_exec_slopes,'\n\n\n')

        sum_init = 0
        for a in ['RES', 'RHS', 'LES', 'LHS']:
            sum_init += abs(ideal_init_slopes[a] - user_slopes[a])

        sum_exec = 0
        for a in ['RES', 'RHS', 'LES', 'LHS']:
            sum_exec += abs(ideal_exec_slopes[a] - user_slopes[a])

        if (sum_exec < sum_init):
            exec_Dict[no] = dict()
            exec_Dict[no]["dist"] = sum_exec
            exec_Dict[no]["Dict"] = user_slopes
            exec_Dict[no]["Point_Dict"] = points
        else:
            init_Dict[no] = dict()
            init_Dict[no]["dist"] = sum_init
            init_Dict[no]["Dict"] = user_slopes
            init_Dict[no]["Point_Dict"] = points

        # print("------------" + "exec_Dict" + " -----------------  ")
        # print(exec_Dict)

        # print("------------" + "init_Dict" + " -----------------  ")
        # print(init_Dict)

        # plt.show()
        return HttpResponse("Working !!")
    else:
        return HttpResponse("Error")


def return_frames(request):
    ans = dict()

    global exec_Dict, init_Dict
    min_Dist = 999999
    min_exec_frame_no = -1

    for i in exec_Dict:
        if (i != '0'):
            print(type(i))
            print("exec dict")
            print(i, exec_Dict[i]["dist"])
            if (exec_Dict[i]["dist"] < min_Dist):
                min_Dist = exec_Dict[i]["dist"]
                min_exec_frame_no = i

    min_Dist = 99999
    min_init_frame_no = -1

    for i in init_Dict:
        if (init_Dict[i]["dist"] < min_Dist):
            min_Dist = init_Dict[i]["dist"]
            min_init_frame_no = i

    print(min_init_frame_no, min_exec_frame_no)
    # print(context)

    execFd = gym_exec_feedback(min_exec_frame_no)
    initFd = gym_init_feedback(min_init_frame_no)

    return render_to_response('feedback.html', context={"execFr": min_exec_frame_no, "initFr": min_init_frame_no, "execFd": execFd,
         "initFd": initFd})


def gym_exec_feedback(number):
    feedbacks = []
    global exec_Dict

    temp_dict = exec_Dict[number]['Dict']

    temp = (temp_dict['RHS'] - temp_dict['RES']) / (1 + (temp_dict['RES'] * temp_dict['RHS']))
    degree = math.degrees(math.atan(temp))
    # print(exec_Dict[number])
    if degree < 0:
        degree = degree + 180
    # print(degree)
    if degree > 165:
        feedbacks.append(["bend your right hand little bit"])

    temp = (temp_dict['LES'] - temp_dict['LHS']) / (1 + (temp_dict['LES'] * temp_dict['LHS']))
    degree = math.degrees(math.atan(temp))

    if degree < 0:
        degree = degree + 180

    if degree > 165:
        feedbacks.append(["bend your left hand little bit"])

    Temp_Dict = exec_Dict[number]["Point_Dict"]

    slope = (Temp_Dict["rightShoulder"][1] - Temp_Dict["rightWrist"][1]) / (
            Temp_Dict["rightShoulder"][0] - Temp_Dict["rightWrist"][0])

    if (slope > 0.35):
        feedbacks.append(["Keep your right hand upward as the straight line with the shoulder"])
    elif (slope < -0.35):
        feedbacks.append(["Keep your right hand downward as the straight line with the shoulder"])

    slope = (Temp_Dict["leftShoulder"][1] - Temp_Dict["leftWrist"][1]) / (
            Temp_Dict["leftShoulder"][0] - Temp_Dict["leftWrist"][0])

    if (slope > 0.35):
        feedbacks.append(["Keep your left hand downward as the straight line with the shoulder"])
    elif (slope < -0.35):
        feedbacks.append(["Keep your left hand upward as the straight line with the shoulder"])

    return feedbacks


def gym_init_feedback(number):
    global init_Dict

    feedbacks = []
    Temp_Dict = init_Dict[number]["Point_Dict"]

    dist = math.sqrt((Temp_Dict["leftWrist"][0] - Temp_Dict["rightWrist"][0]) ** 2 + (
            Temp_Dict["leftWrist"][1] - Temp_Dict["rightWrist"][1]) ** 2)

    if (dist < 150):
        feedbacks.append(["Keep little bit more distance between wrists"])
    elif (dist > 152):
        feedbacks.append(["Keep little bit less distance between wrists"])

    return feedbacks


def user_slope(user_Dict):
    FS = (user_Dict['leftEye'][1] - user_Dict['rightEye'][1]) / (user_Dict['leftEye'][0] - user_Dict['rightEye'][0])
    RSS = (user_Dict['nose'][1] - user_Dict['rightShoulder'][1]) / (
                user_Dict['nose'][0] - user_Dict['rightShoulder'][0])
    LSS = (user_Dict['nose'][1] - user_Dict['leftShoulder'][1]) / (user_Dict['nose'][0] - user_Dict['leftShoulder'][0])
    LES = (user_Dict['leftShoulder'][1] - user_Dict['leftElbow'][1]) / (
                user_Dict['leftShoulder'][0] - user_Dict['leftElbow'][0])
    RES = (user_Dict['rightShoulder'][1] - user_Dict['rightElbow'][1]) / (
                user_Dict['rightShoulder'][0] - user_Dict['rightElbow'][0])
    LHS = (user_Dict['leftWrist'][1] - user_Dict['leftElbow'][1]) / (
                user_Dict['leftWrist'][0] - user_Dict['leftElbow'][0])
    RHS = (user_Dict['rightWrist'][1] - user_Dict['rightElbow'][1]) / (
                user_Dict['rightWrist'][0] - user_Dict['rightElbow'][0])
    RHeS = (user_Dict['rightHip'][1] - user_Dict['rightKnee'][1]) / (
                user_Dict['rightHip'][0] - user_Dict['rightKnee'][0])
    RLS = (user_Dict['rightKnee'][1] - user_Dict['rightAnkle'][1]) / (
                user_Dict['rightKnee'][0] - user_Dict['rightAnkle'][0])
    LHeS = (user_Dict['leftHip'][1] - user_Dict['leftKnee'][1]) / (user_Dict['leftHip'][0] - user_Dict['leftKnee'][0])
    LLS = (user_Dict['leftKnee'][1] - user_Dict['leftAnkle'][1]) / (
                user_Dict['leftKnee'][0] - user_Dict['leftAnkle'][0])

    temp_Dict = dict()
    temp_Dict["FS"] = FS
    temp_Dict["RSS"] = RSS
    temp_Dict["LSS"] = LSS
    temp_Dict["LES"] = LES
    temp_Dict["RES"] = RES
    temp_Dict["LHS"] = LHS
    temp_Dict["RHS"] = RHS
    temp_Dict["RHeS"] = RHeS
    temp_Dict["RLS"] = RLS
    temp_Dict["LLS"] = LLS
    temp_Dict["LHeS"] = LHeS

    return temp_Dict
