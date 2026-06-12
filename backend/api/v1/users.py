from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from backend.api.v1.dependencies import get_user_service, get_link_service
from backend.exceptions.user import UserAlreadyExistsError, UserNotFoundError
from backend.schemas.link import ReadLinks
from backend.schemas.link_click import ReadLinkClicks
from backend.schemas.user import ReadUser, CreateUser, ReadUserWithOptions, ReadUsers
from backend.services.link import LinkService
from backend.services.user import UserService

router = APIRouter(tags=["users"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ReadUser)
async def create_user(
        data: CreateUser,
        user_service: UserService = Depends(get_user_service)
):
    try:
        return await user_service.create(data)
    except UserAlreadyExistsError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь с таким tg_id уже зарегистрирован"
        )


@router.get("/", response_model=ReadUsers)
async def read_users(
        page: int,
        page_size: int,
        user_service: UserService = Depends(get_user_service)
):
    return await user_service.reads(page, page_size)


@router.get("/{user_id}", response_model=ReadUserWithOptions)
async def read_user_by_id(
        user_id: int,
        user_service: UserService = Depends(get_user_service)
):
    try:
        return await user_service.read_by_id(user_id)
    except UserNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь с таким ID не был найден."
        )


@router.get("/{user_id}/links", response_model=ReadLinks)
async def read_links_user(
        user_id: int,
        link_service: LinkService = Depends(get_link_service),
        page: int = 1,
        page_size: int = 15
):
    return await link_service.reads_by_user_id(user_id, page, page_size)



@router.get("/telegram/{tg_id}", response_model=ReadUser)
async def read_user_by_tg_id(
        tg_id: int,
        user_service: UserService = Depends(get_user_service)
):
    try:
        return await user_service.read_by_tg_id(tg_id)
    except UserNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь с таким tg_id не был найден."
        )
