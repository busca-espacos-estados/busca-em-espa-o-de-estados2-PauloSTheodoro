from __future__ import annotations
from typing import List, Optional, Tuple


GOAL_STATE = (1, 2, 3, 4, 5, 6, 7, 8, 0)


class State:
    """Representa um estado do 8-puzzle como tupla imutável de 9 inteiros (0 = espaço vazio)."""

    def __init__(self, tiles: Tuple[int, ...], parent: Optional["State"] = None, action: Optional[str] = None, cost: int = 0):
        if len(tiles) != 9 or set(tiles) != set(range(9)):
            raise ValueError("Estado inválido: deve conter exatamente os valores 0-8.")
        self.tiles = tiles
        self.parent = parent
        self.action = action
        self.cost = cost

    @property
    def is_goal(self) -> bool:
        return self.tiles == GOAL_STATE

    @property
    def blank_index(self) -> int:
        return self.tiles.index(0)

    def neighbors(self) -> List["State"]:
        """Retorna os estados filhos válidos a partir deste estado."""

        filhos = []
        vazio = self.blank_index
        linha, coluna = divmod(vazio, 3)

        movimentos = [
            ("UP", -1, 0),
            ("DOWN", 1, 0),
            ("LEFT", 0, -1),
            ("RIGHT", 0, 1),
        ]

        for acao, desloc_linha, desloc_coluna in movimentos:
            nova_linha = linha + desloc_linha
            nova_coluna = coluna + desloc_coluna

            if 0 <= nova_linha < 3 and 0 <= nova_coluna < 3:
                novo_indice = nova_linha * 3 + nova_coluna

                novas_pecas = list(self.tiles)
                novas_pecas[vazio], novas_pecas[novo_indice] = novas_pecas[novo_indice], novas_pecas[vazio]

                filho = State(
                    tiles=tuple(novas_pecas),
                    parent=self,
                    action=acao,
                    cost=self.cost + 1
                )

                filhos.append(filho)

        return filhos

    def path(self) -> List["State"]:
        """Retorna a sequência de estados do estado inicial até este."""

        caminho = []
        atual = self

        while atual is not None:
            caminho.append(atual)
            atual = atual.parent

        caminho.reverse()
        return caminho

    def actions(self) -> List[str]:
        """Retorna a sequência de ações do estado inicial até este."""

        return [
            estado.action
            for estado in self.path()
            if estado.action is not None
        ]

    def __eq__(self, other: object) -> bool:
        return isinstance(other, State) and self.tiles == other.tiles

    def __hash__(self) -> int:
        return hash(self.tiles)

    def __lt__(self, other: "State") -> bool:
        return self.cost < other.cost

    def __repr__(self) -> str:
        t = self.tiles
        return (
            f"+-------+\n"
            f"| {t[0]} {t[1]} {t[2]} |\n"
            f"| {t[3]} {t[4]} {t[5]} |\n"
            f"| {t[6]} {t[7]} {t[8]} |\n"
            f"+-------+"
        ).replace("0", " ")
