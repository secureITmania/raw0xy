#### Tool Information

In the recent android application testing, I encountered a challenge to import raw HTTP request files (Which are obtained from HTTP Canary, SSL Capture etc.,) to BurpSuite. However, I could not find any method or extension of importing bulk raw HTTP requests into Burp other than manually copying and pasting them into the repeater. That's why I wrote this python tool to parse raw HTTP request file and proxy through BurpSuite.

raw0xy is a python tool that parse the raw request and sends appropriate request via defined proxy.

![](E:\Python\raw0xy\Images\tool_banner.png)



```cmd
usage:

cat test.txt
GET /test h2
Host: www.google.com
user-agent: Mozilla/5.0 (Linux; Android 8.1.0; Nexus 5X Build/OPM4.171019.016.A1; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/61.0.3163.98 Mobile Safari/537.36
accept: image/webp,image/apng,image/*,*/*;q=0.8
referer: http://localhost/
accept-encoding: gzip, deflate
accept-language: en-US

python raw0xy.py test.txt 127.0.0.1:8052
```



The script does not have the multi-threading capability. But we can use in build system capabilities to run on bulk files.

```
For Windows:
for /r %i in (raw_request*) do python raw0xy.py %i <ip:port>

For Linux:
ls raw_request*|parallel python raw0py.py {} <ip:port>
```



#### Limitation:

At present the tool not support 'Transfer-encoding' body format.