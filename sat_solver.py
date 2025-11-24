class Satsolv:
    # Adaptando o codigo do sat de estrutura de dados para o python
    # A logica é exatamente a mesma, mesmo funcionamento

    def __init__(self, num_variaveis, clausulas):
        self.num_variaveis = num_variaveis 
        self.formula = clausulas

        # No original, tinha o valor_da_variavel, que era a variavel de atribuicoes
        # aqwui, teremos uma lista e preenche com zeros e adiciona + 1 o tamanho, igual o original
        self.valor_da_variavel = [0] * (num_variaveis + 1)

    def analisar_formula(self):
        #mesma logica, analisar se com as atribuicoes atuais, as clausulas sao todas true
        for clausula in self.formula:
            clausula_true = False

            for literal in clausula:
                variavel = abs(literal)
                
                valor_atual = self.valor_da_variavel[variavel]
                if((literal > 0 and valor_atual == 1) or (literal < 0 and valor_atual == -1)):
                    clausula_true = True
                    break # mesma logica do C, se achou um literal true, toda a clausula ja esta true
                
            if clausula_true == False:
                return False
        
        return True # se passou todas e nao entrou no false, entao é satisfazivel, é true

    def buscar_solucao(self, nivel_variavel):

        if nivel_variavel > self.num_variaveis:
            if self.analisar_formula():
                return True
            else:
                return False
        
        self.valor_da_variavel[nivel_variavel] = 1
        if self.buscar_solucao(nivel_variavel + 1):
            return True 
        
        self.valor_da_variavel[nivel_variavel] = -1
        if self.buscar_solucao(nivel_variavel + 1):
            return True

        self.valor_da_variavel[nivel_variavel] = 0
        return False
    
    def resolucao(self):

        satisf = self.buscar_solucao(1)

        if satisf:
            resultado_sat = []
            for i in range(1, self.num_variaveis + 1):
                if self.valor_da_variavel[i] == 1:
                    valor = i
                else:
                    valor = -i
                
                resultado_sat.append(valor)
            

            return True, resultado_sat
        else:
            return False, []
