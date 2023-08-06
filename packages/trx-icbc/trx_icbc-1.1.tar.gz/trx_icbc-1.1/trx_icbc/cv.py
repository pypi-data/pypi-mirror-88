from fbprophet import Prophet
import logging
from fbprophet.diagnostics import cross_validation
from fbprophet.diagnostics import performance_metrics
import pandas as pd
from datetime import datetime, timedelta
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



def massive_prediction_cv(initial_forecast_date, data, hyperparams, name, regs, paralell):
    """fits model and outputs a dataframe with validation results
    
    parameters
    ----------
    initial_forecast_date : int
        period to use to run cross validation. time delta = days

    data : dataframe
        dataframe with data for each day

    hyperparams : dict
        dictionary with values for each hyperparámeter

    name : str
        name fo the model

    regs : list
        list with regresors to use in prediction
    
    paralell : bool
        if FALSE, cross validation for model selection is done with one core instead of all cores (default).
    
    Returns
    -------
    df_cv : dataframe 
        dataframe with validated day to day data between prediction and actual value

    """  

    m = Prophet() #instanciamos el modelo
    
    for item in regs:
        m.add_regressor(item, mode='additive')
        logger.debug(item + 'added')  
    

    logger.debug('fitting model')      
    
    with suppress_stdout_stderr():    
        m.fit(data)

    
    
    
    initial = str(abs(data[data.ds> initial_forecast_date].shape[0] - data.shape[0])) + ' days'
    logger.debug('setting initial date to:' + str(initial))      
    
    logger.debug('running cross validation')   
    #with suppress_stdout_stderr():    
   
    df_cv = cross_validation(m, initial=initial, period='10 days', horizon = '10 days', parallel=paralell)
    
    logger.debug('geting day of the week and dropping weekends')      
    df_cv['sem_dia'] = df_cv['ds'].dt.strftime('%a')
    df_cv = df_cv[(df_cv.sem_dia != 'Sat') & (df_cv.sem_dia != 'Sun')]
    
    
         
    logger.debug('geting summary metrics')      
    df_p = performance_metrics(df_cv)
    rmse = df_p.rmse.mean()
    mae =  df_p.mae.mean()
    mape = df_p.mape.mean()
    model_sum = {'rmse':rmse,
                'mae':mae,
                'mape':mape,
                'name': name,
                }
    
    logger.debug('making col name')      
    df_cv['model'] = name
    df_cv['sem_dia'] = df_cv['ds'].dt.strftime('%a')
    logger.debug('returning cv result')      
    return df_cv 




def cv_iteration(to_predict_dict_short, to_predict_dict_long, long, multiproc_off, cv_window):
    """iterates the model lists and runs prediction for each model
    
    parameters
    ----------
    to_predict_dict_short : dict
        dictionary with data, hyperparameters, model name and regresors for each short prediction model.

    to_predict_dict_long : dict
        dictionary with data, hyperparameters, model name and regresors for each long prediction model.

    long : bool
        passed value from main. If False (default), runs short prediciton. If True, runs long prediction.

    multiproc_off : bool
        if FALSE, cross validation is done with all cores (default), instead of one core.
    
    Returns
    -------
    cv_result : dataframe 
        dataframe with validated day to day data for all models appended in one table

    """    

    if long == False:
        to_predict_dict = to_predict_dict_short     
        logger.debug('running cv - short version')      
    if long == True:
        to_predict_dict = to_predict_dict_long   
        logger.debug('running cv - long version')      

    if multiproc_off == False:
        paralell = "processes"
        logger.debug('cv multi processing = TRUE')      
    if multiproc_off == True:
        paralell = None
        logger.debug('cv multi processing = FALSE')      


    cv_result = pd.DataFrame()
    
    for i in to_predict_dict.keys():
            logger.debug('running cv model -> ' + str(i))      

            df_cv = massive_prediction_cv(
                initial_forecast_date=to_predict_dict[i]['data'].ds.iloc[-to_predict_dict[i]['data'].y.isna().sum()] - timedelta(cv_window),
                data=to_predict_dict[i]['data'],
                hyperparams=to_predict_dict[i]['hypers'],
                name=to_predict_dict[i]['name_mod'],
                regs= to_predict_dict[i]['regresores'], paralell = paralell)  
            cv_result = cv_result.append(df_cv, ignore_index=True)
    return cv_result


    