import pickle
import logging

logger = logging.getLogger('trx_main.' + __name__)

def load_regresors_short():
    """loads pickle files to get list of regresors and hyperparameters for short models
         
    Returns
    -------
    regs_dict : dict 
        dictionary with regresors data 

    hyper_dict : dict 
        dictionary with hyperparámeter data     
    
    """  
    logger.debug('iteration to build reg dict and hyper dict short model - > load pickle files')

    
    regs_dict =   { 'ab1' :  'to_load' , 'ab2' : 'to_load', 'ab3' : 'to_load' ,'mb1' : 'to_load', 'mb2' : 'to_load', 'mb3' : 'to_load' }
    for key in regs_dict.keys():
        logger.debug('loading' + key)
        with open("hypers_modelo_10dias/regresores/" + key + "_regs.txt", "rb") as fp:   # Unpickling
            regs_dict[key] = pickle.load(fp)
            logger.debug(key + 'loaded')

    logger.debug('iteration to build hyper dict short - > load pickle files')        
    

    hyper_dict = {'AB_1': 'to_load','AB_1b': 'to_load','AB_2': 'to_load','AB_3': 'to_load','AB_3b': 'to_load','MB_1': 'to_load','MB_1b':'to_load','MB_2': 'to_load','MB_2b': 'to_load','MB_3': 'to_load' }
    for key in hyper_dict.keys():
        logger.debug('loading' + key)
        with open("hypers_modelo_10dias/hiperparametros/" + key + "_hyper.txt", "rb") as fp:   # Unpickling
            hyper_dict[key] = pickle.load(fp)
            logger.debug(key + 'loaded')         

    logger.debug('done')
        
    return regs_dict, hyper_dict

def load_models_short(regs_dict ,hyper_dict, datasets):
    """prepares a list of dictionaries with data, hyperparámeters, regresors and model name to
    iterate with prediction function afterwards
    
    parameters
    ----------
    regs_dict : list
        list with regresor used for each model

    hyper_dict : dict
        dictionary with hyperparámeter data for each model

    datasets : dataframe
        dataframe with data for each day

    
    Returns
    -------
    to_predict_dict_short : dict 
        dictionary with a list of dictionaries inside with all data for short models

    
    """  
    logger.debug('making short prediction dictionaries for each model')            

    data_hypers_AB_1b = {'data':datasets[0], 'hypers':hyper_dict['AB_1b'], 'name_mod': 'AB_1b', 'regresores':regs_dict['ab1']  } 
    data_hypers_AB_2 = {'data':datasets[1], 'hypers':hyper_dict['AB_2'], 'name_mod': 'AB_2', 'regresores':regs_dict['ab2'] }
    data_hypers_AB_3 = {'data':datasets[2], 'hypers':hyper_dict['AB_3'], 'name_mod': 'AB_3' , 'regresores':regs_dict['ab3'] }
    data_hypers_MB_1b = {'data':datasets[3], 'hypers':hyper_dict['MB_1b'], 'name_mod':  'MB_1b', 'regresores':regs_dict['mb1'] }
    data_hypers_MB_2 = {'data':datasets[4], 'hypers':hyper_dict['MB_2'], 'name_mod':  'MB_2', 'regresores': regs_dict['mb2'] }
    data_hypers_MB_3 = {'data':datasets[5], 'hypers':hyper_dict['MB_3'] , 'name_mod': 'MB_3', 'regresores': regs_dict['mb3'] }



    #lista iterable de diccionarios
    predict_list = [
    data_hypers_AB_1b,
    data_hypers_AB_2,
    data_hypers_AB_3,
    data_hypers_MB_1b,
    data_hypers_MB_2,
    data_hypers_MB_3,
    data_hypers_MB_2,
    data_hypers_MB_3
    ]

    to_predict_dict_short = {}
    for item in predict_list:
        key = item['name_mod']
        to_predict_dict_short[key] = item


    logger.debug('dicts done')            
    return to_predict_dict_short