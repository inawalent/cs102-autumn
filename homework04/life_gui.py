import pygame
from life import GameOfLife
from pygame.locals import *
from ui import UI


class GUI(UI):
    def __init__(self, life: GameOfLife, cell_size: int = 10, speed: int = 10) -> None:
        self.life = life
        self.cell_size = cell_size
        self.speed = speed

        # Установка размеров окна
        self.width = self.life.cols * self.cell_size
        self.height = self.life.rows * self.cell_size
        self.screen_size = (self.width, self.height)

        # Инициализация Pygame
        pygame.init()
        self.screen = pygame.display.set_mode(self.screen_size)
        pygame.display.set_caption("Game of Life")

    def draw_grid(self) -> None:
        """Отобразить состояние клеток"""
        for i in range(self.life.rows):
            for j in range(self.life.cols):
                color = pygame.Color("green") if self.life.curr_generation[i][j] == 1 else pygame.Color("black")
                pygame.draw.rect(
                    self.screen, color, (j * self.cell_size, i * self.cell_size, self.cell_size, self.cell_size)
                )
                pygame.draw.rect(
                    self.screen,
                    pygame.Color("white"),
                    (j * self.cell_size, i * self.cell_size, self.cell_size, self.cell_size),
                    1
                )

    def run(self) -> None:
        # Запуск pygame
        clock = pygame.time.Clock()
        running = True
        paused = False

        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                if event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        paused = not paused

                # Определяем куда нажали и меняем состояние клетки

                if event.type == MOUSEBUTTONDOWN and paused:
                    x, y = event.pos
                    i, j = y // self.cell_size, x // self.cell_size
                    self.life.curr_generation[i][j] = 1 if self.life.curr_generation[i][j] == 0 else 0
            # Генерируем следующие поколение
            if not paused:
                self.life.step()

            # Рисуем и делаем выбранную паузу, чтобы учесть скорость обновления картинки
            self.screen.fill(pygame.Color("white"))
            self.draw_grid()
            pygame.display.flip()
            clock.tick(self.speed)

        pygame.quit()
