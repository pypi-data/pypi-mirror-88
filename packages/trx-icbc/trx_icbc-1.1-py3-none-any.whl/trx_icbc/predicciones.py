from fbprophet import Prophet
import logging
import warnings
import os
logger = logging.getLogger('trx_main.' + __name__)



class suppress_stdout_stderr(object):
    """class to silence prophet output during prediction and cv.
    A context manager for doing a "deep suppression" of stdout and stderr in
    Python, i.e. will suppress all print

    """
    
    def __init__(self):
        """opens a pair of null files
        
        """

        self.null_fds = [os.open(os.devnull, os.O_RDWR) for x in range(2)]
        self.save_fds = [os.dup(1), os.dup(2)]

    def __enter__(self):
        """Assign the null pointers to stdout and stderr.

        """

        os.dup2(self.null_fds[0], 1)
        os.dup2(self.null_fds[1], 2)

    def __exit__(self, *_):
        """Re-assign the real stdout/stderr back to (1) and (2)

        """

        os.dup2(self.save_fds[0], 1)
        os.dup2(self.save_fds[1], 2)
        for fd in self.null_fds + self.save_fds:
            os.close(fd)



def massive_prediction_short(predict_days, data, hyperparams, name,regs):
    """fits model and outputs forecasted value for short prediction
    
    parameters
    ----------
    predict_days : int
        horizon of days for forecast

    data : dataframe
        dataframe with data for each day

    hyperparams : dict
        dictionary with values for each hyperparámeter

    name : str
        name of the model

    regs : list
        list with regresors to use in prediction
    
        
    Returns
    -------
    forecast : dataframe 
        dataframe with day to day prediction

    prediccion_hasta : datetime  
        date of the last predicted value to use as filename later

    """  
    logger.info('short - pred ' + name)

    model = Prophet()

    m = Prophet(**hyperparams)
    
           
    logger.debug('adding regresors')      
    for item in regs:
        m.add_regressor(item, mode='additive')
        logger.debug(item + 'added')      

    datos_modelo = data
    df_train = datos_modelo[:-predict_days] 
    df_test = datos_modelo[-predict_days:] 

    logger.debug('fitting model')  
    with suppress_stdout_stderr():    
        m.fit(df_train)

    logger.debug('making prediction')      
    forecast = m.predict(df_test)
    
    logger.debug('making col sem_dia to prediction output')      
    forecast['sem_dia'] = forecast['ds'].dt.strftime('%a') 
    #sacamos los fines de semana porque no sirven a negocio 
    #y en etapas de validacion molesta para estimar errores
    
    logger.debug('droping sabados & domingos')      
    forecast = forecast[(forecast.sem_dia != 'Sat') & (forecast.sem_dia != 'Sun')]
    
    logger.debug('make title variable for csv')      
    prediccion_hasta = df_test.ds.iloc[-1].strftime("%d-%b-%Y")
    
       
    logger.debug('making col name')      
    forecast['model'] = name
    
    #guardamos la prediccion para cada modelo donde podemos ver el impacto de cada regresor y si queremos, sacar
    #regresores que aporten poca información al modelo
    logger.debug('saving prediction detail to csv')      
    forecast.to_csv( 'predicciones/prediccion_corta/' + name +' '+ prediccion_hasta + '.csv')
    logger.info('csv saved:' + 'predicciones/prediccion_corta/' + name +' '+ prediccion_hasta + '.csv')      
    
        
    logger.debug('changing variable type')      
    forecast['yhat'] = forecast['yhat'].astype(int)
    
    forecast['canal'] = name
    
    logger.debug('returning deliverable csv data to append')      
    return forecast[['ds', 'yhat', 'canal']] ,prediccion_hasta
        
    
def massive_prediction_long(predict_days, data, hyperparams, name,regs):
    """fits model and outputs forecasted value for long prediction
    
    parameters
    ----------
    predict_days : int
        horizon of days for forecast

    data : dataframe
        dataframe with data for each day

    hyperparams : dict
        dictionary with values for each hyperparámeter

    name : str
        name of the model

    regs : list
        list with regresors to use in prediction
    
        
    Returns
    -------
    forecast : dataframe 
        dataframe with day to day prediction

    prediccion_hasta : datetime  
        date of the last predicted value to use as filename later

    """  
    logger.info('long - pred ' + name)
    m = Prophet(**hyperparams) 

    
    logger.debug('adding regresors')      
    for item in regs:
        m.add_regressor(item, mode='additive')
        logger.debug(item + 'added')      

      
    datos_modelo = data
    df_train = datos_modelo[:-predict_days]
    df_test = datos_modelo[-predict_days:] 

    logger.debug('fitting model')      
        
    with suppress_stdout_stderr():    
            m.fit(df_train)

    logger.debug('making prediction')      
    forecast = m.predict(df_test) 

    logger.debug('making col sem_dia to prediction output')      
    forecast['sem_dia'] = forecast['ds'].dt.strftime('%a')
    #identificamos y sacamos los fines de semana de la prediccion
    #porque no interesan a negocio y confunden al analizar o validar la capacidad predictiva del modelo.
    
    logger.debug('droping sabados & domingos')
    forecast = forecast[(forecast.sem_dia != 'Sat') & (forecast.sem_dia != 'Sun')]
    
    logger.debug('make title variable for csv')      
    prediccion_hasta = df_test.ds.iloc[-1].strftime("%d-%b-%Y")
    
    #guardamos la prediccion para cada modelo donde podemos ver el impacto de cada regresor y si queremos, sacar
    #regresores que aporten poca información al modelo
    logger.debug('saving prediction detail to csv')      
    forecast.to_csv( 'predicciones/prediccion_larga/' + name +' '+ prediccion_hasta + '.csv')
    logger.info('csv saved:' + 'predicciones/prediccion_larga/' + name +' '+ prediccion_hasta + '.csv')      
    

    logger.debug('changing variable type')      
    forecast['yhat'] = forecast['yhat'].astype(int)
    
    forecast['canal'] = name
        
    logger.debug('returning deliverable csv data to append')      
    return forecast[['ds', 'yhat', 'canal']] ,prediccion_hasta
