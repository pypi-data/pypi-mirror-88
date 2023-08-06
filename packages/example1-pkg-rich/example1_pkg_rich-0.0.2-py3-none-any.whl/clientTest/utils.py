from datetime import datetime    
import os

def utilsFechaOfClient():
    return datetime.now().strftime("%m/%d/%Y, %H:%M:%S")+" - "+os.getenv("OTHER_SECRET")


def variableOfClient():
    return "var: "+os.getenv("OTHER_SECRET")


def testfunctionOfClient():
    return "hello version 0.0.2"
