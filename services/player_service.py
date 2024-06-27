# stdlib
from typing import List

# thirdparty
from sqlalchemy import func, select, text
from sqlalchemy.ext.asyncio import AsyncSession

# project
from db.models.player_model import PlayerModel
from db.schemas.player_schema import PlayerCreate
from utils.pagination import get_pagination


async def get_player_by_username(session: AsyncSession, username: str):
    query = select(PlayerModel).filter(PlayerModel.username == username)  # noqa
    result = await session.execute(query)
    return result.scalar_one_or_none()


async def create_or_get_player(session: AsyncSession, player: PlayerCreate):
    query = """
            WITH new_player AS (
                INSERT INTO players (
                    id, username
                )
                VALUES (
                    :id,
                    :username
                )
                ON CONFLICT (id) DO NOTHING
                RETURNING *
            )
            SELECT * FROM new_player
            UNION
            SELECT * FROM players WHERE id = :id;
        """

    result = await session.execute(text(query), {"id": player.player_id, "username": player.username})
    player = result.mappings().first()
    return player


async def get_player(session: AsyncSession, player_id: int):
    query = select(PlayerModel).filter(PlayerModel.id == player_id)  # noqa
    result = await session.execute(query)
    return result.scalar_one_or_none()


async def get_players_by_ids(session: AsyncSession, player_ids: List[int], page: int, limit: int):
    query = select(PlayerModel).filter(PlayerModel.id.in_(player_ids)).offset((page - 1) * limit).limit(limit)  # noqa

    count_query = select(func.count(PlayerModel.id)).filter(PlayerModel.id.in_(player_ids))  # noqa

    result = await session.execute(query)
    results = await session.execute(count_query)

    players = result.scalars().all()
    total_count = results.scalar()

    pagination = get_pagination(page=page, limit=limit, count=total_count)

    return players, pagination


async def get_players_by_username(session: AsyncSession, username: str, page: int, limit: int):
    query = (
        select(PlayerModel)
        .filter(func.lower(PlayerModel.username).ilike("%" + username + "%"))
        .offset((page - 1) * limit)
        .limit(limit)
    )

    count_query = select(func.count(PlayerModel.id)).filter(
        func.lower(PlayerModel.username).ilike("%" + username + "%")
    )

    result = await session.execute(query)
    results = await session.execute(count_query)

    players = result.scalars().all()
    total_count = results.scalar()

    pagination = get_pagination(page=page, limit=limit, count=total_count)

    return players, pagination


async def get_player_by_id(session: AsyncSession, player_id: int):
    query = select(PlayerModel).filter(PlayerModel.id == player_id)  # noqa
    result = await session.execute(query)
    return result.scalar_one_or_none()
