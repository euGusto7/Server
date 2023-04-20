import re
import subprocess
from support.configs.settings import *
from time import sleep
from win32com.client import GetObject


def clear_sap_processes():
    """
    clear_sap_processes():
        Essa função executa o comando 'tasklist' para obter uma lista de processos em execução no Windows,
        e em seguida utiliza expressões regulares para identificar os processos SAP na lista. Em seguida,
        utiliza o comando 'taskkill' para encerrar os processos SAP encontrados.
    Args:
        None
    """
    result = subprocess.run(
        ['tasklist'], stdout=subprocess.PIPE, text=True)
    tasklist = result.stdout

    sap_processes = re.findall(r'sap.*?\.exe', tasklist, re.IGNORECASE)

    for process in sap_processes:
        subprocess.run(['taskkill', '/f', '/im', process],
                        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
