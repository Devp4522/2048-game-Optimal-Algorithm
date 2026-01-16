import pygame
from utils.grid import Grid

pygame.init()
WIDTH, HEIGHT = 800, 800
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
CLOCK = pygame.time.Clock()
FPS = 7
pygame.display.set_caption("2048")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)



def main():
    
    running = True

    board = Grid()

    generate_now = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif not generate_now and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    moved = board.move(-1)
                elif event.key == pygame.K_s:
                    moved = board.move(1)
                elif event.key == pygame.K_a:
                    moved = board.move(-2)
                elif event.key == pygame.K_d:
                    moved = board.move(2)

                if not moved:
                    break
                generate_now = True
            
        SCREEN.fill((255, 255, 255))

        # generate random
        if generate_now : 
            board.generate_block()
            generate_now = False   

        # display grid
        board.draw(SCREEN, BLACK, 1, WIDTH)

        CLOCK.tick(FPS)
        pygame.display.flip()


if __name__ == '__main__':
    main()
