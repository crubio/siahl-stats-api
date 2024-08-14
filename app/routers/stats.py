import httpx
from typing import Union
from fastapi import APIRouter, HTTPException, status
from ..classes import playerstats

router = APIRouter(
    prefix="/stats",
    tags=["stats"]
)

@router.get("/{player_id}")
async def get_player_stats(player_id: int):
    stats_data = playerstats.PlayerStats(player_id)

    # testing html parsing data file
    # with open('/Users/crubio/Projects/siahl-stats-api/data/sample.html', 'r') as file:
    #   html = file.read()

    try:
        r = httpx.get(stats_data.url())
        r.raise_for_status()
        html = r.text
        stats_data.parse_stats_html(html)
        if stats_data.full_name is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Player not found")
    except httpx.HTTPStatusError as e:
        # the data url will always return a 200 status code afaik
        raise HTTPException(status_code=e.response.status_code, detail="Player not found")

    return {
        "player_id": player_id,
        "full_name": stats_data.full_name,
        "stats_url": stats_data.url(),
        "stats": stats_data,
    }