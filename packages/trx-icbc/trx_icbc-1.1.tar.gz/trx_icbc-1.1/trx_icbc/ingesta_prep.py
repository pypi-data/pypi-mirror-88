from datetime import date
import pandas as pd
import sys
from trx_icbc import data_prepro
import logging

logger = logging.getLogger('trx_main.' + __name__)



def ingesta(data_prep, prediccion_corta=True):
    """gets data file and prepares the data for short prediction (default) 
    or long prediction and returns dataframe subsets for each model
    
    parameters
    ----------
    data_prep : dataframe
        dataframe with data for both channels

    prediccion_corta : bool
        If true, the data will be prepared for short prediction model.

            
    Returns
    -------
    AB2_data : dataframe 
        dataframe with AB channel data for model input 
    
    AB1_data : dataframe 
        dataframe with AB channel data for model input 
    
    AB3_data : dataframe 
        dataframe with AB channel data for model input 

    MB3_data : dataframe  
        dataframe with MB channel data for model input 

    MB2_data : dataframe  
        dataframe with MB channel data for model input 

    MB1_data : dataframe  
        dataframe with MB channel data for model input 

    """  
    
   

    


    logger.debug('running module: data_prepro -> preprocesamiento')
    data_modelmb, data_modelab = data_prepro.preprocesamiento(data_prep, prediccion_corta=prediccion_corta)
    logger.debug('done')

    logger.debug('making dframe subsets')
        #subsets
    AB2_data = data_modelab[data_modelab.ds> "2020-03-15"]
    AB1_data = data_modelab[data_modelab.ds> "2020-01-05"]
    AB3_data = data_modelab[data_modelab.ds> "2018-01-27"]
    logger.debug('subset AB done')

    #subsets
    MB3_data = data_modelmb[data_modelmb.ds> "2020-03-15"]
    MB2_data = data_modelmb[data_modelmb.ds> "2020-01-05"]
    MB1_data = data_modelmb[data_modelmb.ds> "2018-05-05"]
    logger.debug('subset MB done')

    return AB2_data, AB1_data, AB3_data, MB3_data , MB2_data, MB1_data

