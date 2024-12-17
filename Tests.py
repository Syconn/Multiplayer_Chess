# Manages Testing

import pygame
import sys
from Board import Board
from Chess import Chess


def test_loop():
    # Vars
    square_size = 32
    scale = 3
    board_size = square_size * 8
    board = Board(square_size * scale)
    chess = Chess(board, square_size * scale)

    # Pygame Setup
    pygame.init()
    running = True
    screen = pygame.display.set_mode((board_size * scale, board_size * scale))
    clock = pygame.time.Clock()
    pygame.display.set_caption("Multiplayer Chess")

    # Game Loop
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                chess.clicked(event.pos, event.button)
            elif event.type == pygame.K_ESCAPE:
                running = False

        board.render(screen)
        pygame.display.flip()
        clock.tick(60)

    # Safe Exit
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    test_loop()
