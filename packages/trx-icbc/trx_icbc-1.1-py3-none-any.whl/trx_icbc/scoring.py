import logging
import pandas as pd
from datetime import datetime, timedelta, date

logger = logging.getLogger('trx_main.' + __name__)


logger.info('getting hypers and regresors - short model')


def get_model_score(results, sla_over_scoring , sla_scoring  , perc_error_median_scoring , sla_over_threshold,long ):
	"""receives the cross validation output and selects the best model according to score parameters.
    
    parameters
    ----------
    results : dict
        dataframe output from cross validation function. day to day prediction against real value

    sla_over_scoring : int
        score gain if model has the best sla_over metric 

    sla_scoring : int
        score gain if model has the best sla_scoring metric 

    perc_error_median_scoring : int
        score gain if model has the best perc_error_median_scoring metric 

    sla_over_threshold : bool
        how much percentage difference is allowed between best sla_over metric model and other models. 
        if the difference is higher than threshold, the model will be droped out.
	
	long : bool
        passed value from main. If False (default), runs short prediciton scoring. If True, runs long prediction scoring.
    
    Returns
    -------
    score_ab : dict 
    	dictionary with the score of each model for ab

	score_mb : dict 
    	dictionary with the score of each model for mb

	
	exports csv with grouped results used for scoring models
	long prediction  :   csv to predicciones/cv/cv_summary_DATE_long.csv
	short prediciton :  csv to predicciones/cv/cv_summary_DATE_short.csv

    """  
	logger.debug('removing weekends')
	results = results[(results.sem_dia != 'Sat') & (results.sem_dia != 'Sun')]
	logger.debug('results - > making cols perc_error and perc_error_over')
	results['perc_error'] = abs(results['y'] - results['yhat']) / results['y']
	results['perc_error_over'] = (results['y'] - results['yhat']) / results['y']
	#results['perc_error'] = abs(results['y'] - results['yhat']) / results['y']
	logger.debug('results - > making cols SLA and SLA_over')
	results['SLA'] = results['perc_error'] < 0.1
	results['SLA_over'] = results['perc_error_over'] < 0.1

	logger.debug('grouping results')
	group_results =results.groupby('model')['SLA','perc_error','SLA_over'].agg(['sum','median','count']).reset_index().reset_index()
	logger.debug('making col model set')
	group_results['model_set'] = group_results['model'].astype(str).str[0:2]
	logger.debug('re formating columns')
	group_results.columns = ['index','model', 'SLA_sum','SLA_median','SLA_count','perc_error_sum','perc_error_median','perc_error_count','SLA_over_sum','SLA_over_median','SLA_over_count', 'model_set']
	logger.debug('filtering columns')
	group_results = group_results[['model', 'SLA_sum', 'perc_error_median', 'SLA_over_sum', 'model_set']]

	if long == True:
		logger.info('saving cross validation summary results at' + 'predicciones/cv/cv_summary_' + str(date.today()) + 'long.csv')
		group_results.to_csv('predicciones/cv/cv_summary_' + str(date.today()) + 'long.csv') 

	if long == False:
		logger.info('saving cross validation summary results at' + 'predicciones/cv/cv_summary_' + str(date.today()) + 'short.csv')
		group_results.to_csv('predicciones/cv/cv_summary_' + str(date.today()) + 'short.csv') 


	logger.debug('running func -> scoring_models')
	logger.info('getting model score from CV results')
	score_ab = scoring_models(group_data =group_results ,channel = 'AB', sla_over_scoring= sla_over_scoring, sla_scoring = sla_scoring , perc_error_median_scoring = perc_error_median_scoring, sla_over_threshold = sla_over_threshold)
	score_mb = scoring_models(group_data =group_results ,channel = 'MB', sla_over_scoring= sla_over_scoring, sla_scoring = sla_scoring , perc_error_median_scoring = perc_error_median_scoring, sla_over_threshold = sla_over_threshold)
	logger.info('models score AB:' + str(score_ab))
	logger.info('models score MB:' + str(score_mb))

	return score_ab, score_mb
	


def scoring_models(group_data, channel, sla_over_scoring, sla_scoring , perc_error_median_scoring, sla_over_threshold):
    """gets the score for each model according to score values received from parameters file.
    
    parameters
    ----------
    group_data : dataframe
        dataframe output from cross validation function. day to day prediction against real value

    channel : str
		channel 'AB' or 'MB' for filtering cv results before scoring

    sla_over_scoring : int
        score gain if model has the best sla_over metric 

    sla_scoring : int
        score gain if model has the best sla_scoring metric 

    perc_error_median_scoring : int
        score gain if model has the best perc_error_median_scoring metric 

    sla_over_threshold : int
        how much percentage difference is allowed between best sla_over metric model and other models. 
        if the difference is higher than threshold, the model will be droped out.

    
    Returns
    -------
    puntaje_dict : dict
    	dict with the score for each model, for the selected channel.

    """  


    group_channel = group_data[group_data['model_set'] == channel]
    
    logger.debug('getting best metrics from CV results')    
    max_SLA_value = group_channel['SLA_sum'].max()
    max_SLA_over_value = group_channel['SLA_over_sum'].max()
    min_perc_error_median_value = group_channel['perc_error_median'].min()

    logger.debug('getting models with best metrics')    
    models_max_sla = str(group_channel.loc[group_channel['SLA_sum'] == max_SLA_value, 'model'].values)
    models_max_sla_over = str(group_channel.loc[group_channel['SLA_over_sum'] == max_SLA_over_value, 'model'].values)
    models_min_perc_error_median = str(group_channel.loc[group_channel['perc_error_median'] == min_perc_error_median_value, 'model'].values)

    puntaje_dict = {}
    for i in group_channel.model:
        puntaje = models_max_sla.count(i) * sla_over_scoring + models_max_sla_over.count(i) * sla_scoring + models_min_perc_error_median.count(i) * perc_error_median_scoring
        puntaje_dict[i] = puntaje


        if sla_over_threshold < 1 - group_channel[group_channel['model'] == i].SLA_over_sum.values / max_SLA_over_value:
            puntaje_dict[i] = puntaje - 10
            logger.debug('SLA_over for model' + str(i) + ' under threshold set at' + str(sla_over_threshold) + '-> 10 points to score')
    return puntaje_dict