from fastapi import APIRouter, Depends, HTTPException
from pydantic import ValidationError
from starlette import status

from backend.api.v1.dependencies import get_link_service
from backend.exceptions.link import LinkAlreadyExistsError, LinkNotFoundError
from backend.schemas.link import ReadLink, CreateLink, ReadLinks
from backend.schemas.link_click import ReadLinkClicks, ReadLinkClick
from backend.services.link import LinkService

router = APIRouter(tags=["links"])


@router.post("/", response_model=ReadLink, status_code=status.HTTP_201_CREATED)
async def create_link(
        data: CreateLink,
        link_service: LinkService = Depends(get_link_service)
):
    try:
        data.url = str(data.url)
        return await link_service.create(data)
    except LinkAlreadyExistsError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Ошибка при сокращении ссылки.")
    except ValidationError as e:
        for error in e.errors():
            if error['type'] == 'url_parsing':
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Проверьте правильно ли набрана ссылка."
                )


@router.get("/", response_model=ReadLinks)
async def reads_links(
        page: int,
        page_size: int,
        link_service: LinkService = Depends(get_link_service)
):
    return await link_service.reads(page, page_size)


@router.get("/{link_id}", response_model=ReadLink)
async def read_link_by_id(
        link_id: int,
        link_service: LinkService = Depends(get_link_service)
):
    try:
        return await link_service.read_by_id(link_id)
    except LinkNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ссылка с таким ID не существует."
        )


@router.get("/{link_id}/clicks", response_model=ReadLinkClicks)
async def reads_clicks_by_link_id(
        link_id: int,
        page: int = 1,
        page_size: int = 15,
        link_service: LinkService = Depends(get_link_service)
):
    return await link_service.reads_link_clicks_by_id(link_id, page, page_size)


@router.get("/clicks/{click_id}", response_model=ReadLinkClick)
async def read_click_by_id(
        click_id: int,
        link_service: LinkService = Depends(get_link_service)
):
    try:
        return await link_service.read_link_click_by_id(click_id)
    except LinkNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Информации о посещение сайта по такому ID не было найдено."
        )
