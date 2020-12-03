# import paramiko
from airflow.models import Variable
import os
import logging
import pathlib
import datetime as dt

logger = logging.getLogger("airflow.task")

def connect_to_server(**kwargs):
    server = Variable.get("DigiCourseIP")
    response = os.system("ping -c 1 " + server)

    if response == 0:
        logger.info('DigiCourse host is up! - CONTINUE')
        return 'mount'
    else:
        logger.info('DigiCourse host is down! - STOP')
        return 'finish'


def read_source_folder(**kwargs):
    source = Variable.get("DigiCourseSourceFolder")

    d = dt.datetime.now()
    cur_month = d.strftime("%B")
    source = source + cur_month

    data = []
    for child in pathlib.Path(source).iterdir():
        if child.is_dir():
            pass
        if child.is_file():
            data.append(os.path.split(child)[-1:][0])
    logger.info(data)
    kwargs['ti'].xcom_push(key='source_folder', value=data)


def read_dist_folder(**kwargs):
    survey = Variable.get('current_survey')
    destination = Variable.get('data_repository_path')
    destenation_path = os.path.normpath(destination + '/' + survey + '/Barbaros/battery')

    ddata = []
    for child in pathlib.Path(destenation_path).iterdir():
        if child.is_dir():
            pass
        if child.is_file():
            ddata.append(os.path.split(child)[-1:][0])
    logger.info(ddata)
    kwargs['ti'].xcom_push(key='dist_folder', value=ddata)


def compare_log_files(**kwargs):
    data = kwargs['ti'].xcom_pull(key='source_folder', task_ids='read_source')
    ddata = kwargs['ti'].xcom_pull(key='dist_folder', task_ids='read_dist')

    logger.info('DATA: {}'.format(data))
    logger.info('DDATA: {}'.format(ddata))

    def Diff(data, ddata):
        return (list(list(set(data) - set(ddata)) + list(set(ddata) - set(data))))
    
    to_copy = []

    # if len(data) > 0 and len(ddata) > 0:
    to_copy = Diff(data, ddata)

    if len(to_copy) > 0:
        logger.info(to_copy)
        kwargs['ti'].xcom_push(key='file_to_copy', value=to_copy)
        return 'copy_files'
    else:
        return 'finish'


def copy(**kwargs):
    to_copy = kwargs['ti'].xcom_pull(key='file_to_copy', task_ids='get_missing_files')

    source = Variable.get("DigiCourseSourceFolder")
    d = dt.datetime.now()
    cur_month = d.strftime("%B")
    source = source + cur_month

    survey = Variable.get('current_survey')
    destination = Variable.get('data_repository_path')
    destenation_path = os.path.normpath(destination + '/' + survey + '/Barbaros/battery')

    for f in to_copy:
        s = os.path.normpath(source + '/' + f)
        d = os.path.normpath(destenation_path + '/')
        s = s.replace(' ', '\ ')
        d = d.replace(' ', '\ ')
        os.popen('cp ' + s + ' ' + d)
