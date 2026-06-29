import heapq
from puzzle.base_search import BaseSearch
from puzzle.state import State, GOAL_STATE
from puzzle.result import SearchResult


class AStar(BaseSearch):

    def heuristic(self, state: State) -> int:
        """Calcula a distância de Manhattan para o 8-puzzle.

        Soma, para cada peça, a distância entre sua posição atual
        e sua posição no estado objetivo. O espaço vazio, representado
        por 0, é ignorado.
        """

        distancia_total = 0

        for indice_atual, valor in enumerate(state.tiles):
            # Ignora o espaço vazio
            if valor == 0:
                continue

            # Posição atual da peça
            linha_atual, coluna_atual = divmod(indice_atual, 3)

            # Posição correta da peça no estado objetivo
            indice_objetivo = GOAL_STATE.index(valor)
            linha_objetivo, coluna_objetivo = divmod(indice_objetivo, 3)

            # Distância de Manhattan
            distancia_total += abs(linha_atual - linha_objetivo) + abs(coluna_atual - coluna_objetivo)

        return distancia_total

    def search(self, initial: State) -> SearchResult:
        """Executa a Busca A* a partir do estado inicial."""

        # Fila de prioridade.
        # Cada item será uma tupla: (f, contador, estado)
        fronteira = []

        contador = 0

        # f(n) = g(n) + h(n)
        custo_estimado_inicial = initial.cost + self.heuristic(initial)

        heapq.heappush(fronteira, (custo_estimado_inicial, contador, initial))

        # Guarda o menor custo real g(n) conhecido para cada configuração
        melhores_custos = {initial.tiles: initial.cost}

        # Métricas da busca
        nodes_expanded = 0
        nodes_generated = 1
        max_frontier_size = 1

        while fronteira:
            _, _, atual = heapq.heappop(fronteira)

            # Ignora entradas antigas da fila, caso já exista caminho melhor
            if atual.cost > melhores_custos.get(atual.tiles, float("inf")):
                continue

            nodes_expanded += 1

            # Verifica se chegou ao objetivo
            if atual.is_goal:
                return SearchResult(
                    solution=atual,
                    nodes_expanded=nodes_expanded,
                    nodes_generated=nodes_generated,
                    max_frontier_size=max_frontier_size,
                    depth=len(atual.path()) - 1
                )

            # Expande os vizinhos
            for filho in atual.neighbors():
                novo_custo = filho.cost

                # Se esse estado ainda não apareceu ou foi encontrado com custo menor
                if novo_custo < melhores_custos.get(filho.tiles, float("inf")):
                    melhores_custos[filho.tiles] = novo_custo

                    contador += 1

                    # f(n) = g(n) + h(n)
                    prioridade = novo_custo + self.heuristic(filho)

                    heapq.heappush(fronteira, (prioridade, contador, filho))
                    nodes_generated += 1

            max_frontier_size = max(max_frontier_size, len(fronteira))

        # Se a fila acabar e não encontrar solução
        return SearchResult(
            solution=None,
            nodes_expanded=nodes_expanded,
            nodes_generated=nodes_generated,
            max_frontier_size=max_frontier_size,
            depth=0
        )
