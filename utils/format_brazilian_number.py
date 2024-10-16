import re

def format_brazilian_number(wa_id: str) -> str:
    # Remover qualquer caractere não numérico
    cleaned_number = re.sub(r'\D', '', wa_id)

    # Verificar se é um número brasileiro (código do país: 55)
    if cleaned_number.startswith('55') and len(cleaned_number) == 12:
        # Adicionar o '9' após o código de área (com DDD) se faltar
        return cleaned_number[:4] + '9' + cleaned_number[4:]

    # Retornar o número sem alterações se não for necessário ajuste
    return cleaned_number