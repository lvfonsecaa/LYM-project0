import re
def lexer(texto:str):
    texto = texto.lower()
    tokens = texto.split(" ")
    tokens = texto.split(";")
    tokens = re.findall(r"\w+|[^\w\s]", texto)
    return tokens

validos = "m,r,c,b"

#def parser(tokens:list):

cadena  = input ("cadena: ")
print (lexer(cadena))
