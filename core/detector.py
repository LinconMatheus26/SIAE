def detectar_tipo_pdf(texto):
    texto = texto.lower()

    if "neoenergia pernambuco" in texto or "neoenergia" in texto:
        return "Neoenergia"

    elif "compesa" in texto or "companhia pernambucana de saneamento" in texto:
        return "Compesa"

    return "Desconhecido"