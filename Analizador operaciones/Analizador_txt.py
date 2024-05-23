import re

class AnalizadorSintactico:
    def __init__(self, cadena):
        self.cadena = cadena
        self.posicion = 0

    def siguiente_token(self):
        if self.posicion < len(self.cadena):
            token = self.cadena[self.posicion]
            self.posicion += 1
            return token
        else:
            return None

    def retroceder(self):
        self.posicion -= 1

    def factor(self):
        token = self.siguiente_token()
        if token == '(':
            resultado = self.expresion()
            if self.siguiente_token() == ')':
                return resultado
            else:
                raise SyntaxError("Error de sintaxis: paréntesis no cerrado")
        elif re.match(r'\d', token):
            return int(token)
        else:
            raise SyntaxError("Error de sintaxis: factor inválido")

    def verificar_operador_doble(self):
        token1 = self.siguiente_token()
        token2 = self.siguiente_token()
        if token1 in ('*', '/', '+', '-') and token2 in ('*', '/', '+', '-'):
            raise SyntaxError("Error de sintaxis: dos operadores consecutivos")
        self.retroceder()
        self.retroceder()

    def termino(self):
        resultado = self.factor()
        token = self.siguiente_token()
        while token in ('*', '/'):
            self.verificar_operador_doble()
            operador = token
            valor = self.factor()
            if operador == '*':
                resultado *= valor
            elif operador == '/':
                if valor == 0:
                    raise ZeroDivisionError("División por cero")
                resultado /= valor
            token = self.siguiente_token()
        self.retroceder()
        return resultado

    def expresion(self):
        resultado = self.termino()
        token = self.siguiente_token()
        while token in ('+', '-'):
            self.verificar_operador_doble()
            operador = token
            valor = self.termino()
            if operador == '+':
                resultado += valor
            elif operador == '-':
                resultado -= valor
            token = self.siguiente_token()
        self.retroceder()
        return resultado

def leer_expresiones(nombre_archivo):
    expresiones = []
    with open(nombre_archivo, 'r') as archivo:
        for linea in archivo:
            expresiones.append(linea.strip())
    return expresiones

# Uso
expresiones = leer_expresiones("gramatica.txt")

# Analizar expresiones
for expresion_str in expresiones:
    try:
        analizador = AnalizadorSintactico(expresion_str)
        resultado = analizador.expresion()
        print(f"Expresión: {expresion_str} -> Aceptada (Resultado: {resultado})")
    except SyntaxError as e:
        print(f"Expresión: {expresion_str} -> No aceptada ({e})")
