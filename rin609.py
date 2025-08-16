CLIENT_SECRETS_FILE = "client_secret.json"

SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'

import os
import re
import pickle
import json
from time import sleep, time
import serial

import argparse

from bs4 import BeautifulSoup

encode="koi7_n1"

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

    def flush(self):
        return


def clearRin(tty):
	#clear screen
    tty.write(b'\1f')
    sleep(0.1)

pos = 0
row = 0

def sendRin(tty, message):
    global pos
    global row
    start_pos = pos
    print(message)
    length = len(message)
    for item in range(length):
        symbol = message[item:item+1]
        tty.write(symbol)
        pos += 1
        if (symbol == b'\x0a') or (pos > 80):
            delay = (pos - start_pos)*0.0176 + 0.05
            sleep(delay)
            pos = 0
            start_pos = pos
            tty.flush()
    tty.flush()
    delay = (pos - start_pos)*0.0176
    sleep(delay)
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


def get_view_count(youtube):
    request = youtube.channels().list(
        part="snippet,contentDetails,statistics",
        mine=True
    )
    response = request.execute()
    items = response.get('items')
    statistics = items[0].get('statistics')
    views = statistics.get('viewCount')
    subscribers = statistics.get('subscriberCount')
    return (views, subscribers)

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
    if encode == "koi7-n2":
        text = text.upper()
    text = text.replace('Ъ','Ь')
    text = text.replace('Ё','Е')
    text = text.encode(encoding = encode, errors = 'ignore')
    return text

def decode_comment(symbol):
    text = str(symbol)
    text = text.decode(encoding = encode, errors = 'ignore')
    return text

def post_comment(text, youtube, chatId):
    request = youtube.liveChatMessages().insert(
        part="snippet",
        body={
            "snippet": {
                "liveChatId": chatId,
                "type": "textMessageEvent",
                "textMessageDetails": {
                    "messageText": text
                }
            }
        }
    )
    response = request.execute()
    return response

def stats_info(youtube):

    views, subscribers = get_view_count(youtube)
    print("My channel have ", views, " views")
    print("My channel have ", subscribers, " subscribers")

parity = {
    0 : serial.PARITY_NONE,
    1 : serial.PARITY_EVEN,
    2 : serial.PARITY_ODD
}

def connect_tty(tty, file):
    terminal = json.load(open(args.terminal))
    term_parity = parity[terminal["parity"]]
    userport = terminal["userport"]
    dsrdtr = terminal.get("dsrdtr", False)
    rtscts = terminal.get("rtscts", False)
    global encode
    encode = terminal.get("encode", "koi7_n2")
    if args.userport != None:
        userport = args.userport
    tty = serial.Serial(userport,
                            terminal["baudrate"],
                            bytesize=terminal["bytesize"],
                            timeout=terminal["timeout"],
                            parity=term_parity,
                            dsrdtr=dsrdtr,
                            rtscts=rtscts,
                            stopbits = terminal["stopbits"])
    return tty

def test_rin(tty):
    letters = []
    for i in range(256):
        letters.append(i)
    let_b = bytes(letters)
    for i in range(0,256, 16):
        tty.write(let_b[i:i+17])
        tty.write(b'\r\n')
        tty.flush()
    for rows in range(3):
        sendRin(tty, encode_comment('в чащах юга жил бы цитрус? да, но фальшивый экземпляр!\n'))
        sendRin(tty, encode_comment('В ЧАЩАХ ЮГА ЖИЛ БЫ ЦИТРУС? ДА, НО ФАЛЬШИВЫЙ ЭКЗЕМПЛЯР!\n'))
    tty.write(b'\07') #bell

def run_live_chat(youtube, tty, videoId, skip):
    if videoId != None:
        apiRequestCount = 0
        liveChatId = get_chat_id(videoId, youtube)
        if liveChatId == None:
            print("liveChatId with videoId = ", videoId, " Not found!")
            return
        apiRequestCount += 4
        next_page_token = None
        if skip == None:# not a error
            next_page_token = skip_comments(liveChatId, youtube, next_page_token)
            apiRequestCount += 2
        last_name = ''
        threadControl = True
        while threadControl:
            length, next_page_token, last_name = process_comments(RinTTY, liveChatId, youtube, next_page_token, last_name)
            apiRequestCount += 2
            delay = 4#4 seconds if no comments were handled
            if length:
                delay = 2
            sleep(delay)
            if (apiRequestCount % 1000)  == 0:
                print("We spent ", int(apiRequestCount/100), "% of limit")
                RinTTY.write(bytes.fromhex('07'))
    else:
        print("Add youtube stream ID to start. use --skip option to skip previous comments")

def parse_html(tty, rootDir, filePath):
    if not os.path.isfile(filePath):
        return
    with open(filePath, encoding="utf-8") as file:
        soup = BeautifulSoup(file, 'html.parser')
        print(filePath, rootDir, soup.title.text)
        ## try to parse top page
        divBlob = soup.find_all("div", {"class": "b-page-txt"})
        for div in divBlob:
            ## looking for ul_razdel:
            ulBlob = div.find_all("ul", {"class": "ul_razdel"})
            for ul in ulBlob:
                liBlob = ul.find_all("li")
                for li in liBlob:
                    aBlob = li.find_all('a')
                    for a in aBlob:
                        link = a.get('href')
                        print(a.text, link)
                        if "http" in link:
                            if "computer-museum" not in link:
                                continue
                        link = re.sub("^http.*\.ru", '', link)
                        if '#' in link:
                            continue
                        if link[0] == "/":
                            link = link[1:]
                            while link[0] == "/":
                                link = link[1:]
                            dir_path = rootDir
                        else:
                            dir_path = os.path.dirname(path)
                        if link[-1] == "/":
                            link = link + "index.html"
                        if ".htm" in link or ".html" in link:
                            print(dir_path, link, os.path.join(dir_path, link))
                            parse_html(RinTTY, rootDir, os.path.join(dir_path, link))
            textBlob = div.find_all("p", {"class": "StoryBody"})
            for text in textBlob:
                print(text.text)
                sendRin(tty, encode_comment(text.text))
                sendRin(tty, encode_comment('\n'))
            #for ul in ulBlob
            #print(div)

def parse_head_html(RinTTY, path):
    with open(path, encoding="utf-8") as file:
        soup = BeautifulSoup(file, 'html.parser')
        print(soup.title.text)
        ## try to parse top page
        divBlob = soup.find_all("div", {"class": "b-index-section"})
        for div in divBlob:
            ulBlob = div.find_all("ul")
            for ul in ulBlob:
                liBlob = ul.find_all("li")
                for li in liBlob:
                    aBlob = li.find_all('a')
                    for a in aBlob:
                        print(a.text, a.get('href'))

def text_txt(tty, filePath):
    if not os.path.isfile(filePath):
        return
    with open(filePath, encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            chunks, chunk_size = len(line), 60
            cut = [line[i:i+chunk_size] for i in range(0, chunks, chunk_size) ]
            for ch in cut:
                print(ch)
                sendRin(tty, encode_comment(ch))
                sendRin(tty, encode_comment('\r\n'))

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--userport')
    parser.add_argument('-t', '--terminal')
    parser.add_argument('-v', '--videoId')
    parser.add_argument('-s', '--skip', nargs='?', default = False)
    parser.add_argument('-m', '--mode', type = str, choices=['liveChat', 'statistics', 'test','html', 'text'])
    parser.add_argument('--json')

    args = parser.parse_args()

    RinTTY = None

    if args.terminal != None:
        RinTTY = connect_tty(RinTTY, args.terminal)

    if RinTTY == None:
        RinTTY = RinEmul()
    else:
        clearRin(RinTTY)

    if args.mode == "test":
        test_rin(RinTTY)
    elif args.mode == "text":
        text_txt(RinTTY, args.json)
    elif args.mode == "html":
        if args.json and os.path.isfile(args.json):
            cite = json.load(open(args.json))
            if not os.path.isdir(cite['path']):
                print("set proper path in json file")
                exit()
            for folder in cite['folders']:
                path = os.path.join(cite['path'], folder, "index.html")
                print(path, os.path.isfile(path))
                parse_html(RinTTY, cite['path'], path)
        else:
            print("set proper --html<file path>")
    else:
        youtube = get_authenticated_service()
        if args.mode == "liveChat":
            run_live_chat(youtube, RinTTY, args.videoId, args.skip)
        if args.mode == "statistics":
            stats_info(youtube)

    RinTTY.close()



