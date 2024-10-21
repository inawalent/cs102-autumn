import pathlib
import random
import typing as tp

import pygame
from pygame.locals import *

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(self,
                 size: tp.Tuple[int, int],
                 randomize: bool = True,
                 max_generations: tp.Optional[int] = None
                 ) -> None:
        self.rows, self.cols = size
        self.max_generations = max_generations
        self.generations = 1
        self.prev_generation = self.create_grid()
        self.curr_generation = self.create_grid(randomize=randomize)

    def create_grid(self, randomize: bool = False) -> Grid:
        """
               Создание списка клеток.

               Клетка считается живой, если ее значение равно 1, в противном случае клетка
               считается мертвой, то есть, ее значение равно 0.

               Parameters
               ----------
               randomize : bool
                   Если значение истина, то создается матрица, где каждая клетка может
                   быть равновероятно живой или мертвой, иначе все клетки создаются мертвыми.

               Returns
               ----------
               out : Grid
                   Матрица клеток размером `cell_height` х `cell_width`.
               """
        grid = [[0] * self.cols for _ in range(self.rows)]
        if randomize:
            for i in range(self.rows):
                for j in range(self.cols):
                    grid[i][j] = random.randint(0, 1)
        return grid

    def get_neighbours(self, cell: Cell) -> Cells:
        """
        Вернуть список соседних клеток для клетки `cell`.

        Соседними считаются клетки по горизонтали, вертикали и диагоналям,
        то есть, во всех направлениях.

        Parameters
        ----------
        cell : Cell
            Клетка, для которой необходимо получить список соседей. Клетка
            представлена кортежем, содержащим ее координаты на игровом поле.

        Returns
        ----------
        out : Cells
            Список соседних клеток.
        """
        neighbours = []
        row, col = cell
        for i in range(row - 1, row + 2):
            for j in range(col - 1, col + 2):
                if (i == row and j == col) or not (0 <= i < self.rows and 0 <= j < self.cols):
                    continue
                neighbours.append(self.curr_generation[i][j])
        return neighbours

    def get_next_generation(self) -> Grid:
        """
        Получить следующее поколение клеток.

        Returns
        ----------
        out : Grid
            Новое поколение клеток.
        """
        new_grid = self.create_grid()
        for i in range(self.rows):
            for j in range(self.cols):
                alive_neighbours = sum(self.get_neighbours((i, j)))
                if self.curr_generation[i][j] == 1:
                    # Клетка жива и должна выжить, если у нее 2 или 3 соседа
                    new_grid[i][j] = 1 if alive_neighbours in [2, 3] else 0
                else:
                    # В мертвой клетке зарождается жизнь, если есть ровно 3 соседа
                    new_grid[i][j] = 1 if alive_neighbours == 3 else 0
        return new_grid

    def step(self) -> None:
        """
        Сделать один шаг игры.
        """
        self.prev_generation = self.curr_generation
        self.curr_generation = self.get_next_generation()
        self.generations += 1

    @property
    def is_changing(self) -> bool:
        """
        Проверить, изменилось ли состояние клеток с прошлого поколения.
        """
        return self.curr_generation != self.prev_generation

    @property
    def is_max_generations_exceeded(self) -> bool:
        """
        Проверить, превышено ли максимальное число поколений.
        """
        return self.max_generations is not None and self.generations >= self.max_generations

    @staticmethod
    def from_file(filename: str) -> "GameOfLife":
        """
        Загрузить состояние клеток из файла.
        """
        with open(filename, 'r') as f:
            grid = [[int(char) for char in line.strip()] for line in f]
        size = len(grid), len(grid[0])
        print(grid)
        game_copy = GameOfLife(size, randomize=False)
        game_copy.curr_generation = grid
        return game_copy

    def save(self, filename: str) -> None:
        """
        Сохранить текущее состояние клеток в файл.
        """
        with open(filename, 'w') as f:
            for row in self.curr_generation:
                f.write(''.join(map(str, row)) + '\n')
