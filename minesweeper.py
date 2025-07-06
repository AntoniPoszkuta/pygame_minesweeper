import pygame,os
from variables import *

def draw_window():
    WIN.fill((BLACK))
    WIN.blit(backgroundimage,background)
    currentmode = getcurrentmode(modes)
    if menu.mode:
        for mode in modes:
            mode.draw()
        # drawtext('(WORK IN PROGRESS)',font32,RED,50,415)
    elif custommode.mode and not custommode.customcompleted:
        drawcustomtext()
        customx.drawbox()
        customy.drawbox()
        custombomb.drawbox()
        exitmode.drawbutton()
        executeresult(customx,customy,custombomb)
    elif currentmode.completed:
        currentmode.drawboard()
        restartmode.drawbutton()
        exitmode.drawbutton()
    elif currentmode.text == 'Rules' and currentmode.mode:
        exitmode.drawbutton()
        drawrules()
    else:
        drawblankboard(currentmode)
        restartmode.drawbutton()
        exitmode.drawbutton()
    pygame.display.update()

def main():
    run = True
    while run and custommode.run:
        clock.tick(FPS)
        draw_window()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

if __name__ == "__main__":
    main()