# Variáveis
pal_reservadas = ['continue', 'double', 'float', 'if', 'switch', 'char', 'default', 'else', 'main', 'for', 'void',
                  'break', 'int', 'return', 'case', 'const', 'do', 'long', 'while', 'cout', 'cin', 'std', 'endl']
classes = {0: 'ID', 1: 'INT', 2: 'REAL', 3: 'WORD_RESERV', 4: 'VIRGULA(SEPARADOR)', 5: 'PONTO_VIRGULA(FIM_SENT)',
           6: 'OP_ARITM', 7: 'COMPARADOR', 8: 'AGRUPADOR', 9: 'SÍMBOLO', 10: 'STRING', 11: 'CHAR', 12: 'ATRIB'}

simbolos = [':', '!', '#', '%', '&']
atribuicao = ['=', '<<', '>>']
fim_sent = ';'
separador = ','
op_aritm = ['+', '-', '*', '/']
comparadores = ['<', '<=', '>', '>=', '==', '!=']
agrupadores = ['(', ')', '{', '}', '[', ']']

total_simbolos = simbolos + atribuicao + op_aritm + comparadores + agrupadores
total_simbolos.append(fim_sent)
total_simbolos.append(separador)
# print(total_simbolos)
# ===================================================

# Programa
def main():
    tokens = []
    prog_new = ''
    prog = '''
    int main(){
     double num1, num2, res;
     char cond;
     b = 3;
     a = 2.2;
     
     cout<<"digite o primeiro número";
     cin>>num1;
     cout<<"digite a operação desejada";
     cin>>cond;
     cout<<"digite o segundo número";
     cin>>num2;
     if(cond == '+'){
         res=num1+num2;   
        }
         if(cond == '-'){
         res=num1-num2;   
        }
         if(cond == '/'){
         res=num1/num2;   
        }
         if(cond == '*'){
         res=num1*num2;   
        }
        cout<<"o resultado é:"<<res;
        }

    '''
    # ===================================================


    strtemp = ''
    # Pré-processamento: Espaço antes e depois de símbolos, para facilitar o processamento
    for i in range(len(prog)):
        if prog[i] in total_simbolos:
            if prog[i] == '<' or prog[i] == '>':
                if prog[i + 1] == '<' or prog[i + 1] == '>':
                    strtemp += ' ' + prog[i] + prog[i + 1] + ' '
            elif prog[i] == '=':
                if prog[i + 1] == '=':
                    strtemp += ' ' + prog[i] + prog[i + 1] + ' '
                elif prog[i + 1] != '=':
                    # strtemp += ' ' + prog[i] + ' '
                    if prog[i - 1] == '=': # Já passou
                        strtemp += ' '
                    else:
                        strtemp += ' ' + prog[i] + ' '
            else:
                strtemp += ' ' + prog[i] + ' '
        else:
            strtemp += prog[i]
    prog = strtemp
    # print(prog)
    # ===================================================

    # Pré-processamento: Filtro p/ tirar \t
    for i in prog:
        if i != '\t':
            prog_new += i

    # print(prog_new)
    # ===================================================

    # Pré-processamento: Separando as linhas
    b = prog_new.split('\n')
    b = b[1:-1]  # Separando apenas as linhas
    # print(b)

    linhas = {i: b[i] for i in range(0, len(b))}  # Colocando as linhas em um dict
    # print(linhas)
    # ===================================================

    lexema_temp = ''
    estado_string = False
    get_col = True
    col = 0
    # Analisador
    for i in linhas:
        a = linhas[i]
        # print(a)
        for j in range(len(a)):
            if a[j] == '"':
                estado_string = not estado_string
            if not estado_string:
                if a[j] != ' ':
                    if get_col:
                        col = j
                        get_col = False
                    if type(a[j]) == str:
                        lexema_temp += a[j]
                else:  # Espaço
                    if lexema_temp != '':
                        # print("Else: ", lexema_temp)
                        temp_id = lexema_temp[0]
                        if lexema_temp in pal_reservadas:  # Palavra reservada
                            tokens.append([lexema_temp, 3, (i, col)])
                            lexema_temp = ''

                        elif lexema_temp[0].isalpha():  # Se o 1º caractere for letra
                            validacao = None
                            for temp in lexema_temp:
                                if (temp.isdigit() == True) or (temp.isalpha() == True):
                                    validacao = True
                                else:
                                    validacao = False
                            if validacao == True:
                                tokens.append([lexema_temp, 0, (i, col)])
                                lexema_temp = ''

                        elif lexema_temp[0].isdigit():  # INT
                            validacao = 'INT'
                            for temp in lexema_temp:
                                if temp == '.':
                                    validacao = 'REAL'
                                elif not temp.isdigit():
                                    validacao = False
                            if validacao == 'INT':
                                tokens.append([lexema_temp, 1, (i, col)])
                                lexema_temp = ''
                            elif validacao == 'REAL':
                                tokens.append([lexema_temp, 2, (i, col)])
                                lexema_temp = ''

                        elif lexema_temp in atribuicao:  # =, <<, >>
                            tokens.append([lexema_temp, 12, (i, col)])
                            lexema_temp = ''

                        elif lexema_temp == fim_sent:  # Ponto e vírgula
                            tokens.append([lexema_temp, 5, (i, col)])
                            lexema_temp = ''

                        elif lexema_temp == separador:  # Vírgula
                            tokens.append([lexema_temp, 4, (i, col)])
                            lexema_temp = ''

                        elif lexema_temp in op_aritm:  # Operadores aritméticos
                            tokens.append([lexema_temp, 6, (i, col)])
                            lexema_temp = ''

                        elif lexema_temp in comparadores:  # Comparador
                            tokens.append([lexema_temp, 7, (i, col)])
                            lexema_temp = ''

                        elif lexema_temp in agrupadores:  # Agrupador
                            tokens.append([lexema_temp, 8, (i, col)])
                            lexema_temp = ''

                        elif lexema_temp in simbolos:  # Símbolo
                            tokens.append([lexema_temp, 9, (i, col)])
                            lexema_temp = ''

                        elif lexema_temp[0] == '"':  # String
                            # Deveria passar um for aqui?
                            if lexema_temp[-1] == '"':
                                tokens.append([lexema_temp, 10, (i, col)])
                                lexema_temp = ''

                        elif lexema_temp[0] == '\'':  # Char
                            if len(lexema_temp) == 3 and lexema_temp[2] == '\'':
                                tokens.append([lexema_temp, 11, (i, col)])
                                lexema_temp = ''
                    get_col = True
            else:
                if get_col:
                    col = j
                    get_col = False
                if type(a[j]) == str:
                    lexema_temp += a[j]

    print('\n')

    # Print tokens
    # for i in tokens:
        # print(i)
    
    list_return = []
    # Return tokens
    for i in tokens:
        list_return.append(i)
    
    return list_return


if __name__ == '__main__':
    main()
