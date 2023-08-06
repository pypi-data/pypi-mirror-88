import importlib_metadata
from pprint import pprint
from gidtools.gidfiles import writejson, writeit
to_check = ['psutil']
_clean_to_check = []

for item in to_check:
    if ' ' in item:
        item = item.split(' ')[0]
    _clean_to_check.append(item)
_out_list = []
_out_dict = {}
for pack in _clean_to_check:
    x = importlib_metadata.metadata(pack).get_all('Provides-Extra')
    y = importlib_metadata.metadata(pack).get_all('Requires-Dist')
    _uninstall_string = f"call pip uninstall -q -y {pack}"
    _out_list.append(_uninstall_string)
    _out_dict[pack] = {'extras': x, 'requires': y}

writejson(_out_dict, "check.json")
writeit('test.txt', '\n'.join(_out_list))
