def error_message(message):
    """
    error_message():
        Função que recebe um texto e cria um erro para esse texto
        aplicando o padrão ANSI de cor para o terminal.
    Args:
        message: variável que recebe o texto da mensagem  
    """
    text = f"\033[31m"+message+"\033[0m"
    assert False, (str(text))
    
def sucess_message(message):
    """
    sucess_message():
        Função que recebe um texto e retorna esse texto
        aplicando o padrão ANSI de cor para o terminal.
    Args:
        message: variável que recebe o texto da mensagem  
    Returns:
        text: variável que armazena o texto concatenado
        ao padrão ANSI.
    """
    text = f"\033[32m"+message+"\033[0m"
    return text