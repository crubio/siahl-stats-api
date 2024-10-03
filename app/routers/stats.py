import httpx
from typing import Optional
from fastapi import APIRouter, HTTPException, status
from ..classes import playerstats
from ..database import get_db_url
import sqlitecloud


router = APIRouter(
  prefix="/stats",
  tags=["stats"]
)

@router.get("/{player_id}")
async def get_player_stats(player_id: int, sort: Optional[str] = False):
    stats_data = playerstats.PlayerStats(player_id)

    if sort == "team":
      try:
        r = httpx.get(stats_data.url())
        r.raise_for_status()
        html = r.text
        stats_data.parse_stats_html(html)

        if stats_data.full_name is None:
          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Player not found")
        team_stats = stats_data.parse_team_stats(html, json=True)
      except httpx.HTTPStatusError as e:
        # the data url will always return a 200 status code afaik
        raise HTTPException(status_code=e.response.status_code, detail="Player not found")

      return {
        "player_id": player_id,
        "full_name": stats_data.full_name,
        "stats_url": stats_data.url(),
        "team_stats": team_stats,
      } 

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

@router.get("/search/{partial_name_string}")
async def search_for_player(partial_name_string: str):
    conn = sqlitecloud.connect(get_db_url())
    cursor = conn.execute("SELECT * FROM players_fts WHERE full_name LIKE ?", (f"%{partial_name_string}%",))
    results = cursor.fetchall()

    if len(results) == 0:
      conn.close()
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No players found")
    
    conn.close()
    return results
