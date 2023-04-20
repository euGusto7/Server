#!/bin/bash

# Definir o caminho para o arquivo .env
ENV_FILE=C:\ProgramData\Jenkins\.jenkins\workspace\AUTOMATIZAR TESTE NO FATURAMENTO\.env

# Carregar as variáveis de ambiente do arquivo .env
set -a
source $ENV_FILE
set +a

# Executar os testes Behave
behave features/multiples_orders.feature

# Gerar relatório Allure
allure generate -c -o "C:\ProgramData\Jenkins\.jenkins\workspace\AUTOMATIZAR TESTE NO FATURAMENTO\allure-report"
