from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport import requests
import google.auth.transport.requests
import os
import pickle

credentials = None

#reads credentials form picke file if it exist
if os.path.exists('token.pickle'):
    print('Loading Credentials From File...')
    with open('token.pickle', 'rb') as token:
        credentials = pickle.load(token)


if not credentials or not credentials.valid:
    #if we have a credential and it expired and we have a refresh token
    if credentials and credentials.expired and credentials.refresh_token: 
        print('Refreshing Access Token...')
        credentials.refresh(Request())
        
    else:
        print('Fetching New Tokens...')
        #read client secret from json and setting the socpe to readonly
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json',scopes=[
                'openid','https://www.googleapis.com/auth/gmail.readonly','https://www.googleapis.com/auth/userinfo.email'
            ]
        )

        #run local server on 8080, auth msg set to empty so it dosent clug up console
        flow.run_local_server(port=8080, prompt='consent',authorization_prompt_message='')
        credentials = flow.credentials

        # Save the credentials for the next run
        with open('token.json', 'w') as f:
            print('Saving Credentials for Future Use...')
         
            f.write(credentials.to_json())