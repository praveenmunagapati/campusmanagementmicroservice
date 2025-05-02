import pytest
from datetime import datetime
from {service_name}.models import *

def test_model_creation(db):
    """Test basic model creation and attributes."""
    # Create a test instance
    instance = ModelName(
        field1='value1',
        field2=123,
        field3=datetime.now()
    )
    
    # Add to database
    db.session.add(instance)
    db.session.commit()
    
    # Retrieve from database
    retrieved = ModelName.query.first()
    
    # Assert attributes
    assert retrieved.field1 == 'value1'
    assert retrieved.field2 == 123
    assert isinstance(retrieved.field3, datetime)

def test_model_relationships(db):
    """Test model relationships."""
    # Create parent instance
    parent = ParentModel(name='parent')
    db.session.add(parent)
    db.session.commit()
    
    # Create child instance
    child = ChildModel(
        name='child',
        parent_id=parent.id
    )
    db.session.add(child)
    db.session.commit()
    
    # Test relationship
    assert child.parent == parent
    assert child in parent.children

def test_model_validation(db):
    """Test model validation."""
    # Test required fields
    with pytest.raises(Exception):
        instance = ModelName()
        db.session.add(instance)
        db.session.commit()
    
    # Test field constraints
    with pytest.raises(Exception):
        instance = ModelName(
            field1='value1',
            field2=-1  # Assuming field2 should be positive
        )
        db.session.add(instance)
        db.session.commit()

def test_model_methods(db):
    """Test model methods."""
    # Create test instance
    instance = ModelName(
        field1='value1',
        field2=123
    )
    db.session.add(instance)
    db.session.commit()
    
    # Test to_dict method
    data = instance.to_dict()
    assert isinstance(data, dict)
    assert data['field1'] == 'value1'
    assert data['field2'] == 123
    
    # Test other methods
    assert instance.some_method() == expected_result

def test_model_unique_constraints(db):
    """Test unique constraints."""
    # Create first instance
    instance1 = ModelName(
        field1='unique_value',
        field2=123
    )
    db.session.add(instance1)
    db.session.commit()
    
    # Try to create second instance with same unique field
    with pytest.raises(Exception):
        instance2 = ModelName(
            field1='unique_value',  # Same value as instance1
            field2=456
        )
        db.session.add(instance2)
        db.session.commit()

def test_model_cascade_delete(db):
    """Test cascade delete behavior."""
    # Create parent with children
    parent = ParentModel(name='parent')
    child1 = ChildModel(name='child1', parent=parent)
    child2 = ChildModel(name='child2', parent=parent)
    
    db.session.add(parent)
    db.session.commit()
    
    # Delete parent
    db.session.delete(parent)
    db.session.commit()
    
    # Check if children are deleted
    assert ChildModel.query.count() == 0

def test_model_default_values(db):
    """Test default values for model fields."""
    instance = ModelName(field1='value1')
    db.session.add(instance)
    db.session.commit()
    
    assert instance.field2 == default_value
    assert instance.field3 == default_value

def test_model_update(db):
    """Test model update functionality."""
    # Create instance
    instance = ModelName(
        field1='old_value',
        field2=123
    )
    db.session.add(instance)
    db.session.commit()
    
    # Update instance
    instance.field1 = 'new_value'
    instance.field2 = 456
    db.session.commit()
    
    # Retrieve and verify
    retrieved = ModelName.query.first()
    assert retrieved.field1 == 'new_value'
    assert retrieved.field2 == 456 