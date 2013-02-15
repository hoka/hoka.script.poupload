import argparse
import os
import sys
import logging
logger = logging.getLogger('poupload')
logger.setLevel(logging.DEBUG)#

import MultipartPostHandler, urllib2, cookielib

from os.path import abspath, join, expanduser, exists, isfile
from ConfigParser import SafeConfigParser

parser = argparse.ArgumentParser(description="""Parse and upload a po file to the server.""")

parser.add_argument('--path',
                    dest='path',
                    help="""The path, where the po file exists.
                            You can input a po file location or
                            a single po flie for uploading.
                            Example: '/MY_PO_FILES_DIRECTORY/my.po' or /MY_PO_FILES_DIRECTORY""")

class Handler:
    def __init__(self,args):
        """ """
        self.args=args
        self.po=[]


        parser = SafeConfigParser()
        parser.read((expanduser('~/.thepofiles')))
        main_section = 'default'

        self.name = parser.get(main_section, 'name', '')
        self.password = parser.get(main_section, 'password', '')
        self.url = parser.get(main_section, 'url', '')

        self.form={}
        self.form['__ac__name']=self.name
        self.form['__ac__password']=self.password

        self.logger = logging.getLogger("poupload")
        self.logger.setLevel(logging.DEBUG)

        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        formatter = logging.Formatter("%(name)s - %(levelname)s - %(message)s")
        ch.setFormatter(formatter)

        self.logger.addHandler(ch)


    def __call__(self):
        """ """

        path=str(self.args.path)
        if not os.path.exists(path):
            self.logger.error('Path value doess not exist. PATH="%s"'%path)
            return

        self._collect_pos()
        self._upload()

    def _collect_pos(self):
        """ """
        path=self.args.path
        if os.path.isdir(path):
            if not path.endswith(os.sep):
                path=path+os.sep
            for file_name in os.listdir(path):
                if file_name.endswith('.po'):
                    self.po.append(path+file_name)

    def _upload(self):
        """ """
        opener=self._create_opener()

        if not self.po:
            self.logger.info('No po files to upload')

        for full_path in self.po:
            self.form['file']=open(full_path, "rb")

            self.logger.info('Upload %s'%full_path)
            try:
                print [self.url]
                fp=opener.open(self.url, self.form)
                data=fp.read()
                fp.close()
            except Exception,e:
                self.logger.error(e)

            return

    def _create_opener(self):
        """ """
        cookies = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookies),MultipartPostHandler.MultipartPostHandler)
        return  opener

def main(args=None):
    if args is None:
        args = sys.argv[1:]

    args = parser.parse_args()
    handler=Handler(args)
    handler()


if __name__ == '__main__':
    sys.exit(main())
