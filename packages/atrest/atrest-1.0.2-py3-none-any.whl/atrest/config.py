import os
from dotenv import load_dotenv

class Config:

    def __init__(self): 
        self.set_env()
        
    def set_env(self):
        load_dotenv()
        