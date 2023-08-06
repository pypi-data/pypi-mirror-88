import pickle
import logging

logger = logging.getLogger('trx_main.' + __name__)


def load_regresors_long():
    """loads pickle files to get list of regresors and hyperparameters for long models
         
    Returns
    -------
    regs_long_ab : dict 
        regresors for long ab model

    regs_longs_mb : dict 
        regresors for long mb model

    hyper_dict_long : dict 
        hiperparámeter dict with values for each long model
    
    
    """  
    logger.debug('iteration to build hyper dict long - > load pickle files')
    hyper_dict_long = {'AB1': 'to_load','AB3' : 'to_load','MB1': 'to_load','MB2': 'to_load','MB3': 'to_load' }
    for key in hyper_dict_long.keys():
        logger.debug('loading' + key)
        with open("hypers_modelolargo/hiperparametros/" + key + "_hyper.txt", "rb") as fp:   # Unpickling
            hyper_dict_long[key] = pickle.load(fp)      
            logger.debug(key + 'loaded')

    
    logger.debug('loading regresors for AB and MB - > load pickle files')            

    with open("hypers_modelolargo/regresores/regresoresAB.txt", "rb") as fp:   # Unpickling
        regs_long_ab = pickle.load(fp)
        logger.debug('AB regresors loaded')            
    with open("hypers_modelolargo/regresores/regresoresMB.txt", "rb") as fp:   # Unpickling
        regs_longs_mb = pickle.load(fp)      
        logger.debug('MB regresors loaded')            

    return regs_long_ab,regs_longs_mb ,hyper_dict_long

def load_models_long(regs_long_ab ,regs_longs_mb, hyper_dict_long, datasets):
    """prepares a list of dictionaries with data, hyperparámeters, regresors and model name to
    iterate with prediction function afterwards
    
    parameters
    ----------
    regs_long_ab : list
        list with regresor used for each model for mb channel

    regs_longs_mb : list
        list with regresor used for each model for mb channel

    hyper_dict_long : dict
        dictionary with hyperparámeter data

    datasets : dataframe
        dataframe with data for each day

    
    Returns
    -------
    to_predict_dict_long : dict 
        dictionary with a list of dictionaries inside with all data for long models

    
    """     
    logger.debug('making long prediction dictionaries for each model')            

    data_AB1  = {'data':datasets[0], 'hypers':hyper_dict_long['AB1'], 'name_mod': 'AB_1', 'regresores':regs_long_ab} 
    data_AB3 = {'data':datasets[1], 'hypers':hyper_dict_long['AB3'] , 'name_mod': 'AB_3' , 'regresores':regs_long_ab}
    data_MB1  = {'data':datasets[2], 'hypers':hyper_dict_long['MB1'] , 'name_mod':  'MB_1', 'regresores':regs_longs_mb  }
    data_MB2 = {'data':datasets[3], 'hypers':hyper_dict_long['MB2'], 'name_mod':  'MB_2', 'regresores':regs_longs_mb }
    data_MB3 = {'data':datasets[4], 'hypers':hyper_dict_long['MB3'] , 'name_mod': 'MB_3', 'regresores':regs_longs_mb}

    predict_list = [
    data_AB1,
    data_AB3,
    data_MB1,
    data_MB2,
    data_MB3
    ]

    to_predict_dict_long = {}
    for item in predict_list:
        key = item['name_mod']
        to_predict_dict_long[key] = item


    logger.debug('dicts done')            
    return to_predict_dict_long
