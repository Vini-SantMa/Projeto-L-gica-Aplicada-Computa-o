# Projeto-Logica-Aplicada-a-Computacao

@Vinicius_Santana_Martins
@Jorge_Guilherme_da_Silva

Este projeto foi desenvolvido como requisito para a AB2.2, apresentado à disciplina de Lógica Aplicada à Computação 2025.2, no curso de Engenharia da Computação.

O algoritmo é capaz de analisar sentenças lógicas, convertê-las para formas normais e verificar a satisfatibilidade.

## Funcões
O código atende às demandas especificadas na descrição da atividade:

1.  **Verificação de Equivalência:** Recebe duas sentenças, levanta a tabela verdade, as compara e verifica se são equivalentes.
2.  **Conversão para FNC:** Transforma a sentença lógica digitada pelo usuário para a **Forma Normal Conjuntiva**.
3.  **Conversão para FND:** Transforma a sentença lógica digitada pelo usuário para a **Forma Normal Disjuntiva**.
4.  **SAT Solver:** Algoritmo que verifica se uma sentença é Sat ou Unsat por meio de testes consecutivos e recursivos (lógica Back-Tracking). Ao decidir que a sentença é Sat, retorna as atribuições das váriaveis, na combinação que torna a sentença Satisfazivel

##  Tecnologias Utilizadas

* **Linguagem:** Python 3
* **Software:** Google Colab (para "hospedagem" e testes do trabalho)

## Organização do Projeto

* `main.py`: Arquivo principal contendo o menu para interação com usuário e a integração dos demais arquivos.
* `analisador_logico.py`: Arquivo responsável por separar em tokens a expressão e desenvolver a tabela verdade.
* `converter_fnc_fnd.py`: Arquivo com as funções que: aplica as regras para gerar FNC e FND, além de gerar um FNC no formato com números (DIMACS) necessário para funcionamento do Sat Solver.
* `sat_solver.py`: Implementação do código Sat Solver, tomando como base um algoritmo desenvolvido em outro trabalho (em linguagem C).

## Observações e Comentários

* O arquivo `analisador_logico.py` é reaproveitado de um trabalho anterior, apresentado à mesma disciplina. As funções desenvolvidas anteriormente são mantidas e utilizadas novamente, com minímas alterações.
  
* O arquivo `sat_solver.py` trata-se de uma adaptação do código desenvolvido e apresentado à disciplina de Estrutura de Dados. Nesse contexto, o código original (em C) foi "traduzido" para a linguagem Python, mantendo toda a lógica principal inalterada, apenas com pequenas adaptações necessárias para integração com os demais arquivos do projeto.
