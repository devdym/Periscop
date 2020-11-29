from SeisLogAPI.digicourse import read_battery_short
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
    # filter battery logs
    files = dict(filter(lambda elem: "battery" in elem[0], files.items()))
    kwargs['ti'].xcom_push(key='import_files', value=len(files))


def read_data(**kwargs):
    files_list = []
    projectid = None
    importlog_id = None

    # make list of files from folder
    # data = kwargs['ti'].xcom_pull(key='import_files', task_ids='scan_folder')

    files = scan_folder(basepath)
    # filter ballasting logs
    data = dict(filter(lambda elem: "battery" in elem[0], files.items()))

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
            b = read_battery_short(log_path)
            battery_toMySql(b, projectid)
            logger.info('IMPORTED')
            # add into importlog
            save_log_toMySql(log_path, projectid)
            logger.info('LOG is UPDATED')
    # task_instance = kwargs['ti']
    #
    # da = []
    # data = task_instance.xcom_pull(key='import_files', task_ids='scan_folder')
    # for d in data:
    #     da.append(str(d))
    #     logger.info('data: {}'.format(str(d)))
    #
    # data_db = read_db('%battery%')
    # for db in data_db:
    #     logger.info('data_db: {}'.format(db))
    #
    # li_dif = [i for i in da if i not in da or i not in data_db]
    #
    # for d in li_dif:
    #     logger.info('li_dif: {}'.format(d))
    #     b = read_battery_short(d)
    #     battery_toMySql(b)
    #
    # logFiles_toMySql(da)


def move(**kwargs):
    files = scan_folder(basepath)
    # filter ballasting logs
    data = dict(filter(lambda elem: "battery" in elem[0], files.items()))
    # task_instance = kwargs['ti']
    # data = task_instance.xcom_pull(key='import_files', task_ids='scan_folder')
    for s in data:
        d = os.path.dirname(os.path.abspath(s))
        d = str(s).replace('projects', 'archive')
        shutil.move(s, d)


def battery_toMySql(data, id):
    data['project_id'] = id
    # create sqlalchemy engine
    engine = create_engine("mysql+pymysql://{user}:{pw}@localhost/{db}"
                           .format(user="usersql",
                                   pw="usersql",
                                   db="aurora"))
    data.to_sql('batteries', con=engine, if_exists='append', chunksize=1000, index=False)
    # print("***inserted***")
