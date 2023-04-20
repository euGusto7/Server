Funcionalidade: Criar multiplos pedidos 
    Cenario: [Sap] Verificar estoque de produto
        Dado que tenha acesso ao SAP
        Quando fizer login
        E inserir codigo de transferência "mmbe"
        Entao Verificar se todos os produtos possuem estoque / criar inventário
    
    Cenario: criar multiplos pedidos 
        Dado tenha inserirido os dados do produto
        Quando criar conferências 
        E faturar os pedidos
        Entao Verificar status dos pedidos 
        