import support
from support.configs.settings import SAP_STOCK, NORMAL_TYPE, VERSION_DISPLAY
from pywintypes import com_error
from .messages import error_message


def verify_stock(context, center, cod_product, quantity, quantity_to_add=None): 
    """
    verify_stock():
        Função responsável por verificar estoque de produtos, e quando informado
        adiciona quantidade para o produto verificado se este estiver abaixo do 
        desejado.
    Args:
        context: variável de contexto padrão do Behave
        session: variável que armazena o objeto da tela do SAP
        cod_product: codigo do produto para adicionar o estoque 
        quantity: Quantidade a ser verificada
        quantity_to_add: quantidade que deseja inserir
    """
    qtd = float(quantity)
    context.session.findById("wnd[0]").maximize()
    context.session.findById("wnd[0]/tbar[0]/okcd").text = SAP_STOCK
    context.session.findById("wnd[0]").sendVKey(0)
    context.cod_product = context.session.findById(
        "wnd[0]/usr/ctxtMS_MATNR-LOW").text = str(cod_product)
    context.session.findById(
        "wnd[0]/usr/ctxtMS_WERKS-LOW").text = str(center)
    context.session.findById(
        "wnd[0]/usr/ctxtMS_WERKS-HIGH").text = str(center)
    context.session.findById(
        "wnd[0]/usr/ctxtMS_LGORT-LOW").text = NORMAL_TYPE 
    context.session.findById("wnd[0]").sendVKey(0)
    context.session.findById("wnd[0]/usr/ctxtVERNU").text = VERSION_DISPLAY
    context.session.findById("wnd[0]").sendVKey(0)
    context.session.findById("wnd[0]/tbar[1]/btn[8]").press()
    try:
        context.warehouse_object = context.session.findById(
            "wnd[0]/usr/cntlCC_CONTAINER/shellcont/shell/shellcont[1]/shell[1]"
            ).doubleClickItem("          4", "&Hierarchy")
    except com_error:
        raise Exception(error_message("O DEPÓSITO D007 NÃO POSSUI ESTE PRODUTO!"))
    
    try:
        context.table = context.session.findById(
            "wnd[1]/usr/cntlGRID1/shellcont/shell/shellcont[1]/shell")
        context.stock = context.table.GetCellValue(0, 'BSTNDTXT').split(",")[0]
        context.session.findById("wnd[0]/tbar[0]/btn[12]").press()
        context.session.findById("wnd[0]/tbar[0]/btn[12]").press()
        
        if float(context.stock) <= qtd: 
            context.session.findById("wnd[0]/tbar[0]/btn[12]").press()
            support.add_stock(context, context.session, cod_product, quantity_to_add=quantity_to_add)
    except Exception as error:
        raise Exception(error_message(f"{error} AO TENTAR ADICIONAR ESTOQUE PARA O PRODUTO {cod_product}"))
    
    