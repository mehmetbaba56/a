import os

class Config:
    API_ID = int(os.environ.get("API_ID", "23664317")) #Karışmayın
    API_HASH = os.environ.get("API_HASH", "8c246b2d2b2455ff7bef02ae0178eefa") #Karışmayın
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "6828936442:AAEzw1W9uZoyPHMCMcGIzQEWhJp0x8meubQ") #Botunuzun Tokenini Girin .  

