# Home Setup

## Tools

                    
Automation  | Access | Media | Monitoring
------------- | ------------- | ---------- | ---------
[HomeAssistant](https://www.home-assistant.io/) | [OPNSense](https://opnsense.org/) | [Jellyfin](https://jellyfin.org/) | [Graylog](https://www.graylog.org/)
[MariaDB](https://mariadb.org/) | [Nginx Proxy Manager](https://nginxproxymanager.com/) | [TvHeadend](https://tvheadend.org/) | [GoAccess](https://goaccess.io/)
[Mosquitto](https://mosquitto.org/) | [AdGuard](https://adguard.com/) | [OSCam](https://trac.streamboard.tv/oscam/) |[Munin](https://munin-monitoring.org/) 
[Frigate](https://frigate.video/) |  [OpenWRT](https://openwrt.org/) |  [MiniSatIP](https://github.com/catalinii/minisatip) |  [Grafana](https://grafana.com/)
[Motion](https://motion-project.github.io/) | [Wireguard](https://www.wireguard.com/) | [Nextcloud](https://nextcloud.com/de/) | [Smokeping](https://oss.oetiker.ch/smokeping/)
[Zigbee2mqtt](https://www.zigbee2mqtt.io/) | [KVM](https://www.linux-kvm.org/) | [rtsp-simple-server](https://github.com/aler9/rtsp-simple-server) | [InfluxDB](https://www.influxdata.com/)
[PS5mqtt](https://github.com/FunkeyFlo/ps5-mqtt) | [Authentik](https://goauthentik.io/) | [v4l2rtspserver](https://github.com/mpromonet/v4l2rtspserver) | 
[Bt-mqtt-gateway](https://github.com/zewelor/bt-mqtt-gateway) | [Guacamole](https://guacamole.apache.org/) | [Hyperion.NG](https://github.com/hyperion-project/hyperion.ng) | 
[Scrypted](https://www.scrypted.app/) | [Vaultwarden](https://github.com/dani-garcia/vaultwarden) | [Hue-Sync](https://github.com/jdmg94/Hue-Sync) |  
[Deepstack](https://www.deepstack.cc/) | [Code Server](https://github.com/coder/code-server) | [FFMpeg](https://ffmpeg.org/) | 
[OpenZwave](https://github.com/openzwave/) | [Lighttpd](https://www.lighttpd.net/) |  | 
[Speedtest2mqtt](https://github.com/moafrancky/speedtest2mqtt) | [AutoFS](https://wiki.archlinux.org/title/autofs) |  | 
[Docker](https://www.docker.com/) | [SSLH](https://github.com/yrutschle/sslh) |  | 
[WMBusmeter](https://github.com/weetmuts/wmbusmeters) | [Jump](https://github.com/daledavies/jump)| |
| [Stunnel](https://www.stunnel.org/)||

## Docker Compose Files
My Systems heavily rely on Docker and docker compose,
you can find the configurations in `./docker-compose`


## Hardware

### Hosts
- 8x Raspberry Pi (models 2 - 4)
- 1x Atom E3845 running OPNSense
- 1x Odroid XU-4
- 1x BananaPi M1
- 1x Synology DS220j
- 1x Lenovo M900, i7-6700

### Zigbee
- 1x [CC2652R](https://electrolama.com/projects/zig-a-zig-ah/)
- 12x Hue Motion Sensor
- 3x Hue Tap Dial Switch
- 2x Hue Dimmer Remote
- 5x Aqara Door Sensor
- 3x Hue Outdoor Sensor
- 18x Hue Bulbs (LWO003,LLC010,LTW010,LLC020,LST001,LLC012,LCX001)
- 3x Ikea Tradfri Bulbs (E27)
- 9x Ikea Tradfri Outlet
- 1x Hue Bridge V2 (for Hue Gradient Strip)

### Zwave
- Aeotec Z-Stick Gen5 (ZW090)
- 6x Fibaro (FGS22x)
- 5x Fibaro Outlet (FGWP102)
- 3x Aeotec Multi Sensor (ZW074)

### Cameras
- 1x KKmoon 1080p PTZ
- 1x Raspberry Pi Camera
- 1x Peephole Camera (analogue, converted to h264/rtsp with vl2rtsp)

### Openwrt
- 3x OpenWRT AP
  - AVM FRITZ!WLAN Repeater 1750E
  - Ubiquiti UniFi 6 LR v1
  - GL.iNet GL-MT1300
- APs monitoring in HomeAssistant with scripts in `./openwrt` and `./homeassistant/openwrt``

### IpTV
- Multiple Tuners feed into TvHeadend in LAN.4
  - 14x DVB-S2
  - 2x DVB-C2
- MiniSatIP forwards tuners from WAN&WAN2 to LAN.4
- Jellyfin serves Remote Clients

### TV
- LG Webos 5 Tv
  - rooted, mapped remote buttons to open apps on AppleTV
  - runs Piccap to send Framebuffer to Hyperion
  - Hyperion outputs to a named pipe
  - named pipe gets read by Hue-Sync
  - Hue-Sync sends color data to Hue Bridge and the Hue Gradient

### Misc
- Shelly3em, Shelly
- Techem Warm/Cold Water Meter (wmbusmeter)
- Netatmo Weather Station
- 2x Apple HomePod, 1x AppleTv
- 1x Galaxy Tab A
- Eve Aqua

### Experiences
- None

# TODO
- clean up a lot of automations, its a dumpster fire

# Special Thanks
- @ Home-Assistant devs
- [@atxbyea](https://github.com/atxbyea)
- [@DubhAd](https://github.com/DubhAd)
- Discord Folks
- [rootmytv](https://github.com/RootMyTV/RootMyTV.github.io) devs
