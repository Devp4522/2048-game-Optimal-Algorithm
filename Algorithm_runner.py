from time import sleep
import pygame
from utils.grid import Grid
from algo import ExpectimaxAI
import numpy as np

pygame.init()
WIDTH, HEIGHT = 800, 800
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
CLOCK = pygame.time.Clock()
FPS = 120
pygame.display.set_caption("2048")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


def main():
    running = True
    board = Grid()
    ai = ExpectimaxAI(depth=4 )
    
    generate_now = True
    ai_mode = False

    moves = 0
    time = 0
    
    # main loop
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    ai_mode = not ai_mode 
                elif not generate_now and not ai_mode:
                    if event.key == pygame.K_w:
                        moved = board.move(-1)
                    elif event.key == pygame.K_s:
                        moved = board.move(1)
                    elif event.key == pygame.K_a:
                        moved = board.move(-2)
                    elif event.key == pygame.K_d:
                        moved = board.move(2)
                    
                    if moved:
                        generate_now = True


        if ai_mode and not generate_now:
            best_move = ai.get_best_move(board)
            if best_move:
                moved = board.move(best_move)
                if moved:
                    generate_now = True
                    if np.any(board.get_board() == 2048):
                        running = False  # Stop game if 2048 found
                        pygame.display.set_caption(f"2048 Achieved in {moves} moves! Time: {time:.2f}s")

                moves += 1
                time += 1/FPS
                # parameters used moves and time
                pygame.display.set_caption("2048, Moves : "+ str(moves) + " , Time (sec) : " + f"{time:.2f}" )

        
        SCREEN.fill(WHITE)
        
        # generate random block
        if generate_now:
            result = board.generate_block()
            if result == "Game Over":
                running = False
            generate_now = False
        
        # display grid
        board.draw(SCREEN, BLACK, 1, WIDTH)
        
        CLOCK.tick(FPS)
        pygame.display.flip()
    sleep(3)
    print("Moves : "+ str(moves) + " , Time (sec) : " + f"{time:.2f}")

if __name__ == '__main__':
    main()
