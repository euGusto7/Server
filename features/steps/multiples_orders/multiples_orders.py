import json
import support
import allure
import random
import subprocess
from time import sleep
from behave import *
from win32com.client import GetObject
from support.configs.settings import *
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from support.insert_order_infos import insert_order

@given(u'que tenha acesso ao SAP')
def sap_acess(context):
    try:
        global session
        support.clear_sap_processes() #  Fechando o SAP se ele já estiver aberto
        subprocess.Popen(SAP_EXE_PATH) #  Abrindo SAP
        sleep(5)
        sap_gui = GetObject("SAPGUI")
        context.application = sap_gui.GetScriptingEngine
        context.connection = context.application.OpenConnection(
            SAP_EXE_CONNECTION, False) #  Abrindo uma conexão
        sleep(2)
        session = context.connection.Children(0)
        context.session = session
    except Exception as error:
        raise Exception(support.error_message(
            "HOUVE UM ERRO AO TENTAR SE CONECTAR AO SAP:\n"+
            f"{error}"))
    

@when(u'fizer login')
def sap_login(context):
    #  Realizando login
    try:
        context.session.findById("wnd[0]").maximize()
        context.session.findById(
            "wnd[0]/usr/txtRSYST-BNAME").text = SAP_EXE_USER #  Inserindo username
        context.session.findById(
            "wnd[0]/usr/pwdRSYST-BCODE").text = SAP_EXE_PASS #  Inserindo password
        context.session.findById("wnd[0]").sendVKey(0)
        error_msg = context.session.findById("wnd[0]/sbar")
        #  verificando se houve erro ao efetuar login
        if str(error_msg) == ('O nome ou a senha não está correto (repetir o logon)'):
            support.clear_sap_processes()
            assert False
    except AssertionError:
        raise Exception(support.error_message("LOGIN E/OU SENHA INCORRETO!"))
    
    #  Verificando se alguem já está logado no SAP 
    #  e selecionando opção de permitir vários usuários
    try:
        login_already_exist = context.session.FindById(
            'wnd[1]/usr/radMULTI_LOGON_OPT2')
        if (login_already_exist):
            context.session.findById('wnd[1]/usr/radMULTI_LOGON_OPT2').select()
            context.session.findById('wnd[1]/usr/radMULTI_LOGON_OPT2').setFocus()
            context.session.findById('wnd[1]').sendVKey(0)
    except:
        pass
        
        
@when(u'inserir codigo de transferência "mmbe"')        
def insert_stock_code(context):
    #  Indo para transferência mmbe
    context.session.findById("wnd[0]/tbar[0]/okcd").text = SAP_STOCK
    context.session.findById("wnd[0]").sendVKey(0) #  tecla Enter
    sleep(2)
    
        
@then(u'Verificar se todos os produtos possuem estoque / criar inventário')
def create_inventory(context):
    try:
        #  Verificando estoque dos produtos 
        support.verify_stock(context, COD_CD, 5008, 10)
        support.verify_stock(context, COD_CD, 39202, 10) 
        support.verify_stock(context, COD_CD, 50170002, 0.3)
    except:
        raise Exception(support.error_message(
            "ERRO AO VERIFICAR ESTOQUE DE PRODUTOS!"))  
         
            
@given(u'tenha inserirido os dados do produto')
def Insert_orders(context):   
    global session
    product = [] #  lista que recebe o produto que será utilizado no próximo pedido 
    #  lista de produtos a serem testados
    list_products =[{'product': '5008','quantity': '2','lot': None},
                    {'product': '39202','quantity': '10','lot': '22046/6'},
                    {'product': '50170002','quantity': '1','lot': None}]
    
    product.append(random.choice(list_products))
    context.list_cod_orders = []
    #  inserindo todas as informações do pedido 
    insert_order(context, session, COD_CD, list_products)
    context.list_cod_orders.append(context.cod_order)     
    support.clear_sap_processes()


@when(u'criar conferências')
def create_conference(context):
    #  criando conferências
    support.request_multiples_orders(CONFERENCE_API, context.list_cod_orders)  


@when(u'faturar os pedidos')
def faturing_orders(context):
    #  acessando o Portal [CD]
    context.driver.get(f"{CD_PORTAL_LINK}")
    context.driver.maximize_window()
    try:
        #  efetuando o login
        support.sendkeys_element(context.driver,
                                 'input[id="user"]', f"{CD_PORTAL_USER}")
        support.sendkeys_element(context.driver,
                                 'input[name="pass"]', f"{CD_PORTAL_PSWRD}")
        support.click_element(context.driver,
                              'input[value="Acessar"]')
        error_msg = support.text_element(context.driver, 'h2[class="swal2-title"]')
        #  verificando possivel erro de login
        if error_msg == ("Falha ao tentar logar, tente novamente"):
            assert False
    except:
        raise Exception(
            support.error_message("O Usuário ou a Senha não está correto"))

    support.click_element(context.driver,
                          'i[class="fas fa-angle-left right"]') #  acessando menu dropdown [Processos]
    support.click_element(context.driver,
                          'a[href="/invoiceOrder"]') #  selecionando faturamento [Faturar pedido SAP]
    
    while True:
        try:
            for cod_order in context.list_cod_orders:
                support.sendkeys_element(context.driver,
                                         'input[name="search-conference"]',
                                         f'{cod_order}') # inserindo codigo dos pedidos do SAP
                support.click_element(context.driver,
                                      'button[id="sendConferenceToInvoice"]')
                sleep(1)
            break
        except Exception as error:
            raise Exception(support.error_message(
                "[CD] ERRO AO INSERIR OS CODIGOS DO PEDIDO PARA FEATURAMENTO:\n"+
                f"{error}"))
    try:
        #  inserindo [Quantidade de Impressões] e [Observação]
        support.sendkeys_element(context.driver, 'input[id="prints"]', '1')
        support.sendkeys_element(context.driver, 'input[id="note"]', '1')
    except Exception as error:
        raise Exception(
            support.error_message(f"[CD] ERRO:{error}\n"+
                                  "AO INSERIR INFORMAÇÕES DE FATURAMENTO!"))  
    sleep(3)
    try:
        context.driver.execute_script(
            "window.scrollTo(0,document.body.scrollHeight)") #  descendo a tela para clickar no botão [CONCLUIR]
        support.click_element(context.driver,
                              'button[class="btn btn-secondary"]')
        WebDriverWait(context.driver, 10).until(
            EC.alert_is_present()).accept() #  aceitando alerta
        sleep(2)
    except Exception as error:
        raise Exception(
            support.error_message(
                "ERRO AO CONCLUIR FATURAMENTO DE PEDIDO!\n"+
                f"{error}"))        
    
    
@then(u'Verificar status dos pedidos')
def verify_status(context):
    support.click_element(context.driver, 'a[href="/finished"]') #  acessando [Atividades Finalizadas]
    while True:
        #  pesquisando um pedido faturado
        try:
            support.sendkeys_element(context.driver,
                                     'input[id="search_orders"]',
                                     f"{context.list_cod_orders[0]}") 
            support.click_element(context.driver,
                                  'div[style=""] a[class="btn btn-outline-primary float-end"]')
            break 
        except:
            context.driver.refresh()  # Atualizar a página se o elemento não for encontrado
            
    status = support.text_element(context.driver, 'span[name="status"]')
    input_requestor = support.find_element(context.driver,
                                           'visible', 'input[name="requestor"]')
    requestor = input_requestor.get_attribute('value')  
    user_info = support.find_element(context.driver,
                                     'visible', 'a[class="d-block"]')
    username = user_info.get_attribute('title')
    
    #Batendo print da pagina atual
    context.driver.save_screenshot('screenshot01.png')
    context.driver.execute_script(
        "window.scrollTo(0,document.body.scrollHeight)")
    support.click_element(context.driver,
                          'button[onclick="downloadFile(this)"][nl-target="xml_file_1"]')#Botão de download do json
    sleep(1)
    try:
        #  fixando arquivo .json e print da tela no retorno do Allure
        allure.attach.file('screenshot01.png', name='json_result',
                            attachment_type=allure.attachment_type.PNG)
        allure.attach.file(f"{PATH_FILE}\Retorno.json", name='json_result',
                            attachment_type=allure.attachment_type.JSON)
    except:
        raise Exception(support.error_message(
            "Não foi possível anexar o arquivo!"))
    
    with open(f'{PATH_FILE}\Retorno.json', encoding="utf-8") as arq:
        cont = arq.read()
        it = json.loads(cont)
    for x in it['T_PEDIDOS_RET']:
        if (x['ERRO'] == 'X'):
            raise Exception(support.error_message(
                f"Erro no Faturamento do Pedido: {x['VBELN']}, {x['MSG']}"))
    sleep(2)
    #  verificando possiveis erros no status do pedido
    try:
        if str(status) == 'CONCLUIDO':
            assert True
        elif str(status) == 'ERRO':
            assert False
        elif str(status) == 'EM ANDAMENTO':
            context.driver.refresh()
            
        else:
            assert False
    except AssertionError:
        raise Exception(support.error_message(
            f'Era esperado que o status:"{status}" fosse igual a "CONCLUIDO"'))            
    try:
        assert username == requestor
    except AssertionError:
        raise Exception(support.error_message(
            f'Era esperado que o "{username}" '+
            f'fosse igual ao solicitante:"{requestor}"'))  
    