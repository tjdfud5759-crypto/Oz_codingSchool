import re

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field, field_validator


# API 주소들을 하나로 묶는 Router
router = APIRouter(
    prefix="/practice_api",
    tags=["Practice API"],
)


# 기본 회원 데이터
user_list = [
    {
        "id": 1,
        "name": "홍길동",
        "age": 24,
        "email": "gildong24@example.com",
        "password": "Password1234!!",
    },
    {
        "id": 2,
        "name": "장문복",
        "age": 21,
        "email": "moonluck12@example.com",
        "password": "Check1321!",
    },
    {
        "id": 3,
        "name": "임우진",
        "age": 31,
        "email": "limousine33@example.com",
        "password": "lwsPAssword12@",
    },
]


# 이메일 형식 검사 규칙
EMAIL_PATTERN = re.compile(
    r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
)


# 이메일 형식 검사 함수
def check_email(email: str) -> str:
    if not EMAIL_PATTERN.fullmatch(email):
        raise ValueError("올바른 이메일 형식이 아닙니다.")

    return email


# 비밀번호 조건 검사 함수
def check_password(password: str) -> str:
    if not any(character.islower() for character in password):
        raise ValueError("영문 소문자가 1개 이상 필요합니다.")

    if not any(character.isupper() for character in password):
        raise ValueError("영문 대문자가 1개 이상 필요합니다.")

    if not any(not character.isalnum() for character in password):
        raise ValueError("특수문자가 1개 이상 필요합니다.")

    return password


# 회원 조회 결과 형식
# 비밀번호는 조회 결과에서 제외
class UserResponse(BaseModel):
    id: int
    name: str
    age: int
    email: str


# 새 회원 추가 시 입력받는 형식
class UserCreate(BaseModel):
    name: str = Field(min_length=2, max_length=10)
    age: int = Field(ge=14)
    email: str = Field(max_length=30)
    password: str = Field(min_length=8, max_length=20)

    @field_validator("email")
    @classmethod
    def validate_email(cls, email: str) -> str:
        return check_email(email)

    @field_validator("password")
    @classmethod
    def validate_password(cls, password: str) -> str:
        return check_password(password)


# 회원 수정 시 입력받는 형식
class UserUpdate(BaseModel):
    age: int | None = Field(default=None, ge=14)
    email: str | None = Field(default=None, max_length=30)
    password: str | None = Field(
        default=None,
        min_length=8,
        max_length=20,
    )

    @field_validator("email")
    @classmethod
    def validate_email(cls, email: str | None) -> str | None:
        if email is None:
            return None

        return check_email(email)

    @field_validator("password")
    @classmethod
    def validate_password(
        cls,
        password: str | None,
    ) -> str | None:
        if password is None:
            return None

        return check_password(password)


# 회원 번호로 회원을 찾는 함수
def find_user(user_id: int) -> dict | None:
    for user in user_list:
        if user["id"] == user_id:
            return user

    return None


# 1. 모든 회원 조회
@router.get(
    "/users",
    response_model=list[UserResponse],
)
async def get_all_users():
    return user_list


# 2. 특정 회원 조회
@router.get(
    "/users/{user_id}",
    response_model=UserResponse,
)
async def get_user(user_id: int):
    user = find_user(user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="해당 회원을 찾을 수 없습니다.",
        )

    return user


# 3. 새 회원 추가
@router.post(
    "/users",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_user(user_data: UserCreate):
    email_exists = any(
        user["email"] == user_data.email
        for user in user_list
    )

    if email_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="이미 사용 중인 이메일입니다.",
        )

    new_id = max(
        (user["id"] for user in user_list),
        default=0,
    ) + 1

    new_user = {
        "id": new_id,
        **user_data.model_dump(),
    }

    user_list.append(new_user)

    return new_user


# 4. 특정 회원 정보 수정
@router.patch(
    "/users/{user_id}",
    response_model=UserResponse,
)
async def update_user(
    user_id: int,
    user_data: UserUpdate,
):
    user = find_user(user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="해당 회원을 찾을 수 없습니다.",
        )

    update_data = user_data.model_dump(
        exclude_unset=True,
        exclude_none=True,
    )

    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="수정할 항목을 한 개 이상 입력해야 합니다.",
        )

    new_email = update_data.get("email")

    if new_email is not None:
        email_exists = any(
            existing_user["email"] == new_email
            and existing_user["id"] != user_id
            for existing_user in user_list
        )

        if email_exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="이미 사용 중인 이메일입니다.",
            )

    for field_name, field_value in update_data.items():
        user[field_name] = field_value

    return user


# 5. 특정 회원 삭제
@router.delete("/users/{user_id}")
async def delete_user(user_id: int):
    user = find_user(user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="해당 회원을 찾을 수 없습니다.",
        )

    user_list.remove(user)

    return {
        "message": "회원 정보가 삭제되었습니다.",
        "deleted_user_id": user_id,
    }