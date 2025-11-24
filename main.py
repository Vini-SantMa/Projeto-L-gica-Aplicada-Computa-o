import analisador_logico
import converter_fnc_fnd
import sat_solver

def main():
    print(" ------------------------------------")
    print( " Mini Projeto Ab2.2 Logica Aplicada à Computação")
    print(" Este código suporta as váriaveis: P Q R S T U.\n Os operadores são: ~ ; ^ ; v ; -> ; <-> .")

    while True:
        print("\n Selecione uma opção:\n 1 - Verificar Equivalencia entre duas sentenças\n 2 - Converter pra Forma Normal Conjuntiva.\n 3 Converter para Forma Normal Disjuntiva.\n 4 - Sat Solver.\n 0 - Sair.")
        opcao = input("Digite sua escolha: ").strip()
        if opcao == '0':
            print("finalizado")
            break
        elif opcao =='1':
            sentenca1 = input("\nDigite a primeira sentença:")
            sentenca2 = input("\nDigite a segunda sentença:")
            
            infos1 = analisador_logico.calcular_tabverdade(sentenca1)
            infos2 = analisador_logico.calcular_tabverdade(sentenca2)

            if infos1['variaveis'] != infos2['variaveis']:
                print("Escreva sentencas que usam as mesmas variaveis")
            else:
                if infos1['resultados_finais'] == infos2['resultados_finais']:
                    print("\n Sentenças Equivalentes")
                else:
                    print("\n Sentenças não equivalentes")
        elif opcao == '2':
            sent = input("\n Digite a sentença para -> Forma Normal Conjuntiva: ")
            try:
                resultado = converter_fnc_fnd.gerar_fnc(sent)
                print(f"\n Sua sentença em FNC: {resultado}")
            except Exception as e:
                print(f"Erro na conversao:")
        
        elif opcao == '3':
            sent = input("\nDigite sua sentença para -> Forma Normal Disjuntiva: ")
            try:
                resultado = converter_fnc_fnd.gerar_fnd(sent)
                print(f"\n Sua sentença em FND: {resultado}")
            except Exception as e:
                print(f"Erro na conversao")
        
        elif opcao == '4':
            sent = input("\nDigite sua sentença para usar o Sat solver:")
            print("\n O algoritmo ira transformá-la para a FNC e resolver.")
            try:
                elementos_conversao =  converter_fnc_fnd.deixar_modo_sat(sent)
                clausulas_nums = elementos_conversao[0]
                variaveis = elementos_conversao[1]
                if not clausulas_nums and "v" not in sent and "^" not in sent and "->" not in sent: 
                     print("Talvez sua sentença esteja incompleta")
                     continue
                
                resolv = sat_solver.Satsolv(len(variaveis), clausulas_nums)
                elementos_resposta = resolv.resolucao()
                atribuicao = elementos_resposta[0]
                resultadoo = elementos_resposta[1]

                if atribuicao:
                    print("\n SAT")
                    print(f"\n {resultadoo}")
                    interpret = []
                    for valor in resultadoo:
                        indice = abs(valor) - 1
                        nome_da_var = variaveis[indice]
                        if valor > 0:
                            estado = "V"
                        else:
                            estado = "F"
                        interpret.append(f"{nome_da_var} = {estado}")
                    
                    print(f"solução: { ', '.join(interpret)}")
                else:
                    print("\n Unsat")
            except Exception as e:
                print("Algum problema ao executar o Sat solver")

if __name__ == "__main__":
    main()