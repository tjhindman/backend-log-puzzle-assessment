#!/usr/bin/env python2
"""
Logpuzzle exercise

Copyright 2010 Google Inc.
Licensed under the Apache License, Version 2.0
http://www.apache.org/licenses/LICENSE-2.0

Google's Python Class
http://code.google.com/edu/languages/google-python-class/

Given an apache logfile, find the puzzle urls and download the images.

Here's what a puzzle url looks like:
10.254.254.28 - - [06/Aug/2007:00:13:48 -0700] "GET /~foo/puzzle-bar-aaab.jpg HTTP/1.0" 302 528 "-" "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6"

"""


__author__ = "tjhindman"


import os
import re
import sys
import urllib
import shutil
import argparse


def read_urls(filename):
    """
    Returns a list of the puzzle urls from the given log file,
    extracting the hostname from the filename itself.
    Screens out duplicate urls and returns the urls sorted into
    increasing order.
    """

    urls = []

    def sorting(url):
        match = re.search(r'(\w+)-(\w+)\.\w+', url)

        return match.group(2) if match else url


    with open(filename) as f:
        for line in f:
            # Find the path which is after the GET and surrounded by spaces.
            match = re.search(r'"GET (\S+)', line)

            if match:
                path = match.group(1)

                if 'puzzle' in path:
                    urls.append('http://code.google.com' + path)

    return sorted(set(urls), key=sorting)

        # for i, url in enumerate(match):
        #     match[i] = url


        # data = f.read()
        # urls = re.findall(r'GET (\S+.jpg)', data)

        # for i, url in enumerate(urls):
        #     urls[i] = 'http://code.google.com' + url

        # return sorted(set(urls), key=lambda x: re.findall(r'\S{4}.jpg', x)[0])


def download_images(img_urls, dest_dir):
    """
    Given the urls already in the correct order, downloads
    each image into the given directory.
    Gives the images local filenames img0, img1, and so on.
    Creates an index.html in the directory
    with an img tag to show each local image file.
    Creates the directory if necessary.
    """

    html = """
        <html>
            <body>
                {}
            </body>
        </html>
    """

    os.mkdir(dest_dir)

    with open('index.html', 'w') as index:
        img_list = []

        for i, url in enumerate(img_urls):
            print("Retrieving image from {}...".format(url))
            urllib.urlretrieve(url, 'img{}'.format(i))
            print("Copying image to {}...".format(dest_dir))
            shutil.move('img{}'.format(i), '{}'.format(dest_dir))
            print("Populating img_list with HTML image tag...")
            img_list.append("<img src='img{}'>".format(i))

        shutil.move('index.html', dest_dir)
        index.write(html.format(''.join(img_list)))


def create_parser():
    """
    Create an argument parser object
    """
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--todir', help='destination directory for downloaded images')
    parser.add_argument('logfile', help='apache logfile to extract urls from')

    return parser


def main(args):
    """
    Parse args, scan for urls, get images from urls
    """

    parser = create_parser()

    if not args:
        parser.print_usage()
        sys.exit(1)

    parsed_args = parser.parse_args(args)

    img_urls = read_urls(parsed_args.logfile)

    if parsed_args.todir:
        download_images(img_urls, parsed_args.todir)
    else:
        print('\n'.join(img_urls))


if __name__ == '__main__':
    main(sys.argv[1:])
