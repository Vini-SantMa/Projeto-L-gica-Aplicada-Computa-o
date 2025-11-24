from analisador_logico import calcular_tabverdade
""" 
Uma forma de gerarmos as formas normais conjuntiva e disjuntiva das sentencas é por meio da tabela verdade dessas
sentenças logicas. 
O processo para a normal conjuntiva é:
Faz a tabela verdade da sentença
Em todas as linhas que for false, construimos uma "clausula" com disjuncao entre si
  |
  |---> Cada literal com interpretacao True, entra na clausula negado. ou seja: p se torna ~p
  |---> Cada literal com interpretacao False, entra na clausula como true. ou seja: ~p sew torna p
   ----> Depois junta as clausulas por meio de ^

   Por exemplo:  q <-> ~p
   na tabela fica: 
      | p | q | q <-> ~p |
      | v | v |     f    | -> (~p V ~q)
      | v | f |     v    |
      | f | v |     v    |
      | f | f |     f    | -> (p v q)     Agora junta: (~p V ~q) ^ (p v q)  

      Para a forma disjuntiva, é semelhante, mas vamos analisar as linhas que for true 
      e criar as clausulas com conjuncao ^ 
      Onde o literal for true,  ele entra na clausula como true
      Onde o literal for false, ele entra na clausula como negado. Depois junt as clausulas com v   
"""
def gerar_fnc(expressao):
    info = calcular_tabverdade(expressao) #pegar a tabela verdade toda
    literais = info["variaveis"] # Aqui guarda o ['P', 'Q', 'R']
    combinacoes = info["combinacoes"] # Aqui guarda as interpretacoes [(V,V), (V,F)....]
    results = info["resultados_finais"] # Aqui guarda os results da tab [ V, F, V, V, F ..]

    clausulas = []
    for i in range(len(results)):
        if results[i] == False:
            parte_da_claus = []

            for j in range(len(literais)):# ir percorrendo as variaveis daquela linha
                var_nome = literais[j]
                valor_linha = combinacoes[i][j]
                
                if valor_linha == True:
                    parte_da_claus.append(f"~{var_nome}") #Na fnc, se era V fica negado
                else:
                    parte_da_claus.append(var_nome) # se era f, so adiciona o literal mesmo, a variavel, sem negacao

            clausula_escrita = "("+ "v".join(parte_da_claus) + ")"
            clausulas.append(clausula_escrita)
    
    fnc_retorno  = " ^ ".join(clausulas)
    return fnc_retorno

def gerar_fnd(expressao):
    info = calcular_tabverdade(expressao)
    literais = info["variaveis"] # Aqui guarda o ['P', 'Q', 'R']
    combinacoes = info["combinacoes"] # Aqui guarda as interpretacoes [(V,V), (V,F)....]
    results = info["resultados_finais"] # Aqui guarda os results da tab [ V, F, V, V, F ..]

    clausulas = []
    for i in range(len(results)):
        if results[i] == True:
            parte_da_claus = []

            for j in range(len(literais)):# ir percorrendo as variaveis daquela linha
                var_nome = literais[j]
                valor_linha = combinacoes[i][j]
                if valor_linha == True:
                    parte_da_claus.append(var_nome)
                else:
                    parte_da_claus.append(f"~{var_nome}")
            
            clausula_escrita = "(" + " ^ ".join(parte_da_claus) + ")"
            clausulas.append(clausula_escrita)
    
    if not clausulas:
        return "Contradicao"
    fnd_retorno = " v ".join(clausulas)
    return fnd_retorno

def deixar_modo_sat(expressao): #fazer o mesmo do fnc, mas em numeros, pra funcionar no sat
    
    info = calcular_tabverdade(expressao)

    literais = info["variaveis"]
    combinacoes = info["combinacoes"]
    results = info["resultados_finais"]

    clausulas_numericas = [] # Aqui vai ser [[1, -2], [-1, 2]]
    
    for i in range(len(results)):
        if results[i] == False:
            clausula_atual = []
            for j in range(len(literais)):
                valor_linha = combinacoes[i][j]
                indice = j + 1 # Porque nosso sat trabalha com os indices em 1, 2, 3
                if valor_linha == True: #Regra fnc
                    clausula_atual.append(-indice) # -> negativo
                else:
                    clausula_atual.append(indice)  # -> positivo
            
            clausulas_numericas.append(clausula_atual)
            
    return clausulas_numericas, literais
