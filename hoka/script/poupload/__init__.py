import argparse
import os
import sys
import logging
import glob
import urllib2
import cookielib
import json
from polib import POFile,pofile

from posthandler import MultipartPostHandler

from os.path import abspath, join, expanduser, exists, isfile
from ConfigParser import SafeConfigParser

parser = argparse.ArgumentParser(description="""Parse and upload a po file to the server.""")

parser.add_argument('--path',
                    dest='path',
                    help="""The path, where the po file exists.
                            You can input a po file location or
                            a single po flie for uploading.
                            Example: '/MY_PO_FILES_DIRECTORY/my.po' or /MY_PO_FILES_DIRECTORY""")

parser.add_argument('--language',
                    dest='language',
                    help="""Language filter. '--language de,en' uploads only de and en po files""")


logger = logging.getLogger('poupload')
logger.setLevel(logging.DEBUG)#


class Handler:
    def __init__(self,args):
        """ """
        self.args=args
        self.po=[]

        if not self.args.language:
            self.args.language=[]
        else:
            self.args.language=[lang_code.strip() for lang_code in self.args.language.split(',')]

        parser = SafeConfigParser()
        parser.read((expanduser('~/.thepofiles')))
        main_section = 'poupload'

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
            self.logger.error('Path value does not exist. PATH="%s"'%path)
            return

        self._collect_pos()
        self._upload()

    def _walk(self,path):
        for path, directories, file_names in os.walk(path):
            if not path.endswith(os.sep):
                path+=str(os.sep)
            for file_name in file_names:
                if file_name.endswith('.po'):
                    if path+file_name not in self.po:
                        self.po.append(path+file_name)
            for directory_name in directories:
                self._walk(path+directory_name)

    def _collect_pos(self):
        """ """
        path=self.args.path
        if os.path.isdir(path):
            self._walk(path)
        else:
            if os.path.exists(path):
                self.po.append(path)

        if self.args.language:

            for full_path in list(self.po):
                try:
                    po_file=pofile(pofile=full_path)

                    metadata={}
                    for pair in po_file.ordered_metadata():
                        metadata[pair[0]]=pair[1]
                    if metadata.has_key('Language-Code'):
                        if metadata['Language-Code'] not in self.args.language:
                            self.po.remove(full_path)
                    else:
                        self.logger.error('Po file has no language defined.')
                        self.logger.error('Path: %s'%full_path)

                        self.po.remove(full_path)
                except Exception,e:
                    self.logger.error('An error appears while getting po file language.')
                    self.logger.error('Path: %s'%full_path)
                    self.logger.error(e)
                    self.po.remove(full_path)


    def _upload(self):
        """ """
        opener=self._create_opener()

        if not self.po:
            self.logger.info('No po files to upload')
        else:
            self.logger.info('%s po files found'%len(self.po))

        print ''

        for full_path in self.po:
            self.form['file']=open(full_path, "rb")

            self.logger.info('Upload %s'%full_path)
            try:
                fp=opener.open(self.url, self.form)
                data=fp.read()
                fp.close()

                data=json.loads(data)
                method=data.keys()[-1]
                getattr(self.logger,method)(data[method])
                print ''

            except Exception,e:
                self.logger.error(e)
                print ''

    def _create_opener(self):
        """ """
        cookies = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookies),MultipartPostHandler)
        return  opener

def main(args=None):
    if args is None:
        args = sys.argv[1:]

    args = parser.parse_args()
    handler=Handler(args)
    handler()


if __name__ == '__main__':
    sys.exit(main())
