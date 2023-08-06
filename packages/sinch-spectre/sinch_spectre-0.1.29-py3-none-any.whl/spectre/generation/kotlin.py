from enum import Enum
from spectre import utils
from spectre import serializer
from spectre.model import Entity, SpectreType, Field, UnknownTypeException
from spectre.config import Config

BASE_IMPORTS = [ 'java.util.List' ]

class ClassType(Enum):
    ENTITY = 1,
    REPOSITORY = 2
    MANAGER = 3
    REST_CONTROLLER = 4
    DTO = 5

    def get_name(self, entity_name: str):
        name = utils.to_pascal(entity_name)
        if self is ClassType.ENTITY:
            return name
        if self is ClassType.DTO:
            return f'{name}DTO'
        if self is ClassType.REPOSITORY:
            return f'{name}Repository'
        if self is ClassType.MANAGER:
            return f'{name}Manager'
        if self is ClassType.REST_CONTROLLER:
            return f'{name}Controller'
        raise UnknownTypeException(f'Unknown Kotlin class type (Naming not yet implemented): {self}')
        
def get_out_path(entity: Entity, config: Config, t: ClassType):
    path = ['src/main/kotlin']
    package = get_package(entity, config, t)
    path.append(package.replace('.', '/'))
    path.append(f'{t.get_name(entity.name)}.kt')
    return '/'.join(path)

def get_package(entity: Entity, config: Config, t: ClassType):
    package = [config.namespace]
    if t is ClassType.ENTITY:
        package.append(f'model')
    if t is ClassType.DTO:
        package.append(f'model.dto')
    if t is ClassType.REPOSITORY:
        package.append(f'dao')
    if t is ClassType.MANAGER:
        package.append(f'manager')
    if t is ClassType.REST_CONTROLLER:
        package.append(f'rest')
    return '.'.join(package).lower()

def get_type(t: SpectreType, name = None):
    '''
    Convert from a generic Spectre type to a specific Java type. Name of field is used if type is an enum, not needed otherwise
    '''
    if t is SpectreType.INT:
        return 'Int'
    if t is SpectreType.STRING:
        return 'String'
    if t is SpectreType.TIMESTAMP:
        return 'Instant'
    if t is SpectreType.BOOL:
        return 'Boolean'
    if t is SpectreType.FLOAT:
        return 'Double'
    if t is SpectreType.ENUM:
        return 'String'
    if t is SpectreType.UUID:
        return 'UUID'
    if t is SpectreType.BINARY:
        return 'ByteArray'
    raise UnknownTypeException(f'Unknown Spectre type (Kotlin mapping not yet implemented): {t.name}')

def generate(config: Config, path):
    entities = utils.read_entities(path)
    written = []
    for ent in entities:
        written.extend(write_classes(ent, config))
    return written

def get_class_stub(entity: Entity, imports, config: Config, class_type: ClassType):

    output = [f'package {get_package(entity, config, class_type)}', '']
    entity_name = utils.to_pascal(ClassType.ENTITY.get_name(entity.name))

    if imports:
        output.extend([ get_import(i) for i in imports ])
        output.append('')

    class_name = class_type.get_name(entity.name)
    if class_type is ClassType.ENTITY:
        if config.generator_options.get('spring_data', False):
            output.append('@Entity')
        output.append(f'class {class_name} (')
    if class_type is ClassType.DTO:
        output.append(f'class {class_name} (')
    if class_type is ClassType.MANAGER:
        output.append('@Service')
        output.append(f'class {class_name} (')
    if class_type is ClassType.REPOSITORY:
        output.append('@Repository')
        output.append(f'interface {class_name}: JpaRepository<{entity_name}, {get_type(SpectreType.UUID)}> {{')
    if class_type is ClassType.REST_CONTROLLER:
        output.append('@RestController')
        output.append('@RequestMapping("' + f'/api/{entity_name}")'.lower())
        output.append(f'class {class_name} (')

    output.append('')
    return output

def get_imports(fields):
    output = set()
    for field in fields:
        if field.type is SpectreType.TIMESTAMP:
            output.add('java.time.Instant')
        if field.type is SpectreType.UUID:
            output.add('java.util.UUID')
    return list(output)

def get_import(name):
    return f'import {name}'

def get_entity_imports():
    output = []
    for c in [ 'Entity', 'GeneratedValue', 'GenerationType', 'Id' ]:
        output.append(f'javax.persistence.{c}')
    return output

def get_field(field: Field, config: Config, t: ClassType):
    output = []
    if t is ClassType.ENTITY:
       if config.generator_options.get('spring_data', False) and field.type is SpectreType.UUID:
            output.extend(['\t@Id', '\t@GeneratedValue(strategy=GenerationType.AUTO)'])
    output.append(f'\tval {utils.to_camel(utils.to_pascal(field.name))}: {get_type(field.type, field.name)},\n')
    return output

def create_constructor(name, arguments):
    signature = f'{create_signature(name=name, arguments=arguments)} {{'
    output = [ signature ]
    for arg_tuple in arguments:
        arg_name = utils.to_camel(arg_tuple[0])
        output.append(f'\t\tthis.{arg_name} = {arg_name};')
    output.extend([ '\t}', '' ] )
    return output

def create_signature(name, arguments=[], visibility='public', return_type=None):
    signature = [f'\tfun ']
    signature.append(f'{name}')
    signature.append('(')
    for index, val in enumerate(arguments):
        (t, var) = val
        signature.append(f'{var}: {t}')
        if len(arguments) > index + 2:
            signature.append(',')
    signature.append(')')
    if return_type:
        signature.append(f': {return_type}')
    return ''.join(signature)

def create_function(visibility, return_type, name, arguments, body=None, annotation=None):
    output = []
    if annotation:
        output.append(f'\t{annotation}')
    signature = create_signature(visibility=visibility, return_type=return_type, arguments=arguments, name=name)
    if body:
        signature = "".join(signature) + ' {'
        output.append(signature) 
        [ output.append(f'\t\t{line}') for line in body ]
        output.append('\t}')
        return output
    else:
        output.append("".join(signature))
        return output

def get_getter_parameters(entity: Entity):
    """Get argument type and variable name for an entity using ID. For use in function signatures
    
    Arguments:
        entity {Entity} -- The entity for which to generate the getter arguments
    
    Returns:
        [tuple] -- Tuple holding the Type [0] and Variable Name [1]
    """
    return ( get_type(SpectreType.UUID), get_id_name(entity.name) )

def get_id_name(entity_name):
    return f'{utils.to_camel(entity_name)}Id'

def generate_model(entity: Entity, config: Config, class_type: ClassType = ClassType.ENTITY):
    imports = get_imports(entity.fields)
    if config.generator_options.get('spring_data', False):
        for imprt in get_entity_imports():
            imports.append(imprt)
    output = get_class_stub(entity, imports, config, class_type)
    for field in entity.fields:
        output.extend(get_field(field, config, class_type))
    """ Remove trailing comma """
    output.append(output.pop()[:-2] + "\n")
    output.append(')')
    return output

def write_model(entity: Entity, config: Config):
    output = "\n".join(generate_model(entity, config))
    path = get_out_path(entity, config, ClassType.ENTITY)
    return utils.write_to_file(output, path, config)

def generate_method(method_name, method_map):
    try:
        return create_function(
            visibility=method_map.get('visibility', 'public'), 
            return_type=method_map['return_type'],
            name=method_map['name'], 
            arguments=method_map.get('arguments', []),
            body=method_map.get('body', None),
            annotation=method_map.get('annotation', None)
        )
    except KeyError:
        raise Exception(f'Java generator does not implement method {method_name}')

def generate_repository(entity: Entity, config: Config):
    entity_name = ClassType.ENTITY.get_name(entity.name)

    method_map = {
        'delete_by_id': {
            'name': 'deleteById',
            'return_type': 'Unit',
            'arguments': [ (get_type(SpectreType.UUID), get_id_name(entity_name)) ]
        },
    }

    imports = [f'{get_package(entity, config, ClassType.ENTITY)}.{entity_name}']
    imports.extend(BASE_IMPORTS)
    imports.extend([f'org.springframework.{c}' for c in ['data.jpa.repository.JpaRepository', 'stereotype.Repository']])
    imports.append('java.util.UUID')
    output = get_class_stub(entity, imports, config, ClassType.REPOSITORY)
    output.extend(generate_method('delete_by_id', method_map['delete_by_id']))
    output.append('}')
    return output

def write_repository(entity: Entity, config: Config):
    path = get_out_path(entity, config, ClassType.REPOSITORY)
    return utils.write_to_file('\n'.join(generate_repository(entity, config)), path, config)

#TODO: Finish method generation, add some kind of httpresponses etc to imports
def generate_controller(entity: Entity, config: Config):

    entity_type = ClassType.ENTITY.get_name(entity.name)
    entity_var = utils.to_camel(entity.name)
    manager_type = ClassType.MANAGER.get_name(entity.name)
    manager_var = utils.to_camel(ClassType.MANAGER.get_name(entity.name))
    id_parameters = get_getter_parameters(entity)

    #TODO: Add bodies
    method_map = {
        'list': {
            'name': 'list',
            'return_type': f'List<{entity_type}>',
            'body': [
                f'log.info("Request to retrieve all {entity_type}")',
                f'return {manager_var}.getAll()',
            ],
            'annotation': f'@GetMapping("")'
        },
        'get': {
            'name': 'get',
            'return_type': f'ResponseEntity<{entity_type}>',
            'arguments': [ (id_parameters[0], f'@PathVariable {id_parameters[1]}') ],
            'body': [
                f'log.info("Request to retrieve {entity_type}: {{}}", {id_parameters[1]})',
                f'val entity = {manager_var}.get({get_id_name(entity_type)})',
                f'return if(null == entity) ResponseEntity.notFound().build() else ResponseEntity.ok(entity)',
            ],
            'annotation': f'@GetMapping("/{{{id_parameters[1]}}}")'
        },
        'create': {
            'name': 'create',
            'return_type': entity_type,
            'arguments': [ (entity_type, f'@RequestBody {entity_var}') ],
            'body': [
                f'log.info("Request to create {entity_type}: {{}}", {entity_var})',
                f'return {manager_var}.save({entity_var})'
            ],
            'annotation': '@PostMapping'
        },
        'update': {
            'name': 'update',
            'return_type': entity_type,
            'arguments': [ (entity_type, f'@RequestBody {entity_var}') ],
            'body': [
                f'log.info("Request to update {entity_type}: {{}}", {entity_var})',
                f'return {manager_var}.save({entity_var})'
            ],
            'annotation': '@PutMapping'
        },
        'delete': {
            'name': 'delete',
            'return_type': 'Unit',
            'arguments': [ (id_parameters[0], f'@PathVariable {id_parameters[1]}') ],
            'body': [ 
                f'log.info("Request to delete {entity_type} with ID {{}}", {id_parameters[1]})',
                f'{manager_var}.deleteById({get_id_name(entity_type)})',
            ],
            'annotation': f'@DeleteMapping("/{{{id_parameters[1]}}}")'
        }
    }

    imports = [f'{get_package(entity, config, ClassType.ENTITY)}.{ClassType.ENTITY.get_name(entity.name)}']
    imports.extend(BASE_IMPORTS)
    imports.append(f'{get_package(entity, config, ClassType.MANAGER)}.{ClassType.MANAGER.get_name(entity.name)}')
    imports.extend([ 'org.slf4j.LoggerFactory', 'org.springframework.http.ResponseEntity', 'java.util.UUID' ])
    imports.extend(
        [ 
            f'org.springframework.web.bind.annotation.{c}' for c in 
                [
                    'GetMapping',
                    'PathVariable',
                    'RequestBody',
                    'RequestMapping',
                    'RestController',
                    'PostMapping',
                    'PutMapping',
                    'DeleteMapping',
                ]
        ]
    )
    output = get_class_stub(entity, imports, config, ClassType.REST_CONTROLLER)

    output.append(f'\tprivate val {manager_var}: {manager_type}\n')

    output.append(f') {{')

    output.append(f'\tprivate val log = LoggerFactory.getLogger(javaClass)')
    output.append('')

    for method in config.methods:
        if method in method_map.keys():
            output.extend(generate_method(method, method_map[method]))
            output.append('')

    output.append('}')
    return output

def write_controller(entity: Entity, config: Config):
    path = get_out_path(entity, config, ClassType.REST_CONTROLLER)
    return utils.write_to_file('\n'.join(generate_controller(entity, config)), path, config)

def generate_manager(entity: Entity, config: Config):
    entity_name = ClassType.ENTITY.get_name(entity.name)
    imports = [f'{get_package(entity, config, ClassType.ENTITY)}.{entity_name}']
    imports.append('org.springframework.stereotype.Service')
    imports.extend(BASE_IMPORTS)
    imports.extend(['org.slf4j.LoggerFactory', 'java.util.UUID'])
    imports.append(f'{get_package(entity, config, ClassType.REPOSITORY)}.{ClassType.REPOSITORY.get_name(entity.name)}')
    output = get_class_stub(entity, imports, config, ClassType.MANAGER)
    repo_pascal = ClassType.REPOSITORY.get_name(entity_name)
    repo_camel = utils.to_camel(repo_pascal)
    method_map = {
        'list': {
            'name': 'getAll',
            'return_type': f'List<{entity_name}>',
            'body': [f'return {repo_camel}.findAll()'],
        },
        'get': {
            'name': f'get',
            'return_type': f'{entity_name}?',
            'arguments': [get_getter_parameters(entity)],
            'body': [f'return {repo_camel}.findByIdOrNull({get_id_name(entity.name)})'],
        },
        'create': {
            'name': 'save',
            'return_type': entity_name,
            'arguments': [ (entity_name, utils.to_camel(entity_name)) ],
            'body': [f'return {repo_camel}.save({utils.to_camel(entity.name)})'],
        },
        'delete': {
            'name': 'delete',
            'return_type': 'Unit',
            'arguments': [ (entity_name, utils.to_camel(entity_name)) ],
            'body': [f'{repo_camel}.delete({utils.to_camel(entity.name)})'],
        },
        'delete_by_id': {
            'name': 'deleteById',
            'return_type': 'Unit',
            'arguments': [ (get_type(SpectreType.UUID), get_id_name(entity_name)) ],
            'body': [f'{repo_camel}.deleteById({get_id_name(entity_name)})'],
        },
    }
    output.append(f'\tprivate val {repo_camel}: {repo_pascal}\n')

    output.append(f') {{')

    output.append(f'\tprivate val log = LoggerFactory.getLogger(javaClass)')
    output.append('')

    for method in config.methods:
        #update and create is currently the same. dont want to generate twice. If different impl is needed, add update to method map and remove check
        if method in method_map.keys():
            output.extend(generate_method(method, method_map[method]))
            output.append('')
    if 'delete' in config.methods:
        output.extend(generate_method('delete_by_id', method_map['delete_by_id']))
    output.append('}')
    return output

def write_manager(entity: Entity, config: Config):
    path = get_out_path(entity, config, ClassType.MANAGER)
    return utils.write_to_file('\n'.join(generate_manager(entity, config)), path, config)

def write_dto(entity: Entity, config: Config):
    #TODO: Add mapping interface between this and model and convenience methods
    path = get_out_path(entity, config, ClassType.DTO)
    return utils.write_to_file('\n'.join(generate_model(entity, config, ClassType.DTO)), path, config)

def write_classes(entity: Entity, config: Config):
    output = []
    if config.generator_options.get('pojo', False):
        output.append(write_model(entity, config))
    if config.generator_options.get('manager', False):
        output.append(write_manager(entity, config))
    if config.generator_options.get('dto', False):
        output.append(write_dto(entity, config))
    if config.generator_options.get('spring_data', False):
        output.append(write_repository(entity, config))
    if config.generator_options.get('spring_web', False):
        output.append(write_controller(entity, config))
    return output
