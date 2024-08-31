from DatabaseSchema import Ban
from dotenv import load_dotenv
from sqlalchemy import create_engine, select, URL, desc, func
from sqlalchemy.orm import Session
import os

load_dotenv()

# Mostly based off of the ScamGuard Database Option
class DatabaseDriver():
  Database = None

  ### Initialization/Teardown ###
  def __init__(self, *args, **kwargs):
    self.Open()

  def __del__(self):
    self.Close()

  def Open(self):
    self.Close()

    database_url = URL.create(
      'sqlite',
      username='',
      password='',
      host='',
      database=DatabaseDriver.GetDatabaseFile(),
    )
    self.Database = Session(create_engine(database_url))

  def Close(self):
    if (self.IsConnected()):
      self.Database.get_bind().dispose()
      self.Database = None
    
  def IsConnected(self) -> bool:
    if (self.Database is not None):
      return True
    return False

  @staticmethod
  def GetDatabaseFile() -> str:
    return os.getenv("DATABASE_FILE")

  ### Lookup Data ###
  def DoesBanExist(self, TargetId:int) -> bool:
    if (TargetId <= 0):
      return False
      
    stmt = select(Ban).where(Ban.discord_user_id==TargetId)
    result = self.Database.scalars(stmt).first()

    if (result is None):
      return False

    return True

  def GetBanInfo(self, TargetId:int) -> Ban|None:
    if (TargetId <= 0):
      return None
    
    stmt = select(Ban).where(Ban.discord_user_id==TargetId)
    return self.Database.scalars(stmt).first()

  def GetNumBans(self) -> int:
    stmt = select(func.count()).select_from(Ban)
    return self.Database.scalars(stmt).first()
