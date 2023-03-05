import os

dirname = os.path.dirname(__file__)

path_to_files = os.path.join(dirname, 'logs')
log_dir = 'uilogs'
pomp_tagged_dir = 'pompTagged'
output_dir = 'output'

context_attributes_ActionLogger = ["eventType", "target.name", "targetApp", "target.workbookName", "target.sheetName", "target.innerText", "target.tagName"]
context_attributes_smartRPA = ["category","application","event_type","worksheets","current_worksheet","tag_category","tag_type","tag_name","tag_title","xpath","xpath_full"]
# Attributes that classify the type of object interacted with, i.e. tag_type in smartRPA can be "Submit" or the field value
semantic_attributes = ["target.innerText", "target.name"] # "tag_type"
value_attributes = ["target.innerText", "url", "target.value", "content"]


# POMP Action Dimensions
action_Dimensions = ["Open Action", "Navigate Action", "Transform Action", "Transfer Action","Conclude Action", "Close Action", "Empty Action"]