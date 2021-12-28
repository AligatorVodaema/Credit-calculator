import ast
import re
from typing import Dict, List

from Levenshtein import distance
from loguru import logger


class InputSerializerError(Exception):
    pass


class InputSerializer:
    """Class for serializing input."""
    REQUIRED_KEYS = ('amount', 'interest', 'downpayment', 'term')
    
    def __init__(self, user_input: str) -> None:
        logger.success('Raw input: {}', user_input)
        self.raw_input = user_input
        return None
    
    def parse_input(self) -> Dict:
        """Parse the inputted string into Dict."""
        array_raw_strings = (self.raw_input).split('\n')
        four_raw_string = [string for string in array_raw_strings if string]
        
        if len(four_raw_string) != 4:
            raise InputSerializerError(
                'Not four values received. \n'
                f'Must be: {", ".join(self.REQUIRED_KEYS)}'
            )
            
        result_dict = self._parse_key_value(four_raw_string)
        logger.success(f'Parsed data: {result_dict}')
        return result_dict
    
    def _parse_key_value(self, four_raw_string: List[str]) -> Dict:
        """Split strings into key and value."""
        result_dict = {}
        for _ in range(4):
            key, value = four_raw_string[_].split(': ')
            if not key or not value:
                raise InputSerializerError('Missing field or value.')
            
            # correcting typos.
            if min([distance(key, word) for word in self.REQUIRED_KEYS]) > 2:
                raise InputSerializerError(
                    f'"{key}" wrong field. Available fields is: '
                    f'{", ".join(self.REQUIRED_KEYS)}'
                )
            key = self.REQUIRED_KEYS[_]
            
            incorrect_msg = 'Incorrect value: "{}" for field: "{}".'
            try:
                value = re.search(r'[\d.|,]+', value).group(0)
                value = ast.literal_eval(value.replace(',', '.'))
            except Exception:
                raise InputSerializerError(incorrect_msg.format(value, key))
            
            if not isinstance(value, (int, float)):
                raise InputSerializerError(incorrect_msg.format(value, key))
            
            result_dict.update({key: value})
        return result_dict
    
    
if __name__ == '__main__':
    ser1 = InputSerializer(
        'amount: 100000\ninterest: 5.5%\ndownpayment: 20000\nterm: 30\n'
    )
    print(ser1.parse_input())
    
    ser2 = InputSerializer(
        'amount: 300000\nintredt: 10.16\ndownpsyment: 0\ntermn: 5\n'
    )
    print(ser2.parse_input())
    