import requests
import sys
import pyfiglet
import json
import gzip
import re
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#for window to run for bulk files "for /r %i in (http_req*) do python raw0xy.py %i <ip:port>"
#for Linux to run for bulk files "ls http_req*|parallel python raw0py.py {} <ip:port>"

def split_on_empty_lines(s):
    blank_line_regex = r"(?:\r?\n){2,}"
    return re.split(blank_line_regex, s.strip())

def  helpMessage():
	ascii_banner = pyfiglet.figlet_format("raw0xy")
	print(ascii_banner+"\t\t\tBeta v1.0 ")
	print("""No arguments are passed
       Usage: python3 raw0xy <raw_request_file> <ip:port>\r\n
       For window to run for bulk files "for /r %i in (regex_file) do python raw0xy.py %i <ip:port>\r\n
       For Linux to run for bulk files "ls regex_file*|parallel python raw0py.py {} <ip:port>""")
 
def getRequest(param_url,params_headers,proxy):
    s = requests.Session()
    s.proxies = {'http' : proxy, 'https' : proxy}
    try:
    	r = s.get(param_url, headers=params_headers,verify=False)
    	print(r.status_code)
    except requests.exceptions.RequestException as e:
    	raise SystemExit(e)
def postRequest(param_url,params_headers,param_body,proxy):
    s = requests.Session()
    s.proxies = {'http' : proxy, 'https' : proxy}
    try:
    	r = s.post(param_url,headers=params_headers,data=body,verify=False)
    	print(r.status_code)
    except requests.exceptions.RequestException as e:
    	raise SystemExit(e)

def putRequest(param_url,params_headers,param_body,proxy):
    s = requests.Session()
    s.proxies = {'http' : proxy, 'https' : proxy}
    try:
    	r = s.put(param_url,headers=params_headers,data=body,verify=False)
    	print(r.status_code)
    except requests.exceptions.RequestException as e:
    	raise SystemExit(e)
    except UnicodeEncodeError:
     	print("UnicodeEncodeError") 

def deleteRequest(param_url,params_headers,param_body,proxy):
    s = requests.Session()
    s.proxies = {'http' : proxy, 'https' : proxy}
    try:
    	r = s.delete(param_url,headers=params_headers,data=body,verify=False)
    	print(r.status_code)
    except requests.exceptions.RequestException as e:
    	raise SystemExit(e)

def optionsRequest(param_url,params_headers,param_body,proxy):
    s = requests.Session()
    s.proxies = {'http' : proxy, 'https' : proxy }
    try:
    	r = s.options(param_url,headers=params_headers,data=body,verify=False)
    	print(r.status_code)
    except requests.exceptions.RequestException as e:
    	raise SystemExit(e)

def requestHeaders(request_head_list, host_header_index):
	del request_head_list[0]
	host_header_index=host_header_index-1
	del request_head_list[host_header_index]
	return request_head_list

try:
	file=sys.argv[1]
	proxy_ip=sys.argv[2]
except IndexError:
	helpMessage()
	sys.exit(1)



with open(file, 'r',errors='ignore') as my_file:
    raw_data=my_file.read()
a=split_on_empty_lines(raw_data)
if 'Transfer-Encoding' in a[0]:
	print("Not supported format found: Transfer-Encoding: chunked")
	sys.exit()
request_head=a[0].splitlines()
#print(request_head)
method=request_head[0].split()[0]
query=request_head[0].split()[1]
get_index=[i for i, word in enumerate(request_head) if word.startswith('Host:')]
hostname=request_head[get_index[0]].split(" ")[1]+":443"
# print(method)
# print(query)
# print(host)
url="https://"+hostname+query

if len(a) == 2:
	body=a[1].encode('utf-8')
	#print(type(body))

raw_headers=requestHeaders(request_head,get_index[0])
#print(raw_headers)
headers = {}

for a in raw_headers:
	#print(a)
	k=a.split(":")[0].strip()
	#print(k)
	v=a.split(":")[1].strip()
	#print(v)
	d=dict({k:v})
	headers.update(d)

if method == 'GET':
    getRequest(url,headers,proxy_ip)
elif method == 'POST':
    postRequest(url,headers,body,proxy_ip)
elif method == 'PUT':
    putRequest(url,headers,body,proxy_ip)
elif method == 'DELETE':
    deleteRequest(url,headers,body,proxy_ip)
elif method == 'OPTIONS':
    optionsRequest(url,headers,body,proxy_ip)
