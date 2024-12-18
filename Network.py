# Handles Networking

import ctypes
import os
import random
import socket
import sys
import pygame
from Board import Board
from Chess import Chess


def start():
    mode = input()
    if mode[:2] == "-s":
        start_server(mode[3:] if len(mode) > 3 and mode[3:].isnumeric() else "12345")
    elif mode[:2] == "-c":
        start_client(mode[3:] if len(mode) > 3 and mode[3:].isnumeric() else "12345")


def start_server(port: str):
    network = socket.socket()
    network.bind(("localhost", int(port)))
    network.listen(1)
    print("Starting Server on " + str(port))
    client, address = network.accept()
    print("Client Joined at " + str(address))
    main_loop(False, client)
    client.close()
    network.close()


def start_client(port: str):
    network = socket.socket()
    network.connect(("localhost", int(port)))
    print("Joined Server on " + port)
    main_loop(True, network)
    network.close()


def start_chess(network: socket.socket, board: Board, scalar: int, client: bool) -> Chess:
    if not client:
        turn = random.randint(1, 2)
        network.send(str(turn % 2 + 1).encode())
        return Chess(board, scalar, turn)
    return Chess(board, scalar, int(network.recv(1028).decode()))


def main_loop(client: bool, network: socket.socket):
    # Vars
    square_size = 32
    scale = 3
    board_size = square_size * scale * 8
    board = Board(square_size * scale)
    chess = start_chess(network, board, square_size * scale, client)
    board.set_flip(chess.flip())
    print("Playing as " + ("Black" if chess.flip() else "White"))

    # Pygame Setup
    screensize = ctypes.windll.user32.GetSystemMetrics(0), ctypes.windll.user32.GetSystemMetrics(1)
    if not client:
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (screensize[0] / 4 - board_size / 2,
                                                        screensize[1] / 2 - board_size / 2)
    else:
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (screensize[0] / 1.5 - board_size / 2,
                                                        screensize[1] / 2 - board_size / 2)
    pygame.init()
    running = True
    screen = pygame.display.set_mode((board_size, board_size))
    clock = pygame.time.Clock()
    pygame.display.set_caption("Multiplayer Chess -" + ("client" if client else "server"))

    # Game Loop
    while running:
        data = " ".encode()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if chess.clicked(event.pos, event.button): data = board.send()
            elif event.type == pygame.K_ESCAPE:
                running = False

        if client:
            network.send(data)
            rdata = network.recv(1028).decode()
            if rdata != " ":
                board.receive(rdata)
                chess.next_turn()
        else:
            rdata = network.recv(1028).decode()
            if rdata != " ":
                board.receive(rdata)
                chess.next_turn()
            network.send(data)

        board.render(screen)
        pygame.display.flip()
        clock.tick(60)

    # Safe Exit
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    start()
