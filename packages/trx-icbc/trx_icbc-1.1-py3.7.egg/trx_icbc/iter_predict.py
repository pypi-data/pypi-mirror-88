
import logging
import pandas as pd
from datetime import datetime, timedelta
from trx_icbc import predicciones

logger = logging.getLogger('trx_main.' + __name__)

def predict(to_predict_dict_short, to_predict_dict_long, long):
    """iterates the dictionaries into the prediction functions and exports csv prediction
    
    parameters
    ----------
    to_predict_dict_short : dict
        dictionary with data, hyperparameters, model name and regresors for each short prediction model.

    to_predict_dict_long : dict
        dictionary with data, hyperparameters, model name and regresors for each long prediction model.

    long : bool
        passed value from main. If False (default), runs short prediciton. If True, runs long prediction.

    """  
 

    if long == False:

        logger.info('starting short prediction iteration')
        summary_list = pd.DataFrame()
        for i in to_predict_dict_short.keys():
            logger.info('to predict model '+ str(to_predict_dict_short[i]['name_mod']) + ' | days to predict:' + str(to_predict_dict_short[i]['data']['dias_predict'].iloc[0]))
            model_summary, prediccion_hasta  = predicciones.massive_prediction_short(predict_days=to_predict_dict_short[i]['data']['dias_predict'].iloc[0],
                                               data=to_predict_dict_short[i]['data'], hyperparams=to_predict_dict_short[i]['hypers'],
                                               name=to_predict_dict_short[i]['name_mod'],
                                               regs=to_predict_dict_short[i]['regresores'])
           
            logger.debug('guardando ' + to_predict_dict_short[i]['name_mod'] + 'forecast')
            summary_list = summary_list.append(model_summary, ignore_index=True) #concatenamos datos de prediccion
            logger.debug('model append to summary ok')

        logger.debug('renaming summary columns')         
        summary_list.rename(columns = {'ds': 'fecha', 'yhat' : 'prediccion_trx'}, inplace=True) #renombramos columnas
        summary_list.to_csv( 'predicciones/prediccion_corta/entregable/' + 'prediccion_' +prediccion_hasta + '.csv') #guardamos entregable
        logger.info('saved summary csv:' + 'predicciones/prediccion_corta/entregable/' + 'prediccion_' +prediccion_hasta + '.csv') 

    

    if long == True:   
        logger.info('starting long prediction iteration')    
        summary_list = pd.DataFrame()
        for i in to_predict_dict_long.keys():
            logger.info('to predict model '+ str(to_predict_dict_long[i]['name_mod']) + ' | days to predict:' + str(to_predict_dict_long[i]['data']['dias_predict'].iloc[0]))
            model_summary, prediccion_hasta  = predicciones.massive_prediction_long(predict_days=to_predict_dict_long[i]['data']['dias_predict'].iloc[0],
                                               data=to_predict_dict_long[i]['data'], hyperparams=to_predict_dict_long[i]['hypers'],
                                               name=to_predict_dict_long[i]['name_mod'],
                                               regs=to_predict_dict_long[i]['regresores'])
            
            logger.debug('guardando ' + to_predict_dict_long[i]['name_mod'] + 'forecast')
            summary_list = summary_list.append(model_summary, ignore_index=True)
            logger.debug('model append to summary ok')

        logger.debug('renaming summary columns')         
        summary_list.rename(columns = {'ds': 'fecha', 'yhat' : 'prediccion_trx'}, inplace=True) 
        summary_list.to_csv( 'predicciones/prediccion_larga/entregable/' + 'prediccion_' +prediccion_hasta + '.csv') 
        logger.info('saved summary csv:' + 'predicciones/prediccion_larga/entregable/' + 'prediccion_' +prediccion_hasta + '.csv') 

    return summary_list