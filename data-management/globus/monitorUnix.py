
#!/usr/bin/env python

import globus_sdk
import sys, os.path, time, datetime, logging
import psutil
import ntpath

from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

from globus_sdk import AuthClient, TransferClient, AccessTokenAuthorizer, RefreshTokenAuthorizer, NativeAppAuthClient

import webbrowser

from utils import start_local_server, is_remote_session
#
# Script to automate the transfer of data files via globus
#

#
# This is the linux version of the monitor script which expects file paths in linux format
#

# REDIRECT_URI: specific webpage or local URI where you want to handle the auth_code sent from Globus Auth.
# SCOPES: set of Globus Auth scopes which you are requesting. By default, this will be set to request access to the
# full Globus Transfer service

SERVER_ADDRESS = ('127.0.0.1', 8000)
REDIRECT_URI = 'http://localhost:8000'
SCOPES = ('openid email profile '
          'urn:globus:auth:scope:transfer.api.globus.org:all')
#
# source_endpoint is the Globus endpoint id that is the origin for the data transfer
# target_endpoint is the Globus endpoint id of the destination of the transfer
#
source_endpoint = "9d5aa7a4-bbc3-11e5-9a07-22000b96db58"  # (rick's laptop endpoint: Rick_ResearchIT_UCBerkeley); was: "3276961a-47a4-11e6-80e6-22000b1701d1"
target_endpoint = "d47068d3-6d04-11e5-ba46-22000b92c6ec"  # (ucb#brc)
#target_endpoint = "ddb59aef-6d04-11e5-ba46-22000b92c6ec"  # (Globus Tutorial Endpoint 1)

#
# watched_dir is the full path to the top folder of the data files for transfer
# patterns are the types of files that are valid for transfer
# endpoint_path is the base path at the endpoint where data files should be saved
#
watched_dir = '/Users/rjaffe/Documents/Dev/code/globus/data/'   # LINUX STLYE PATH . was '/Users/mmmanning/Documents/Dev/code/globus/data'
patterns = ['*.jpg', '*.tif', '*.png', '*.txt']   
endpoint_path = '/~/globustest/'

#
# transfer_client is the globus client used to manage transfers
transfer_client = None
count = 0



def authorize():
    global transfer_client

    CLIENT_ID = '76af25c8-c96b-49b2-9be7-56767395db6b'
    #client = globus_sdk.NativeAppAuthClient(CLIENT_ID)
    #client.oauth2_start_flow_native_app(refresh_tokens=True)

    client = NativeAppAuthClient(client_id=CLIENT_ID)
    client.oauth2_start_flow(requested_scopes=SCOPES,
                                        redirect_uri=REDIRECT_URI,
                                        refresh_tokens=True)
    authorize_url = client.oauth2_get_authorize_url()

    server = start_local_server(listen=SERVER_ADDRESS)

    if not is_remote_session():
        webbrowser.open(authorize_url, new=1)

    auth_code = server.wait_for_code()
    token_response = client.oauth2_exchange_code_for_tokens(auth_code)

    server.shutdown()


    #token_response = client.oauth2_exchange_code_for_tokens(auth_code)

    # the useful values that you want at the end of this
    globus_auth_data = token_response.by_resource_server['auth.globus.org']
    globus_transfer_data = token_response.by_resource_server['transfer.api.globus.org']
    globus_refresh_token = globus_auth_data['refresh_token']
    globus_auth_token = globus_auth_data['access_token']
    globus_transfer_token = globus_transfer_data['access_token']
    globus_token_expires = globus_transfer_data['expires_at_seconds']
    ts = datetime.datetime.fromtimestamp(globus_token_expires).strftime('%Y-%m-%d %H:%M:%S')
    logging.info ("globus token expires: %s" % ts)

    auth_client = AuthClient( authorizer=AccessTokenAuthorizer(globus_auth_token))
    #transfer_client = TransferClient( authorizer=AccessTokenAuthorizer(globus_transfer_token))


    # create refresh token for looooong running monitor
    auth_authorizer2 = globus_sdk.RefreshTokenAuthorizer(globus_refresh_token, client, access_token=globus_transfer_token, expires_at=globus_token_expires)
    transfer_client = TransferClient( authorizer=auth_authorizer2 )

    ep2result = transfer_client.endpoint_autoactivate(source_endpoint)

    logging.info ("source_endpoint autoactivate response code: %s" % ep2result["code"])
    logging.info ("source_endpoint autoactivate response message: %s" % ep2result["message"])



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

    def transfer(self, file_path):
        global count
        label = "test transfer " + str(count)

        # check that the file write has completed
        inuse = self.checkFileInUse(file_path)
        if ( inuse ):
            logging.info("File %s is open by anopther process, cant transfer." % file_path)
            return

        logging.info("Transfer file %s via globus" % file_path)
        tdata = globus_sdk.TransferData(transfer_client, source_endpoint,  target_endpoint, label=label)

        mvfilename = os.path.basename(file_path)
        logging.info("Transfer file endpoint_path: %s " % endpoint_path)
        logging.info ('Transfer file folder structure: %s' % os.path.dirname(file_path))

        prefix_path = os.path.commonprefix([watched_dir, file_path])
        logging.info("Watched dir prefix: %s " % prefix_path)

        relative_path = os.path.relpath(file_path, prefix_path)
        logging.info("relative path: %s " % relative_path)

        target_path = endpoint_path + relative_path
        logging.info("target path: %s " % target_path)


        logging.info("Transfer file mvfilename: %s" % mvfilename)

        # schedule each incoming file into a separate transfer
        #tdata.add_item( file_path,  target_path + mvfilename)
        tdata.add_item( file_path,  target_path)

        submit_result = transfer_client.submit_transfer(tdata)
        print("Task ID:", submit_result["task_id"])


        logging.info("Transfer scheduled.")
        count = count + 1

    def checkFileInUse(self, file_path):
        maxTry = 10
        count = 0
        newfileopen = True
        while ( newfileopen and count < maxTry):
            newfileopen = self.isOpen(file_path)
            logging.info("checkFileStatus checking: %s" % newfileopen)
            if (newfileopen):
                time.sleep(1)

        logging.info("checkFileStatus in use: %s" % newfileopen)
        return newfileopen

    def isOpen(self, file_path):

        for p in psutil.process_iter():
            try:
                print (p.open_files())
                for of in p.open_files():
                    logging.info("current file in use: %s" % of.path)
                    if ( of.path == file_path):
                        logging.info("file in use ******   : %s" % file_path)
                        return True
            except:
                pass
        logging.info("file NOT in use: %s" % file_path)
        return False


def main():
    global watched_dir

    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s',  datefmt='%Y-%m-%d %H:%M:%S')

    logging.info ( 'source folder: %s' % os.path.dirname(watched_dir))

    authorize()

    event_handler = MyEventHandler(patterns=patterns)
    observer = Observer()
    observer.schedule(event_handler, watched_dir, recursive=True)
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
