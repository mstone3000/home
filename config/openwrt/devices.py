import urllib.request, json, sys, os, time, datetime, requests
from datetime import timedelta
from filelock import FileLock

def older(file, seconds=300): 
    file_time = os.path.getmtime(file)
    return ((time.time() - file_time) > seconds)

envpath=os.path.realpath('.')+"/pyenv.env"
exec(open(envpath).read())

#homeassistant_wifi_update = "http://172.17.0.1:8123/api/webhook/"
cache = os.path.realpath('.')+"/openwrt/cache/devicecache.json"
cacheauth = os.path.realpath('.')+"/openwrt/cache/auth_"
headers = {"content-type": "application/json", "cache-control": "no-cache"}
use_cache = True
aps = {}

lockfile = cache
lock = FileLock(lockfile + ".lock")
locked = True
while locked:
  try:
    lock.acquire(timeout=0.1)
    locked = False
  except:
    time.sleep(0.3)

def authenticate(router):
  filename = router[0].replace(".", "_")+".tmp"
  auth = ""
  if os.path.exists(cacheauth+filename) and not older(cacheauth+filename, 300):
    cachedauth = open(cacheauth+filename, "r").read()
    cachedauth = json.loads(cachedauth)
    auth = cachedauth[3]
  else:
      url = "http://"+router[0]+"/cgi-bin/luci/rpc/auth"
      data = {}
      data["id"]= 1
      data["method"] = "login"
      data["params"] = [router[1], router[2]]
      req = requests.post(url, data = json.dumps(data))
      auth = json.loads(req.text)["result"]
      router.append(auth)
      cachedauth = open(cacheauth+filename, "w")
      cachedauth.write(json.dumps(router))
      cachedauth.close()
  return auth

def output(jsonString=False):
  if jsonString:
    aps = json.loads(jsonString)
  else:
    aps = open(cache, "r").read()
    aps = json.loads(aps)
    outdevices = aps
    json_object = json.dumps(outdevices) 
  for ak, ap in enumerate(aps):
    for ik, iface in enumerate(aps[ap]):
        ifaceclients = []
        for ck, client in enumerate(aps[ap][iface]["data"]["clients"]):
          ifaceclients.append(client)
        aps[ap][iface]["data"]["ifaceclients"] = ifaceclients
    outdevices = {}
    array = {}
    array["24"] = []
    array["5"] = []
    for ak, ap in enumerate(aps):
        for ik, iface in enumerate(aps[ap]):
            freq=aps[ap][iface]["info"]["freq"]
            if freq > 2700:
              freq = "5"
            else:
              freq = "24"
            if 'ifaceclients' in aps[ap][iface]["data"]:
              if len(aps[ap][iface]["data"]["ifaceclients"]) > 0:
                for ck, client in enumerate(aps[ap][iface]["data"]["clients"]["clients"]):
                  clientObj = {}
                  clientObj["mac"] = client
                  clientObj["iface"] = str(aps[ap][iface]["data"]["iface"])
                  clientObj["router"] = ap
                  if "rate" in aps[ap][iface]["data"]["clients"]["clients"][client]:
                    clientObj["rate"] = aps[ap][iface]["data"]["clients"]["clients"][client]["rate"]
                  else:
                    rate = {}
                    rate["rx"] = 0
                    rate["tx"] = 0
                    clientObj["rate"] = rate
                  if "signal" in aps[ap][iface]["data"]["clients"]["clients"][client]:
                    clientObj["signal"] = aps[ap][iface]["data"]["clients"]["clients"][client]["signal"]
                  else:
                    clientObj["signal"] = 0
                  array[freq].append(clientObj)
    if len(sys.argv) > 1:
      if sys.argv[1] == "nocache" or sys.argv[1] == "all":
        outdevices["devices"] = array["5"]+array["24"]
      elif sys.argv[1] == "24":
        outdevices["devices"] = array["24"]
      elif sys.argv[1] == "5":
        outdevices["devices"] = array["5"]
    else:
      outdevices["devices"] = array["5"]+array["24"]
    json_object = json.dumps(outdevices) 
  print(json_object)

def deleteclient(aps, mac):
  deleted = False
  for ak, ap in enumerate(aps):
      for ik, iface in enumerate(aps[ap]):
        if mac in aps[ap][iface]["data"]["clients"]["clients"]:
          aps[ap][iface]["data"]["clients"]["clients"].pop(mac)
          deleted = True
  if deleted:
    f = open(cache, "w")
    f.write(json.dumps(aps))
    f.close()
    print("deleted")
  else:
    print("nothing found")

if len(sys.argv) > 1:
  if sys.argv[1] == "kickclient":
    aps  = open(cache, "r").read()
    aps = json.loads(aps)
    if len(sys.argv) > 3:
      for router in routers:
        if router[0] == sys.argv[4]:
          break
      auth = authenticate(router)
      url = "http://"+router[0]+"/cgi-bin/luci/rpc/sys?auth="+auth
      data = {}
      data["method"] = "exec"
      data["params"] = ["ubus call hostapd."+sys.argv[3]+" del_client \"{'addr':'"+sys.argv[2]+"', 'reason':1, 'deauth':true, 'ban_time':10000}\""]
      req = requests.post(url, data = json.dumps(data), headers=headers)
    deleteclient(aps, sys.argv[2])
    req = requests.post(homeassistant_wifi_update, data = json.dumps(""), headers=headers)
    exit()

  if sys.argv[1] == "addclient":
    #{"info":{ "status": "ENABLED", "bssid": "aa:bb:cc:dd:ee:ff", "ssid": "SSID", "freq": 5260, "channel": 52, "op_class": 119, "beacon_interval": 100, "phy": "wlan1", "rrm": { "neighbor_report_tx": 1 }, "wnm": { "bss_transition_query_rx": 0, "bss_transition_request_tx": 0, "bss_transition_response_rx": 0 }, "airtime": { "time": 2269720, "time_busy": 36058, "utilization": 5 }, "dfs": { "cac_seconds": 60, "cac_active": false, "cac_seconds_left": 0 } },"mac":"aa:bb:cc:dd:ee:ff","iface":"wlan1","router":"a.b.c.d","clients":{ "freq": 5260, "clients": { "aa:bb:cc:dd:ee:ff": { "auth": true, "assoc": true, "authorized": true, "preauth": false, "wds": false, "wmm": true, "ht": true, "vht": true, "he": true, "wps": false, "mfp": false, "rrm": [ 49, 8, 1, 0, 0 ], "extended_capabilities": [ 0, 0, 0, 0, 0, 0, 0, 64 ], "aid": 1, "bytes": { "rx": 13850, "tx": 10560 }, "airtime": { "rx": 14782, "tx": 279500 }, "packets": { "rx": 66, "tx": 48 }, "rate": { "rx": 24000, "tx": 541600 }, "signal": -53, "capabilities": { "vht": { "su_beamformee": true, "mu_beamformee": false, "mcs_map": { "rx": { "1ss": 9, "2ss": 9, "3ss": -1, "4ss": -1, "5ss": -1, "6ss": -1, "7ss": -1, "8ss": -1 }, "tx": { "1ss": 9, "2ss": 9, "3ss": -1, "4ss": -1, "5ss": -1, "6ss": -1, "7ss": -1, "8ss": -1 } } } } } } }}
    newClient = sys.argv[2].replace("'", "\"").replace("False", "\"False\"").replace("True", "\"True\"")
    newClient = json.loads(newClient)
    aps  = open(cache, "r").read()
    aps = json.loads(aps)
    deleteclient(aps, newClient["mac"])
    collectedClient = {}
    collectedClient["mac"] = newClient["mac"]
    collectedClient["iface"] = newClient["iface"]
    collectedClient["router"] = newClient["router"]
    collectedClient["rate"] = newClient["clients"]["clients"][newClient["mac"]]["rate"]
    collectedClient["signal"] = newClient["clients"]["clients"][newClient["mac"]]["signal"]
    if newClient["iface"] in aps[newClient["router"]]:
      aps[newClient["router"]][newClient["iface"]]["data"]["clients"]["clients"][newClient["mac"]] = collectedClient
    else:
      aps[newClient["router"]][newClient["iface"]] = {}
      aps[newClient["router"]][newClient["iface"]]["data"]["clients"]["clients"][newClient["mac"]] = collectedClient

    f = open(cache, "w")
    f.write(json.dumps(aps))
    f.close()
    req = requests.post(homeassistant_wifi_update, data = json.dumps(""), headers=headers)
    print(req)
    exit()

if not os.path.exists(cache):
  use_cache = False
elif older(cache, 1800):
  use_cache = False

if len(sys.argv) > 1:
  if sys.argv[1] == "nocache":
    use_cache = False
  if len(sys.argv) > 2:
    if sys.argv[2].isdigit() and int(sys.argv[2])<len(routers)+1:
      routers = [routers[int(sys.argv[2])-1]]  

if not use_cache:
  with FileLock(cache):
    for rk, router in enumerate(routers):
      routerdata = {}
      auth = authenticate(router)
      url = "http://"+router[0]+"/cgi-bin/luci/rpc/sys?auth="+auth
      data = {}
      data["method"] = "exec"
      data["params"] = ["ubus list hostapd.*"]
      req = requests.post(url, data = json.dumps(data), headers=headers)
      ifaces = json.loads(req.text)["result"].split("\n")[:-1]
      for iface in ifaces:
        ifacename = iface.replace("hostapd.", "")
        routerdata[ifacename] = {}
        data["params"] = ["ubus call "+iface+" get_status"]
        req = requests.post(url, data = json.dumps(data), headers=headers)
        status = json.loads(json.loads(req.text)["result"])
        routerdata[ifacename]["info"] = status
        routerdata[ifacename]["info"]["router"] = router[0]
        data["params"] = ["ubus call "+iface+" get_clients"]
        req = requests.post(url, data = json.dumps(data), headers=headers)
        clients = json.loads(json.loads(req.text)["result"])
        routerdata[ifacename]["data"] = {}
        routerdata[ifacename]["data"]["iface"] = ifacename
        routerdata[ifacename]["data"]["clients"] = clients
      aps[router[0]] = routerdata
  f = open(cache, "w")
  f.write(json.dumps(aps))
  f.close()
  req = requests.post(homeassistant_wifi_update, data = json.dumps(""), headers=headers)
else:
  aps = open(cache, "r").read()
  aps = json.loads(aps)
  
try:
  aps_live = {}
  for router in routers:
    aps_live[router[0]] = aps[router[0]]
  aps_live = json.dumps(aps_live)
  output(aps_live)
except:
  print('{"devices": []}')