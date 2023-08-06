import pickle
import numpy as np
from pydantic import (BaseModel, 
    NegativeInt,
    PositiveInt,
    conint,
    conlist,
    constr,
    StrictBool, Field)

# Server
import uvicorn
from fastapi import FastAPI, Query, File, UploadFile
from typing import Optional

#model
import sys
sys.path.append('..')
import main


app1 = FastAPI()

app2 = FastAPI()


#////APP1 ////# - NO LOGRO PASAR LOS PARAMETROS CON **params a la funcion principal
#prediction = main.principal(params) probe tambien con (**params)

class parameters(BaseModel):
   long :Optional[StrictBool] =  False
   cv_off: Optional[StrictBool] = False
   multiproc_off: Optional[StrictBool] = False
   cv_window :Optional[PositiveInt] = Query(100, description='cantidad de dias para hacer cv')


        
        
@app1.post("/predict")
def predict(params: parameters, ):
    
    prediction = main.principal()

    #prediction = main.principal(params) probe tambien con (**params)

    return prediction #si la corro sin return obtengo error

    

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)



#////APP2 ////# - funcionan bien pasar los parámetros desde  /docs o curl
#pero no lo puedo mandar desde html "405 - method not allowed"

#si en la función predict, uso cv_off: Optional[StrictBool] = False , /docs no me la deja correr porque dice q no es booleano, le pasa false no False.
#no es tan importante


        
        
@app2.post("/predict")
def predict(long: bool = False, cv_off: Optional[StrictBool] = False ,multiproc_off: bool = False, cv_window: int = Query(100, description='cantidad de dias para hacer cv', gt=10)):
    
    prediction = main.principal(long = long, cv_off = cv_off, multiproc_off = multiproc_off, cv_window = cv_window)


    return prediction #si la corro sin return obtengo error

    

if __name__ == '__main__':
    uvicorn.run(app2, host='127.0.0.1', port=8000)




#////APP3 ////# prueba Request body + path + query parameters -> https://fastapi.tiangolo.com/tutorial/body/



class Item_3(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None


app3 = FastAPI()


@app3.put("/items/{item_id}")
async def create_item(item_id: int, item: Item_3, q: Optional[str] = None):

    result = {"item_id": item_id, **item.dict(), "dict_prueba" : item_id + 1}
    if q:
        result.update({"q": q})
    return result  




#////APP3 ////# prueba upload file


from fastapi import FastAPI, File, UploadFile

app4 = FastAPI()


@app4.post("/files/")
async def create_file(file: bytes = File(...)):
    return {"file_size": len(file)}


@app4.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    return {"filename": file.filename}












# # MODULO PARA TEST
# import requests
# to_predict_dict = {'satisfaction_level': 0.38,
#                    'last_evaluation': 0.53,
#                    'number_project': 2,
#                    'average_montly_hours': 157,
#                    'time_spend_company': 3,
#                    'Work_accident': 0,
#                    'promotion_last_5years': 0,
#                    'sales': 'support',
#                    'salary': 'low'}

# url = 'http://127.0.0.1:8000/predict'
# r = requests.post(url,json=to_predict_dict); r.json()

#r = requests.post(url)