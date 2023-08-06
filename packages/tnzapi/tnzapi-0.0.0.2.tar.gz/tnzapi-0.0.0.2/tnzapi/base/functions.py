import json
import base64
import os

class Functions(object):

    """ Format JSON into pretty format """
    def __pretty__(self, obj):

        return json.dumps(obj,indent=4)

    """ Parse JSON """
    def __parsejson__(self, json_string):
        
        try:
            json_object = json.loads(json_string)
        except ValueError:
            return None

        return json_object

    """ Get Attachment File Name """
    def __getfilename__(self, file_loc):

        file = open(file_loc)

        return os.path.basename(file.name)

    """ Parse Attachment """
    def __getfilecontents__(self, file_loc):

        return base64.b64encode(open(file_loc,"rb").read()).decode("utf-8")
