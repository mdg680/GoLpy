import sys
import getopt
import pygame

SCRN_DIM = (800, 600)
SCALE = 8
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 100, 0)
TOTAL_T = 0

def main(argv):
    input_mode = ''
    input_selection = ''

    try:
        opts, args = getopt.getopt(argv, 'crde:', ['selection=', 'dim_x=', 'dim_y='])
    except getopt.GetoptError:
        print "select mode and selection"
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-r', 'dim_x', 'dim_y'):
            input_mode = args
            print "Create empty:", "Dimensions="
        elif opt in ('-e', 'dim_x', 'dim_y'):
            input_mode = arg
            print "Create randomized:", "Dimensions=", input_mode
        elif opt in ("-c', '--selection"):
            input_selection = arg
            print "Create from config:", input_selection[0]
    gol()
        
def gol():

    from grid import Grid as g
    from lifes import Lifes as l


    # Loaded grid
    #current_grid = g(l.blinker)

    # Empty Grid
    current_grid = g((240, 135))
    # exit condition
    exit_cond = False

    pygame.init()
    icon = pygame.image.load('./glider.bmp')
    pygame.display.set_icon(icon)
    pygame.display.set_caption('GoLpy')
    pygame.mouse.set_visible(False)
    screen = pygame.display.set_mode(
        (current_grid.get_height() * SCALE,
         current_grid.get_width() * SCALE), pygame.FULLSCREEN)

    # Initialize clock
    clock = pygame.time.Clock()

    # Set black bacground
    screen.fill(BLACK)

    # Render loop
    t_iter = 1000
    show_visits = False
    sample = False
    paused = False

    while not exit_cond and t_iter > 0:
        clock.tick(60)

        if not paused:
            current_grid.iterate_optimized()

        #print clock.get_fps()
        screen.fill(BLACK)
        #pygame.draw.line(screen, (0, 0, 200), (0, 49),(400, 49))

        if show_visits:
            for x in current_grid.cell_visits:
                pygame.draw.rect(screen, GREEN, (x[0] * SCALE, x[1] * SCALE, SCALE, SCALE))

        for (x, row) in enumerate(current_grid.array):
            for (y, cell) in enumerate(row):
                if cell == 1:
                    pygame.draw.rect(screen, WHITE, (x * SCALE, y * SCALE, SCALE, SCALE))

        mouse_x_pos = pygame.mouse.get_pos()[0]
        mouse_y_pos = pygame.mouse.get_pos()[1]

        pygame.draw.rect(screen, (100, 000, 100),
                         (mouse_x_pos - (mouse_x_pos % SCALE),
                          mouse_y_pos - (mouse_y_pos % SCALE), SCALE, SCALE))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_cond = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    exit_cond = True
                if event.key == pygame.K_SPACE:
                    paused = not paused
                if event.key == pygame.K_v:
                    show_visits = not show_visits
                if event.key == pygame.K_r:
                    current_grid.rand_fill()
            
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                insert_index_in_x = (mouse_x_pos - (mouse_x_pos % SCALE)) / SCALE
                insert_index_in_y = (mouse_y_pos - (mouse_y_pos % SCALE)) / SCALE
                current_grid.array[insert_index_in_x][insert_index_in_y] = 1


        pygame.display.flip()
        if sample:
            t_iter -= 1

if __name__ == "__main__":
    #main([sys.argv[1:]])
    main(['-r', '300', '400'])
