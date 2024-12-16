import socket
import sys
import pygame
from Board import Board
from Chess import Chess


def setup():
    mode = input()
    if mode[:2] == "-s":
        server(mode[3:] if len(mode) > 3 and mode[3:].isnumeric() else 12345)
    elif mode[:2] == "-c":
        client(mode[3:] if len(mode) > 3 and mode[3:].isnumeric() else 12345)


def server(port):
    network = socket.socket()
    network.bind(("localhost", int(port)))
    network.listen(1)
    print("Starting Server on " + str(port))
    client, address = network.accept()
    print("Client Joined at " + str(address))
    main_loop("server")
    network.close()

def client(port):
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

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: running = False
            elif event.type == pygame.MOUSEBUTTONDOWN: chess.clicked(event.pos, event.button)
            elif event.type == pygame.K_ESCAPE: running = False

        board.render(screen)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()