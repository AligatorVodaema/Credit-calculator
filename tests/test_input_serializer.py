import pytest

from serializers import InputSerializer, InputSerializerError


def test_success_parse():
    """Default successful case."""
    input_string = (
        'amount: 100000\ninterest: 5.5%\ndownpayment: 20000\nterm: 30\n'
    )
    result_dict = InputSerializer(input_string).parse_input()
    assert isinstance(result_dict, dict) == True
    assert len(result_dict) == 4
    assert tuple(result_dict) == InputSerializer.REQUIRED_KEYS
    assert all(
        [isinstance(val, (float, int)) for _, val in result_dict.items()]
    ) == True


def test_fail_parse_fields():
    """No field term."""
    input_string = (
        'amount: 40000\ninterest: 3.9%\ndownpayment: 0\n\n'
    )
    with pytest.raises(
        InputSerializerError, match='Not four values received'
    ):
        InputSerializer(input_string).parse_input()
    

def test_success_parse_with_typos():
    """Fix typos in fields."""
    input_string = (
        'amut: 300000\nintetesst: 10%\ndwnpaument: 0\ntrme: 10\n'
    )
    result_dict = InputSerializer(input_string).parse_input()
    assert tuple(result_dict) == InputSerializer.REQUIRED_KEYS


def test_fail_parse_with_hard_typo():
    """Field 'percent' must be 'intetesst'."""
    input_string = (
        'amount: 200000\npercent: 3.3%\ndownpayment: 1000\nterm: 5\n'
    )
    with pytest.raises(InputSerializerError, match='"percent" wrong field'):
        InputSerializer(input_string).parse_input()
    
    
def test_fail_parse_no_field():
    """Input string without field."""
    input_string = (
        ': 32000\ninterest: 2.1%\ndownpayment: 0\nterm: 30\n'
    )
    with pytest.raises(InputSerializerError, match='Missing field or value'):
        InputSerializer(input_string).parse_input()
    
    
def test_fail_parse_no_value():
    """Input string without value on field downpayment."""
    input_string = (
        'amount: 32000\ninterest: 2.1%\ndownpayment: \nterm: 30\n'
    )
    with pytest.raises(InputSerializerError, match='Missing field or value'):
        InputSerializer(input_string).parse_input()
    
    
def test_fail_parse_inccorrect_value():
    """Incorrect amount field."""
    input_string = (
        'amount: eval("print(\"hello\")")\ninterest: 3,1%\n'
        'downpayment: 500\nterm: 4\n'
    )
    with pytest.raises(InputSerializerError, match='Incorrect value'):
        InputSerializer(input_string).parse_input()
