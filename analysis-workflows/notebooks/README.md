<H2>iPython notebooks</H2>

**BoxAuthenticationBootstrap.ipynb** - This is a utility script used to authenticate the user with CalNet and store the resulting auth and refresh tokens to be used in other scripts. Tested with boxsdk (2.0.0a2) on python 3.5 kernel (pip install -Iv boxsdk==2.0.0a2)

**TransferFilesFromBoxToSavioScratch.ipynb** - This notebook is an exemplar which demonstrates transferring files from a Box folder to a users home directory on Savio. Tested with boxsdk (2.0.0a2) on python 3.5 kernel (pip install -Iv boxsdk==2.0.0a2)
- **__please note:__** To authenticate with Box the BoxAuthenticationBootstrap notebook must be executed before using this notebook. The token store used in store_tokens method of BoxAuthenticationBootstrap must be also used in the store_tokens and REFRESH_TOKEN read methods of this notebook.
