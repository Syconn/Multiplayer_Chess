# Handles Networking

import socket
import sys
import pygame
from Board import Board
from Chess import Chess


def update():
    pass


def receive():
    pass


def start():
    mode = input()
    if mode[:2] == "-s":
        start_server(mode[3:] if len(mode) > 3 and mode[3:].isnumeric() else 12345)
    elif mode[:2] == "-c":
        start_client(mode[3:] if len(mode) > 3 and mode[3:].isnumeric() else 12345)


def start_server(port):
    network = socket.socket()
    network.bind(("localhost", int(port)))
    network.listen(1)
    print("Starting Server on " + str(port))
    client, address = network.accept()
    print("Client Joined at " + str(address))
    main_loop("server")

    network.close()


def start_client(port):
    network = socket.socket()
    network.connect(("localhost", int(port)))
    main_loop("client")
    network.close()


def main_loop(version):
    # Vars
    square_size = 32
    board_size = square_size * 8
    scale = 3
    board = Board(square_size, scale)
    chess = Chess(board, square_size * scale)

    # Pygame Setup
    pygame.init()
    running = True
    screen = pygame.display.set_mode((board_size * scale, board_size * scale))
    clock = pygame.time.Clock()
    pygame.display.set_caption("Multiplayer Chess -" + version)

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
    start()
