import re
from spectre import serializer
from spectre.config import Config
from spectre.model import Entity, SpectreType, Field
from spectre import utils
from spectre.utils import make_form, get_form_name, to_pascal, write_to_file, is_id

CHANGE_SET_COUNTER = 1

def write(doc, config):
    outfile = f"liquibase/db.changelog-master.yaml"
    yamlstr = serializer.to_yml(doc)
    return write_to_file(yamlstr, outfile, config)

def generate(config: Config, path):

    changelog = []
    entities = utils.read_entities(path)
    for ent in entities:
        changelog.append( {'changeSet': build_initial_change_set(ent, config) } )

    doc = { 'databaseChangeLog': changelog }
    return [ write(doc, config) ]

def build_initial_change_set(ent: Entity, config: Config):
    global CHANGE_SET_COUNTER
    change_set = {}
    change_set['id'] = CHANGE_SET_COUNTER
    change_set['author'] = config.author
    change_set['changes'] = [ {'createTable': create_table(ent) }]
    CHANGE_SET_COUNTER += 1 
    return change_set

def create_table(ent: Entity):
    table = {}
    table['tableName'] = ent.name
    columns = []
    for field in ent.fields:
        
        column = {}
        column['name'] = field.name
        column['type'] = convert_type(field)
        if is_id(field):
            column['constraints'] = {
                'primaryKey': True,
                'nullable': False
            }
        elif field.required:
            column['constraints'] = {
                'nullable': False
            }
        columns.append( {'column': column})
    table['columns'] = columns
    return table

def convert_type(field: Field):
    if field.type is SpectreType.UUID: 
        return 'binary(16)'
    if field.type is SpectreType.FLOAT:
        return 'double'
    if field.type is SpectreType.STRING: 
        return f'varchar()'
    if field.type is SpectreType.INT: 
        return 'int'
    if field.type is SpectreType.BINARY:
        return 'varbinary()'
    if field.type is SpectreType.ENUM:
        return "enum('foo','bar')"
    if field.type is SpectreType.TIMESTAMP:
        return 'datetime'
    if field.type is SpectreType.UNDEFINED:
        return 'undefined'
    #Return mapped value if present, otherwise default to given type
    return f'UNSUPPORTED_TYPE({field.type})'
