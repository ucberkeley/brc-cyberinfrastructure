#!/usr/bin/env python3
#coding=utf-8

'''
Current scoring approach:
- To be counted, the score for a word must be between 25 and 70, this removes some garbage characters at the low end.
- If a line contains between 6 and 9 scoring words it registers as a small hit, if it contains 10 or more then the line registers as a big hit.
- If the total score for the last three lines (a rolling window) is > 15 then that is a small hit and > 25 is a big hit.
- if a "paragraph" (currently using the dev tag in the hocr xml) has > 25 scoring words that is a small hit and > 40 is a bit hit.


This scoring approach seems to be doing a good job of finding target text. However, it also includes a number of false positives that I 
have not been able to reduce significantly. Table and figures are usually tagged as hits. The Teissier_Sealings doc has a number of tables, 
rotated to landscape, which show up in the big hits list. I have not found a way to identify a table or figure from the xml results. 
There are a couple papers online with complex detection algorithms but nothing I could implement without significant development time.
'''

from multiprocessing import Pool
from html.parser import HTMLParser
from bs4 import BeautifulSoup
from html.entities import name2codepoint
import sys, os.path, time, datetime, logging
import subprocess
import fnmatch
import collections
import re
import csv

srch = re.compile(r'.*[-—]+.*[-—]+[.-—]*')

#logging.basicConfig(filename='ocrparse.log', level=logging.INFO, format='%(message)s',  datefmt='%Y-%m-%d %H:%M:%S')
logging.basicConfig(handlers=[logging.FileHandler('ocrparse.log', 'w', 'utf-8')], level=logging.INFO, format='%(message)s',  datefmt='%Y-%m-%d %H:%M:%S')


#
# source_directory is the folder that has pdf input files
# target_directory the the folder where output files are placed
#
#source_directory = "/scratch/test/"
#target_directory = "/scratch/test/output/"

#source_directory = "/home/mmanning/test/"
#target_directory = "/home/mmanning/test/output/"

source_directory = "/Users/mauricemanning/Documents/Dev/code/ocr/"
target_directory = "/Users/mauricemanning/Documents/Dev/code/ocr/output/"


# Absolute path to Ghostscript executable here or command name if Ghostscript is
# in your PATH.
# TEMPLATE: gs -dBATCH -dNOPAUSE -dQUIET -sDEVICE=png16m -sOutputFile=/scratch/test/output/test-%d.png -r300 /scratch/test/germanocr.pdf
GHOSTSCRIPTCMD = ['gs', '-dBATCH', '-dNOPAUSE', '-dQUIET', '-sDEVICE=png16m', '-sOutputFile={}{}-%d.png', '-r300', '{}{}' ]

#
#
# template: tesseract --tessdata-dir /opt/tessdata /scratch/germanocr_Page_01.png  germanout  -l deu -c tessedit_create_hocr=1
TESSERACTCMD = ['tesseract', '--tessdata-dir', '/opt/tessdata', '{}{}', '{}{}',  '-l', 'deu+eng+tur+fra', '-c', 'tessedit_create_hocr=1' ]



def vetHitList(hitlist):

    #logging.info('vetHitList  hitlist: %s ', hitlist )
    totalHits= len(hitlist)
    count = 0
    for hit in hitlist:
        found = srch.search(hit)
        if found:
            #logging.info('good hit: %s ', hit )
            count = count + 1
        #else:
            #logging.info('BAD hit:  %s ', hit )

    percent = count / totalHits
    #logging.info('vetHitList percent: %s ', percent)
    if percent > .666:
        return True
    else:
        return False



def parseHocrFiles(filenameroot, fileList):


    last_three_lines = collections.deque(3*[0], 3)
    last_three_line_words = collections.deque(3*[''], 3)
    div_count=0
    avg_low_score = 0
    low_score_ctr = 0
    low_score_words = []
    div_words = []
    line_id = ''
    bighits = []
    smallhits = []



    for filename in fileList :

        if not filename.endswith(".hocr"):
            continue

        print (' filename: ', filename)

        # split out the file name and the page (image) number
        splittokens = re.split(r"-|\.", filename)
        tot = len(splittokens)
        image_number = splittokens[tot - 2]
        image_number_decimal = int(image_number.strip())
        #doc_name = splittokens[0]
        print (' doc name: ', filenameroot)
        print (' image number: ', image_number)
        soup = BeautifulSoup(open(filename, encoding='utf-8'), "html5lib")
        #print ('==========>', filename )
        logging.info("==========> %s", filename )

        last_three_lines.clear()
        last_three_line_words.clear()

        for div_tag in soup.find_all('div'):


            div_id = div_tag['id']
            if div_id is None:
                div_id = 'None'
            else:
                div_id = div_id.strip()


            div_count = len(div_words)
            #check words in hit list for hypens
            #logging.info("div words: %s ", div_words)

            if div_count > 0 :
                gooddivwords = vetHitList( div_words )
            else:
                gooddivwords = False

            if gooddivwords :
                logging.info("good div words: %s ", div_words)

            # if more than 25 words in this dev section then add to hit list
            if div_count > 20 and gooddivwords:
                bighits.append([filenameroot, image_number_decimal, "div count: " + str(div_count), div_words] )
                logging.info("file: %s  div count: %d tag: %s ", filename, div_count, div_id )
            elif div_count > 10 and gooddivwords:
                smallhits.append([filenameroot, image_number_decimal, "div count: " + str(div_count), div_words] )
                logging.info("file: %s  div count: %d tag: %s ", filename, div_count, div_id )

            div_count = 0
            div_words = []


            #print 'tag initial: ', tag
            #print ('tag class: ', div_tag['class'] )
            if 'ocr_page' in div_tag['class']:
                #logging.info("ocr_page: %s" % tag['title'])
                #print 'tag filtered: ', tag
                for span_tag in div_tag.find_all('span'):
                    #print spantag

                    if 'ocr_line' in span_tag['class']:
                        line_id = span_tag['id'].strip().encode('utf-8')
                        #print ('new line :', line_id,  ' process prev set then reset counters')

                        #check words in hit list for hypens
                        if len(low_score_words) > 0:
                            goodwords = vetHitList( low_score_words )
                        else:
                            goodwords = False
                        #print("goodwords: ", goodwords)

                        if low_score_ctr > 6 and low_score_ctr <= 9 and goodwords :
                            print ('mid range hit: ',  [x.encode('utf-8') for x in low_score_words]  )
                            logging.info("line:  %s   score: %d   avg low score: %f  words:  %s",  line_id, low_score_ctr, (avg_low_score/low_score_ctr) , low_score_words  )
                            smallhits.append( [filenameroot, image_number_decimal, low_score_ctr, low_score_words] )

                        if low_score_ctr >= 10 and goodwords :
                            print ('high range hit', [x.encode('utf-8') for x in low_score_words]  )
                            logging.info("line:  %s   score: %d    avg low score: %f  words:  %s",  line_id, low_score_ctr, (avg_low_score/low_score_ctr),   low_score_words )
                            bighits.append( [filenameroot, image_number_decimal, low_score_ctr, low_score_words] )

                        div_words.extend(low_score_words)


                        # add to the counter of the last three lines and if total is over the threahold then log
                        last_three_lines.appendleft(low_score_ctr)
                        last_three_line_words.appendleft(low_score_words)
                        total_last_three_lines = sum(last_three_lines)
                        if total_last_three_lines > 25 :
                            logging.info("line:  %s   last three lines:  %s",  line_id, last_three_lines )
                            bighits.append( [filenameroot, image_number_decimal, "three line total:" + str(total_last_three_lines) , list(last_three_line_words) ] )
                        elif total_last_three_lines > 15 :
                            logging.info("line:  %s   last three lines:  %s",  line_id, last_three_lines )
                            smallhits.append( [filenameroot, image_number_decimal, "three line total:" + str(total_last_three_lines), list(last_three_line_words) ] )


                        low_score_words = []
                        avg_low_score = 0
                        low_score_ctr = 0

                        # that is all the processing when a new line is reached
                        continue

                    if span_tag.string is None:
                        continue

                    spantagword = span_tag.string.strip()
                    #print ('span tag: ', spantagword.encode("utf-8")  )
                    span_title_split = span_tag['title'].split(';')
                    for span_title_element in span_title_split:
                        if 'x_wconf' in span_title_element:
                            #label, score = title_element.split(' ')
                            score = span_title_element.replace('x_wconf', '').strip()
                            #print( 'word: ', spantagword.encode("utf-8"), 'score: ', int(score.strip()) )

                            # if score less than 25 the could be table. diagram, or figure
                            if int(score.strip())  < 70 and int(score.strip()) > 25 :
                                #logging.info('word:  %s score: %s ',  spantagconverted, score.strip() )
                                low_score_ctr = low_score_ctr + 1
                                low_score_words.append( spantagword )
                                avg_low_score = avg_low_score + int(score.strip())




    #files to hold totalsi
    print("create results files for: ", filenameroot)
    bighitssorted = open( target_directory + filenameroot + '_bighits.txt', 'w')
    smallhitssorted = open( target_directory + filenameroot + '_smallhits.txt', 'w')

    bigsortedlist =  sorted(bighits, key=lambda row: row[1], reverse=False)
    logging.info('bigsortedlist: %s ', bigsortedlist)
    smallsortedlist =  sorted(smallhits, key=lambda row: row[1], reverse=False)
    logging.info('smallsortedlist: %s ', smallsortedlist)

    unique = []
    for hit in bigsortedlist:
        if hit[1] not in unique :
            unique.append( hit[1] )
            print("big hit:", hit)
            bighitssorted.write(hit[0] + ';' + str(hit[1]) + ';' + str(hit[3])  + "\n"  )
    bighitssorted.close()

    for hit in smallsortedlist:
        if hit[1] not in unique :
            unique.append( hit[1] )
            print("small hit:", hit)
            smallhitssorted.write(hit[0] + ';' + str(hit[1]) + ';' + str(hit[3]) + "\n"  )
    smallhitssorted.close()



def parseOcrOutputForFileset(filename):
    print(" parseOcrFileset: ", filename)

    hocrfileList = []
    #pattern = name + '*.hocr'
    pattern = '*.hocr'
    for hocrname in os.listdir(target_directory):
        if (fnmatch.fnmatch(hocrname, pattern) and hocrname.startswith(filename) ):
            print("hocr name: ", hocrname)
            hocrfileList.append(target_directory+hocrname)

    #file = open(outfile, 'r', encoding='utf8')
    #print( "file path: ", os.path.dirname(file) )
    #soup = BeautifulSoup(file, 'html.parser')
    #file.close()
    #print("parseOcrOutputForFileset list: ", hocrfileList)
    parseHocrFiles(filename, hocrfileList)
    print("parseOcrOutputForFileset completed file set parse: ", filename)


def runGhostscript(pdfFile):
    print("runGhostscript pdfFile : ", pdfFile)
    #
    # convert the pdf to png files, one for each page
    #
    name, extension = os.path.splitext(pdfFile)

    # print(os.path.join(directory, filename))
    GHOSTSCRIPTCMD[5] = GHOSTSCRIPTCMD[5].format(target_directory, name)
    GHOSTSCRIPTCMD[7] = GHOSTSCRIPTCMD[7].format(source_directory, pdfFile)

    print("gs cmd: ", GHOSTSCRIPTCMD)
    result = subprocess.call(GHOSTSCRIPTCMD)
    print("gs result: ", result)




def runTesseract(imagefile):
    print("runTesseract imagename: ", imagefile)
    #
    # ocr the pngs
    #
    basename, ext = os.path.splitext(imagefile)
    TESSERACTCMD[3] = TESSERACTCMD[3].format(target_directory, imagefile)
    TESSERACTCMD[4] = TESSERACTCMD[4].format(target_directory,basename)
    print("tesseract cmd: ", TESSERACTCMD)
    result2 = subprocess.call(TESSERACTCMD)
    print("tesseract result: ", result2)
    TESSERACTCMD[3] = '{}{}'
    TESSERACTCMD[4] = '{}{}'



def main():

    filenameList = []
    pdffileList = []
    for filename in os.listdir(source_directory):
        print("filename: ", filename)
        if filename.endswith(".pdf") :
            pdffileList.append(filename)

            # split out the file name and the page (image) number
            splittokens = re.split(r"-|\.", filename)
            tot = len(splittokens)
            filenameList.append( splittokens[0] )

    print("pdffileList: ", pdffileList)
    print("filenameList: ", filenameList )


    #
    # multiprocess the pdf to png work work
    #
    #pool0 = Pool(20)
    #pool0.map(runGhostscript, pdffileList)
    #pool0.close()
    #pool0.join()

    imageList = []
    for imagename in os.listdir(target_directory):
        if imagename.endswith(".png"):             #  and imagename.startswith(name):
            imageList.append(imagename)

    print("imageList: ", imageList )

    #
    # multiprocess the ocr work
    #

    #pool1 = Pool(20)
    #pool1.map(runTesseract, imageList)
    #pool1.close()
    #pool1.join()


    #
    # parse the ocr result
    #
    # multiprocess the hocr parsing
    #
    print("create the pool for the parsing")
    pool2 = Pool(20)
    pool2.map(parseOcrOutputForFileset, filenameList)
    pool2.close()
    pool2.join()



#
#
#

if __name__ == "__main__":

    main()
 
