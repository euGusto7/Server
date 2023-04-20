from support import *
from time import sleep
from support.configs.settings import *
from .sap import *
from .constraints import *
from .messages import *

def insert_order(context, session, warehouse, products):
    """
    insert_order():
        Função responsável por inserir os produtos do pedido
    Args:
        context: variável de contexto padrão do Behave
        session: variável que armazena o objeto da tela do SAP
        warehouse: codigo do fonecedor para o pedido
        quantity_to_add: quantidade que deseja inserir 
    Returns:
        cod_order: codigo do pedido gerado no SAP
    """
    sleep(1)
    session.findById("wnd[0]").sendVKey(3)
    sleep(1)
    session.findById("wnd[0]/tbar[0]/okcd").text = SAP_EXE_COD
    session.findById("wnd[0]").sendVKey(0)
    sleep(1)
    session.findById(f"{SAP_GUI_ELEMENT}/{SAP_CORP_DATA_FIELD}/cmbMEPO_TOPLINE-BSART").setFocus()
    session.findById(f"{SAP_GUI_ELEMENT}/{SAP_CORP_DATA_FIELD}/cmbMEPO_TOPLINE-BSART").key = "UD"
    session.findById(f"{SAP_GUI_ELEMENT}/{SAP_CORP_DATA_FIELD}/ctxtMEPO_TOPLINE-SUPERFIELD").text = f"{warehouse}"
    session.findById(f"{SAP_GUI_ELEMENT}/{SAP_CORP_DATA_FIELD}/ctxtMEPO_TOPLINE-SUPERFIELD").setFocus()
    session.findById("wnd[0]").sendVKey(0)
    session.findById(f"{SAP_GUI_ELEMENT}/{SAP_CORP_DATA_DETAILS}/ctxtMEPO1222-EKORG").text = COD_MB_COMECIO
    session.findById("wnd[0]").sendVKey(0)
    session.findById(f"{SAP_GUI_ELEMENT}/{SAP_CORP_DATA_DETAILS}/ctxtMEPO1222-EKGRP").text = "001"

    data_list = []     
    line = 0
    test1 = SAP_GUI_ELEMENT
    test2 = SAP_GUI_ELEMENT_UPDATE
    for x in products:
        session.findById(f"{test1}/{SAP_PROD_FIELD}ctxtMEPO1211-EMATN[4,{line}]").text = f"{x['product']}"
        session.findById(f"{test1}/{SAP_PROD_FIELD}ctxtMEPO1211-EMATN[4,{line}]").setFocus()
        session.findById("wnd[0]").sendVKey(0)
        session.findById(f"{test2}/{SAP_PROD_FIELD}txtMEPO1211-MENGE[6,{line}]").text = f"{x['quantity']}"
        session.findById(f"wnd[0]").sendVKey(0)
        session.findById(f"wnd[0]/sbar").text
        session.findById(f"{test2}/{SAP_PROD_FIELD}ctxtMEPO1211-NAME1[11,{line}]").text = COD_AS
        session.findById("wnd[0]").sendVKey(0)
        test1 = test2
        if x['lot'] != None:
            session.findById(f"{LOT_INFO}/ctxtMEPO1211-CHARG[13,{line}]").text = x['lot']
            session.findById(f"wnd[0]").sendVKey(0)
        line += 1

    input_date = session.findById(f"{SAP_DATE_DETAILS}").text.split('.')[0]
    data_list.append(input_date)
    sleep(2)        
    try:            
        if len(set(data_list)) == 1:
            assert True
        else:
            assert False
    except AssertionError:
        raise Exception(error_message("DATAS DIFERENTES!"))
    
    try:
        session.findById("wnd[0]").sendVKey(11)
        session.findById("wnd[1]/usr/btnSPOP-VAROPTION1").press()
        context.cod_order = session.findById("wnd[0]/sbar").text.split(" ")[-1]
        sleep(3)            
        if len(context.cod_order) != 10:
            assert False
        else:
            pass
    except:
        raise Exception(error_message("NÃO FOI POSSIVEL PEGAR O CODIGO DO PEDIDO!"))
        
    return context.cod_order