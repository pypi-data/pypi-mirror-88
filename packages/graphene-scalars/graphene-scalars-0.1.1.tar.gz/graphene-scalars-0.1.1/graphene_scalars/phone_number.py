from graphene.types import Scalar
from graphql.language import ast
from pydantic import BaseModel, validator
from phonenumbers import parse, is_valid_number


class PhoneNumberModel(BaseModel):
    value: str

    @validator("value")
    def value_phone_number(v):
        assert str(v), "value must be string"
        assert is_valid_number(parse(v, None)), "value must be a valid phone number"
        return v


class PhoneNumber(Scalar):
    """PhoneNumber: E.164 numbers are formatted
    [+] [country code] [subscriber number including area code]
    and can have a maximum of fifteen digits"""

    @staticmethod
    def serialize(value):
        return PhoneNumberModel(value=value).value

    @staticmethod
    def parse_literal(node):
        if isinstance(node, ast.StringValue):
            return PhoneNumberModel(value=node.value).value

    @staticmethod
    def parse_value(value):
        return PhoneNumberModel(value=value).value
