import logging,flet as ft, os.path
from utilits import bd
from Desktop import pages


logger_main=logging.getLogger("main")
logger_main.setLevel(logging.INFO)

if (__name__=="__main__"):
    
    logging.basicConfig(filename=".\Logs.log", format='[%(levelname)s] [%(asctime)s] - %(name)s: %(message)s')

    logger_main.info("App Started")
    
    ft.app(pages.start_page)