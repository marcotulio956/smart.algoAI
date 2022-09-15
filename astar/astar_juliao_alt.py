# Prática 1 - Laboratório de Inteligência Artificial
# Julio Cesar Rocha & Marco Tulio
import csv;

# Função para transformar os dados do CSV em uma matriz.
def csvMatriz(arquivo):
    matriz = [];
    matriz_linha = [];
    resultado = [];

    with open(arquivo) as arq:
        leitor = csv.reader(arq, delimiter=',');
        for linha in leitor:
            matriz_linha.append(linha);
            
    for linha in matriz_linha:
        matriz_linha = [];
        for elemento in linha:
            if elemento == '0.': matriz_linha.append(0);
            else: matriz_linha.append(float(elemento));
        resultado.append(matriz_linha);
    return resultado;

# Função para obter a borda de um nó (estacao_atual).
def obterBorda(estacao_atual, matriz_custo):
    adjacentes = [];
    cont = 0;
    for linha in matriz_custo:
        index = 0;
        for elemento in linha:
            if (cont == (estacao_atual - 1) and elemento != 0):
                adjacentes.append(index + 1);
            index = index + 1;
        cont = cont + 1;
    return adjacentes;  

# Função para obter o valor f(n) da função (f(n) = h(n) + g(n)) para cada um dos nós adjacentes á estação atual
# e salvar esse valor em um vetor de custo.
def obterFuncao(matriz_heuristica, matriz_custo, adjacentes, estacao_atual, alvo, rota):
    funcao = [];
    alvo = alvo - 1;
    estacao_atual = estacao_atual - 1;
    for adjacente in adjacentes:
        adjacente = adjacente - 1;
        funcao.append(round(matriz_heuristica[adjacente][alvo] + matriz_custo[adjacente][estacao_atual] + custoRota(rota), 2));
    return funcao;

# Função para obter o proximo nó a ser escolhido. É escolhido o nó com menor custo f(n).
def obterProx(adjacentes, custo_adjacentes):
    menor_custo = custo_adjacentes[0];
    index_menor_custo = 0;
    index = 0;
    for elemento in custo_adjacentes:
        if(elemento < menor_custo):
            menor_custo = elemento;
            index_menor_custo = index;
        index = index + 1;
    return index_menor_custo;

# Função para dada ORIGEM, encontrar o melhor caminho até o DESTINO.
def melhorRota():    
    estacao_atual = origem;
        
    rota = [];
    visitados = [];
    borda = []; 
    custo_borda = [];
    
    rota.append(estacao_atual);
    visitados.append(estacao_atual);
    
    print("Calculando Rota...");    
    while estacao_atual != destino:   
        nova_borda = obterBorda(estacao_atual, matriz_custo);                      
        borda = borda + nova_borda          
        custo_borda += obterFuncao(matriz_heuristica, matriz_custo, nova_borda, estacao_atual, destino, rota);
        
        if len(visitados) > 0:
            for visitado in visitados:
                index_visita = 0;
                for elemento in borda:
                    index_visita = index_visita + 1;
                    if visitado == elemento:
                        del borda[index_visita - 1];
                        del custo_borda[index_visita - 1];
                        
        index_estacao = obterProx(borda, custo_borda);
        prox_estacao = borda[index_estacao];
        custo_prox_estacao = custo_borda[index_estacao];  
        
        print("\nRota atual: " + str(rota));
        print("Estação atual: E" + str(estacao_atual));
        print("Borda: " + str(borda));
        print("Custo por conexão: " + str(custo_borda));
        print("Proxima estação: E" + str(prox_estacao) + " (-----Destino-----)" if prox_estacao == destino else "Proxima estação: E" + str(prox_estacao));
        print("Custo proxima estação: " + str(custo_prox_estacao));
        print("Estações expandidas: " + str(visitados));
        
        # Se a proxima estação com menor custo não for adjacente da estação atual, então a rota é atualizada até a estação adjacente á proxima estação com menor custo >:)
        while prox_estacao not in obterBorda(estacao_atual, matriz_custo) or custo_prox_estacao not in obterFuncao(matriz_heuristica, matriz_custo, borda, estacao_atual, destino, rota):
            print("::::: E" + str(estacao_atual) + " não possui rota para " + "E" + str(prox_estacao) + " OU não é o adjacente com custo minímo.");
            print("::::: Atualizando Rota...");
            rota.remove(estacao_atual);
            estacao_atual = rota[len(rota) - 1];
            print("::::: Nova rota: " + str(rota));
        print("=========================================================");

        estacao_atual = prox_estacao;
        rota.append(prox_estacao);
        visitados.append(estacao_atual);
        del borda[index_estacao];
        del custo_borda[index_estacao]; 
        
        if(estacao_atual == destino):
            print("============= Você chegou ao seu destino :3 =============");
            print("=========================================================");
    return rota;

# Função para dada uma Rota, calcular o custo total de seu inicio até seu fim.
def custoRota(rota):
    custo = 0;
    if len(rota) > 1:
        for x in range(0, len(rota)):
            if rota[x] != rota[len(rota) - 1]:
                custo = custo + matriz_custo[rota[x+1] - 1][rota[x] - 1];
    return round(custo, 2);
  
origem = int(input("\nDigite o numero da estação ORIGEM: "));
destino = int(input("Digite o numero da estação DESTINO: "));

heuristica_csv = "heuristics.csv";
custo_csv = "real-distances.csv";
matriz_heuristica = csvMatriz(heuristica_csv);
matriz_custo = csvMatriz(custo_csv);

rota_escolhida = melhorRota();
custo_total = custoRota(rota_escolhida);

print("\nMelhor rota: " + str(rota_escolhida));
print("Custo total: " + str(custo_total) + "\n");