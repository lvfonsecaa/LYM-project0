import re
import leer_txt as leer

texto = leer.abrir(input("nombre archivo sin .txt: "))

def lexer(texto:str):
    texto = texto.lower()
    tokens = re.findall(r"\w+|[^\w\s]", texto)
    return tokens

