import pygame as pg
import numpy as np

size = 600
black = (0,0,0)
white = (255,255,255)
gray = (125,125,125)
grid_size = 50
cell_size = size/grid_size

pg.init()
screen = pg.display.set_mode( (size+1, size+1+40) )
pg.display.set_caption( "Conway's Game of Life")

def controls():
    global time_delay, play, selection, main_loop
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                main_loop = False
                return( False )
            if event.key == pg.K_MINUS:
                time_delay += 25
            if event.key == pg.K_EQUALS:
                time_delay -= 25
            if event.key == pg.K_RETURN:
                selection = True
                return( False )
    return( True )
        
def next_state():
    global state, white, black
    future = state.copy()
    for x in range(grid_size):
        for y in range(grid_size):
            if state[x+1,y+1] == False:
                if state[x:x+3, y:y+3].sum() == 3:
                    future[x+1,y+1] = True
            else:
                if (state[x:x+3, y:y+3].sum() <= 2) or (state[x:x+3, y:y+3].sum() >= 5):
                    future[x+1,y+1] = False
    state = future.copy()   
                
def selection_stage():
    global cell_size, state, play, main_loop
    for event in pg.event.get():    
        if event.type == pg.QUIT:
            pg.quit()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RETURN:
                return( False )
            if event.key == pg.K_ESCAPE:
                main_loop = False
                play = False
                return( False )
            if event.key == pg.K_SPACE:
                state = np.zeros((grid_size+2, grid_size+2), dtype = bool)
        mouse_1, mouse_2, mouse_3 = pg.mouse.get_pressed()
        if mouse_1:
            mouse_x, mouse_y = pg.mouse.get_pos()
            x, y = (int(mouse_x // cell_size)), (int(mouse_y//cell_size)) 
            if (mouse_x % cell_size != 0) and (mouse_y % cell_size != 0) and (mouse_y <= size):
                state[x+1,y+1] = 1
        if mouse_3:
            mouse_x, mouse_y = pg.mouse.get_pos()
            x, y = (int(mouse_x // cell_size)), (int(mouse_y//cell_size)) 
            if (mouse_x % cell_size != 0) and (mouse_y % cell_size != 0):
                state[x+1,y+1] = 0
    return( True )

def draw_cells():
    global screen, grid_size, state, white, black
    for x in range(grid_size):
        for y in range(grid_size):
            x_screen, y_screen = (x*cell_size)+1, (y*cell_size)+1
            if state[x+1,y+1] == True:
                pg.draw.rect(screen, white, ( x_screen, 
                                             y_screen,
                                             cell_size-1,
                                             cell_size-1))
            else:
                pg.draw.rect(screen, black, ( x_screen, 
                                             y_screen, 
                                             cell_size-1, 
                                             cell_size-1))
                
def draw_grid():
    global screen, white, size, grid_size
    for i in range( grid_size+1):
        coord = i*(size/grid_size)
        pg.draw.line( screen, gray,
        (coord, 0),(coord, size) )
        pg.draw.line( screen, gray,
        (0, coord),(size, coord) )

# Text used during the game
font = pg.font.SysFont('timesnewroman', 14)
introduction = font.render("Welcome to Conway's game of life. Selection stage.", 
        True, white, None)
select_instructions = font.render("Left click to select, right click to deselect, space to erase and enter to begin.",
                           True, white, None)
play_instructions = font.render("Enter to go back to select stage, + or - to adjust iteration speed.",
                         True, white, None)
play_phase = font.render("Play phase.",
                         True, white, None)
select_phase = font.render("Selection phase.",
                         True, white, None)

# We used +2 so the logic for checking the amount of live cells around the given cell is simpler
state = np.zeros((grid_size+2, grid_size+2), dtype = bool)

draw_grid()
main_loop = True
while main_loop:
    
    #This is the selection stage
    pg.draw.rect( screen, black, (0, size+2, size+1, 39))
    screen.blit(select_phase, dest=(1,size+2))
    screen.blit(select_instructions, dest=(1,size+22))
    selection = True
    play = True
    while selection:
        pg.display.update()
        selection = selection_stage()
        draw_cells()
    
    #Now the play stage
    time_delay = 100
    pg.draw.rect( screen, black, (0, size+2, size+1, 39))
    screen.blit(play_instructions, dest=(1,size+22))
    screen.blit(play_phase, dest=(1,size+2))
    while play:
        pg.time.delay( time_delay )
        next_state()
        draw_cells()
        pg.display.update()
        play = controls()
        
pg.quit()