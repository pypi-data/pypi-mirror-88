import pytest
from spectre.model import Entity, SpectreType, Field
from builtins import any
from spectre.generation import kotlin
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
    return Entity('TestEntity', 'An entity used for testing kotlin generation', sample_fields)

@pytest.fixture
def config():
    output = Config()
    output.namespace = 'spectre.kotlin.test'
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
    imports = kotlin.get_imports(fields)
    assert 'java.time.Instant' in imports
    assert 'java.util.UUID' in imports

    fields = [
        Field(name='BarTimestamp', type=SpectreType.TIMESTAMP),
    ]
    imports = kotlin.get_imports(fields)
    assert 'java.time.Instant' in imports

    fields = [
        Field(name='Id', type=SpectreType.UUID),
    ]
    imports = kotlin.get_imports(fields)
    assert 'java.util.UUID' in imports

    fields = []
    imports = kotlin.get_imports(fields)
    assert len(imports) == 0

def test_generate_dto(entity, config):
    output = kotlin.generate_model(entity, config, kotlin.ClassType.DTO)
    assert string_in_collection('package spectre.kotlin.test.model.dto', output)
    assert string_in_collection('class TestEntityDTO', output)
    assert string_in_collection('val stringField: String', output)
    assert string_in_collection('val id: UUID', output)
    assert string_in_collection('val fooInt: Int', output)
    assert string_in_collection('val barTimestamp: Instant', output)
    assert not string_in_collection(';', output)

def test_generate_model(entity, config):
    output = kotlin.generate_model(entity, config)
    assert string_in_collection('package spectre.kotlin.test.model', output)
    assert string_in_collection('class TestEntity', output)
    assert string_in_collection('val stringField: String', output)
    assert string_in_collection('val id: UUID', output)
    assert string_in_collection('val fooInt: Int', output)
    assert string_in_collection('val barTimestamp: Instant', output)

def test_generate_repository(entity, config):
    output = kotlin.generate_repository(entity, config)
    assert string_in_collection('import spectre.kotlin.test.model.TestEntity', output)
    assert string_in_collection('import org.springframework.data.jpa.repository.JpaRepository', output)
    assert string_in_collection('import org.springframework.stereotype.Repository', output)
    assert string_in_collection('@Repository', output)
    assert string_in_collection('TestEntityRepository: JpaRepository<TestEntity, UUID>', output)

def test_generate_manager(entity, config):
    output = kotlin.generate_manager(entity, config)
    assert string_in_collection('import spectre.kotlin.test.model.TestEntity', output)
    assert string_in_collection('import spectre.kotlin.test.dao.TestEntityRepository', output)
    assert string_in_collection('@Service', output)
    assert string_in_collection('class TestEntityManager', output)
    assert string_in_collection('fun get(', output)
    assert string_in_collection('return testEntityRepository.findByIdOrNull(testEntityId)', output)

def test_generate_controller(entity, config):
    output = kotlin.generate_controller(entity, config)
    test = "\n".join(output)
    assert string_in_collection('@RestController', output)
    assert string_in_collection('@RequestMapping("/api/testentity")', output)
    assert string_in_collection('@GetMapping("")', output)
    assert string_in_collection('@GetMapping("/{testEntityId}")', output)
    assert string_in_collection('@PostMapping', output)
    assert string_in_collection('@PutMapping', output)
    assert string_in_collection('@DeleteMapping', output)
    assert string_in_collection('val log = LoggerFactory.getLogger(javaClass)', output)
    assert string_in_collection('log.info("Request to retrieve all TestEntity"', output)
    assert string_in_collection('fun list(): List<TestEntity>', output)
    assert string_in_collection('fun get(@PathVariable', output)
    assert string_in_collection('val entity = testEntityManager.get(testEntityId)', output)
    assert string_in_collection('return if(null == entity) ResponseEntity.notFound().build() else ResponseEntity.ok(entity)', output)
    assert string_in_collection('fun create(@RequestBody testEntity: TestEntity): TestEntity', output)
    assert string_in_collection('return testEntityManager.save(testEntity)', output)
    assert string_in_collection('fun update(@RequestBody testEntity: TestEntity): TestEntity', output)
    assert string_in_collection('fun delete(@PathVariable', output)
    assert string_in_collection('testEntityManager.deleteById(testEntityId)', output)