import requests


def request_api(url,cod_order):
    """
    request_api():
        Essa função recebe uma URL e um código de pedido como argumentos,
        e realiza uma requisição GET para a API concatenando a URL com o 
        código de pedido. Em caso de sucesso (status code 200), exibe uma
        mensagem de confirmação. Caso contrário, exibe uma mensagem de erro
        com o código e motivo do status de resposta.
    Args:
        url: url da pagina de criação de confência
        cod_order: codigo do pedido gerado no SAP  
    """
    try:
        url = str(url+cod_order)
        res = requests.get(url)
        if res.status_code == 200:
            print(f"\033[32mA conferência para o pedido:{cod_order} foi gerada!\033[0m")
            assert True
        else:
            print(f"\033[31mErro ao buscar produto {cod_order}: {res.status_code} - {res.reason}\033[0m")
            assert False
    except:
        raise Exception("\033[31mAPI ESTÁ FORA DO AR!!!\033[0m") 
    
def request_multiples_orders(url, order_cod_list):
    """
    request_multiples_orders():
        Essa função recebe uma URL e uma lista de códigos de pedido como
        argumentos, e realiza uma requisição GET para a API para cada código
        de pedido na lista. Em caso de sucesso (status code 200), exibe uma
        mensagem de confirmação. Caso contrário, exibe uma mensagem de erro
        com o código e motivo do status de resposta.
    Args: 
        url: url da pagina de criação de confência
        order_cod_list: lista de codigos do pedidos gerados no SAP  
    """
    try:
        for order in order_cod_list:
            order_list = order.split(",")
            url_with_order = url + ','.join(order_list)
            res = requests.get(url_with_order)
            if res.status_code == 200:
                print(f"\033[32mSucesso ao buscar produto {order}: {res.status_code} - {res.reason}\033[0m")
            else:
                print(f"\033[31mErro ao buscar produto {order}: {res.status_code} - {res.reason}\033[0m")
    except:
        raise Exception("\033[31mAPI ESTÁ FORA DO AR!!!\033[0m")
