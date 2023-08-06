"""main.py module description

module that runs transaction prediction using facebook prophet.

inputs:
preprocessed data from rscript module.
hyper parameter and regresors for each model stored in pickle files

extra:
verbosity from prophet PREDICT fit is silenced.

"""

#ISSUES: 
#resolver pantalla q muestra debug
#verbosity from prophet cross validation, is not silenced yet.




from datetime import date
import pandas as pd
import sys
import typer
import logging
import operator
import datetime

sys.path.append('..')
#import mods
from trx_icbc import ingesta_prep
from trx_icbc import carga_modelo_corto
from trx_icbc import carga_modelo_largo
from trx_icbc import cv
from trx_icbc import scoring
from trx_icbc import iter_predict
from trx_icbc import monitoring_report



logger = logging.getLogger('trx_main')
logger.setLevel(logging.DEBUG)


fh = logging.FileHandler('log_trx.log')
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh) ####!


sh = logging.StreamHandler()
sh.setLevel(logging.INFO)
logger.addHandler(sh)


formatterstr = logging.Formatter('%(asctime)s - %(message)s')
sh.setFormatter(formatterstr)

# filter out everything that is above INFO level (WARN, ERROR, ...)
#sh.addFilter(lambda record: record.levelno <= logging.INFO)



#FUNCION MAIN QUE CORRE TYPER
def principal(long :bool =  False, cv_off: bool = False, multiproc_off: bool = False, cv_window :int = 100, monitoring:bool = False):
    """runs short prediction (default) or long prediction. outputs saved in /predicciones
    performs cross validation to select best model  of 3 models for each channel

    exports csv files
    csv with prediction to predicciones/entregable/
    csv with prediction detailed data to predicciones/
    csv with cv summary results, optional
    

    parameters
    ----------
    long : bool
        changes output to long prediction.

    paralell : bool
        cross validation for model selection is done with one core instead of all cores.

    cv-off : bool
        cancels cross validation for model selection. Uses best model from previous run.

    cv_window : int
        number of days back from last data point, will be used for rolling cross validation

    """
    
    #MAIN SETTINGS

    logger.info('running forecast model with settings as:')
    logger.info('long prediction = ' + str(long))
    logger.info('stop cross validation = ' + str(cv_off))
    logger.info('running cv with one procesor only  = ' + str(multiproc_off))
    logger.info('generating monitoring record ' + str(monitoring))



    ## IMPORT AND DATA PRE PROCESSING ##

    logger.info('loading config.csv - > taking path parameters')     
    config = pd.read_csv('config.csv')
    path_dataprep = config[config.variable == 'input_path_data_prep_csv'].val.values
    path_monitoring = config[config.variable == 'output_path_monitoring'].val.values
    logger.debug('path values loaded correctly')


    path_dataprep = '../../data/raw/'
    logger.info('getting data from' + str(path_dataprep))

    data_prep = pd.read_csv(path_dataprep + 'data_prep.csv') 
    logger.debug('data imported correctly')


    logger.debug('running module: ingesta_prep - short prediction version')
    AB2_data, AB1_data, AB3_data, MB3_data , MB2_data, MB1_data = ingesta_prep.ingesta(data_prep)
    logger.debug('module end')


    datasets_short = [AB1_data, AB2_data, AB3_data, MB1_data, MB2_data, MB3_data]

    logger.info('running module: ingesta_prep - > ingesta (long prediction version)')
    AB2_data_long, AB1_data_long, AB3_data_long, MB3_data_long, MB2_data_long, MB1_data_long = ingesta_prep.ingesta(data_prep, prediccion_corta=False)
    logger.debug('module end')
    datasets_long = [AB1_data_long, AB3_data_long, MB1_data_long, MB2_data_long, MB3_data_long]
    logger.info('data prepared')

    
    ## PREPARING SHORT MODEL DATA ##

    logger.debug('running module: carga_modelo_corto - > load_regresors_short')
    logger.info('getting hypers and regresors - short model')
    regs_dict_short, hyper_dict_short = carga_modelo_corto.load_regresors_short()
    logger.debug('module end')

    
    logger.debug('running module: carga_modelo_corto -> load_models_short')
    to_predict_dict_short = carga_modelo_corto.load_models_short(regs_dict_short ,hyper_dict_short, datasets_short)
    logger.debug('module end')
    logger.info('short models to predict - ready')


    ## PREPARING LONG MODEL DATA ##

    logger.debug('running module: carga_modelo_largo - > load_regresors_long')
    logger.info('getting hypers and regresors - short long')
    regs_long_ab,regs_longs_mb ,hyper_dict_long = carga_modelo_largo.load_regresors_long()
    logger.debug('module end')

    
    logger.debug('running module: carga_modelo_largo -> load_models_long')
    to_predict_dict_long = carga_modelo_largo.load_models_long(regs_long_ab ,regs_longs_mb, hyper_dict_long, datasets_long)
    logger.info('long models to predict - ready')
    logger.debug('module end')

   
    ## MODEL SELECTION ##

    if cv_off == False:
## MODEL SELECTION FROM CROSS VALIDATION ##

        logger.debug('running module: cv -> cv_iteration')
        logger.info('running cross validation for all models, best model will be selected for each channel')

        cv_result = cv.cv_iteration(to_predict_dict_short, to_predict_dict_long, long = long, multiproc_off = multiproc_off, cv_window = cv_window)
        logger.debug('module end')

        
        logger.info('loading config.csv - > scoring parameters for model selection')     
        config = pd.read_csv('config.csv') #base de trx 01 enero 20018 a 31 ago 2020
        sla_over_scoring = config[config.variable == 'sla_over_scoring'].val.values
        sla_scoring = config[config.variable == 'sla_scoring'].val.values
        perc_error_median_scoring = config[config.variable == 'perc_error_median_scoring'].val.values
        sla_over_threshold = config[config.variable == 'sla_over_threshold'].val.values
        logger.debug('scoring vars loaded correctly')

        logger.debug('running module: scoring -> get_model_score')
        logger.info('scoring with parameters:')
        logger.info('sla_over score:' + str(sla_over_scoring))
        logger.info('sla_score:' + str(sla_scoring))
        logger.info('perc_error_median score:' + str(perc_error_median_scoring))
        logger.info('sla_over_threshold:' + str(sla_over_threshold))

        logger.debug('running module: scoring -> get_model_score')
        score_ab, score_mb = scoring.get_model_score(results = cv_result, sla_over_scoring = float(sla_over_scoring), sla_scoring = float(sla_scoring) , perc_error_median_scoring = float(perc_error_median_scoring), sla_over_threshold = float(sla_over_threshold), long=long)
        logger.debug('module end')

        logger.debug('getting max score for each channel')
        ab_best_model = max(score_ab.items(), key=operator.itemgetter(1))[0]
        mb_best_model = max(score_mb.items(), key=operator.itemgetter(1))[0]

        logger.info('best_ab_model ->' + str(ab_best_model))
        logger.info('best_mb_model ->' + str(mb_best_model))

        logger.debug('subseting predict dict to winners models only')

        if long == False:
            #to_predict_dict_short = to_predict_dict_short[ab_best_model,mb_best_model]
            logger.debug('subseting dict - short prediction')
            to_predict_dict_short = {k: to_predict_dict_short[k] for k in [ab_best_model,mb_best_model] if k in to_predict_dict_short}

            best_model_record = pd.read_csv('predicciones/cv/best_model_record.csv')
            best_model_record = best_model_record.append({'winner_ab': ab_best_model, 'winner_mb' : mb_best_model, 'type' : 'short', 'date' : str(datetime.datetime.now())}, ignore_index=True)
            best_model_record.to_csv('predicciones/cv/best_model_record.csv')

        if long == True:
            #to_predict_dict_long = to_predict_dict_long[ab_best_model,mb_best_model]
            logger.debug('subseting dict - long prediction')
            to_predict_dict_long = {k: to_predict_dict_long[k] for k in [ab_best_model,mb_best_model] if k in to_predict_dict_long}

            best_model_record = pd.read_csv('predicciones/cv/best_model_record.csv')
            best_model_record = best_model_record.append({'winner_ab': ab_best_model, 'winner_mb' : mb_best_model, 'type' : 'long', 'date' : str(datetime.datetime.now())}, ignore_index=True)
            best_model_record.to_csv('predicciones/cv/best_model_record.csv')

        print('short models=' + str(to_predict_dict_short.keys()))
        print('long models=' + str(to_predict_dict_long.keys()))

    ## MODEL SELECTION FROM PREVIOUS RESULTS ##
    else:
        logger.info('getting best model from predicciones/cv/best_model_record.csv')
        try:
            best_model_record = pd.read_csv('predicciones/cv/best_model_record.csv')
            logger.debug('read csv - ok')
    
        except:
            logger.error('cannot import best_model_record.csv from "predicciones/cv/" - program will exit')
            quit()        

        logger.debug('datetime formating and sorting values by date')
        best_model_record['date'] = pd.to_datetime(best_model_record['date'])
        best_model_record.sort_values(by='date', inplace=True)

        if long == False:
            
            ab_best_model = best_model_record[best_model_record['type'] == 'short'].iloc[-1]['winner_ab']
            mb_best_model = best_model_record[best_model_record['type'] == 'short'].iloc[-1]['winner_mb']

            logger.info('best_ab_model ->' + str(ab_best_model))
            logger.info('best_mb_model ->' + str(mb_best_model))

            to_predict_dict_short = {k: to_predict_dict_short[k] for k in [ab_best_model,mb_best_model] if k in to_predict_dict_short}
            logger.debug('updated predict dict with best models from record')

        if long == True:   

            ab_best_model = best_model_record[best_model_record['type'] == 'long'].iloc[-1]['winner_ab']
            mb_best_model = best_model_record[best_model_record['type'] == 'long'].iloc[-1]['winner_mb']

            logger.info('best_ab_model ->' + str(ab_best_model))
            logger.info('best_mb_model ->' + str(mb_best_model))


            to_predict_dict_long = {k: to_predict_dict_long[k] for k in [ab_best_model,mb_best_model] if k in to_predict_dict_long} 
            logger.debug('updated predict dict with best models from record')


    ## PREDICTION ##

    logger.debug('running module: iter_predict -> predict / long prediction =' + str(long))
    prediction = iter_predict.predict(to_predict_dict_short, to_predict_dict_long, long = long)
    logger.debug('module end')
    #return prediction

    if monitoring == True:

        logger.debug('running module: monitoring -> evaluation')
        monitoring_report.evaluation(data_prep= data_prep,path_to_dir='predicciones/prediccion_corta/entregable/' , output_path='predicciones/monitoring/' )
        logger.debug('module end')


    exit()



if __name__ == "__main__":
    
    typer.run(principal)

    logger.info('program finished')
 
 
