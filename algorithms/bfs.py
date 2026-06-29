from collections import deque
from puzzle.base_search import BaseSearch
from puzzle.state import State
from puzzle.result import SearchResult


class BFS(BaseSearch):

    def search(self, initial: State) -> SearchResult:
        """Executa a Busca em Largura (BFS) a partir do estado inicial."""

        # Fila FIFO: primeiro que entra é o primeiro que sai
        fronteira = deque([initial])

        # Conjunto para evitar visitar o mesmo estado várias vezes
        visitados = {initial}

        # Métricas da busca
        nodes_expanded = 0
        nodes_generated = 1  # conta o estado inicial
        max_frontier_size = 1

        while fronteira:
            # Remove o primeiro estado da fila
            atual = fronteira.popleft()
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

            # Gera os estados filhos
            for filho in atual.neighbors():
                if filho not in visitados:
                    visitados.add(filho)
                    fronteira.append(filho)
                    nodes_generated += 1

            # Atualiza o maior tamanho que a fronteira já teve
            max_frontier_size = max(max_frontier_size, len(fronteira))

        # Se a fila acabar e não encontrar solução
        return SearchResult(
            solution=None,
            nodes_expanded=nodes_expanded,
            nodes_generated=nodes_generated,
            max_frontier_size=max_frontier_size,
            depth=0
        )
