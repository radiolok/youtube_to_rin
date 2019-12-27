CLIENT_SECRETS_FILE = "client_secret.json"

SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'

import os
import pickle
import json
from time import sleep
import serial

import argparse

import google.oauth2.credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow


class RinEmul():
    def __init__(self):
        self.out_waiting = 0
        self.emulation = True

    def write(self, message):
        print(message, end='', flush=True)
        pass


def clearRin(tty):
	#clear screen
	tty.write(chr(0x1F))

pos = 0
row = 0

def sendRin(tty, message):
    global pos
    global row
    length = len(message)
    for item in range(length):
        symbol = chr(message[item])
        tty.write(symbol)
        pos += 1
        if (symbol == chr(0x0a)) or (pos > 79):
            pos = 0
            while tty.out_waiting > 0:
                pass
            sleep(0.1)
            if tty.emulation != None:
                print("")
    while tty.out_waiting > 0:
        pass
    return    

def get_authenticated_service():
    
    credentials = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            credentials = pickle.load(token)
    #  Check if the credentials are invalid or do not exist
    if not credentials or not credentials.valid:
        # Check if the credentials have expired
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CLIENT_SECRETS_FILE, SCOPES)
            credentials = flow.run_console()

        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(credentials, token)

    return build(API_SERVICE_NAME, API_VERSION, credentials = credentials)

def get_chat_id(link, youtube):    
    request = youtube.liveBroadcasts().list(
        part="snippet,contentDetails,status",
        id=link
    )
    response = request.execute()
    items = response.get('items')
    snippet = items[0].get('snippet')
    liveChatId = snippet.get('liveChatId')
    return liveChatId

def skip_comments(id, youtube, next_page_token):
    response = youtube.liveChatMessages().list(
        liveChatId=id,
        part="id,snippet,authorDetails",
        pageToken = next_page_token
    ).execute()
    nextPageToken = response.get('nextPageToken')
    return (nextPageToken)

def process_comments(tty, id, youtube, next_page_token, last_name):
    response = youtube.liveChatMessages().list(
        liveChatId=id,
        part="id,snippet,authorDetails",
        pageToken = next_page_token
    ).execute()
    items = response.get('items')
    length = 0
    for item in items:
        name = item.get('authorDetails').get('displayName')
        #print (name)
        message = item.get('snippet').get('displayMessage')
        #print(message)
        message_encoded = encode_comment(message)
        if len(message_encoded) == 0: #skip empty messages
            pass
        #for new author print his name first:
        if name != last_name:
            if len(last_name):
                sendRin(tty, encode_comment('\n'))
                sleep(0.1)
                length += 1
            name_encoded = encode_comment(name)
            sendRin(tty, name_encoded)
            length += len(name_encoded)
            sendRin(tty, encode_comment(": "))
            length += 2
        else: #for next comment just add it to the same line with separation
            sendRin(tty, encode_comment(", "))
            length += 2
        sendRin(tty, message_encoded)
        length += len(message_encoded)
        last_name = name
    nextPageToken = response.get('nextPageToken')
    return (length, nextPageToken, last_name)

def encode_comment(text):
    text = text.upper()
    text = text.replace('Ъ','Ь')
    text = text.encode(encoding = 'koi7_h2', errors = 'ignore')
    return text

def decode_comment(symbol):
    text = str(symbol)
    text = text.decode(encoding = 'koi7_h2', errors = 'ignore')
    return text

def post_comment(text, youtube):
    request = youtube.liveChatMessages().insert(
        part="snippet",
        body={
            "snippet": {
                "liveChatId": liveChatId,
                "type": "textMessageEvent",
                "textMessageDetails": {
                    "messageText": text
                }
            }
        }
    )
    response = request.execute()
    return response


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--userport')
    parser.add_argument('-t', '--test')
    parser.add_argument('-y', '--youtube')
    parser.add_argument('-s', '--skip')

    args = parser.parse_args()

    RinTTY = None

    if args.userport != None:
        RinTTY = serial.Serial(args.userport, 625, bytesize=7, timeout=0,
                            parity=serial.PARITY_EVEN, stopbits = 2)

    if RinTTY == None:
        RinTTY = RinEmul()

    clearRin(RinTTY)
    
    if args.test != None:
        for rows in range(12):
            sendRin(RinTTY, encode_comment('Проверка сообщения с переносом строки\n'))
            sendRin(RinTTY, encode_comment('Проверка сообщения с переносом строки и текстом, который гораздо длиннее 80 символов и поэтому потребует еще одного переноса строки\n'))
        exit()
    # When running locally, disable OAuthlib's HTTPs verification. When
    # running in production *do not* leave this option enabled.
    # os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    # Get credentials and create an API client
    if args.youtube != None:
        apiRequestCount = 0
        youtube = get_authenticated_service()
        liveChatId = get_chat_id(args.youtube, youtube)
        apiRequestCount += 4
        next_page_token = None
        if args.skip != None:
            next_page_token = skip_comments(liveChatId, youtube, next_page_token)
            apiRequestCount += 2
        last_name = ''
        while True:
            length, next_page_token, last_name = process_comments(RinTTY, liveChatId, youtube, next_page_token, last_name)
            apiRequestCount += 2
            sleep(2)
            if (apiRequestCount % 100)  == 0:
                print("We spent ", int(apiRequestCount/100), " of limit")
    else:
        print("Add youtube stream ID to start. use skip option to skip previous comments")
    
