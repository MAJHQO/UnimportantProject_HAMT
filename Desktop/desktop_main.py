import logging,flet as ft,pages, os.path


if (__name__=="__main__"):
    
    logging.basicConfig(filename="Logs.log")
    
    if(os.path.isfile("./Desktop/admin_condigure.txt")==False):
    
        ft.app(pages.startAdmin_page)

    else:

        ft.app(pages.start_page)