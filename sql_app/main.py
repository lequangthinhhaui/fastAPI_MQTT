from msilib.schema import tables
from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

from sqlalchemy import insert

models.Base.metadata.create_all(bind=engine)

from pydoc_data.topics import topics
from fastapi import FastAPI
from fastapi_mqtt import FastMQTT, MQTTConfig

import json

app = FastAPI()

# mqtt config
mqtt_config = MQTTConfig(host = "13.229.146.39",
    port= 1883,
    keepalive = 60,
    username="",
    password="")


mqtt = FastMQTT(
    config=mqtt_config
)

mqtt.init_app(app)
# mqtt config

def saveToDB(data, status):
    if status == "RunTime":
        myInsert = insert(models.dataMqtt).values(RunTime=data)
    elif status == "HeldTime":
        myInsert = insert(models.dataMqtt).values(HeldTime=data)
    elif status == "MCStatus":
        myInsert = insert(models.dataMqtt).values(MCStatus=data)
    elif status == "Avaibility":
        myInsert = insert(models.dataMqtt).values(Avaibility=data)
    elif status == "Vol":
        myInsert = insert(models.dataMqtt).values(Vol=data)
    elif status == "Amp":
        myInsert = insert(models.dataMqtt).values(Amp=data)
    elif status == "Pow":
        myInsert = insert(models.dataMqtt).values(Pow=data)    
    with engine.connect() as conn:
        result = conn.execute(myInsert)

@mqtt.on_connect()
def connect(client, flags, rc, properties):
    mqtt.client.subscribe("stat/tasmota_590DC4/RM_DATA") #subscribing mqtt topic
    print("Connected: ", client, flags, rc, properties)


@mqtt.on_message()
async def message(client, topic, payload, qos, properties):
    global topicGL
    topicGL = payload.decode()
    print("Received message: ",topic, payload.decode(), qos, properties)
    y = json.loads(topicGL)
    RunTime = y['RM_DATA']['RunTime']
    HeldTime = y['RM_DATA']['HeldTime']
    MCStatus = y['RM_DATA']['MCStatus']
    Avaibility = y['RM_DATA']['A']
    Vol = y['RM_DATA']['Vol']
    Amp = y['RM_DATA']['Amp']
    Pow = y['RM_DATA']['Pow']

    saveToDB(RunTime, "RunTime")
    saveToDB(HeldTime, "HeldTime")
    saveToDB(MCStatus, "MCStatus")
    saveToDB(Avaibility, "Avaibility")
    saveToDB(Vol, "Vol")
    saveToDB(Amp, "Amp")
    saveToDB(Pow, "Pow")




    print(type(HeldTime))








# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()




@app.get("/{id}")
def create_user_2():
    valueData = int(id)
    myInsert = insert(models.dataMqtt).values(RunTime=valueData)
    print(myInsert)
    # compiled = myInsert.compile()
    # print(compiled)
    with engine.connect() as conn:
        result = conn.execute(myInsert)

@app.get("/users/{user_id}/items/", response_model=schemas.Item)
def create_item_for_user(user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)):
    return crud.create_user_item(db=db, item=item, user_id=user_id)




# @app.post("/users/", response_model=schemas.User)
# def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
#     db_user = crud.get_user_by_email(db, email=user.email)
#     if db_user:
#         raise HTTPException(status_code=400, detail="Email already registered")
#     return crud.create_user(db=db, user=user)


# @app.get("/users/", response_model=List[schemas.User])
# def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     users = crud.get_users(db, skip=skip, limit=limit)
#     return users


# @app.get("/users/{user_id}", response_model=schemas.User)
# def read_user(user_id: int, db: Session = Depends(get_db)):
#     # db_user = crud.get_user(db, user_id=user_id)
#     # if db_user is None:
#     #     raise HTTPException(status_code=404, detail="User not found")
#     print(db.query(models.User))


# @app.post("/users/{user_id}/items/", response_model=schemas.Item)
# def create_item_for_user(
#     user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
# ):
#     return crud.create_user_item(db=db, item=item, user_id=user_id)


# @app.get("/items/", response_model=List[schemas.Item])
# def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     items = crud.get_items(db, skip=skip, limit=limit)
#     return items
