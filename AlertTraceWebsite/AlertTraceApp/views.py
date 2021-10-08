from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
import urllib.request
from urllib.error import HTTPError

import json


# Create your views here.

#home page login page
def index(request):
    return render(request, 'AlertTraceApp/hi.html')

#login based (get all info)
def send(request):
    if request.method == 'POST':

        email = request.POST.get("email")
        password = request.POST.get("password")

        body = {"email": email, "password": password}
        myurl = "https://app-api.alerttrace.com/login"
        try:
            req = urllib.request.Request(myurl)
            req.add_header('Content-Type', 'application/json; charset=utf-8')
            jsondata = json.dumps(body)
            jsondataasbytes = jsondata.encode('utf-8')  # needs to be bytes
            req.add_header('Content-Length', len(jsondataasbytes))

            response = urllib.request.urlopen(req, jsondataasbytes)
            response1result = response.read().decode("utf-8")
            resp_dict = json.loads(response1result)
            tokenresult = resp_dict.get('token')

            ####QUERY ALL DEVICES####
            myurl2 = "https://app-api.alerttrace.com/device"
            req2 = urllib.request.Request(myurl2)
            req2.add_header('authorization', 'Bearer' + " " + tokenresult)
            response2 = urllib.request.urlopen(req2)
            response2result = response2.read().decode("utf-8")
            resp_dict2 = json.loads(response2result)
            # Filter empty devices only
            EmptyMiniSerial = [{'serial': dct['serial']} for dct in resp_dict2 if (dct['subject']) == None]
            status_code = response.status
            if status_code == 200 or status_code == 201 or status_code == 204:  # request succeeded
                item_list = {k + str(i + 1): v for i, d in enumerate(EmptyMiniSerial) for k, v in d.items()}
                totalMinis = len(item_list.keys())

                ###LSIT SUBJECT GROUPS
                '''
                curl --request GET \
                --url https://app-api.alerttrace.com/subject \
                --header 'authorization: Bearer [token]'''

                myurl3 = "https://app-api.alerttrace.com/subject"
                req3 = urllib.request.Request(myurl3)
                req3.add_header('authorization', 'Bearer' + " " + tokenresult)
                response3 = urllib.request.urlopen(req3)
                response3result = response3.read().decode("utf-8")
                resp_dict3 = json.loads(response3result)
                #print(resp_dict3)
                # Filter all 'groups' that have value

                lst = [{'groups': dct['groups']} for dct in resp_dict3 if (dct['groups']) != []]


                seen = set()
                result = []

                for d in lst:
                    for e in d["groups"]:
                        if e not in seen:
                            result.append(e)
                            seen.add(e)
                global context
                context = {
                    'totalMinis': totalMinis,
                    'item_list': item_list,
                    'groupresult': (listToString(result)),
                    'filterserial':   [item[1] for item in item_list.items()]

                }
                print(item_list)

                print(result)
                print(listToString(result))
                #print(allgroup)


                return render(request, 'AlertTraceApp/mainpage.html', context)
            else:
                messages.error(request, 'username or password not correct')
        except HTTPError as err:
            if err:
                print("error")
                messages.error(request, 'username or password not correct')

                return render(request, 'AlertTraceApp/hi.html')
            else:
                raise


# Function to convert
def listToString(s):
    # initialize an empty string
    str1 = ", "

    # return string
    return (str1.join(s))

#upload
def upload(request):
    print("post")
    if request.method =='POST':
        uploaded_file = request.FILES['file']


    return render(request, 'AlertTraceApp/mainpage.html', context)

