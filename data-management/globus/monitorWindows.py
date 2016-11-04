#!/usr/bin/env python

import globus_sdk
import sys, os.path, time, datetime, logging
import ntpath, platform

from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

from globus_sdk import AuthClient, TransferClient, AccessTokenAuthorizer, RefreshTokenAuthorizer


#
# Script to automate the transfer of data files via globus
#

# On running the script the user will be given a url that can be copied into a browser to authenticate
# Follow the instructions and copy the resulting auth code back to the command prompt. Once authorized,
# the script will begin to watch for actions on files in the watched folder.

#
# This is the windows version of the monitor script which expects file paths in windows format
# globus does not accept windows path specs so they must be converted
#  use the syntax "/drive_letter/path", for example "/C/xinfo" lists the C:\xinfo directory.
# This version of the monitor script converts file paths into globus convertions 

#
# source_endpoint is the Globus endpoint id that is the origin for the data transfer
# target_endpoint is the Globus endpoint id of the destination of the transfer 
#
source_endpoint = "20be28ee-962c-11e6-b0a4-22000b92c261"
target_endpoint = "d47068d3-6d04-11e5-ba46-22000b92c6ec"  # (ucb#brc)

#
# watched_dir is the full path to the top folder of the data files for transfer

#
# patterns are the types of files that are valid for transfer
# endpoint_path is the base path at the endpoint where data files should be saved
#
watched_dir_windows = 'C:\\Users\\vagrant\\Documents'    # WINDOWS FOMAT PATH HERE
patterns = ['*.jpg', '*.tif', '*.png', '*.txt']
endpoint_path = '/~/globustest/'


#
# transfer_client is the globus client used to manage transfers
#
transfer_client = None
count = 0

#
# Verify that the user is on a Windows platform
#
def initialize():
    print("initialize")


def authorize():
    global transfer_client

    CLIENT_ID = '76af25c8-c96b-49b2-9be7-56767395db6b'
    client = globus_sdk.NativeAppAuthClient(CLIENT_ID)    
    client.oauth2_start_flow_native_app(refresh_tokens=True)

    authorize_url = client.oauth2_get_authorize_url()
    print('Please go to this URL and login: {0}'.format(authorize_url))

    auth_code = input('Please enter the code you get after login here: ').strip()
    token_response = client.oauth2_exchange_code_for_tokens(auth_code)

    # the useful values that you want at the end of this
    globus_auth_data = token_response.by_resource_server['auth.globus.org']
    globus_transfer_data = token_response.by_resource_server['transfer.api.globus.org']
    globus_refresh_token = globus_auth_data['refresh_token']
    globus_auth_token = globus_auth_data['access_token']
    globus_transfer_token = globus_transfer_data['access_token']
    globus_token_expires = globus_transfer_data['expires_at_seconds']
    ts = datetime.datetime.fromtimestamp(globus_token_expires).strftime('%Y-%m-%d %H:%M:%S')
    logging.info ("globus token expires: %s" % ts)

    # create the globus client
    auth_client = AuthClient( authorizer=AccessTokenAuthorizer(globus_auth_token))
    transfer_client = TransferClient( authorizer=AccessTokenAuthorizer(globus_transfer_token))


    # This refresh capability is not currently working as defined in the globus sdk
    # create a couple of authorizers
    auth_authorizer2 = RefreshTokenAuthorizer(globus_refresh_token,  client)


    # connect to the endpoint
    ep2result = transfer_client.endpoint_autoactivate(source_endpoint)
    logging.info ("source_endpoint autoactivate response code: %s" % ep2result["code"])
    logging.info ("source_endpoint autoactivate response message: %s" % ep2result["message"])


#
# This is the handler class that is called whenever actions take place in the watched folder.
# Currently the script only utilizes the on_created action to moe new files to Savio scratch
# However the user can modify to perform additional actions based on events
#

class MyEventHandler(PatternMatchingEventHandler):

    def on_moved(self, event):
        super(MyEventHandler, self).on_moved(event)
        logging.info("File %s was just moved" % event.src_path)

    def on_created(self, event):
        super(MyEventHandler, self).on_created(event)
        logging.info("File %s was just created" % event.src_path)
        self.transfer(event.src_path)

    def on_deleted(self, event):
        super(MyEventHandler, self).on_deleted(event)
        logging.info("File %s was just deleted" % event.src_path)

    def on_modified(self, event):
        super(MyEventHandler, self).on_modified(event)
        logging.info("File %s was just modified" % event.src_path)

    #
    # Transfer the file to the target folder defined in endpoint_path 
    # If the file is located in subfolders, the folder structure will be replicated under 
    # the endpoint_path folder. 
    #
    def transfer(self, file_path):
        global count
        label = "test transfer " + str(count)

        logging.info("Transfer file %s via globus" % file_path)
        tdata = globus_sdk.TransferData(transfer_client, source_endpoint,  target_endpoint, label=label)

        mvfilename = os.path.basename(file_path)
        logging.info("Transfer file endpoint_path: %s " % endpoint_path)
        logging.info ('Transfer file folder structure: %s' % os.path.dirname(file_path))

        prefix_path = os.path.commonprefix([watched_dir_windows, file_path])
        logging.info("Watched dir prefix: %s " % prefix_path)
        
        relative_path = os.path.relpath(file_path, prefix_path)
        relative_path_win = relative_path.replace('\\', '/')
        logging.info("relative path win: %s " % relative_path_win)

        target_path = endpoint_path + relative_path_win
        logging.info("target path: %s " % target_path)

        # globus does not accept windows path specs so they must be converted
        #  use the syntax "/drive_letter/path", for example "/C/xinfo" lists the C:\xinfo directory.
        file_path_fixed = file_path.replace('\\', '/')
        file_path_fixed = file_path_fixed.replace(':', '')
        file_path_fixed = '/' + file_path_fixed
        logging.info("filepath fixed: %s" % file_path_fixed)
        tdata.add_item( file_path_fixed,  target_path )

        submit_result = transfer_client.submit_transfer(tdata)
        print("Task ID:", submit_result["task_id"])

        logging.info("Transfer scheduled.")
        count = count + 1


def main():

    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s',  datefmt='%Y-%m-%d %H:%M:%S')

    logging.info ( 'source folder: %s' % os.path.dirname(watched_dir_windows))

    initialize()    

    authorize()

    # define the types of files that are of interest in the patterns variable
    event_handler = MyEventHandler(patterns=patterns)
    observer = Observer()

    # create the oserver which will call the handler methods abooe with file events.
    observer.schedule(event_handler, watched_dir_windows, recursive=True)

    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

#
#
# 

if __name__ == "__main__":

    main()

