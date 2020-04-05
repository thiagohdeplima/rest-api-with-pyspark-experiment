import os
import re

import gzip
import shutil
import tempfile

import logging

import urllib
import ftplib
import requests

from celery import Celery
from pyspark import SparkContext, SparkConf

DATA_DIR = '/srv/data'

sc = SparkContext(conf=SparkConf())

app = Celery(__name__, broker=os.environ['REDIS_URL'])

@app.task
def perform_file_operations(url):
  archive = download(url)

  if archive.endswith('.gz'):
    archive = extract_gzip_file(archive)

  get_stats_from_spark(archive)


def download(url):
  _, ext = os.path.splitext(url)

  parsed_url = urllib.parse.urlparse(url)
  destination = tempfile.mktemp(dir=DATA_DIR, suffix=ext)

  logging.info("Downloading file %s into %s" % (url, destination))

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
  logging.info("Extracting file %s" % gzip_file_path)

  destination = tempfile.mktemp(dir=DATA_DIR)

  with gzip.open(gzip_file_path, 'r') as gzip_file:
    with open(destination, 'wb') as text_file:
      shutil.copyfileobj(gzip_file, text_file)

  return destination

def get_stats_from_spark(text_file):
  logging.info("Processing file %s into Spark" % text_file)

  txt = sc.textFile(text_file)

  bytes_regex = re.compile('(\d+)$')
  status_regex = re.compile('(\d+)\s[\d|\-]+$')
  host_regex = re.compile('^([\w+\.]+[\w+]{1,}[^\s])')

  unique_hosts = txt \
    .flatMap(lambda line: host_regex.findall(line)) \
    .distinct() \
    .count()

  total_errors = txt \
    .filter(lambda line: status_regex.findall(line) == ['404']) \
    .count()

  top_5_urls = None
  qty_404_by_day = None

  total_bytes = txt \
    .filter(lambda line: bytes_regex.findall(line) != []) \
    .map(lambda line: bytes_regex.findall(line)) \
    .map(lambda nbytes: int(nbytes[0])) \
    .sum()

  logging.info(
    'We have %d unique hosts, with a total of %d 404 errors, and %d bytes transferred' % (
      unique_hosts,
      total_errors,
      total_bytes
    )
  )