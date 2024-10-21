import curses

from life import GameOfLife
from ui import UI


class Console(UI):
    def __init__(self, life: GameOfLife) -> None:
        self.life = life

    @staticmethod
    def draw_borders(screen) -> None:
        """ Отобразить рамку. """
        screen.border(0)

    def draw_grid(self, screen) -> None:
        """ Отобразить состояние клеток. """
        for i in range(self.life.rows):
            for j in range(self.life.cols):
                if self.life.curr_generation[i][j] == 1:
                    screen.addch(i + 1, j + 1, '*')
                else:
                    screen.addch(i + 1, j + 1, ' ')

    def run(self) -> None:
        screen = curses.initscr()
        curses.curs_set(0)  # Отключить курсор
        screen.nodelay(True)  # Сделать ввод не блокирующим
        screen.timeout(500)  # Установить тайм-аут

        running = True
        paused = False

        try:
            while running:
                screen.clear()

                # Отрисовка рамки и клеток
                self.draw_borders(screen)
                self.draw_grid(screen)

                # Обработка пользовательского ввода
                event = screen.getch()
                if event == ord("q"):
                    running = False  # Завершить игру
                if event == ord("p"):
                    paused = not paused  # Поставить игру на паузу

                if not paused:
                    self.life.step()  # Сделать шаг игры

                screen.refresh()

        finally:
            curses.endwin()  # Восстановить настройки терминала
