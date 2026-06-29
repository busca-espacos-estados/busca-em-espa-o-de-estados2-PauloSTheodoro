from puzzle.base_search import BaseSearch
from puzzle.state import State
from puzzle.result import SearchResult

DEFAULT_DEPTH_LIMIT = 50


class DFS(BaseSearch):

    def __init__(self, depth_limit: int = DEFAULT_DEPTH_LIMIT):
        self.depth_limit = depth_limit

    def search(self, initial: State) -> SearchResult:
        """Executa a Busca em Profundidade (DFS) com limite de profundidade."""

        # Pilha LIFO: último que entra é o primeiro que sai
        fronteira = [initial]

        # Guarda a menor profundidade em que cada estado já foi encontrado
        visitados = {initial: 0}

        # Métricas da busca
        nodes_expanded = 0
        nodes_generated = 1
        max_frontier_size = 1

        while fronteira:
            # Remove o último estado inserido
            atual = fronteira.pop()
            nodes_expanded += 1

            # Calcula a profundidade atual
            profundidade_atual = len(atual.path()) - 1

            # Verifica se chegou ao objetivo
            if atual.is_goal:
                return SearchResult(
                    solution=atual,
                    nodes_expanded=nodes_expanded,
                    nodes_generated=nodes_generated,
                    max_frontier_size=max_frontier_size,
                    depth=profundidade_atual
                )

            # Se chegou no limite, não expande esse nó
            if profundidade_atual >= self.depth_limit:
                continue

            # Gera os filhos
            for filho in atual.neighbors():
                profundidade_filho = profundidade_atual + 1

                # Adiciona o filho se ele ainda não foi visitado
                # ou se foi encontrado agora em uma profundidade menor
                if filho not in visitados or profundidade_filho < visitados[filho]:
                    visitados[filho] = profundidade_filho
                    fronteira.append(filho)
                    nodes_generated += 1

            # Atualiza o maior tamanho da fronteira
            max_frontier_size = max(max_frontier_size, len(fronteira))

        # Se a pilha acabar e não encontrar solução
        return SearchResult(
            solution=None,
            nodes_expanded=nodes_expanded,
            nodes_generated=nodes_generated,
            max_frontier_size=max_frontier_size,
            depth=0
        )
