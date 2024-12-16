import Network
# from Board import Board
# from Chess import Chess

# def main_loop():
#     # Pygame Setup
#     pygame.init()
#     running = True
#
#     screen = pygame.display.set_mode((board_size * scale, board_size * scale))
#     clock = pygame.time.Clock()
#     pygame.display.set_caption("Multiplayer Chess")
#
#     while running:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT: running = False
#             elif event.type == pygame.MOUSEBUTTONDOWN: chess.clicked(event.pos, event.button)
#             elif event.type == pygame.K_ESCAPE: running = False
#
#         board.render(screen)
#         pygame.display.flip()
#         clock.tick(60)
#
#     pygame.quit()
#     sys.exit()

# Network Setup

Network.setup()