# -*- coding: utf-8 -*-
"""
aco_tsp.py
==========

Implementação do algoritmo de Otimização por Colônia de Formigas (Ant Colony
Optimization - ACO) aplicado ao Problema do Caixeiro Viajante (Traveling
Salesman Problem - TSP).

O problema é lido a partir de um arquivo .csv com o formato:

    Cidade;X;Y
    A;10;20
    B;30;15
    ...

Cada linha representa uma cidade com suas coordenadas cartesianas
(X, Y). O objetivo do algoritmo é encontrar a rota de menor distância total
que visita todas as cidades exatamente uma vez e retorna à cidade de origem.
"""

from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import List, Tuple, Optional, Callable

import numpy as np
import pandas as pd


# --------------------------------------------------------------------------- #
# 1. Leitura e preparação dos dados
# --------------------------------------------------------------------------- #

def carregar_cidades(caminho_csv: str, sep: str = ";") -> pd.DataFrame:
    """
    Carrega o arquivo .csv contendo as cidades e suas coordenadas.

    Parameters
    ----------
    caminho_csv : str
        Caminho para o arquivo .csv com colunas "Cidade;X;Y".
    sep : str
        Separador usado no .csv (padrão ";").

    Returns
    -------
    pd.DataFrame
        DataFrame com as colunas ["Cidade", "X", "Y"].
    """
    df = pd.read_csv(caminho_csv, sep=sep, encoding="utf-8-sig")
    colunas_esperadas = {"Cidade", "X", "Y"}
    if not colunas_esperadas.issubset(set(df.columns)):
        raise ValueError(
            f"O arquivo deve conter as colunas {colunas_esperadas}, "
            f"mas contém {list(df.columns)}"
        )
    df["X"] = df["X"].astype(float)
    df["Y"] = df["Y"].astype(float)
    return df.reset_index(drop=True)


def matriz_distancias(df: pd.DataFrame) -> np.ndarray:
    """
    Calcula a matriz de distâncias euclidianas entre todas as cidades.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame com colunas ["Cidade", "X", "Y"].

    Returns
    -------
    np.ndarray
        Matriz NxN de distâncias euclidianas.
    """
    coords = df[["X", "Y"]].to_numpy()
    diff = coords[:, np.newaxis, :] - coords[np.newaxis, :, :]
    dist = np.sqrt(np.sum(diff ** 2, axis=-1))
    # Evita divisão por zero na diagonal (distância da cidade a ela mesma)
    np.fill_diagonal(dist, 0.0)
    return dist


# --------------------------------------------------------------------------- #
# 2. Estrutura para guardar o histórico de execução (útil para gráficos)
# --------------------------------------------------------------------------- #

@dataclass
class HistoricoACO:
    melhor_distancia_por_iteracao: List[float] = field(default_factory=list)
    distancia_media_por_iteracao: List[float] = field(default_factory=list)
    melhor_rota_global: Optional[List[int]] = None
    melhor_distancia_global: float = float("inf")


# --------------------------------------------------------------------------- #
# 3. Algoritmo ACO
# --------------------------------------------------------------------------- #

class AntColonyTSP:
    """
    Implementação do algoritmo Ant Colony Optimization (variante Ant System)
    para o Problema do Caixeiro Viajante.

    Parameters
    ----------
    distancias : np.ndarray
        Matriz NxN de distâncias entre as cidades.
    n_formigas : int
        Número de formigas utilizadas em cada iteração.
    n_iteracoes : int
        Número de iterações (gerações) do algoritmo.
    alpha : float
        Peso dado ao feromônio na regra de decisão (importância do feromônio).
    beta : float
        Peso dado à visibilidade/heurística 1/distância (importância da
        distância).
    taxa_evaporacao : float
        Taxa de evaporação do feromônio a cada iteração (entre 0 e 1).
    Q : float
        Constante usada para calcular quanto feromônio cada formiga deposita
        (geralmente proporcional a Q / distância_da_rota).
    feromonio_inicial : float
        Quantidade inicial de feromônio em todas as arestas.
    semente : Optional[int]
        Semente para reprodutibilidade dos resultados aleatórios.
    """

    def __init__(
        self,
        distancias: np.ndarray,
        n_formigas: int = 20,
        n_iteracoes: int = 100,
        alpha: float = 1.0,
        beta: float = 3.0,
        taxa_evaporacao: float = 0.5,
        Q: float = 100.0,
        feromonio_inicial: float = 1.0,
        semente: Optional[int] = None,
    ):
        self.distancias = distancias
        self.n_cidades = distancias.shape[0]
        self.n_formigas = n_formigas
        self.n_iteracoes = n_iteracoes
        self.alpha = alpha
        self.beta = beta
        self.taxa_evaporacao = taxa_evaporacao
        self.Q = Q

        if semente is not None:
            random.seed(semente)
            np.random.seed(semente)

        # Matriz de feromônio (mesma dimensão da matriz de distâncias)
        self.feromonio = np.full(
            (self.n_cidades, self.n_cidades), feromonio_inicial, dtype=float
        )

        # Visibilidade (heurística) = 1 / distância, evitando divisão por zero
        with np.errstate(divide="ignore"):
            self.visibilidade = np.where(
                self.distancias > 0, 1.0 / self.distancias, 0.0
            )

        self.historico = HistoricoACO()

    # ----------------------------------------------------------------- #
    # Construção de uma rota por uma única formiga
    # ----------------------------------------------------------------- #
    def _construir_rota(self, cidade_inicial: int) -> List[int]:
        rota = [cidade_inicial]
        visitadas = set(rota)

        for _ in range(self.n_cidades - 1):
            atual = rota[-1]
            proxima = self._escolher_proxima_cidade(atual, visitadas)
            rota.append(proxima)
            visitadas.add(proxima)

        return rota

    def _escolher_proxima_cidade(self, atual: int, visitadas: set) -> int:
        candidatas = [c for c in range(self.n_cidades) if c not in visitadas]

        feromonio = self.feromonio[atual, candidatas] ** self.alpha
        visibilidade = self.visibilidade[atual, candidatas] ** self.beta
        atratividade = feromonio * visibilidade

        soma = atratividade.sum()
        if soma == 0 or np.isnan(soma):
            # fallback: escolha uniforme caso todas as atratividades sejam 0
            probabilidades = np.full(len(candidatas), 1.0 / len(candidatas))
        else:
            probabilidades = atratividade / soma

        escolhida = np.random.choice(candidatas, p=probabilidades)
        return int(escolhida)

    # ----------------------------------------------------------------- #
    # Cálculo de distância total de uma rota (fechando o ciclo)
    # ----------------------------------------------------------------- #
    def distancia_rota(self, rota: List[int]) -> float:
        total = 0.0
        for i in range(len(rota)):
            origem = rota[i]
            destino = rota[(i + 1) % len(rota)]
            total += self.distancias[origem, destino]
        return total

    # ----------------------------------------------------------------- #
    # Atualização de feromônio
    # ----------------------------------------------------------------- #
    def _atualizar_feromonio(self, rotas: List[List[int]], distancias_rotas: List[float]):
        # Evaporação
        self.feromonio *= (1.0 - self.taxa_evaporacao)

        # Depósito de feromônio proporcional à qualidade da rota
        for rota, dist in zip(rotas, distancias_rotas):
            deposito = self.Q / dist if dist > 0 else 0.0
            for i in range(len(rota)):
                origem = rota[i]
                destino = rota[(i + 1) % len(rota)]
                self.feromonio[origem, destino] += deposito
                self.feromonio[destino, origem] += deposito  # simétrico

    # ----------------------------------------------------------------- #
    # Execução principal do algoritmo
    # ----------------------------------------------------------------- #
    def executar(self, callback: Optional[Callable[[int, HistoricoACO], None]] = None) -> HistoricoACO:
        """
        Executa o algoritmo ACO pelo número de iterações configurado.

        Parameters
        ----------
        callback : Optional[Callable]
            Função opcional chamada ao final de cada iteração, recebendo
            (numero_da_iteracao, historico). Útil para exibir progresso.

        Returns
        -------
        HistoricoACO
            Objeto com o histórico de melhores distâncias, distância média
            por iteração e a melhor rota/distância encontrada globalmente.
        """
        for iteracao in range(self.n_iteracoes):
            rotas = []
            distancias_rotas = []

            for _ in range(self.n_formigas):
                cidade_inicial = random.randrange(self.n_cidades)
                rota = self._construir_rota(cidade_inicial)
                dist = self.distancia_rota(rota)
                rotas.append(rota)
                distancias_rotas.append(dist)

            self._atualizar_feromonio(rotas, distancias_rotas)

            melhor_iter_idx = int(np.argmin(distancias_rotas))
            melhor_iter_dist = distancias_rotas[melhor_iter_idx]
            melhor_iter_rota = rotas[melhor_iter_idx]

            self.historico.melhor_distancia_por_iteracao.append(melhor_iter_dist)
            self.historico.distancia_media_por_iteracao.append(float(np.mean(distancias_rotas)))

            if melhor_iter_dist < self.historico.melhor_distancia_global:
                self.historico.melhor_distancia_global = melhor_iter_dist
                self.historico.melhor_rota_global = melhor_iter_rota

            if callback is not None:
                callback(iteracao, self.historico)

        return self.historico


# --------------------------------------------------------------------------- #
# 4. Funções utilitárias de visualização (usam matplotlib, chamado no notebook)
# --------------------------------------------------------------------------- #

def plotar_rota(df: pd.DataFrame, rota: List[int], ax=None, titulo: str = "Melhor rota encontrada"):
    """
    Plota a rota encontrada sobre as coordenadas das cidades.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame original com colunas ["Cidade", "X", "Y"].
    rota : List[int]
        Sequência de índices das cidades representando a rota.
    ax : matplotlib.axes.Axes, optional
        Eixo onde o gráfico será desenhado. Se None, cria uma nova figura.
    titulo : str
        Título do gráfico.
    """
    import matplotlib.pyplot as plt

    if ax is None:
        fig, ax = plt.subplots(figsize=(8, 6))

    coords = df[["X", "Y"]].to_numpy()
    rota_fechada = rota + [rota[0]]

    xs = coords[rota_fechada, 0]
    ys = coords[rota_fechada, 1]

    ax.plot(xs, ys, "o-", color="tab:blue", markersize=8, linewidth=1.5)
    for i, cidade_idx in enumerate(rota):
        ax.annotate(
            str(df.loc[cidade_idx, "Cidade"]),
            (coords[cidade_idx, 0], coords[cidade_idx, 1]),
            textcoords="offset points",
            xytext=(5, 5),
            fontsize=9,
        )

    # destaca a cidade inicial
    ax.plot(coords[rota[0], 0], coords[rota[0], 1], "o", color="tab:red", markersize=12)

    ax.set_title(titulo)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.grid(alpha=0.3)
    return ax


def plotar_convergencia(historico: HistoricoACO, ax=None):
    """
    Plota a curva de convergência do algoritmo (melhor distância e distância
    média por iteração).
    """
    import matplotlib.pyplot as plt

    if ax is None:
        fig, ax = plt.subplots(figsize=(8, 5))

    iteracoes = range(1, len(historico.melhor_distancia_por_iteracao) + 1)

    ax.plot(iteracoes, historico.melhor_distancia_por_iteracao, label="Melhor distância (iteração)", color="tab:green")
    ax.plot(iteracoes, historico.distancia_media_por_iteracao, label="Distância média (iteração)", color="tab:orange", alpha=0.7)
    ax.axhline(historico.melhor_distancia_global, color="tab:red", linestyle="--", label="Melhor global")

    ax.set_title("Convergência do algoritmo ACO")
    ax.set_xlabel("Iteração")
    ax.set_ylabel("Distância total da rota")
    ax.legend()
    ax.grid(alpha=0.3)
    return ax


def rota_para_nomes(df: pd.DataFrame, rota: List[int]) -> List[str]:
    """Converte uma rota de índices em uma lista com os nomes das cidades."""
    return [df.loc[i, "Cidade"] for i in rota]