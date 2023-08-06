import copy
import json
from .encdec import EncDec
from .defaults import Defaults


class Settings:

    def __init__(self):
        defaults = Defaults()
        # make a non-referenced copy of the defaults.
        self.items = []
        self.appname = ''
        self.load_config()

    def config_filename(self):
        import os
        osname = os.name
        if osname == 'nt':
            _data_folder = os.path.join(os.getenv('APPDATA'), Defaults().appname)
        else:
            _data_folder = os.path.join(os.getenv('HOME'), Defaults().appname)

        if not os.path.exists(_data_folder):
            os.makedirs(_data_folder)

        filename = os.path.join(_data_folder, 'settings')
        return filename

    def load_config(self):
        filename = self.config_filename()
        try:
            with open(filename, 'r') as f:
                _enc_ = f.read()
                _text_ = EncDec().decrypt(_enc_)
                self.items = json.loads(_text_)
        except FileNotFoundError:
            self.items = copy.deepcopy(Defaults().values)
        except OSError as e:
            print(str(e))

        #
        # add any missing items
        #
        for i in Defaults().values:
            def_name = i['name']
            found = False
            for item in self.items:
                if item['name'] == def_name:
                    found = True
                    break
            if not found:
                new_item = {'name': i['name'], 'value': i['value']}
                self.items.append(new_item)

        # determine appname
        for i in self.items:
            if i['name'] == 'appname':
                self.appname = i['value']

        return

    def save_config(self):
        filename = self.config_filename()
        try:
            with open(filename, 'w') as output_file:
                _text_ = json.dumps(self.items)
                _enc_ = EncDec().encrypt(_text_)
                output_file.write(_enc_)
        except Exception as e:
            print(str(e))

    def get(self, name: str = ''):
        result = ''
        for item in self.items:
            if name == item['name']:
                result = item['value']
                break
        return result

    def set(self, name: str = '', value: str = ''):
        item_found = False
        for item in self.items:
            if name == item['name']:
                item['value'] = value
                item_found = True
                break
        if not item_found:
            item = {'name': name, 'value': value}
            self.items.append(item)

        return

    def __str__(self):
        return json.dumps(self.items)