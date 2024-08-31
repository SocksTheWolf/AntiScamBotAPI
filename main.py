from fastapi import FastAPI
from DatabaseDriver import DatabaseDriver
from DatabaseSchema import Ban

app = FastAPI()
db = DatabaseDriver()

@app.get("/")
def main():
  return {"msg": "There is no war in ba sing sei"}
  
@app.get("/check/{user_id}")
def check_ban(user_id: int):
  IsDataGood:bool = (user_id >= 1)
  return {"banned": db.DoesBanExist(user_id), "valid": IsDataGood}

@app.get("/ban/{user_id}")
def get_ban_info(user_id: int):
   BanInfo:Ban|None = db.GetBanInfo(user_id)
   if BanInfo is None:
     return {"banned": False, "user_id": user_id}
     
   return {"banned": True, "user_id": BanInfo.discord_user_id, "banned_by": BanInfo.assigner_discord_user_name, "banned_on": BanInfo.created_at}

@app.get("/bans")
def get_ban_stats():
   return {"count": db.GetNumBans()}
