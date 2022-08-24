from urllib.parse import urlencode
from urllib.request import urlopen, Request
import json
from imaplib import IMAP4_SSL
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport import requests
import google.auth.transport.requests
import os
import webbrowser
from email.message import EmailMessage
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import PKCS1_v1_5
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
import hashlib
import smtplib
import base64
import random
import json
import os
import email
import imaplib


def read_cred(value):
    with open('credentials.json', 'r') as cred_file:
        Recived_Credential = json.load(cred_file)
    return Recived_Credential['installed'][value]

def read_token(user_email,value):
    with open(user_email+'_token.json', 'r') as cred_file:
        Recived_Credential = json.load(cred_file)
    return Recived_Credential[value]

def generate_auth_url():
    url = "https://accounts.google.com/o/oauth2/auth?" + urlencode({
        "client_id": read_cred("client_id"),
        "redirect_uri": "urn:ietf:wg:oauth:2.0:oob",
        "scope": "https://mail.google.com/ email",
        "response_type": "code",
    })
    return url

def save_user(user_email):
    if os.path.exists('past_users.json'):
        #read the json file and update the tempdic
        with open('past_users.json', 'r') as f:
            print("in open past users")
            tempdic = json.load(f)
            
            tempstr = tempdic["Past_users"].split(', ')
            
            if user_email in tempstr:
                print("user already exists")
            else:
                tempstr = tempdic["Past_users"] + ", " + user_email
                tempdic.update({"Past_users":tempstr})
                    
        #write josn file with contents in tempdic
        with open('past_users.json', 'w') as f:
            json_str = json.dumps(tempdic)
            f.write(json_str)
        
    else:
        with open('past_users.json', 'w') as f:
            print("in write past users")
            tempdic = {"Past_users":user_email}
            json_str = json.dumps(tempdic)
            f.write(json_str)
            
def save_token(user_email,access_token):
    with open(user_email + "_token.json",'w') as f:
        print("in save token")
        tempdic = {"access_token":access_token}
        json_str = json.dumps(tempdic)
        f.write(json_str)
            
def conn_with_imap(code):
    try:
        # exchange code with access token
        with urlopen(Request("https://accounts.google.com/o/oauth2/token", data=urlencode({
                "client_id": read_cred("client_id"),
                "client_secret": read_cred("client_secret"),
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

        print("in imap, saving email")
        save_user(ures["email"])
        
        print("saving credentials to json")
        save_token(ures["email"], eres["access_token"])
        
        imap.select("INBOX")
    
        print("in inbox")
    
        search_term = input("enter the term you want to search\n")
        
        msgs = get_emails(search("ALL",search_term,imap),imap)
    
        for msg in msgs: 
            print(get_body(email.message_from_bytes(msg[0][1])))
        
        
    except Exception as e:
        print(e)
        print("")
        
def conn_with_exist(user_email,access_token):
    # connect to imap
    mail = IMAP4_SSL("imap.gmail.com")

    # authenticate the gmail way
    mail.authenticate("XOAUTH2", lambda x:
        "user=%s\1auth=Bearer %s\1\1" % (user_email, access_token))

    mail.select("INBOX")
    
    print("in inbox")
    
    _, search_data = mail.search(None, 'ALL')                        #underscore is used to skip the first data in the tuple(data with no use)
    my_message = []
    
    for num in search_data[0].split():                                  #turning bytes returned from search data in to a list of byte based on spaces(defualt)
        email_data = {}
        _, data = mail.fetch(num, '(RFC822)')                           #getting the msg data from gmail
        _, b = data[0]                                                  #data in bytes
        
        email_message = email.message_from_bytes(b)                     #turnind byte into str

        for header in ['subject', 'to', 'from', 'date']:
            print("{}: {}".format(header, email_message[header]))
            email_data[header] = email_message[header]
            #print("in header parsing")
            
        my_message.append(email_data)
        
        #getting the body byte, turn it into str, then remove extra bits
        body_text = get_body(email_message)
        body_text = str(body_text, 'utf-8')
        body_text = body_text.replace('\r', '')
        body_text = body_text.replace('\n', '')
        
        print(body_text)
    
def get_body(msg):
    if msg.is_multipart():
        return get_body(msg.get_payload(0))
    
    else: 
        return msg.get_payload(None,True)
    
def search(key, value, con): #returns result byte matches the search parameter that can be put in get_email
    result, data = con.search(None, key,'"()"'.format(value))
    return data

def get_emails(result_bytes,con):
    msgs = []
    for num in result_bytes[0].split():
        typ, data = con.fetch(num, '(RFC822')
        msgs.append(data)
    return msgs

while True:
    menu_select  = input("Enter 1 to Login to Gmail\nEnter 2 exit\n\n")
    print("")
    
    if menu_select == "1":
        login_select = input("Enter 1 to Login as New User\nEnter 2 to Login as Existing User\n\n")
        
        if login_select == "1":
            print("Redirecting...")
            webbrowser.open(generate_auth_url())
            
            while True:
                code = input("paste reponse code: ")
                print("")
                
                if code == "exit":
                    break
                else:
                    conn_with_imap(code)
                    break
        
        elif login_select == "2":
            print("Checking Existing User....")
            if os.path.exists("past_users.json"):
                
                with open('past_users.json', 'r') as f:
                    
                    print("in open past users")
                    tempdic = json.load(f)
                    tempstr = tempdic["Past_users"].split(', ')
                    
                    for i in tempstr:
                        print(i)
                    print("")
                    
                    while True:
                        user_select = input("Enter the email you want to login as, Enter exit to cancle\n")
                        if user_select == "exit":
                            print('')
                            break
                        else:
                            if user_select.lower() in tempstr:
                                print("logging in as: " + user_select.lower())
                                
                                conn_with_exist(user_select.lower(), read_token(user_select.lower(),"access_token"))
                                
                                break
                            
                            else:
                                print("Pls Enter a Valid Email address")
                            
            else:
                print("There is no Existing User currently")
        
    elif menu_select == "2":
        break