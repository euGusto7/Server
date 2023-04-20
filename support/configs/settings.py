import os
from dotenv import load_dotenv
load_dotenv()

try:
    ADD_STOCK = os.environ['ADD_STOCK']
    COD_PRODUCT_01 = os.environ['COD_PRODUCT_01']
    COD_PRODUCT_02 = os.environ['COD_PRODUCT_02']
    COD_PRODUCT_03 = os.environ['COD_PRODUCT_03']
    COD_AS = os.environ['COD_AS']
    COD_CD = os.environ['COD_CD']
    CREATE_INVENTORY = os.environ['CREATE_INVENTORY']
    ADD_QUANTITY = os.environ['ADD_QUANTITY']
    INSERT_DOC = os.environ['INSERT_DOC']
    COD_MB_COMECIO = os.environ['COD_MB_COMECIO']
    CONFERENCE_API = os.environ['CONFERENCE_API']
    CD_PORTAL_LINK = os.environ['CD_PORTAL_LINK']
    CD_PORTAL_USER = os.environ['CD_PORTAL_USER']
    VERSION_DISPLAY= os.environ['VERSION_DISPLAY']
    CD_PORTAL_PSWRD = os.environ['CD_PORTAL_PSWRD']
    SAP_EXE_CONNECTION = os.environ['SAP_EXE_CONNECTION']
    SAP_EXE_PATH = os.environ['SAP_EXE_PATH']
    SAP_EXE_USER = os.environ['SAP_EXE_USER']
    SAP_EXE_PASS = os.environ['SAP_EXE_PASS']
    SAP_EXE_COD = os.environ['SAP_EXE_COD']
    SAP_STOCK = os.environ['SAP_STOCK']
    NORMAL_TYPE = os.environ['NORMAL_TYPE']
    PATH_FILE = os.environ['PATH_FILE']
    print("\033[32m VARIÁVEIS DE AMBIENTE CARREGADAS!\033[0m")
except Exception as error:
    raise Exception(
        f"\033[31m ERRO AO CARREGAR AS VARIÁVEIS DE AMBIENTE!\n {error}\033[0m")  
