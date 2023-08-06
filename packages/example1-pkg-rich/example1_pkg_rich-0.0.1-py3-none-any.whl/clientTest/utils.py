from datetime import datetime    
import os

def utilsFechaOfClient():
    return datetime.now().strftime("%m/%d/%Y, %H:%M:%S")+" - "+os.getenv("OTHER_SECRET")
