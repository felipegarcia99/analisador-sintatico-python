import os
from ALexico_Final2 import *

tokens = main()

def is_number_tryexcept(s):
    """ Returns True is string is a number. """
    try:
        float(s)
        return True
    except ValueError:
        return False

def passos(cont, tipo):
	# print('passo {}: {}'.format(cont, tipo))
	return 'passo {}: {}'.format(cont, tipo)


tok = 0
tipo = 1
pos = 2
tipo_var = ['int', 'string', 'char', 'float', 'double', 'bool']


def sintatico():
    '''
    for i in tokens:
        print(i)
    print('================================')
    '''
    # Pré-processamento: verificar int main(){}
    if tokens[-1][0] != '}':  # Se não houver } no final nem continua o programa
        print('Erro: falta de } na função principal')
        return 0
    else:
        tokens.pop(-1)

    cabecalho = []  # Listando até onde vai o {
    for i in tokens:
        if i[0] == '{':
            cabecalho.append(i)
            break
        else:
            cabecalho.append(i)
    print(cabecalho)

    for i in range(len(cabecalho)):  # Removendo da lista principal o int main
        tokens.pop(0)
    
    listtempcabec = []  # Verificação se o cabecalho da funcao está certo
    for i in cabecalho:
        listtempcabec.append(i[0])
        print(i[0])
    if listtempcabec != ['int', 'main', '(', ')', '{']:
        print('Erro: cabeçalho da funcao incorreto')
    # ===================================================

    # Loop principal
    ncomandos = 1
    resultados_print = []
    comando = []
    ja_foi_mexida = False

    ativa_cochete = False
    while True:
        if len(tokens) == 0:
            break
        comando = []
        for i in tokens:
            if not ativa_cochete:
                if i[0] == ';':
                    comando.append(i)
                    break
                elif i[0] == '{':
                    comando.append(i)
                    ativa_cochete = True
                else:
                    comando.append(i)
            else:
                if i[0] == '}':
                    comando.append(i)
                    ativa_cochete = False
                    break
                else:
                    comando.append(i)

        print(comando)
        # Análise
        # Declaração de variáveis
        cont = 0
        if comando[cont][tok] in tipo_var:
        	resultados_print.append('={}º COMANDO___:DECLARAÇÃO DE VARIÁVEIS'.format(ncomandos))
        	resultados_print.append(passos(cont, classes[comando[cont][tipo]]))
        	cont += 1
        	while True:
        		if (comando[cont][tipo] == 0) and (comando[cont+1][tipo] != 5): # ID
        			resultados_print.append(passos(cont, classes[comando[cont][tipo]]))
        			cont += 1
        			if comando[cont][tipo] == 4: # Virgula
        				resultados_print.append(passos(cont, classes[comando[cont][tipo]]))
        				cont += 1
        				pass # Tem que continuar...
        		elif (comando[cont][tipo] == 0) and (comando[cont+1][tipo] == 5):
        			resultados_print.append(passos(cont, classes[comando[cont][tipo]]))
        			resultados_print.append(passos(cont+1, classes[comando[cont+1][tipo]]))
        			ja_foi_mexida = True
        			break
        cont = 0
        # Atribuição
        if not ja_foi_mexida:
        	if len(resultados_print) > 0:
        		resultados_print = []

	        if comando[cont][tipo] == 0:  # ID
	        	resultados_print.append('={}º COMANDO___:ATRIBUIÇÃO'.format(ncomandos))
	        	resultados_print.append(passos(cont, classes[comando[cont][tipo]]))
	        	cont += 1
	        	if comando[cont][0] == atribuicao[0]:
	        		resultados_print.append(passos(cont, classes[comando[cont][tipo]]))
	        		cont += 1
	        		if (comando[cont][tipo] == 0) or ((comando[cont][tok].isdigit()) or (is_number_tryexcept(comando[cont][tok]))):
	        			resultados_print.append(passos(cont, classes[comando[cont][tipo]]))
	        			cont += 1
	        			while True:
	        				if comando[cont][tipo] == 6: # op_arit
	        					resultados_print.append(passos(cont, classes[comando[cont][tipo]]))
	        					cont += 1
	        					if comando[cont][tipo] == 0:
	        						resultados_print.append(passos(cont, classes[comando[cont][tipo]]))
	        						cont += 1
	        						if comando[cont][tipo] == 5: # fim
	        							resultados_print.append(passos(cont, classes[comando[cont][tipo]]))
	        							print('fim {} comando'.format(ncomandos))
	        							ja_foi_mexida = True
	        							break
	        						else:
	        							pass # continua...
	        				elif comando[cont][tipo] == 5: # fim
	        					resultados_print.append(passos(cont, classes[comando[cont][tipo]]))
	        					print('fim {} comando'.format(ncomandos))
	        					ja_foi_mexida = True
	        					break
        # Cout
        cont = 0
        if not ja_foi_mexida:
            if comando[cont][tok] == 'cout':
                resultados_print.append('={}º COMANDO___:COUT'.format(ncomandos))
                resultados_print.append(passos(cont, classes[comando[cont][tipo]]))
                cont += 1
                if comando[cont][tok] == '<<':
                    resultados_print.append(passos(cont, classes[comando[cont][tipo]]))
                    cont += 1
                    if comando[cont][tipo] == 10: # String
                        resultados_print.append(passos(cont, classes[comando[cont][tipo]]))
                        cont += 1
                        if comando[cont][tipo] == 5: # fim
                            resultados_print.append(passos(cont, classes[comando[cont][tipo]]))
                            ja_foi_mexida = True
       	# Cin
        cont = 0
        if not ja_foi_mexida:
            if comando[cont][tok] == 'cin':
                resultados_print.append('={}º COMANDO___:CIN'.format(ncomandos))
                resultados_print.append(passos(cont, classes[comando[cont][tipo]]))
                cont += 1
                if comando[cont][tok] == '>>':
                    resultados_print.append(passos(cont, classes[comando[cont][tipo]]))
                    cont += 1
                    if comando[cont][tipo] == 0: # ID
                        resultados_print.append(passos(cont, classes[comando[cont][tipo]]))
                        cont += 1
                        if comando[cont][tipo] == 5: # fim
                            resultados_print.append(passos(cont, classes[comando[cont][tipo]]))
                            # cont += 1
                            ja_foi_mexida = True
       	# if-else
        cont = 0
       	if not ja_foi_mexida:
            if comando[cont][tok] == 'if':
                resultados_print.append('={}º COMANDO___:IF-ELSE'.format(ncomandos))
                resultados_print.append(passos(cont, classes[comando[cont][tipo]]))
                cont += 1
                if comando[cont][tok] == '(':
                    resultados_print.append(passos(cont, classes[comando[cont][tipo]]))
                    cont += 1
                    # while True: # expr
                    if comando[cont][tipo] == 0:
                        resultados_print.append(passos(cont, classes[comando[cont][tipo]]))
                        cont += 1
                        if comando[cont][tipo] == 7:
                            resultados_print.append(passos(cont, classes[comando[cont][tipo]]))
                            cont += 1
                            if ((comando[cont][tipo] == 0) or (comando[cont][tipo] == 1) or (comando[cont][tipo] == 2) or (comando[cont][tipo] == 10) or (comando[cont][tipo] == 11)):
                                resultados_print.append(passos(cont, classes[comando[cont][tipo]]))
                                cont += 1
                                if comando[cont][tok] == ')':
                                    if comando[cont][tok] == '{':
                                        while True: # cmd
                                            pass
                                    if comando[cont][tok] == '}':
                                        end

       	# Printando os resultados
       	for i in resultados_print:
       		print(i)

       	resultados_print = []
        for i in range(len(comando)):
            tokens.pop(0)

       	ncomandos += 1
       	ja_foi_mexida = False
        print('================================')
        #break

if __name__ == '__main__':
    sintatico()
    os.system('pause')