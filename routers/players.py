# stdlib
from typing import Union

# thirdparty
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

# project
from db.db_setup import get_session
from db.schemas.common_schema import ResultResponse, ResultsResponse
from db.schemas.player_schema import PlayerCreate, PlayerSchema
from services.player_service import create_or_get_player, get_player, get_players_by_ids, get_players_by_username
from utils.errors import ErrorResponseEnum
from utils.helpers import CustomHTTPException, response_wrapper_result, response_wrapper_results

players_router = APIRouter(tags=["1. Players"], prefix="/players")


@players_router.post("", response_model=ResultResponse[PlayerSchema])
async def get_current_or_create_player(player: PlayerCreate, session: AsyncSession = Depends(get_session)):
    """
    Get or create player
    """
    player = await create_or_get_player(session=session, player=player)

    return response_wrapper_result(result=PlayerSchema(**player))


@players_router.get("/{player_ids}", response_model=Union[ResultsResponse[PlayerSchema], ResultResponse[PlayerSchema]])
async def get_other_players(
    player_ids: str,
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=20, ge=1),
    session: AsyncSession = Depends(get_session),
):
    """
    Get other players
    """
    if "," in player_ids:
        players, pagination = await get_players_by_ids(
            session=session, player_ids=[int(number) for number in player_ids.split(",")], page=page, limit=limit
        )

        return response_wrapper_results(
            results=[PlayerSchema(**player.__dict__) for player in players], pagination=pagination
        )

    player = await get_player(session=session, player_id=int(player_ids))

    if not player:
        raise CustomHTTPException(error_response=ErrorResponseEnum.PLAYER_NOT_FOUND)

    return response_wrapper_result(result=PlayerSchema(**player.__dict__))


@players_router.get("/username/{username}", response_model=ResultsResponse[PlayerSchema])
async def search_players(
    username: str,
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=20, ge=1),
    session: AsyncSession = Depends(get_session),
):
    """
    Search users by username
    """
    players, pagination = await get_players_by_username(session=session, username=username, page=page, limit=limit)

    return response_wrapper_results(
        results=[PlayerSchema(**player.__dict__) for player in players], pagination=pagination
    )
