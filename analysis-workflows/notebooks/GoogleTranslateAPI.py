
# coding: utf-8

# # Google Translate API
# 
# This notebook demonstrates retrieving text file from Google drive, sending it to the Google translate API, receiving the translation, and uploading the result to Google drive. (Nicolas Chan)
# 
# ### Kernel Setup
# ```bash
# conda create --name=translate python=3.6 ipykernel
# source activate translate
# ipython kernel install --user --name translate
# pip install --upgrade google-cloud-translate nltk google-api-python-client google-auth-httplib2
# ```
# ### Credentials
# IMPORTANT: Store your service account JSON credentials in `client_secret.json`.

# In[ ]:


# Configuration
target_language = 'en'

# Limit maximum character length of text sent to Google translate at once
# Larger limit yields better translations because Google translate uses context
# Too large of a length might be rejected by Google translate (maximum allowed: 5000)
# See: https://cloud.google.com/translate/faq
max_length = 4000

# Delay between sending chunks
delay = 20 # seconds

# Set to True only if it makes sense to send chunks split by line breaks.
# If line breaks might occur in the middle of sentences, set this to False.
preserve_line_breaks = True

input_folder = '1dIVXCpexYecYUWj4NdL-4IhGzDMvOakN'
completed_folder = '1b9yvvDsm2lH6bLT8wRJnErFSdcMnfwYa'
results_folder = '1lVJoATSlYFyb6I_N8EwGVyhSn_AM6vuX'

# Credentials
# translate_secret = 'shapreau_translate.json'
translate_secret = 'translate_id.json'
google_drive_secret = 'client_id.json'


# ## Google Drive Authentication
# Google drive interaction uses code from `AdamAndersonFindSumerian.ipynb`

# In[ ]:


from gdrive import GDrive
gdrive = GDrive(google_drive_secret) 


# In[ ]:


# Identify file to process
import sys

files = gdrive.list_files(input_folder, 'txt')
if (files):
    file = files[0]
else:
    print('No files to process')
    sys.exit()
    
print("Found file to process:", file)


# ## Download file to translate

# In[ ]:


input_filename = file['id'] + '.txt'
output_filename = file['id'] + '_translated.txt'
input_contents = gdrive.download_file(file['id'], input_filename)


# | Prefix | Language
# |---------|---------|
# | cze | czech |
# | dut | dutch |
# | est | estonian |
# | fre | french |
# | gre | greek |
# | nor | norwegian |
# | por | portuguese |
# | spa | spanish |
# | tur | turkish |
# | dan | danish |
# | eng | english |
# | fin | finnish |
# | ger | german |
# | ita | italian |
# | pol | polish |
# | slv | slovene |
# | swe | swedish |

# In[ ]:


# Set tokenizer language
# punkt_tokenizer is used to identify where sentences end for splitting into chunks.
# It should be set to the INPUT language.
# For more info: http://www.nltk.org/api/nltk.tokenize.html#module-nltk.tokenize.punkt
# Available languages: czech, dutch, estonian, french, greek, norwegian, portuguese, 
#   spanish, turkish, danish, english, finnish, german, italian, polish, slovene, swedish

language_code = file['name'][:3]
def lookup_language(code):
    languages = {
        'cze': 'czech',
        'dut': 'dutch',
        'est': 'estonian',
        'fre': 'french',
        'gre': 'greek',
        'nor': 'norwegian',
        'por': 'portuguese',
        'spa': 'spanish',
        'tur': 'turkish',
        'dan': 'danish',
        'eng': 'english',
        'fin': 'finnish',
        'ger': 'german',
        'ita': 'italian',
        'pol': 'polish',
        'slv': 'slovene',
        'swe': 'swedish'
    }
    return languages[code]
punkt_tokenizer = 'tokenizers/punkt/' + lookup_language(language_code) + '.pickle'


# ## Run Translation

# In[ ]:


# Read input file contents
input_contents = gdrive.read_local_file(input_filename)

from html import escape
input_contents = escape(input_contents)
if preserve_line_breaks:
    input_contents = input_contents.replace('\n', '<br>')
    input_contents = input_contents.replace('\r', '<br>')


# In[ ]:


# Function to combine sentences into larger chunks
def condense(lst, length):
    """Concatenates elements in lst until each element in lst is at most length"""
    if len(lst) == 0:
        return lst
    
    # Split elements at spaces if they exceed length
    number_split = 0
    new_lst = []
    for elem in lst:
        if len(elem) > length:
            number_split += 1
            new_lst.extend(elem.split(' '))
        else:
            new_lst.append(elem)
    lst = new_lst
    
    if number_split > 0:
        print('WARNING! Had to split', number_split, 
              'sentences because the sentence length exceeded', length, 'characters.')
    if max([ len(elem) for elem in lst ]) > length:
        raise Exception('A single word exceeded ' + length + ' characters')
    
    # Now that all elements are guaranteed to be <= length,
    # combine them as long as they do not exceed length.
    chunks = []
    current_chunk = ''
    for sentence in lst:
        if len(current_chunk) + len(sentence) < length:
            current_chunk += ' ' + sentence
        else:
            chunks.append(current_chunk)
            current_chunk = sentence
    if current_chunk:
        chunks.append(current_chunk)
    return chunks


# In[ ]:


# Translate file contents
from google.cloud import translate
client = translate.Client.from_service_account_json(translate_secret)
def google_translate(text):
    return client.translate(text, target_language=target_language)['translatedText']


# In[ ]:


# Split at sentences
# Uses nltk to identify sentence breaks (http://www.nltk.org/api/nltk.tokenize.html#module-nltk.tokenize.punkt)
import nltk
nltk.download('punkt')

# Split into sentences
import nltk.data
tokenizer = nltk.data.load(punkt_tokenizer)

import time
def translate(text):
    sentences = tokenizer.tokenize(text)
    print('Identified', len(sentences), 'sentences')
    
    chunks = condense(sentences, max_length)
    print('Condensed into', len(chunks), 'chunks')
    
    translated_chunks = []
    for chunk in chunks:
        translated_chunks.append(google_translate(chunk))
        print('Progress:', str(round(len(translated_chunks) / len(chunks) * 100)) + '%')
        time.sleep(delay) # Avoid rate limit error
    
    translation = ' '.join(translated_chunks)
    return translation


# In[ ]:


translation = translate(input_contents)


# In[ ]:


# Translation contains escaped HTML charcaters such as '&#39;' for an apostrophe.
# To fix this, unescape HTML
from html import unescape
translation_text = translation
if preserve_line_breaks:
    translation_text = translation_text.replace('<br>', '\n')
translation_text = unescape(translation_text)


# In[ ]:


# Write output to output file
output_file = open(output_filename, 'w', encoding='utf8')
print('Writing translation to file', output_filename)
output_file.write(translation_text)
output_file.close()
print('Done writing translation to file')
get_ipython().system('sync # Make sure the file is finished writing to disk')


# In[ ]:


print('Uploading to Google Drive')

# Uploading sometimes fails, so try up to 10 times, waiting a minute between each try
def upload(tries):
    if tries > 10:
        print('Maximum tries exceeded, giving up on uploading')
        return
    try:
        print('Upload attempt', tries)
        gdrive.upload_file('eng_translated' + file['name'][3:], output_filename, results_folder)
        print('Uploaded successfully')
    except:
        print('Error uploading')
        if (tries > 10):
            print ('Maximum tries exceeded, giving up on uploading')
            gdrive.move_file(file['id'], completed_folder, error_folder)
        else:
            time.sleep(60)
            upload(tries + 1)
upload(0)


# In[ ]:


# Move input text file to completed folder so it is not processed again
gdrive.move_file(file['id'], completed_folder, input_folder)

