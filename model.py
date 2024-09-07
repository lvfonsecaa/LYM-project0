import re
import leer_txt as leer

texto = leer.abrir(input("nombre archivo sin .txt: "))
def lexer(texto):
    texto = texto.lower()
    tokens = re.findall(r"\w+|[^\w\s]", texto)
    return tokens
condiciones =["blocked", "facing", "zero", "isblocked", "isfacing"]
comandos_sin_parametros = ["nop"]
funciones_lenguaje = ["turntomy", "turntothe", "moves", "safeexe"]
funciones_valor = [ "walk", "jump", "drop", "pick", "grab", "letgo", "pop"]
direcciones = ["left", "right", "back"]
tokens_validos =["(", ")", ",", "{", "}", ";", "?", "=", "while", "if ", "then", "not", "else", "fi", "do", "od"]

def validar_parametros(lista) :
    parametros = []
    if len(lista) == 1:
        parametros.append(lista)
        return True, parametros
    for i in range(lista):
        if lista[i].isalnum():
            if lista[i+1] != ",":
                return False
            else:
                parametros.append(lista[i])
                i+=2
        else: return False
    
    return True, parametros

def busca_llave_cierre(lista):
    #llega el arreglo desde la {
    pila = []
    contador_abiertos = 0
    contador_cerrados = 0
    for i in range(lista):
        
        if lista[i] == "{":
            contador_abiertos += 1
        elif lista[i] == "}":
            contador_cerrados += 1
        
        if contador_abiertos == contador_cerrados and contador_abiertos>0:
            return i
    return -1

def parser_macro (tokens:list):
    nombre_macro = tokens.pop(0)
    if nombre_macro.isalnum() and len(tokens)>0:
    #se añade el nombre de la macro
        token_parentesis_a = tokens.pop(0)
        if token_parentesis_a == "(" and len(tokens)>0:
            if ")" in tokens:
                indice_cierre_parentesis = tokens.index(")")
                parametros = tokens[0:indice_cierre_parentesis]
                tokens = tokens.skip(indice_cierre_parentesis+1).ToArray()
                valido, arreglo_parametros = validar_parametros(parametros)
                #valida que los parametros dentro de la macro sean correctos y esten separados por comas
                if valido and len(tokens)>0:
                    token_llave_a = tokens.pop(0)
                    #saltarse var, new, macro (y parametros hasta )
                    
                    if token_llave_a == "{" and len(tokens)>0:
                        indice_cierre_llave = busca_llave_cierre(tokens)
                        if indice_cierre_llave == -1:
                            return False
                        else:
                            bloque = tokens[0:indice_cierre_llave]
                            tokens = tokens.skip(indice_cierre_llave+1).ToArray()
                            #llamar funcion del parser, ahora con el bloque y los parametros de la macro!
                            validar_bloque = parser_bloque(bloque, arreglo_parametros)
                            if validar_bloque == False:
                                return False                                    
                    else: return False
                    
                else: return False
            else:
                return False
            #parametros de la macro
        else:
            return False
    else: 
        return False
    
    return True, nombre_macro
    

def parser_bloque(tokens_bloque:list, parametros):
    macros = []
    while len(tokens_bloque)>0:
        token = tokens_bloque.pop(0)
        if token in funciones_valor and len(tokens_bloque)>0:
            token_parentesis_a = tokens_bloque.pop(0)
            if token_parentesis_a == "(" and len(tokens_bloque)>0 :
                token_numero = tokens_bloque.pop(0)
                if int.tryparse(token_numero) and len(tokens_bloque)>0: 
                    token_parentesis_c = tokens_bloque.pop(0)
                    if token_parentesis_c != ")":
                        return False 
                else:
                    return False
            else:
                return False
        elif token == "new" and len(tokens_bloque)>0:
            token_macro = tokens_bloque.pop(0)
            if token_macro == "macro" and len(tokens_bloque)>0:
                validar_macro, nombre_macro = parser_macro(tokens_bloque) 
                if validar_macro:
                    macros.append(nombre_macro)
                else: 
                    return False
            else:
                return False
            

def parser(tokens:list):
    variables = []
    macros = []
    tokens = lexer()
    while len(tokens)>0:
        token = tokens.pop(0)
        if token == "new" and len(tokens)>0:
            tokentipo = tokens.pop(0)    
            if tokentipo == "var" and len(tokens)>0:
                tokenvariable = tokens.pop(0)
                if tokenvariable.isalnum() and len(tokens)>0:
                    variables.append(tokenvariable)
                    tokenigual = tokens.pop(0)
                    if tokenigual != "=" or len(tokens)==0:
                        return False
                    else:
                        tokenvalor = tokens.pop(0)
                        #solo si las variables son numericas
                        if int.tryparse(tokenvalor):
                            return False
                else: 
                    return False
                
            elif tokentipo == "macro":
                validar_macro, macro = parser_macro(tokens)
                if validar_macro:
                    macros.append(macro)
                else:
                    return False
            else:
                #porque estoy dentro del new y no hay ni variable ni macro
                return False

        #no es new
        elif token == "exec" and len(tokens)>0:
            token_llave_a = tokens.pop(0)
            if token_llave_a == "{":
                indice_cierre_llave = busca_llave_cierre(tokens)
                if indice_cierre_llave == -1:
                    return False
                else:
                    bloque = tokens[0:indice_cierre_llave]
                    tokens = tokens.skip(indice_cierre_llave+1).ToArray()
                    #llamar funcion del parser, ahora con el bloque y los parametros de la macro!
                    validar_bloque = parser_bloque(bloque, parametros)
                    if validar_bloque == False:
                        return False                                    
            
            else:
                #no es valida porque exec debe ir seguida de una llave
                return False
        else: 
            #porque en el bloque principal solo puede haber new var, new macro o exec
            return False