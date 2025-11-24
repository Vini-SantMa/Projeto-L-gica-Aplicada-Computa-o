def separar(expressao): #Le a expressao em um conjunto, listinha de simbolos que usamos nos exercicios.Pega a string e transforma em simbolos unicos, pra poder usar na analise depois
    simbolo = []
    i = 0  # i é o indice pra posiçao na string
    while i < len(expressao):
        if expressao[i] == ' ': # ignorar o espaço vazio e avançar 1 posiçao
            i += 1
            continue
        if expressao[i:i+3] == '<->': #aqui é pra começar tentando identificar os operadores grandes implica e biimplica
            simbolo.append('<->')
            i += 3  #pula 3 posições para passar do <->
            continue
        if expressao[i:i+2] == '->':
            simbolo.append('->')
            i += 2
            continue
        char = expressao[i] #agora é pra buscar os operadores mis simpoles
        if char in ('(', ')', '^', 'v', '~'):
            simbolo.append(char)
        elif char in ('P', 'Q', 'R', 'S', 'T', 'U'): # estabeleci 6 variaveis
            simbolo.append(char)
        else:
            print(f" Digite um simbolo permitid!")
            raise ValueError(f" Caractere inválido na posição {i}: {char}") #se digitar algo fora do esperado
        i += 1
    return simbolo

#Parte da analise sintatica: pega a sequencia de simbolos da funçao anterior e constroi um tipo de arvore de dados, pra gente poder ditar a hierarquia das operaçoes na sentença
def analise_expressao(simbolo): #aqui serve para pegar a lista de simbolos
    # Inicia a análise na posição 0 e começa vendo a parte do -> porque fica la no finzinho da prioridade, junto de <->
    arvore, pos = analise_implicacao(simbolo, 0) # aqui começa vendo a parte do ->, que vem no finzinho da prioridade, junto do <->
    if pos < len(simbolo): #pra saber se os simbolos todos foram vistos, e se tem algo irregular na sentença
        raise SyntaxError(f"simbolo não esperados no final da expressão: {simbolo[pos:]}")
    return arvore

def analise_atom(simbolo, pos): # Analisando a parte mais elementar, as variaveis atomicas e parenteses
    token = simbolo[pos] if pos < len(simbolo) else None #considerando o simbolo da posiçao que está e o verificador pra os maiores
    if not token:
        raise SyntaxError(" Expressão vazia ou insuficiente.")
    # Se o token for uma variável atômica, ele é a nossa folha da árvore.
    if token in ('P', 'Q', 'R', 'S', 'T', 'U'): #se o token for uma variavel, ela é um nó sem filho, ai joga pra arvore
        return (token, pos + 1)
    elif token == '(': # se for (, a funçao vai analisar o que ta dentro, ou seja, uma expressao filha do todo
        # analisa a expressão interna de forma recursiva, com a funcao do inicio e depois procura o ) pra fechar
        pos += 1
        expr, pos = analise_implicacao(simbolo, pos)
        if simbolo[pos] != ')':
            raise SyntaxError("Faltou fechar com o ).")
        pos += 1
        return (expr, pos) #retornando tanto a expressao que foi analisada, quanto a posiçao que parou
    else:
        raise SyntaxError(f" simbolo inválido para uma fórmula atômica: {token}")

def analise_negacao(simbolo, pos): # pra analisar o not. começa checando o simbolo se é not
    if simbolo[pos] == '~':
        # consome o '~' e chama a si mesma, porque pode ter dupla negação
        operand, new_pos = analise_negacao(simbolo, pos + 1)
        # Retorna o conjunto (operador, operando) e a nova posição.
        return (('~', operand), new_pos)
    else:
        # Se não houver negação, passa para a proxima prioridade.
        return analise_atom(simbolo, pos)

def analise_conjuncao(simbolo, pos):
    esquerdo, pos = analise_negacao(simbolo, pos) #pegar o que esta na esquerdad operaçao
    while pos < len(simbolo) and simbolo[pos] in ('^', 'v'): #enquanto tiver os ^ e v, ela vaianalisando
        operador = simbolo[pos]
        pos += 1
        direito, pos = analise_negacao(simbolo, pos)#faz o mesmo, mas na direita.
        esquerdo = (operador, esquerdo, direito) # junto os dois, criando uma estrutura tipo p ^ q vira: ^ p q

    return (esquerdo, pos) #retorna tudo, no formato da estrutura operador, lado esquerdo e lado direito, ai joga pra proxima parte

def analise_implicacao(simbolo, pos): #analisar as -> e <->
    # Pega o operando da esquerda do próximo nível de precedência.
    esquerdo, pos = analise_conjuncao(simbolo, pos)

    if pos < len(simbolo) and simbolo[pos] in ('->', '<->'): # Checa se há um operador de implicação ou biimplicação.
        operador = simbolo[pos]
        pos += 1
        direito, pos = analise_implicacao(simbolo, pos)#chamando si mesma, pra garantir que tudo seja interpretado corretamente

        return ((operador, esquerdo, direito), pos) #retorna a estrutura operador, esquerda, direita e posicao
    return (esquerdo, pos) #se nao tem -> ou <->, volta como tava

def encontrar_variaveis(arvore): #Achar as variaveis da estrutura sintatica cosntruida
    variaveis = set()
    def percorrer(no):
        if isinstance(no, str) and no in ('P', 'Q', 'R', 'S', 'T', 'U'): #se fpr string, o no é varivavel, o instance serve pra comparar o no com a classe string
            variaveis.add(no)
        # percorrer seus filhos recursivamente.
        elif isinstance(no, tuple): #se  for um conjuntinho (tupla), ai vai ser operador, tipo ->. Ai vai olhando dentro dessa tupla
            for filho in no:
                percorrer(filho)
    percorrer(arvore)
    return sorted(list(variaveis)) #aqui traz uma lista na ordem, com as variaveis, pra fazer as tabelas

def gerar_combinacoes(num_variaveis):
    combinacoes = [] #aqui vai fazer as combinações com as 6 possiveis variaveis
    valores = [True, False]

    if num_variaveis == 1:
        for v1 in valores:
            combinacoes.append((v1,))
    elif num_variaveis == 2:
        for v1 in valores:
            for v2 in valores:
                combinacoes.append((v1, v2))
    elif num_variaveis == 3:
        for v1 in valores:
            for v2 in valores:
                for v3 in valores:
                    combinacoes.append((v1, v2, v3))
    elif num_variaveis == 4:
        for v1 in valores:
            for v2 in valores:
                for v3 in valores:
                    for v4 in valores:
                        combinacoes.append((v1, v2, v3, v4))
    elif num_variaveis == 5:
        for v1 in valores:
            for v2 in valores:
                for v3 in valores:
                    for v4 in valores:
                        for v5 in valores:
                            combinacoes.append((v1, v2, v3, v4, v5))
    elif num_variaveis == 6:
        for v1 in valores:
            for v2 in valores:
                for v3 in valores:
                    for v4 in valores:
                        for v5 in valores:
                            for v6 in valores:
                                combinacoes.append((v1, v2, v3, v4, v5, v6))
    return combinacoes

def avaliar_expressao(arvore, valores_variaveis): #vai pegar aquela estrutura das expressoes, ai pega as
#combinações da tabela e dá o resultado pra expressao com as combinações possiveis

    if isinstance(arvore, str): #se for so uma variavel, ai nao tem o que fzer
        return valores_variaveis[arvore]

    operador = arvore[0]
    if operador == '~':
        operand = arvore[1] #chamou exatamente quem vem depois do ~ e retornou o not dele
        return not avaliar_expressao(operand, valores_variaveis)
    # Para lidar com os operadores, ai avalia os dois lados da sentença
    operando_esquerda = arvore[1]
    operando_direita = arvore[2]

    valor_esquerda = avaliar_expressao(operando_esquerda, valores_variaveis)
    valor_direita = avaliar_expressao(operando_direita, valores_variaveis)
# depois de avaliar os dois lados, ai vai ver qual operador está presente
    if operador == '^':
        return valor_esquerda and valor_direita
    elif operador == 'v':
        return valor_esquerda or valor_direita
    elif operador == '->':
        # usando a tabela de equivalencia: p -> q = ~p v q
        return (not valor_esquerda) or valor_direita
    elif operador == '<->':
        # p <-> q  se  p == q.
        return valor_esquerda == valor_direita

    raise ValueError(f" simbolo de operação desconhecido: {operador}")

def calcular_tabverdade(expressao):
    try:
        simbolos = separar(expressao)
        arvore_sintatica = analise_expressao(simbolos)
        variaveis = encontrar_variaveis(arvore_sintatica)
        combinacoes = gerar_combinacoes(len(variaveis))

        resultados_finais = []
        for combinacao in combinacoes:
            valores_mapa = {}
            for k in range(len(variaveis)):
                valores_mapa[variaveis[k]] = combinacao[k]
            resultado = avaliar_expressao(arvore_sintatica, valores_mapa)
            resultados_finais.append(resultado)

        return {
            "variaveis": variaveis,
            "combinacoes": combinacoes,
            "resultados_finais": resultados_finais
        }
    except (ValueError, SyntaxError) as e:
        print(f" Erro na expressão: {e}")
        return None