## Description

This scripts can be used for grabbing liveChat messages from youtube Streams in Real-Time and sending them to Serial port.

## Prerequisites

*   Python 2.6 or greater

*   The pip package management tool

    ```
    pip install beautifulsoup4 pyserial
    ```

*   The Google APIs Client Library for Python:
    ```
    pip install --upgrade google-api-python-client
    ```
*   The google-auth, google-auth-oauthlib, and google-auth-httplib2 for user authorization.
    ```
    pip install --upgrade google-auth google-auth-oauthlib google-auth-httplib2
    ```
 
## Youtube Setup

*   You need a [Google Account](https://www.google.com/accounts/NewAccount) to access the Google API Console, request an API key, and register your application.

*   [Create OAuth key](https://developers.google.com/youtube/v3/guides/authentication) and download it

## Installation

*   Clone repository to /RIN folder

*   Copy koi7-n2 file into <Python>/Lib/encodings/ folder
  
*   Run rin609.py
    ```
    rin609.py --userport COM1 --youtube StreamId
     ```

 
