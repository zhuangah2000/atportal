import urllib.request
import json

######LOGIN AND GET TOKEN#####
body = {"email": "zhuangah@macrovention.com","password": "584584goh"}
myurl = "https://app-api.alerttrace.com/login"


req = urllib.request.Request(myurl)
req.add_header('Content-Type', 'application/json; charset=utf-8')
jsondata = json.dumps(body)
jsondataasbytes = jsondata.encode('utf-8')   # needs to be bytes
req.add_header('Content-Length', len(jsondataasbytes))

response = urllib.request.urlopen(req, jsondataasbytes)
response1result = response.read().decode("utf-8")
resp_dict = json.loads(response1result)
tokenresult = resp_dict.get('token')
#print(tokenresult)

####QUERY ALL DEVICES####
myurl2= "https://app-api.alerttrace.com/device"
req2 = urllib.request.Request(myurl2)
req2.add_header('authorization', 'Bearer'+" "+tokenresult)
response2= urllib.request.urlopen(req2)
response2result = response2.read().decode("utf-8")
resp_dict2 = json.loads(response2result)
# Filter empty devices only
EmptyMiniSerial =[{'serial': dct['serial']} for dct in resp_dict2 if (dct['subject']) == None]
#print(EmptyMiniSerial)




List_A = EmptyMiniSerial
a = {k+str(i+1): v for i,d in enumerate(List_A) for k,v in d.items()}
print(a)