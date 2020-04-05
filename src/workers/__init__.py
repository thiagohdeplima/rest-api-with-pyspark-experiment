import os
import gzip
import shutil
import tempfile

import logging

import urllib
import ftplib
import requests

from celery import Celery
from pyspark import SparkContext

app = Celery(__name__, broker=os.environ['REDIS_URL'])

@app.task
def perform_file_operations(url):
  archive = download(url)

  if archive.endswith('.gz'):
    archive = extract_gzip_file(archive)

def download(url):
  logging.info("Downloading file %s" % url)

  _, ext = os.path.splitext(url)

  parsed_url = urllib.parse.urlparse(url)
  destination = tempfile.mktemp(dir='/dev/shm', suffix=ext)

  if parsed_url.scheme == 'ftp':
    return download_from_ftp(parsed_url, destination)
  elif parsed_url.scheme == 'http':
    return download_from_http(parsed_url, destination)
  else:
    logging.error("Unsupported URL scheme %s" % parsed_url.scheme)

def download_from_http(parsed_url, destination):
  filecontent = requests.get(parsed_url.geturl(), stream=True)

  with open(destination, 'wb') as f:
    for chunck in response.iter_content(chunck_size=1024):
      f.write(chunck)

  return destination

def download_from_ftp(parsed_url, destination):
  username = 'anonymous'

  if parsed_url.username is not None:
    username = parsed_url.username

  with open(destination, 'wb') as f:
    ftp = ftplib.FTP(parsed_url.hostname, username, parsed_url.password)
    ftp.retrbinary("RETR " + parsed_url.path, f.write)

  return destination

def extract_gzip_file(gzip_file_path):
  destination = tempfile.mktemp(dir='/dev/shm')

  with gzip.open(gzip_file_path, 'r') as gzip_file:
    with open(destination, 'wb') as text_file:
      shutil.copyfileobj(gzip_file, text_file)

  return destination
