import calendar
import pandas as pd
import numpy as np
import logging
logger = logging.getLogger('trx_main.' + __name__)


#preprocesamiento noviembre 5 2020
def preprocesamiento(dframe, prediccion_corta = True):
    """runs minor preprocesing data steps into input dataframe and returns 
    one dataset for each channel
    
    parameters
    ----------
    dframe : dataframe
        dataframe with data for each day for both channels

    prediccion_corta : bool
        If true (default) will prepare data for short prediction.
    
        
    Returns
    -------
    dframe_mobile : dataframe 
        dataframe with data input for mb channel

    dframe_access : dataframe 
        dataframe with data input for ab channel
    
    """  

    logger.debug('ds feature to datetime')
    dframe['ds'] = pd.to_datetime(dframe['ds'], format='%Y-%m-%d')
    
    logger.debug('apply dframe.ds -> week_of_month')
    dframe['week_nr'] = dframe['ds'].apply(week_of_month)
    
    #usamos branch_lag como un regresor ejemplo para parametrizar el subset del dataframe para la prediccion
    #nos quedamos con el dataframe donde un regresor que vamos a usar para predecir en su version 
    #lag no tiene NA values, el resto no nos sirve.
    
    if prediccion_corta == True:
        logger.debug('prediccion corta = TRUE -> filtering rows with NA in branch_lag')
        dframe = dframe[dframe['branch_lag'].notna()]
        
    
    logger.debug('drop dframe.canal')
    dframe.drop(columns='canal', inplace=True)
    
    
    
    logger.debug('making new col -> posfe_habil')
    dframe.loc[(dframe['posferiado'] ==1) & (dframe['habil'] ==1), 'posfe_habil'] = 1
    dframe.loc[(dframe['posfe_habil'].isna()), 'posfe_habil'] = 0
    
    logger.debug('making dframe access + making dias_predict col')
    dframe_access = dframe.rename(columns={'y_access':'y'}).drop(columns='y_mobile')
    dframe_access['dias_predict'] = (dframe_access.branch_lag.notna().sum() - dframe_access.y.notna().sum()) 
    
    logger.debug('making dframe mobile + making dias_predict col')
    dframe_mobile = dframe.rename(columns={'y_mobile':'y'}).drop(columns='y_access')
    dframe_mobile['dias_predict'] = (dframe_mobile.branch_lag.notna().sum() - dframe_mobile.y.notna().sum()) 
    
    logger.debug('return dframes')
    return dframe_mobile, dframe_access



def week_of_month(date):
    """gets the week number from 1 to 5
    
    parameters
    ----------
    date : datetime
        date of the record to check for the week number
        
    Returns
    -------
    week_number : int 
        number of the week from 1 to 5
    
    """  

    cal_object = calendar.Calendar(6)
    month_calendar_dates = cal_object.itermonthdates(date.year,date.month)
    day_of_week = 1
    week_number = 1

    for day in month_calendar_dates:
        
        if day_of_week > 7:
            week_number += 1
            day_of_week = 1

        if date == day:
            break
        else:
            day_of_week += 1

    return week_number

