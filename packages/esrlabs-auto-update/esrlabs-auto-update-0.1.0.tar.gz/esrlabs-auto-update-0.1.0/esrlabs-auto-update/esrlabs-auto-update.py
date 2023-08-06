import schedule
import platform
import time
import requests
import hashlib
import urllib.parse
import shutil
import json
import os
import getpass
from crontab import CronTab
import logging


ARTIFACTORY_URL = 'https://artifactory.int.esrlabs.com/artifactory/'
SCRIPT_DIR = os.path.dirname(__file__)
INSTALL_DIR = os.path.join(SCRIPT_DIR, '..')

logging.basicConfig(filename='esrlabs-auto-update.log',
                    encoding='utf-8', level=logging.DEBUG,
                    format='%(asctime)s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p')


def get_sha1_digest(file):
    BUF_SIZE = 65536
    sha1 = hashlib.sha1()
    with open(file, 'rb') as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            sha1.update(data)
    return sha1.hexdigest()


def check_updates(install_dir):
    logging.info('Checking for updates...')
    tool_path = os.path.join(install_dir, 'flashmate')
    old_sha1 = get_sha1_digest(os.path.join(tool_path, 'flashmate.jar'))
    url = urllib.parse.urljoin(
        ARTIFACTORY_URL, 'api/storage/esr-flashmate-local/latest/flashmate.jar')
    r = requests.get(url)
    sha1 = json.loads(r.content)['checksums']['sha1']
    return old_sha1 != sha1


def install(install_dir):
    logging.info('Installing: flashmate')
    tool_path = os.path.join(install_dir, 'flashmate')
    os.makedirs(tool_path, exist_ok=True)
    files = ['flashmate.jar', 'ChangeLog.md']
    for file in files:
        url = urllib.parse.urljoin(
            ARTIFACTORY_URL, f'esr-flashmate-local/latest/{file}')
        r = requests.get(url)
        if r.ok:
            open(os.path.join(tool_path, file),
                 'wb').write(r.content)
    shutil.copy(os.path.join(
        SCRIPT_DIR, 'helpers/flashmate/flashmate'), tool_path)
    shutil.copy(os.path.join(
        SCRIPT_DIR, 'helpers/flashmate/flashmate.bat'), tool_path)
    logging.info('Successfully installed flashmate')


def job():
    logging.info('Schedule update job')
    if check_updates(INSTALL_DIR):
        install(INSTALL_DIR)


def set_startup_rules():
    if platform.system() == 'Linux':
        command = 'python {} &'.format(__file__)
        username = getpass.getuser()
        cron = CronTab(user=username)
        for job in cron:
            if job.comment == 'esrlabs-auto-update':
                cron.remove(job)
                break
        job = cron.new(command=command, comment='esrlabs-auto-update')
        job.every_reboot()
        cron.write()


set_startup_rules()
schedule.every().day.at("01:00").do(job, 'It is 01:00')

while True:
    schedule.run_pending()
    time.sleep(60)
