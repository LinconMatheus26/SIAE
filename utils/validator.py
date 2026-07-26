def validar_energia(df):
    obrigatorias = ["codigo_energia", "nome_unidade"]
    for col in obrigatorias:
        if col not in df.columns:
            return False, f"Coluna obrigatória faltando: {col}"
    return True, "OK"


def validar_agua(df):
    obrigatorias = ["matricula_agua", "nome_unidade"]
    for col in obrigatorias:
        if col not in df.columns:
            return False, f"Coluna obrigatória faltando: {col}"
    return True, "OK"


def validar_nome_unidade(nome_unidade):
    if "DEL" not in nome_unidade:
        return False, f"Nome fora do padrão: {nome_unidade}"
    return True, "OK"