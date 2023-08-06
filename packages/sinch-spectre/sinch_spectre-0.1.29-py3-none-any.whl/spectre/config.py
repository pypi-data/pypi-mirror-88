import sys
import os
import yaml
from spectre import serializer
from dataclasses import dataclass, field, asdict
from typing import List, Any, Dict

CONFIG_FILE = 'spectre.yml'

def load(spectre_path = None):
    
    if not spectre_path:
        spectre_path = Config.spectre_dir
    return from_file(f'{spectre_path}/{CONFIG_FILE}')

def from_file(path):
    try:
        with open(path, 'r') as config_file:
            config_dict = yaml.full_load(config_file.read())
            output = from_dict(config_dict)
            output.spectre_dir = os.path.dirname(path)
            return output
    except Exception:
        sys.stderr.write('Could not load config file, using default config\n')
        return Config()

def from_dict(cfg):
    output = Config()
    for key, val in cfg.items():
        setattr(output, key, val)
    return output

@dataclass
class Config(object):
    namespace: str = 'com.sinch'
    name: str = 'GeneratedService'
    base_url: str = 'sinch.com'
    description: str = 'No description'
    spectre_dir: str = 'spectre'
    author: str = 'Spectre'
    generator_options: Dict = field(default_factory=dict)
    methods: List[str] = field(default_factory=lambda: [ 'list', 'get', 'create', 'update', 'delete', ])
    debug: bool = False
    

    def to_yml(self):
        settable = [ 'namespace', 'name', 'base_url', 'description', 'methods', ]
        self_dict = { k: v for k,v in asdict(self).items() if k in settable }

        return serializer.to_yml(self_dict)