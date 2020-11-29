from SeisLogAPI.seal408 import read_tension408
from SeisLogAPI.folderscaner import scan_folder, logFiles_toMySql
import os, shutil
import logging
from pathlib import Path
from core.utils import read_db, check_project_id, save_project_name_toMySql, check_log_id, save_log_toMySql
from sqlalchemy import create_engine
from airflow.models import Variable

source = Variable.get("data_repository_path")
logger = logging.getLogger("airflow.task")
basepath = Path(source)


def scan(**kwargs):
    files = scan_folder(basepath)
    # filter tension logs
    files = dict(filter(lambda elem: "tension" in elem[0], files.items()))
    for f in files:
        logger.info(f)
    kwargs['ti'].xcom_push(key='import_files', value=len(files))


def read_data(**kwargs):
    files_list = []
    projectid = None
    importlog_id = None

    # make list of files from folder
    # data = kwargs['ti'].xcom_pull(key='import_files', task_ids='scan_folder')

    files = scan_folder(basepath)
    # filter tension logs
    data = dict(filter(lambda elem: "tension" in elem[0], files.items()))

    # for every file
    for k, l in data.items():
        files_list.append(l['file_path'])
        log_path = l['file_path']
        logger.info('files: {}'.format(l['file_path']))

        # get Project name
        projectname = l["project_name"]
        # get Vessel name
        vesselname = l["vessel_name"]

        logger.info('project name: {}, vessel name: {}'.format(projectname, vesselname))

        # search Project_name + vessel_name in Project table
        projectid = check_project_id(projectname, vesselname)
        if projectid is not None:
            # get id
            logger.info('project id {} already exists'.format(projectid))
        else:
            logger.info('project doesn`t exist')
            # add into Project table
            save_project_name_toMySql(projectname, vesselname)
            projectid = check_project_id(projectname, vesselname)
            # get id
            logger.info('project id {} already exists'.format(projectid))
        # search importlog+project_name+vessel_name in importlog+Project tables
        importlog_id = check_log_id(log_path, projectid)
        if importlog_id is not None:
            logger.info('importlog id {}'.format(importlog_id))
        else:
            logger.info('importlog file dosn`t exist')
            # import file into ballasting table
            b = read_tension408(log_path)
            tension_toMySql(b, projectid)
            logger.info('IMPORTED')
            # add into importlog
            save_log_toMySql(log_path, projectid)
            logger.info('LOG is UPDATED')


def move(**kwargs):
    # task_instance = kwargs['ti']
    # data = task_instance.xcom_pull(key='import_files', task_ids='scan_folder')

    files = scan_folder(basepath)
    # filter tension logs
    data = dict(filter(lambda elem: "tension" in elem[0], files.items()))
    
    for s in data:
        d = os.path.dirname(os.path.abspath(s))
        d = str(s).replace('projects', 'archive')
        shutil.move(s, d)


def tension_toMySql(data, id):
    data['project_id'] = id
    # create sqlalchemy engine
    engine = create_engine("mysql+pymysql://{user}:{pw}@localhost/{db}"
                           .format(user="usersql",
                                   pw="usersql",
                                   db="aurora"))
    data.to_sql('tension', con=engine, if_exists='append', chunksize=1000, index=False)


def get_raw(**kwargs):
    res = []
    engine = create_engine("mysql+pymysql://{user}:{pw}@localhost/{db}"
                           .format(user="usersql",
                                   pw="usersql",
                                   db="aurora"))

    result = engine.execute('SELECT DISTINCT(date_) FROM aurora.tension;')
    for r in result:
        logger.info(r[0])
        res.append(r[0])

    result.close()
    kwargs['ti'].xcom_push(key='raw_dates', value=res)


def get_avg(**kwargs):
    res = []
    engine = create_engine("mysql+pymysql://{user}:{pw}@localhost/{db}"
                           .format(user="usersql",
                                   pw="usersql",
                                   db="aurora"))

    result = engine.execute('SELECT DISTINCT(date_) FROM aurora.tensionavg;')
    for r in result:
        logger.info(r[0])
        res.append(r[0])
    result.close()
    kwargs['ti'].xcom_push(key='db_dates', value=res)


def calc_avg(**kwargs):
    dates = kwargs['ti'].xcom_pull(key='pross_dates', task_ids='compare_dates')
    
    engine = create_engine("mysql+pymysql://{user}:{pw}@localhost/{db}"
                           .format(user="usersql",
                                   pw="usersql",
                                   db="aurora"), pool_size=20, max_overflow=0)

    for d in dates:
        for streamer in range(1, 7):
            result = engine.execute('insert into tensionavg(date_, streamer, tension) '
                                    'values(%s, %s, (SELECT avg(tension) from tension where streamer = %s and date_ like %s));',
                                    (d, streamer, streamer, d))
            result.close()


def compare(**kwargs):
    raw = kwargs['ti'].xcom_pull(key='raw_dates', task_ids='get_dates_raw')
    avg = kwargs['ti'].xcom_pull(key='db_dates', task_ids='get_dates_avg')

    process_list = []
    for d in raw:
        if d not in avg:
            process_list.append(d)
            logger.info("TO BE PROCESSED: {}".format(d))
    
    if len(process_list) > 0:
        kwargs['ti'].xcom_push(key='pross_dates', value=process_list)
        return 'calc_avg'
    else:
        return 'finish'
