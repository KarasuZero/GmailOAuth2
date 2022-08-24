from urllib.parse import urlencode
from urllib.request import urlopen, Request
import json
from imaplib import IMAP4_SSL
import webbrowser
# create a Google app here https://console.developers.google.com
# then fill the following variables
GMAIL_CLIENT_ID = "318209208709-nsev09p1lsu5vt1eved2o0ghak2bgb30.apps.googleusercontent.com"
GMAIL_CLIENT_SECRET = "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"

# generate and print authorization link
# url = "https://accounts.google.com/o/oauth2/auth?" + urlencode({
#     "client_id": GMAIL_CLIENT_ID,
#     "redirect_uri": "urn:ietf:wg:oauth:2.0:oob",
#     "scope": "https://mail.google.com/ email",
#     "response_type": "code",
# })
# print("visit\n%s\n" % url)
# webbrowser.open(url)

# read response code
code = input("paste reponse code: ")
print("")

# exchange code with access token
with urlopen(Request("https://accounts.google.com/o/oauth2/token", data=urlencode({
        "client_id": GMAIL_CLIENT_ID,
        "client_secret": GMAIL_CLIENT_SECRET,
        "code": code,
        "redirect_uri": "urn:ietf:wg:oauth:2.0:oob",
        "grant_type": "authorization_code",
    }).encode())) as res:
    eres = json.loads(res.read())
    print("eres: %s"%(eres))

# request user email
with urlopen(Request("https://www.googleapis.com/oauth2/v2/userinfo", headers={
        "Authorization": "Bearer %s" % eres["access_token"],
    })) as res:
    ures = json.loads(res.read())
    print("ures: %s"%(ures))

# connect to imap
imap = IMAP4_SSL("imap.gmail.com", 993)

# authenticate the gmail way
imap.authenticate("XOAUTH2", lambda x:
    "user=%s\1auth=Bearer %s\1\1" % (ures["email"], eres["access_token"]))

# the following is just an example that shows available folders
# you can use any function provided by imaplib
# https://docs.python.org/3/library/imaplib.html

print("available folders:")
res,data = imap.list('""', "*")
for mbox in data:
    print(mbox.decode())

print("")