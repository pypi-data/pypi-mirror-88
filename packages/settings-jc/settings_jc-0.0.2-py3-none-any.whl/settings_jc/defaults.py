from os import listdir, environ
from os.path import isfile, dirname, abspath, join


class Defaults:

    def __init__(self, filename=None):
        self.values = []
        self.appname = ''

        file_name = filename
        env_filename = environ.get('SETTINGS_JC_FILE')
        if env_filename != None:
            file_name = env_filename
        else:
            if (file_name is None) or (file_name <= ''):
                file_name = self.getfilename()
            else:
                file_name = filename

        self.filename = file_name
        self.load(filename=self.filename)

    def fileinpath(self, filename, pathname):
        result = False
        files = listdir(pathname)
        lowername = filename.lower()
        for name in files:
            if lowername == name.lower():
                result = True
                break
        return result

    def getfilename(self):
        result = ''
        done = False
        curpath = dirname(abspath(__file__))
        while not done:
            if self.fileinpath('settings.txt', curpath):
                result = join(curpath, 'settings.txt')
                done = True
            else:
                oldpath = curpath
                curpath = dirname(curpath)

                if oldpath == curpath:
                    done = True
                if len(curpath) < 3:
                    done = True
        return result

    def load(self, filename):
        self.values = []
        #
        # Load data, and populate values array
        #
        # https://stackoverflow.com/a/8010133
        with open(filename, mode='rt') as f:
            for line in f:
                if len(line) > 1:
                    if line[0] == '#':
                        pass
                    else:
                        linetxt = line.replace('\n','')
                        x = linetxt.split('=', 1)
                        name = x[0]
                        val = x[1]
                        self.values.append({'name': name, 'value': val})
                        if name == 'appname':
                            self.appname = val
        return

    def get(self, name):
        result = ''
        try:
            for v in self.values:
                if v['name'].lower() == name.lower():
                    result = v['value']
                    break
        except KeyError as e:
            result = str(e)
        return result
