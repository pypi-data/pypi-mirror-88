"""
    Client side functions for working with LDM framework.
"""

import json
import requests
import shutil
import sys

#SERVER_URL = "http://127.0.0.1:80"

DEFAULT_SERVER_URL = "http://localhost:5000"

SERVER_URL = DEFAULT_SERVER_URL
CURR_PROJECT_ID = ""
CURR_RUN_ID = ""
TOKEN = ""


def log(msg, role_name = "" ):
    """ Log message msg to server.
  
    Parameters: 

    msg (string): Message to log 

    role_name (string): Role name of a message. Role name is optional and can be ommited.
  
    Returns: 

    None  
    """
    print("logging msg to server")
    try:
        print(TOKEN)
        print("logging run " + CURR_RUN_ID)
        r = requests.get(
            SERVER_URL + "/log", 
            {
                'run_id': CURR_RUN_ID, 
                'msg': msg, 
                'token': TOKEN,
                'role_name': role_name
            },
            headers={'Content-Type':'application/json', "Authorization": "Bearer " + TOKEN}
        )
        if r.status_code != 200:
            print(r)
            print(r.content)
            print("Log FAILED. \n" + r.json())
            # print("Log FAILED. \n" + r.json()['err'])
    except:
        print("Unknown Error in log(msg)")
        print(sys.exc_info()[0])
        raise


def start_run(project_ID, comment = "", git_commit_url = "" ):
    """ 
    Start a new run.
  
    Parameters: 

    project_ID (string): ID of a project this newly started run will belong to.

    comment (string): Comment for a run.  This parameter is optional and can be ommited.

    git_commit_url (string): URL of a git commit representing the state of a code base used in this run. This prm is optional and can be ommited.
  
    Returns: 

    None  
    """
    print("starting run")

    global CURR_PROJECT_ID
    global CURR_RUN_ID
    global TOKEN

    CURR_PROJECT_ID = project_ID
    try:
        print(TOKEN)
        print(type(TOKEN))
        print('')
        r = requests.get(
            # SERVER_URL + "/start_run/" + CURR_PROJECT_NAME, 5fcb9ad87b0d77697fab4bd4
            SERVER_URL + "/start_run/" + project_ID,
            {
                'token': TOKEN, 
                'comment': comment, 
                'git_commit_url': git_commit_url
            },
            headers={'Content-Type':'application/json', "Authorization": "Bearer " + TOKEN}
        )
        #TODO: add authorization header bearer + " " + token
        print(r)
        print(r.json())
        if r.status_code == 200:
            CURR_RUN_ID = r.json()['id']
            print(CURR_RUN_ID)
            print("START RUN SUCCEEDED.")
        else:
            print("START RUN FAILED. \n" + r.json()['err'])
    except:
        print("Unknown Error in start_run.")
        print(sys.exc_info()[0])
        raise


def finish_run():
    """ 
    Finish the current run.
  
    Parameters: 
  
    Returns: 

    None
  
    """    
    # finish current run
    global CURR_RUN_ID
    print("finishing run")
    try:
        print(" finish run run_id " + CURR_RUN_ID)
        r = requests.get(
            SERVER_URL + "/finish_run", 
            {
                'run_id': CURR_RUN_ID, 
                # 'token': TOKEN
            },
            headers={'Content-Type':'application/json', "Authorization": "Bearer " + TOKEN}
        )
        if r.status_code == 200:
            print("FINISH RUN SUCCEEDED.")
        else:
            print("Finish run FAILED. \n" + r.json()['err'])
    except:
        print("Unknown error in finish_run.")
        print(sys.exc_info()[0])
        raise


def upload_file(file_name, role_name = "", comment = "" ):
    """ 
    Upload file (file_name) to the logging server and attaches it to the current run.
  
    Parameters: 

    file_name (string): File path (on a local machine) of file to be uploaded.

    comment (string): Comment for a file to be uploaded.  This prm is optional and can be ommited.

    role_name (string): Role name for a file to be uploaded. This prm is optional and can be ommited.

  
    Returns: 

    None
  
    """    
    global CURR_RUN_ID
    try:
        with open(file_name, 'rb') as f:
            r = requests.post(SERVER_URL + '/upload_file',
                              params = {
                                  'run_id' : CURR_RUN_ID,
                                  'token' : TOKEN,
                                  'comment': comment,
                                  'role_name': role_name
                              },
                              files={'file': f}
            )
    except:
        print("Unknown error in upload_file.")
        print(sys.exc_info()[0])
        raise


def login(user_id, psw, server_url_prm = DEFAULT_SERVER_URL ):
    """ 
    Authorize user user_id with password psw on server server_url_prm.
    
    Parameters: 
    
    user_id (string): User ID.

    psw (string): User password.

    server_url_prm (URL): URL of an instance of LDM framework to connect to. All subsequent calls to LDM framework functions will be directed to this URL. This prm is optional and can be ommited, in this case default URL of "http://localhost:5000" will be used .
  
    Returns: 
    
    True in case of success, False otherwise.  
    """   
    try:
        global TOKEN
        print(TOKEN)
        global SERVER_URL
        
        SERVER_URL = server_url_prm

        r = requests.post(
            SERVER_URL + '/login/', 
            json={
                'email': user_id, 
                'password': psw
            }
        )
        
        if r.status_code == 200:
            # print(r)
            # print(r.json())
            print(r.json()['response']['token'])
            # token = r.json()['token'].split('.')
            # print(token)
            #TOKEN = r.json()['token']
            TOKEN = r.json()['response']['token']
            print(TOKEN)
            print("LOGIN succeeded.")
            return True
        else:
            print('Login failed.')
            return False
    except:
        print("Failed to login ... ")
        print("Unknown error in login.")
        e = sys.exc_info()[0]
        print(e)


def get_local_filename_from_url(url):
    local_filename = url.split('/')[-1]
    # print( local_filename )
    quest_mark_ind = local_filename.find("?")
    if quest_mark_ind != -1:
        local_filename = local_filename[0:quest_mark_ind]
    # print(local_filename)
    return local_filename


def download_file_as_stream(url):
    """ 
    Download a file located at url and store it in a current dir.
    
    Parameters: 
    
    url (string): URL of file to download.

    Returns: 
    
    Name of a file downloaded.  
    """   
    local_filename = ""
    try:
    # https://stackoverflow.com/questions/16694907/download-large-file-in-python-with-requests
    # see second answer

        local_filename = get_local_filename_from_url( url )
        with requests.get(url, stream=True) as r:
            with open(local_filename, 'wb') as f:
                # https://github.com/psf/requests/issues/2155#issuecomment-287628933
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)
                
    except:
        print("Failed to download file " + url)
        print("Unknown error in download_file as stream.")

    return local_filename


def download_file_naive(url):
    local_filename = get_local_filename_from_url( url )
    r = requests.get(url, allow_redirects=True)
    
    with open(local_filename, 'wb') as f:
        f.write(r.content)
    return local_filename


def download_file_by_chunks(url):
    # https://stackoverflow.com/questions/16694907/download-large-file-in-python-with-requests
    local_filename = get_local_filename_from_url( url )
    # NOTE the stream=True parameter below
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192): 
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)
                    # f.flush()
    return local_filename
