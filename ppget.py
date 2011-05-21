from piratepad import parse_pp
import sys
import os
import urllib

class ppget(object):
    def __init__(self, page):
        self.pg = page
        self.data = {}
        self.c = {'d': "want to d/l '%s'? "%page}


    def confirm(self,x):
        return raw_input(x)


    def zalir(self):
        sys.exit()


    def create_dir(self, d):
        os.mkdir( self.pg ) if self.confirm( self.c['d'] ) else self.zalir()


    def get_data(self):
        return parse_pp(self.pg)


    def get_urls(self, format='txt'):
        self.data = self.get_data()
        r = [{'n': self.pg,
              'u':self.data[self.pg]['export'][format] }
             ]
        for pg in self.data[self.pg]['related']:
            r.append( {'n':pg, 'u':self.data[self.pg]['related'][pg]['export'][format]} )
        return r
    
        
    def download(self,format='txt'):
        self.create_dir(self.pg)
        urls=self.get_urls(format)
        for u in urls:
            urllib.urlretrieve(u['u'], "%s" % os.path.join(self.pg, "%s.%s"%(u['n'], format)))


if __name__ == "__main__":
    ppget( sys.argv[1] if len(sys.argv)>1 else 'piratepadpy' ).download()
