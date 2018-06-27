These instructions cover how to update the GoogleTranslateAPI.ipynb notebook with the correct API keys for your project, and run it on the Jupyterhub instance on UC Berkeley's Savio cluster.

## Using the translation notebook

The relevant files are [GoogleTranslateAPI.ipynb](https://github.com/ucberkeley/brc-cyberinfrastructure/blob/dev/analysis-workflows/notebooks/GoogleTranslateAPI.ipynb) and [gdrive.py](https://github.com/ucberkeley/brc-cyberinfrastructure/blob/dev/analysis-workflows/notebooks/gdrive.py). As an alternative approach, [GoogleTranslateRunner.ipynb](https://github.com/ucberkeley/brc-cyberinfrastructure/blob/dev/analysis-workflows/notebooks/GoogleTranslateRunner.ipynb) can be used for running it continuously on Jupyterhub. To download each of these files, click the "Raw" button above the code, then save the resulting page (Ctrl + S).

## Creating API keys

Two API keys are needed to run the notebook. Create a new [Google cloud console](https://console.cloud.google.com/?pli=1) project and enable Google Translate and Google Drive APIs.

1.  translate_secret.json - From Google cloud console credentials page, select Create Credentials > Service account key, and save it as a text file named translate_secret.json.

2.  google_drive_secret.json - From Google cloud console credentials page, select Create Credentials > OAuth Client ID > Other, and save it as a text file named google_drive_secret.json.

## Running the notebook on the Savio cluster

-   Log into [Jupyterhub on Savio](https://jupyter.brc.berkeley.edu/) using your Savio username and password (PIN + one-time password)

-   Click the green "Start my server" button

-   For "Select a job profile", choose "Local server" and click "Spawn"

-   Click the "upload" button in the upper right, and upload [GoogleTranslateAPI.ipynb](https://github.com/ucberkeley/brc-cyberinfrastructure/blob/dev/analysis-workflows/notebooks/GoogleTranslateAPI.ipynb) and [gdrive.py](https://github.com/ucberkeley/brc-cyberinfrastructure/blob/dev/analysis-workflows/notebooks/gdrive.py)

-   Double-click GoogleTranslateAPI.ipynb to launch it in a new tab. At the top of GoogleTranslateAPI.ipynb are the exact commands you can copy/paste into Savio to set up your kernel.

-   Go back on the Jupyterhub home screen, click the "New" button in the upper right, then select "Terminal".

-   Paste the commands from GoogleTranslateAPI.ipynb into the terminal, one at a time. Answer "Y" when prompted.

-   Close the tab with the terminal.

-   Back on the Jupyterhub home screen, click on the GoogleTranslateAPI.ipynb notebook and click the orange "Shutdown" button at the top of the screen.

-   Double-click the GoogleTranslateAPI.ipynb notebook again to relaunch it.

-   Select the "translate" kernel under Kernel > Change kernel in the toolbar menu.

-   Change the input_folder, completed_folder, and results_folder to the folders you want to use for each of those.

-   Change translate_secret to translate_secret.json

-   Change google_drive_secret to google_drive_secret.json
