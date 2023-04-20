import support
import subprocess
from behave import *
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import WebDriverException
from support.configs.settings import *


def before_all(context):
    """
    before_all():
        Função que é chamada antes de qualquer outra função
        Behave. Nesse caso ela configura o diretorio para 
        download de arquivos e instala o driver.
    Args:
        context: variável de contexto padrão do Behave
    """
    try:
        context.options = webdriver.ChromeOptions()
        context.options.add_experimental_option(
            "prefs",
            {"download.default_directory": f"{PATH_FILE}"})
        context.chrome_service = Service(ChromeDriverManager().install())
        context.driver = webdriver.Chrome(
            service=context.chrome_service,chrome_options=context.options)
        
    except WebDriverException:
        raise Exception(support.error_message(
            "ERRO NA INSTALAÇÃO DO DRIVER!"))

def after_all(context):
    """
    after_all():
        Função que é chamada após todas as funções do
        Behave. Nesse caso ela é responsável por fechar o 
        driver e excluir arquivo que foi instalado no 
        processo. 
    Args:
        context: variável de contexto padrão do Behave
    """
    support.clear_sap_processes()
    if context.driver:
        context.driver.quit()

    path = f'{PATH_FILE}\Retorno.json'
    if os.path.isfile(path):
        os.remove(path)
    else:
        raise Exception(support.error_message(
            'ARQUIVO NÃO ENCONTRADO'))

