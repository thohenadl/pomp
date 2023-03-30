import os

dirname = os.path.dirname(__file__)
seperator = ";"

log_dir = 'uilogs'
pomp_tagged_dir = 'pompTagged'
output_dir = 'output'

path_to_files = os.path.join(dirname, 'logs')
path_to_untagged = os.path.join(path_to_files, log_dir)
path_to_pomp = path_to_files + "/" + pomp_tagged_dir + "/"
# Only used for storing logs:
csv_sep = ";"

overhead_columns = ["case:concept:name", "time:timestamp", "org:resource", "case:creator", "lifecycle:transition"]
context_attributes_ActionLogger = ["eventType", "target.name", "targetApp", "target.workbookName", "target.sheetName", "target.innerText", "target.tagName"]
context_attributes_smartRPA = ["concept:name","category","application","id","event_type","tag_category","tag_type","tag_title"]
context_attributes_all = context_attributes_ActionLogger + context_attributes_smartRPA
# Attributes that classify the type of object interacted with, i.e. tag_type in smartRPA can be "Submit" or the field value
semantic_attributes = ["target.innerText", "target.name"] # "tag_type"
value_attributes = ["target.innerText", "url", "target.value", "content"]

TERMS_FOR_MISSING = ['MISSING', 'UNDEFINED', 'undefined', 'missing', 'none', 'nan', 'empty', 'empties', 'unknown',
                     'other', 'others', 'na', 'nil', 'null', '', "", ' ', '<unknown>', "0;n/a", "NIL", 'undefined',
                     'missing', 'none', 'nan', 'empty', 'empties', 'unknown', 'other', 'others', 'na',
                     'nil', 'null', '', ' ']


# POMP Action Dimensions
action_Dimensions = ["","Open Action", "Navigate Action", "Transform Action", "Transfer Action","Conclude Action", "Close Action", "Empty Action"]