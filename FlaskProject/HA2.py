from pydantic import BaseModel, EmailStr, Field, ValidationError, field_validator
import json


class Address(BaseModel):
    city: str = Field(min_length=2)
    street: str = Field(min_length=3)
    house_number: int = Field(gt=0)


class User(BaseModel):
    name: str = Field(..., min_length=2, pattern="^[a-zA-Z]+$")
    age: int = Field(..., ge=0, le=120)
    email: EmailStr
    is_employed: bool
    address: Address

    @field_validator("age")
    def validate_employment_age(cls, age, values):
        is_employed = values.data.get("is_employed")
        if is_employed and (age < 18 or age > 65):
            raise ValueError("Если занят, возраст от 18 до 65 лет")
        return age


def process_user_registration(json_str: str):
    try:
        user = User.model_validate_json(json_str)
        return user.model_dump_json(indent=4)
    except ValidationError as e:
        return json.dumps({"error": e.errors()}, indent=4, ensure_ascii=False)




json_input = """{
    "name": "John Doe",
    "age": 70,
    "email": "john.doe@example.com",
    "is_employed": true,
    "address": {
        "city": "New York",
        "street": "5th Avenue",
        "house_number": 123
    }
}"""

print(process_user_registration(json_input))


