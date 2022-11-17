import urllib.request, json, sys, os, time, datetime, re

with open('vpntraffic.txt') as f:
    vpntraffic=f.readlines()
endpoints = {}
j=0
if len(sys.argv) > 1:
    searchedEndpoint = sys.argv[1]
for line in vpntraffic:
    if line[0:1] == " ":
        index = line.split(": ")[0]
        value = line.split(": ")[1].replace("\n", "")
        index = index.strip()
        endpoint[index] = value
        if index == "allowed ips":
            value = value.split(", ")[0].replace("\n", "")
            endpoints[value] = endpoint
        if index == "transfer":
            total = 0
            metrics = value.split(",")
            for metric in metrics:
                if "received" in metric:
                    prop = "download"		
                if "sent" in metric:
                    prop="upload"
                if "KiB" in metric:
                    val = float(re.sub('[^0-9.\-]','',metric))/1024
                elif "GiB" in metric:
                    val = float(re.sub('[^0-9.\-]','',metric.split(",")[0]))
                else:
                    val = float(re.sub('[^0-9.\-]','',metric.split(",")[0]))
                total += val
                endpoint[prop] = round(val, 4)
            endpoint["total"] = round(total, 2)
    elif len(line) > 3:
        endpoint = {}
        endpoint["name"] = line
        endpoint["total"] = 0.0
        j=j+1

if len(sys.argv) > 1:
    for key, endpoint in enumerate(endpoints):
        if str(searchedEndpoint).strip() == endpoint:
            jsondump = json.dumps(endpoints[endpoint])
            print(jsondump)
            exit()
    print('{"total": 0,"endpoint": "0", "download": 0, "upload": 0, "nonefound": true}')
    exit()

jsondump = json.dumps(endpoints)
print(jsondump)

