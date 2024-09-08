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
orientaciones = ["north", "south", "east", "west"]
tokens_validos =["(", ")", ",", "{", "}", ";", "?", "=", "while", "if ", "then", "not", "else", "fi", "do", "od"]
funciones_exe = ["walk", "jump", "drop", "pick", "grab", "letgo", "pop"]
valores = ["size", "myx", "myy", "mychips", "myballoons", "balloonshere", "roomforchips"]
condiciones = ["blocked,", "isblocked", "facing", "isfacing", "zero"]

def validar_y_extraer_parametros(arr):
    # Verificar que el array empiece con '('
    if arr[0] != '(':
        return False, []
    
    # Inicializar un contador de paréntesis para manejar el anidamiento
    contador_par = 1
    indice_cierre = -1
    
    # Buscar el paréntesis de cierre correspondiente al primer '('
    for i in range(1, len(arr)):
        if arr[i] == '(':
            contador_par += 1
        elif arr[i] == ')':
            contador_par -= 1
            if contador_par == 0:
                indice_cierre = i
                break
    
    # Si no se encontró un cierre correspondiente
    if indice_cierre == -1:
        return False, []
    
    # Extraer los elementos entre el primer '(' y su correspondiente ')'
    contenido = arr[1:indice_cierre]
    
    # Validar que los elementos intermedios tengan las comas en posiciones correctas
    for i in range(1, len(contenido), 2):
        if contenido[i] != ',':
            return False, []
    
    # Extraer los elementos que están en las posiciones impares (sin los separadores)
    resultado = [contenido[i] for i in range(0, len(contenido), 2)]
    
    # Eliminar los elementos desde el inicio hasta el paréntesis de cierre incluido
    del arr[:indice_cierre + 1]
    
    return True, resultado  
            

def validar_parametros(lista) :
    parametros = []
    if len(lista) == 1:
        parametros.append(lista[0])
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

def validar_direcciones(lista):
    if len(lista) == 1:
        if lista[0] in direcciones:
            return True
        else: 
            return False
    elif len(lista) == 0:
        return False
    for i in range(lista):
        if lista[i] in direcciones:
            if lista[i+1] != ",":
                return False
            else:
                i+=2
        else: return False
    
    return True

def validar_funciones_safeexe(lista, parametros):
    if lista[0] in funciones_exe:
        parentesis_a = lista.pop(0)
        if parentesis_a == "(" and len(lista)>0:
            token_par = lista.pop(0)
            if validar_value(token_par,parametros) and len(lista > 0):
                parentesis_c1 = lista.pop(0)
                if parentesis_c1 == ")" and len(lista)>0:
                    parentesis_c2 = lista.pop(0)
                    if parentesis_c2 != ")":
                        return False
                else:
                    return False
            else:
                return False
        else:
            return False
    else: 
        return False
    return True
    
def validar_value(value, variables):
    if value.isdigit():
        return True
    elif value in valores:
        return True
    elif value in variables:
        return True
    else:
        return False
    
def validar_condition(lista, parametros):
    validar_parentesis, interior_parentesis = validar_y_extraer_parametros(lista)
    if validar_parentesis and len(interior_parentesis) == 5:
        if interior_parentesis[0] in condiciones and interior_parentesis[1] == "?" and interior_parentesis[2] == "(" and interior_parentesis[4] == ")":
            condicional = interior_parentesis[0]
            if condicional == "blocked" or condicional == "isblocked":
                if interior_parentesis[3] not in direcciones:
                    return False
            
            elif condicional == "facing" or condicional == "isfacing":
                if interior_parentesis[3] not in direcciones:
                    return False
            
            elif condicional == "zero":
                if validar_value(interior_parentesis[3], parametros) == False:
                    return False
            else:
                return False
        else:
            return False
    else:
            return False
    return True
    
def validar_if (lista, variables):
    token_if = lista.pop(0)
    if token_if == "if":
        if lista[0] == "not":
            lista.pop(0)
        if not validar_condition(lista, variables):
            return False
    else:
        return False
    token_then = lista.pop(0)
    if token_then == "then":
        if parser_bloque(lista, variables) == False:
            return False
    else:
        return False
    token_else = lista.pop(0)
    if token_else == "else":
        if parser_bloque(lista, variables) == False:
            return False
    else:
        return False
    token_fi = lista.pop(0)
    return token_fi == "fi"

def validar_loop (lista, parametros):
    token_do = lista.pop(0)
    if token_do == "do":
        if lista[0] == "not":
            lista.pop(0)
        if not validar_condition(lista, parametros):
            return False
    else:
        return False
    if not parser_bloque(lista, parametros):
        return False
    token_od = lista.pop(0)
    return token_od == "od"


def validar_repeat_times(lista,parametros):
    token_repeat = lista.pop(0)
    if token_repeat == "repeat" and len(lista)>2 and validar_value(lista[0], parametros) and lista[1] == "times":
        lista = lista[2:]
        if not parser_bloque(lista, parametros):
            return False
    else:
        return False
    return True    
    
def buscar_caracter_cierre(lista,caracter_abierto, caracter_cerrado):
    #llega el arreglo desde la {
    contador_abiertos = 0
    contador_cerrados = 0
    i = 0
    for str in lista:        
        if str == caracter_abierto:
            contador_abiertos += 1
        elif str == caracter_cerrado:
            contador_cerrados += 1
        
        if contador_abiertos == contador_cerrados:
            return i
        
        i+=1
    return -1

def parser_macro (tokens:list, parametros):
    nombre_macro = tokens.pop(0)
    if nombre_macro.isalnum() and len(tokens)>0:
    #se añade el nombre de la macro
        validar, parametros_internos = validar_y_extraer_parametros(tokens,parametros)
        if validar and len(tokens)>0:
            parametros_internos = parametros_internos.append(parametros)
            validar_bloque = parser_bloque(tokens, parametros_internos)
            if validar_bloque == False:
                return False                                    
        else:
            return False
    else: 
        return False

    return True, nombre_macro
    


def parser_bloque(tokens, parametros, macros):
    macros = []
    while len(tokens):
        token_llave_abierta = tokens.pop(0)
        if token_llave_abierta == "{":
            posicion_llave_cierre = buscar_caracter_cierre(tokens, "{", "}")
            if  posicion_llave_cierre == -1:
                return False
            else:
                tokens_bloque = tokens[0,posicion_llave_cierre]
                tokens = tokens[posicion_llave_cierre+1:]
                token = tokens_bloque.pop(0)
                if token in funciones_valor and len(tokens_bloque)>0:
                    validar, interior_parentesis = validar_y_extraer_parametros(tokens_bloque)
                    if not validar:
                        return False
                    else:
                        if len(interior_parentesis) == 1 and validar_value(interior_parentesis[0], parametros):
                            token_semicolon = tokens_bloque.pop(0)
                            if token_semicolon != ";":
                                return False
                            
                elif token == "new" and len(tokens_bloque)>0:
                    token_macro = tokens_bloque.pop(0)
                    if token_macro == "macro" and len(tokens_bloque)>0:
                        validar_macro, nombre_macro = parser_macro(tokens_bloque) 
                        if validar_macro:
                            macros.append(nombre_macro)
                            validar_macro, parametros_macro = validar_y_extraer_parametros(tokens_bloque)
                            if validar_macro: 
                                if  not parser_bloque(tokens_bloque, parametros_macro.append(parametros), macros):
                                    return False
                            else:
                                return False
                        else: 
                            return False
                    else:
                        return False
                elif token == "turntomy" and len(tokens_bloque) >0 :
                    token_parentesis_a = tokens_bloque.pop(0)
                    if token_parentesis_a == "(" and len(tokens_bloque)> 0:
                        token_direccion = tokens_bloque.pop(0)
                        if token_direccion in direcciones and len(tokens_bloque)>0:
                            token_parentesis_c = tokens_bloque.pop(0)
                            if token_parentesis_c != ")":
                                return False 
                        else:
                            return False
                    else:
                        return False
                elif token == "turntothe" and len(tokens_bloque) >0 :
                    token_parentesis_a = tokens_bloque.pop(0)
                    if token_parentesis_a == "(" and len(tokens_bloque)> 0:
                        token_direccion = tokens_bloque.pop(0)
                        if token_direccion in orientaciones and len(tokens_bloque)>0:
                            token_parentesis_c = tokens_bloque.pop(0)
                            if token_parentesis_c != ")":
                                return False 
                        else:
                            return False
                    else:
                        return False
                elif token == "moves" and len(tokens_bloque) > 0:
                    validar, interior_moves =validar_y_extraer_parametros(tokens_bloque)
                    if validar:
                        if len(interior_moves) == 1:
                            validar_value = validar_value(interior_moves[0], parametros)
                
                elif token == "safeexe":
                    token_parentesis_a = tokens_bloque.pop(0)
                    if token_parentesis_a == "(" and len(tokens_bloque)> 0:
                        if validar_funciones_safeexe(tokens_bloque) == False:
                            return False
                    else:
                        return False
    return True
        
        
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
                if tokenvariable.isalnum() and len(tokens)>0 :
                    variables.append(tokenvariable)
                    tokenigual = tokens.pop(0)
                    if tokenigual != "=" or len(tokens)==0:
                        return False
                    else:
                        tokenvalor = tokens.pop(0)
                        #solo si las variables son numericas
                        if not validar_value(tokenvalor, variables):
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
            validar_bloque = parser_bloque(tokens, variables, macros)
            if not validar_bloque:
                return False
        else: 
            #porque en el bloque principal solo puede haber new var, new macro o exec
            return False
    return True