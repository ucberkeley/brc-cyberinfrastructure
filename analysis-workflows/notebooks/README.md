<H2>iPython notebooks</H2>

**BoxAuthenticationBootstrap.ipynb** - This is a utility script used to authenticate the user with CalNet and store the resulting auth and refresh tokens to be used in other scripts. Tested with boxsdk (2.0.0a2) on python 3.5 kernel (pip install -Iv boxsdk==2.0.0a2)

**TransferFilesFromBoxToSavioScratch.ipynb** - This notebook is an exemplar which demonstrates transferring files from a Box folder to a users home directory on Savio. Tested with boxsdk (2.0.0a2) on python 3.5 kernel (pip install -Iv boxsdk==2.0.0a2)

Read more in this [RIT blog post](http://research-it.berkeley.edu/blog/16/11/22/ipython-notebook-available-ease-data-transfer-between-savio-and-box).

- **__please note:__** To authenticate with Box the BoxAuthenticationBootstrap notebook must be executed before using this notebook. The token store used in store_tokens method of BoxAuthenticationBootstrap must be also used in the store_tokens and REFRESH_TOKEN read methods of this notebook.

**AriannaCampianiTest.ipynb** - Workflow to retrieve image files from Box, process with Photoscan then return results to BOx including project file and model files.

**Tesseract Test.ipynb** - Workflow to retrieve pdf files from Box, generate png images with Ghostscript, OCR with Tesseract, merge individual text files per page into result text file and place in Box folder.
