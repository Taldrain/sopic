from sopic.dag import is_valid_dag


def test_is_valid_dag():
    assert is_valid_dag({
        'foo': (None, ['bar']),
    })
    assert is_valid_dag({
        'foo': (None, {}),
    })
    assert is_valid_dag({
        'foo': (None, {'ok': 'bar'}),
        'bar': (None, {}),
    })
    assert is_valid_dag({
        'foo': (None, ['bar']),
        'bar': (None, []),
    })
    assert is_valid_dag({
        'foo': (None, ['bar']),
        'bar': (None, ['baz']),
    })
    assert is_valid_dag({
        'start': (None, ['left', 'right']),
        'left': (None, ['end']),
        'right': (None, ['end']),
    })
    assert not is_valid_dag({
        'start': (None, ['end']),
        'end': (None, ['start']),
    })
    assert not is_valid_dag({
        'start': (None, ['foo']),
        'foo': (None, {'ok': 'start'}),
        'end': (None, ['start']),
    })
    assert not is_valid_dag({
        'start': (None, ['end']),
        'end': (None, ['end']),
    })
