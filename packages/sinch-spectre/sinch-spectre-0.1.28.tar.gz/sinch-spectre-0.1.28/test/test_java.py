import pytest
from spectre.model import Entity, SpectreType, Field
from builtins import any
from spectre.generation import java
from spectre.config import Config

@pytest.fixture
def sample_fields():
    fields = [
        Field(name='StringField', type=SpectreType.STRING, description='A required field', required=True, default='default str val', example='AnExampleValue'),
        Field(name='Id', type=SpectreType.UUID),
        Field(name='FooInt', type=SpectreType.INT),
        Field(name='BarTimestamp', type=SpectreType.TIMESTAMP),
    ]
    return fields

@pytest.fixture
def entity(sample_fields):
    return Entity('TestEntity', 'An entity used for testing java generation', sample_fields)

@pytest.fixture
def config():
    output = Config()
    output.namespace = 'spectre.java.test'
    output.generator_options = {
        'spring_data': True,
        'spring_web': True,
    }
    return output

def string_in_collection(string, collection):
    return any(string in str for str in collection)

def test_get_imports(sample_fields):
    fields = [
        Field(name='StringField', type=SpectreType.STRING, description='A required field', required=True, default='default str val', example='AnExampleValue'),
        Field(name='Id', type=SpectreType.UUID),
        Field(name='FooInt', type=SpectreType.INT),
        Field(name='BarTimestamp', type=SpectreType.TIMESTAMP),
    ]
    imports = java.get_imports(fields)
    assert 'java.time.Instant' in imports
    assert 'java.util.UUID' in imports

    fields = [
        Field(name='BarTimestamp', type=SpectreType.TIMESTAMP),
    ]
    imports = java.get_imports(fields)
    assert 'java.time.Instant' in imports

    fields = [
        Field(name='Id', type=SpectreType.UUID),
    ]
    imports = java.get_imports(fields)
    assert 'java.util.UUID' in imports

    fields = []
    imports = java.get_imports(fields)
    assert len(imports) == 0

def test_generate_dto(entity, config):
    output = java.generate_model(entity, config, java.ClassType.DTO)
    assert string_in_collection('package spectre.java.test.model.dto', output)
    assert string_in_collection('public class TestEntityDTO', output)
    assert string_in_collection('private String stringField', output)
    assert string_in_collection('private UUID id', output)
    assert string_in_collection('private Integer fooInt', output)
    assert string_in_collection('private Instant barTimestamp', output)

def test_generate_model(entity, config):
    output = java.generate_model(entity, config)
    assert string_in_collection('package spectre.java.test.model', output)
    assert string_in_collection('public class TestEntity', output)
    assert string_in_collection('private String stringField', output)
    assert string_in_collection('private UUID id', output)
    assert string_in_collection('private Integer fooInt', output)
    assert string_in_collection('private Instant barTimestamp', output)

def test_generate_repository(entity, config):
    output = java.generate_repository(entity, config)

    assert string_in_collection('import spectre.java.test.model.TestEntity', output)
    assert string_in_collection('import org.springframework.data.jpa.repository.JpaRepository;', output)
    assert string_in_collection('import org.springframework.stereotype.Repository;', output)
    assert string_in_collection('@Repository', output)
    assert string_in_collection('TestEntityRepository extends JpaRepository<TestEntity', output)
    assert string_in_collection('public List<TestEntity> findAll();', output)
    assert string_in_collection('public Optional<TestEntity> findById(', output)
    assert string_in_collection('public TestEntity save(TestEntity testEntity);', output)
    assert string_in_collection('public void delete(TestEntity testEntity);', output)
    assert string_in_collection('public void deleteById(UUID testEntityId);', output)

def test_generate_manager(entity, config):
    output = java.generate_manager(entity, config)
    assert string_in_collection('import spectre.java.test.model.TestEntity', output)
    assert string_in_collection('import spectre.java.test.dao.TestEntityRepository', output)
    assert string_in_collection('@Service', output)
    assert string_in_collection('public class TestEntityManager', output)
    assert string_in_collection('public Optional<TestEntity> get(', output)
    assert string_in_collection('return testEntityRepository.findById(testEntityId);', output)

def test_generate_controller(entity, config):
    output = java.generate_controller(entity, config)
    assert string_in_collection('@RestController', output)
    assert string_in_collection('@RequestMapping("/api/testentity")', output)
    assert string_in_collection('@GetMapping("")', output)
    assert string_in_collection('@GetMapping("/{testEntityId}")', output)
    assert string_in_collection('@PostMapping', output)
    assert string_in_collection('@PutMapping', output)
    assert string_in_collection('@DeleteMapping', output)
    assert string_in_collection('private final Logger log = LoggerFactory.getLogger(TestEntityController.class);', output)
    assert string_in_collection('log.info("Request to retrieve all TestEntity"', output)
    assert string_in_collection('public List<TestEntity> list()', output)
    assert string_in_collection('public Optional<TestEntity> get(@PathVariable', output)
    assert string_in_collection('return testEntityManager.get(testEntityId);', output)
    assert string_in_collection('public TestEntity create(@RequestBody TestEntity testEntity)', output)
    assert string_in_collection('return testEntityManager.save(testEntity);', output)
    assert string_in_collection('public TestEntity update(@RequestBody TestEntity testEntity)', output)
    assert string_in_collection('public void delete(@PathVariable', output)
    assert string_in_collection('testEntityManager.deleteById(testEntityId);', output)