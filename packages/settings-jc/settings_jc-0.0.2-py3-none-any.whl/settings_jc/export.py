from os import path, remove
from .settings import Settings
import arrow

class Export:

    def __init__(self, settings: Settings):
        self.settings = settings

    def export_to_file(self, filename):
        curdatestr = arrow.now().format()
        if path.exists(filename):
            remove(filename)

        with open(filename, mode='wt') as fp:
            fp.write('# Settings Exported\n')
            fp.write('# on: ' + curdatestr + '\n')
            fp.write('# for appname = ' + self.settings.appname + '\n' )
            for item in self.settings.items:
                s = f"{item['name']}={item['value']}\n"
                fp.write(s)
        return
