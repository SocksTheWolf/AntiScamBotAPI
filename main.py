from fastapi import FastAPI
from typing import Union
from DatabaseDriver import DatabaseDriver
from DatabaseSchema import Ban
from pydantic import BaseModel
from datetime import datetime

app = FastAPI(docs_url=None)
db = DatabaseDriver()

class APIBan(BaseModel):
  banned: bool
  user_id: int
  valid: bool = False
  
  def Create(self, user_id:int=0):
    self.user_id = user_id
    self.valid = (user_id >= 1)
    return self
   
  def Check(self):
    BanInfo:Ban|None = db.GetBanInfo(self.user_id)
    IsBanned:bool = (BanInfo is not None)
    self.banned = IsBanned
    return self

class APIBanDetailed(APIBan):
  banned_on: Union[datetime, None] = None
  banned_by: str = ""
  
  def Create(self, user_id:int=0):
    super().Create(user_id)
    self.banned_on = None
    self.banned_by = ""
    return self
  
  def Check(self):    
    BanInfo:Ban|None = db.GetBanInfo(self.user_id)
    IsBanned:bool = (BanInfo is not None)
    self.banned = IsBanned
    
    if IsBanned:
      self.banned_on = BanInfo.created_at
      self.banned_by = BanInfo.assigner_discord_user_name
      
    return self

@app.get("/", include_in_schema=False)
def main():
  return {"msg": "There is no war in ba sing sei"}
  
@app.get("/check/{user_id}", summary="Check if a Discord UserID is banned", response_model=APIBan)
def check_ban(user_id: int):
  return APIBan().Create(user_id).Check()

@app.get("/ban/{user_id}", summary="Get extensive information as to an UserID being banned", response_model=APIBanDetailed)
def get_ban_info(user_id: int):
  return APIBanDetailed().Create(user_id).Check()

@app.get("/bans", summary="Get Number of All Bans")
def get_ban_stats():
   return {"count": db.GetNumBans()}
