from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def find_element(context, condition, locator, nullable=False):
    """
    conditions():a
        Essa função utiliza a biblioteca WebDriverWait do Selenium para aguardar a ocorrência de uma determinada
        condição em um elemento web identificado pelo localizador (locator) fornecido. As ações a serem executadas
        no elemento dependem da condição passada como argumento. As condições disponíveis são:
        - 'clickable': espera até que o elemento esteja clicável e então o clica.
        - 'present': espera até que o elemento esteja presente na página e então insere o texto fornecido.
        - 'visible': espera até que o elemento esteja visível na página e então obtém seu texto.
    """
    wait = WebDriverWait(context, 10)
    try:
        if 'clickable' in condition:
            return wait.until(EC.element_to_be_clickable(('css selector', locator)))
        if 'present' in condition:
            return wait.until(EC.presence_of_element_located(('css selector', locator)))
        if 'visible' in condition:
            return wait.until(EC.visibility_of_element_located(('css selector', locator)))
    except TimeoutException:
            if nullable:
                return False
            print(context.driver.current_url,
                  'TimeoutException at', condition, locator)
            if (context.max_retries <= 0):
                context.max_retries = 20
                return False

            context.max_retries -= 1
            return context.find_element(condition, locator)

def click_element(context, locator):
    """
    click_element():
        Clica em um elemento identificado por um localizador, com base em uma condição, dentro de um contexto.
        Args:
            context (objeto): Contexto em que o elemento será procurado.
            condition (str): Condição para localização do elemento.
            locator (str): Localizador do elemento.
        Returns:
            element (objeto): Elemento clicado.
    """
    element = find_element(context, 'clickable', locator).click()
    return element

def sendkeys_element(context, locator, text):
    """
    sendkeys_element():
        Escreve um texto em um elemento identificado por um localizador, com base em uma condição, dentro de um contexto.
        Args:
            context (objeto): Contexto em que o elemento será procurado.
            condition (str): Condição para localização do elemento.
            locator (str): Localizador do elemento.
            text (str): Texto a ser escrito no elemento.
        Returns:
            element (objeto): Elemento em que o texto foi escrito.

    """
    element = find_element(context, 'present', locator).send_keys(text)
    return element

def text_element(context, locator):
    """
    write_elements():
        Armazena o texto de um elemento identificado por um localizador, com base em uma condição, dentro de um contexto.
        Args:
            context (objeto): Contexto em que o elemento será procurado.
            condition (str): Condição para localização do elemento.
            locator (str): Localizador do elemento.
        Returns:
            element (objeto): Texto do Elemento.

    """
    element = find_element(context, 'visible', locator).text
    return element