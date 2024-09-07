import re
import leer_txt as leer

texto = leer.abrir(input("nombre archivo sin .txt: "))

def lexer(texto:str):
    texto = texto.lower()
    tokens = re.findall(r"\w+|[^\w\s]", texto)
    return tokens

palabras_reservadas = ["turntomy", "turntothe", "walk", "jump", "drop", "pick", "grab", "letgo", "pop", "moves", "nop", "safeexe", "exec", "new", "var", "macro", "isblocked", "isfacing", "blocked", "facing", "zero"]
tokens_validos =["(", ")", ",", "{", "}", ";", "?", "=", "while", "if ", "then", "not", "else", "fi", "do", "od"]

def parser(tokens:list):
    variables = []
    macros = []
    tokens = lexer()
    for element in tokens:
        if tokens[element] == "new":    
            if tokens[element+1] == "var":
                #mirar parentesis?
                variables.append(tokens[element+3])
            elif tokens[element+1] == "macro":
                valido = []
                #...
                macros.append()
            else:
                return False
            
        #if 
        