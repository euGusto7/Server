from support.messages import error_message
from support.configs.settings import *
from time import sleep


def add_stock(context, session, cod_product, quantity_to_add=None):
    """
    add_stock():
        Função responsável por adicionar estoque de um produto 
    Args:
        context: variável de contexto padrão do Behave
        session: variável que armazena o objeto da tela do SAP
        cod_product: codigo do produto para adicionar o estoque 
        quantity_to_add: quantidade que deseja inserir
    """
    try:
        session.findById("wnd[0]/tbar[0]/okcd").text = CREATE_INVENTORY
        session.findById("wnd[0]").sendVKey(0)
        purchasing_org = session.findById("wnd[0]/usr/ctxtIKPF-WERKS")
        session.findById("wnd[0]/usr/ctxtIKPF-WERKS").text = COD_CD
        session.findById("wnd[0]/usr/ctxtIKPF-LGORT").text = NORMAL_TYPE
        session.findById("wnd[0]/tbar[1]/btn[7]").press()
        session.findById("wnd[0]/usr/sub:SAPMM07I:0721/ctxtISEG-MATNR[0,4]").text = f"{cod_product}"
        session.findById("wnd[0]/tbar[0]/btn[11]").press()
        session.findById("wnd[0]/tbar[0]/btn[15]").press()
        session.findById("wnd[0]/tbar[0]/okcd").text = ADD_QUANTITY
        session.findById("wnd[0]").sendVKey(0)
        session.findById("wnd[0]/tbar[1]/btn[6]").press()
        session.findById("wnd[0]/usr/sub:SAPMM07I:0731/txtISEG-ERFMG[0,55]").text = f"{quantity_to_add}"
        session.findById("wnd[0]/tbar[0]/btn[11]").press()
        session.findById("wnd[0]/tbar[0]/btn[15]").press()
        session.findById("wnd[0]/tbar[0]/btn[0]").press()
        sleep(2)
        session.findById("wnd[0]/tbar[0]/okcd").text = INSERT_DOC
        session.findById("wnd[0]").sendVKey(0)
        session.findById("wnd[0]/tbar[0]/btn[11]").press()
        sleep(2)
        session.findById("wnd[0]/tbar[0]/btn[12]").press()
        sleep(2)
    except Exception as e:
        raise Exception(error_message(f"{e} AO TENTAR ADICIONAR ESTOQUE!"))