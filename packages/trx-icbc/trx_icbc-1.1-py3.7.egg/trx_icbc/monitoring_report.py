import os
import glob
import pandas as pd
import numpy as np
import time
from datetime import date

import plotly.express as px
import plotly.graph_objects as go

from os import listdir

import logging
logger = logging.getLogger('trx_main.' + __name__)

def find_csv_filenames( path_to_dir , suffix=".csv" ):
    """get the list of csv files in a given path.
        
        parameters
        ----------
        path_to_dir : str
            path to predictions folder made in the past

        suffix : str
            suffix of files to find, in this case .csv files

        
        Returns
        -------
        list : list 
            list with file names

        
	"""
	
    filenames = listdir(path_to_dir)
    return [ filename for filename in filenames if filename.endswith( suffix ) ]



def evaluation(data_prep,path_to_dir,output_path):
    """imports all the predictions made in the past and cross checks with the real values. 
    
    parameters
    ----------
    data_prep : dataframe
        dataframe output from cross validation function. day to day prediction against real value

    path_to_dir : str
        path to predictions folder made in the past

    output_path : str
        path to save the output of transactions vs prediction monitoring


    """  

    logger.debug('loading find_csv_filenames function')


    
    all_filenames = find_csv_filenames(path_to_dir)
    logger.debug('got all csv prediction files from' + str(path_to_dir))

    logger.debug('building dataframe pronosticos with predictions')
    pronosticos = pd.DataFrame()
    for file in all_filenames:
        logger.debug('merging file' + str(file))
        a = pd.read_csv(path_to_dir+file)
        a['file_date'] = pd.to_datetime(time.ctime(os.path.getmtime(path_to_dir + file)))
        pronosticos = pd.concat([pronosticos, a])

    pronosticos.sort_values(by='file_date', ascending=False, inplace=True)
    logger.debug('donne')


    pronosticos['fecha'] = pd.to_datetime(pronosticos.fecha, format='%Y-%m-%d')


    logger.debug('dataframe pronosticos: merging prediction data with real trx from data_prep')
    pronosticos = pd.merge(pronosticos, data_prep[['y_mobile', 'y_access', 'ds']], how='left',left_on='fecha', right_on='ds').drop(columns='ds')
    
    logger.debug('dataframe pronosticos: formating')
    pronosticos['mes_año'] = pronosticos['fecha'].dt.year.map(str) + pronosticos['fecha'].dt.month.map(str)
    pronosticos['model'] = pronosticos['canal']
    pronosticos['canal'] = pronosticos.canal.str[:2]
    pronosticos['perc_error'] = np.where(pronosticos.canal == 'AB', (pronosticos.y_access - pronosticos.prediccion_trx) / pronosticos.y_access ,(pronosticos.y_mobile - pronosticos.prediccion_trx) / pronosticos.y_mobile)
    pronosticos['SLA'] = abs(pronosticos['perc_error']) < 0.1
    pronosticos['SLA_over'] = pronosticos['perc_error'] < 0.1

    logger.debug('dataframe pronosticos: dropping NA values - meaning no real data to cross with prediction')
    pronosticos.dropna(how= 'any', inplace= True)

    logger.debug('building real trx dataframes for plotting - dropping duplicates, latest predictions for same day kept')
    AB_real_trx = pronosticos[['y_access','fecha']].drop_duplicates(subset=['fecha'], keep='first').sort_values(by='fecha')
    MB_real_trx = pronosticos[['y_mobile','fecha']].drop_duplicates(subset=['fecha'], keep='first').sort_values(by='fecha')
    pronosticos.drop_duplicates(subset=['fecha', 'canal'], keep='first', inplace=True)

    logger.debug('sorting pronosticos dataframe')
    pronosticos.sort_values(by=['canal', 'fecha'])

    logger.debug('building predictions dataframes by channel - sorted')
    modelo_AB = pronosticos[pronosticos['canal'] == 'AB'].sort_values(by='fecha')
    modelo_MB = pronosticos[pronosticos['canal'] == 'MB'].sort_values(by='fecha')


    logger.debug('grouping results in pronosticos dataframe')
    group_monitoreo = pronosticos.groupby(['canal', 'mes_año']).agg(SLA =('SLA', 'mean'), SLA_over =('SLA_over', 'mean'),
                                   perc_error_median=('perc_error', 'median'), cant_predicciones = ('canal', 'count' ))

    pronosticos.to_csv(output_path + str('prono_table') + str(date.today()) +'.csv')
    group_monitoreo.to_csv(output_path + str('group_prono_table') + str(date.today()) +'.csv')
    

    logger.debug('running module: monitoring -> monitoring_plot')
    monitoring_plot(AB_real_trx = AB_real_trx, MB_real_trx = MB_real_trx, modelo_AB = modelo_AB, modelo_MB = modelo_MB, output_path= output_path)
    logger.debug('module end')



def monitoring_plot(AB_real_trx, MB_real_trx, modelo_AB, modelo_MB, output_path):
    """plots a linegraph to verify the perfomance of the model against real trx value.
    
    parameters
    ----------
    AB_real_trx : dataframe
        dataframe with real AB trx

    MB_real_trx : dataframe
        dataframe with real MB trx

    modelo_AB : dataframe
        dataframe with predicted AB trx

    modelo_MB : dataframe
        dataframe with predicted MB trx

    output_path : str
        path to save the output of transactions vs prediction monitoring
    
    """  
    fig = go.Figure()

    logger.debug('adding trace AB models')
    fig.add_trace(go.Scatter(x=modelo_AB.fecha, y=modelo_AB.prediccion_trx , name='Prediccion_AB',
                        text=["tweak line smoothness<br>with 'smoothing' in line object"],
                        line_shape='spline'))
      
    logger.debug('adding trace MB models')
    fig.add_trace(go.Scatter(x=modelo_MB.fecha, y=modelo_MB.prediccion_trx , name='Prediccion_MB',
                        text=["tweak line smoothness<br>with 'smoothing' in line object"],
                        line_shape='spline'))
       

    logger.debug('building +- 10% intervals ')
    AB_real_trx['upper_graph'] = AB_real_trx.y_access * 1.1
    AB_real_trx['lower_graph'] = AB_real_trx.y_access * 0.9
    MB_real_trx['upper_graph'] = MB_real_trx.y_mobile * 1.1
    MB_real_trx['lower_graph'] = MB_real_trx.y_mobile * 0.9


    logger.debug('adding trace - real AB')
    ab_real1 = fig.add_trace(go.Scatter(x=AB_real_trx.fecha, y=AB_real_trx.y_access , name='trx_reales_AB',
                        text=["tweak line smoothness<br>with 'smoothing' in line object"],
                         line=dict(color='black', width=2, dash='dot')))
    logger.debug('adding trace - real AB upper interval')
    ab_real2 = fig.add_trace(go.Scatter(x=AB_real_trx.fecha, y=AB_real_trx['upper_graph'],
                                        name='upper_ab', fill='tonexty', 
                                        fillcolor='rgba(60,60,60,0.1)',
                        text=["tweak line smoothness<br>with 'smoothing' in line object"],
                                        mode='lines', line=dict(width=0)))
    logger.debug('adding trace - real AB lower interval')
    ab_real2 = fig.add_trace(go.Scatter(x=AB_real_trx.fecha, y=AB_real_trx['lower_graph'],
                                        name='lower_ab', fill='tonexty', 
                                        fillcolor='rgba(60,60,60,0.1)',
                        text=["tweak line smoothness<br>with 'smoothing' in line object"],
                                        mode='lines', line=dict(width=0)))

    logger.debug('adding trace - real MB')
    mb_real1 = fig.add_trace(go.Scatter(x=MB_real_trx.fecha, y=MB_real_trx.y_mobile , name='trx_reales_MB',
                        text=["tweak line smoothness<br>with 'smoothing' in line object"],
                         line=dict(color='black', width=2, dash='dot')))
    
    logger.debug('adding trace - real MB upper interval')
    mb_real2 = fig.add_trace(go.Scatter(x=MB_real_trx.fecha, y=MB_real_trx['upper_graph'],
                                        name='upper_ab', fill='tonexty', 
                                        fillcolor='rgba(60,60,60,0.1)',
                        text=["tweak line smoothness<br>with 'smoothing' in line object"],
                                        mode='lines', line=dict(width=0)))
    
    logger.debug('adding trace - real MB lower interval')
    mb_real2 = fig.add_trace(go.Scatter(x=MB_real_trx.fecha, y=MB_real_trx['lower_graph'],
                                        name='lower_ab', fill='tonexty', 
                                        fillcolor='rgba(60,60,60,0.1)',
                        text=["tweak line smoothness<br>with 'smoothing' in line object"],
                                        mode='lines', line=dict(width=0)))


    logger.debug('updating plot extra settings')
    fig.update_traces(mode="markers+lines", hovertemplate=None)
    fig.update_layout(hovermode="x")
    fig.update_layout(hovermode="y unified")
    fig.update_layout(legend=dict(y=0.5, traceorder='reversed', font_size=13))
    
    logger.debug('saving plot')
    fig.write_html(output_path + 'plot_forecasts_vs_real_monitoring.html')
    logger.debug('saved')

       

    

               
    
