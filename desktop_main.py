import logging,flet as ft, os.path
from utilits import bd
from Desktop import pages

from cryptography.fernet import Fernet


logger_main=logging.getLogger("main")
logger_main.setLevel(logging.INFO)

if (__name__=="__main__"):
    
    logging.basicConfig(filename="Desktop\\Logs.log", format='[%(levelname)s] [%(asctime)s] - %(name)s: %(message)s')

    logger_main.info("App Started")
    bd.connect=bd.connectionToDatabase()
    
    if(os.path.isfile("Desktop\\Admin Configure")==False):
        ft.app(pages.startAdmin_page)

    else:
        ft.app(pages.start_page)