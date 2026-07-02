from pydantic import BaseModel, Field, field_validator


class LoginRequest(BaseModel):
    username: str
    password: str


class RegisterRequest(BaseModel):
    """Admin self-registration."""

    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=6)
    confirm_password: str

    @field_validator("username")
    @classmethod
    def username_alphanumeric(cls, v: str) -> str:
        v = v.strip()
        if not v.replace("_", "").replace(".", "").isalnum():
            raise ValueError("Username can only contain letters, numbers, '.' and '_'.")
        return v


class StudentRegisterRequest(BaseModel):
    """Student self-registration. Any hall ticket can register; it links to
    a published Student record automatically if one exists."""

    hallticket: str = Field(min_length=3, max_length=30)
    password: str = Field(min_length=6)
    confirm_password: str

    @field_validator("hallticket")
    @classmethod
    def normalize_hallticket(cls, v: str) -> str:
        return v.strip().upper()


class StudentLoginRequest(BaseModel):
    hallticket: str
    password: str

    @field_validator("hallticket")
    @classmethod
    def normalize_hallticket(cls, v: str) -> str:
        return v.strip().upper()


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str = "admin"
    username: str
    name: str | None = None


class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str = Field(min_length=6)
