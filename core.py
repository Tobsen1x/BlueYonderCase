# -*- coding: utf-8 -*-
"""
Created on Mon Nov  2 22:48:12 2015

@author: Tobias Diederich
"""
import logging.config
import urllib.request
import sys

def initLogging():
    logging.config.fileConfig('config/logging.conf')

def extractFilePath(url, destDir):
    # Extract filename
    splits = url.split('/')
    # Last element in path should be the filename        
    fileName = splits[len(splits) - 1]
    # Remove request parameters
    fileName = fileName.split('?')[0]
    # Complete path to dest folder
    if not(destDir.endswith('/')):
        destDir = destDir + '/'
    destPath = destDir + fileName
    return(destPath)        

def readLines(filePath):
    f = open(filePath)
    lines = f.readlines()
    return(lines)
    
def downloadFile(url):
    request = urllib.request.urlopen(url)
    data = request.read()
    return(data)

def saveFile(content, destPath):
    file = open(destPath, 'wb+')
    file.write(content)
    file.close()

# service function
def downloadFromTxtFile(filePath, destDir):
    initLogging()        
    try:    
        # readlines
        lines = readLines(filePath)
    except Exception as e:
        e.with_traceback()
        logging.exception('Error while reading the file ' + filePath + ": " + e.strerror)
        sys.exit(1)
    
    # Iterate over files to download
    for line in lines:
        try:        
            # download file
            content = downloadFile(line)

            # Extract path to destination file
            destPath = extractFilePath(line, destDir)        
        
            # save file
            saveFile(content, destPath)        
            logging.info('File saved: ' + destPath)
        except Exception as e:
            logging.exception('Problem Downloading or saving file ' + 
                line + " into " + destDir + ": " + e.strerror)
            sys.exit(1)
    
    logging.info('Finished download files from ' + filePath + 
        ' to directory ' + destDir + '.')

if __name__ == "__main__":
    if(len(sys.argv) != 3):               
        print('Please pass file path and destination dir as parameters.')
        sys.exit(1)
    downloadFromTxtFile(sys.argv[1], sys.argv[2])