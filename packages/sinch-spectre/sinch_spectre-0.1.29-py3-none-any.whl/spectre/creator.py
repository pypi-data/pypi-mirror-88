import click
from spectre import utils
from spectre.config import Config
from spectre.model import Entity, Field, SpectreType

def write_config(config: Config = None):
    config = create_config(config)
    output = config.to_yml()
    path = f'{Config.spectre_dir}/spectre.yml'
    with open(path, mode='w') as file:
        file.write(output)
    return path

def create_config(config: Config = None):
    if not config:
        config = Config()
    defaults = Config()
    config.name = click.prompt('App/service Name', type=str, default=config.name)
    config.namespace = click.prompt('Namespace/package', type=str, default=config.namespace)
    config.description = click.prompt('Service description', type=str, default=config.description)
    click.echo('Select which methods to implement in interfaces')
    methods = []
    for choice in defaults.methods:
        if click.confirm(f'Add {choice} method?', default=choice in config.methods):
            methods.append(choice)
    config.methods = methods
    return config

def create_entity():
    name = click.prompt('Entity name', type=str)
    entity = Entity(name)
    entity.description = click.prompt('Description', type=str, default='')

    fields = []
    if click.confirm('Add ID field?', default=True):
        fields.append(Field(name='id', type=SpectreType.UUID, required=True, primary_key=True))
        click.echo('ID field added')
    add_field = True
    while add_field:
        click.echo('Adding new field')
        field = create_field()
        fields.append(field)
        add_field = click.confirm('Add another field?')
    entity.fields = fields
    entity.validate()
    return entity

def write_entity(config):
    entity = create_entity()
    output = entity.to_json()
    path = f'{entity.name.lower()}.spec'
    with open(path, mode='w') as file:
        file.write(output)
    return path

def create_field():
    field = Field()
    field.name = click.prompt('Field name', type=str)
    field.type = prompt_type()
    field.description = click.prompt('Field description', type=str, default='')
    field.required = prompt_boolean('Required?')
    return field

def prompt_boolean(prompt):
    choice = click.prompt(f'{prompt}', type=click.Choice(['y', 'N'], case_sensitive=False), default='N')
    return 'y' in choice.lower()

def prompt_type():
    choices = []
    for index, value in enumerate(SpectreType):
        if value is not SpectreType.UNDEFINED:
            print(f'{index}: {value.name}')
            choices.append(f'{index}')
    choice = click.prompt('Field type', type=click.Choice(choices), show_choices=False)
    return SpectreType(int(choice))