import pygame,os,random,time
from minesweeper import *

class menubutton():
    def __init__(self,text,font,color,x,y,size,count,restart1=False,exit=False,real_obraz=None):
        self.size = size
        self.text = text
        self.color = color
        self.count = count
        self.font = font
        self.obraz = font.render(text,True,color)
        self.rect = self.obraz.get_rect()
        self.rect.topleft = (x,y)
        self.x = x
        self.y = y
        self.mode = False
        self.mainboard = []
        self.completed = False
        self.time = 0
        self.restart = restart1
        self.exit = exit
        self.real_obraz = real_obraz
        self.customcompleted = False
        self.run = True
        self.custom = False
        self.defeat = False

    def draw(self):
        self.color = WHITE
        self.obraz = self.font.render(self.text,True,self.color)
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if self.text != 'Minesweeper':
                self.color = YELLOW
            self.obraz = self.font.render(self.text,True,self.color)
            if pygame.mouse.get_pressed()[0] == 1:
                self.customcompleted = False
                customx.text = '0'
                customy.text = '0'
                custombomb.text = '0'
                for mode in modes:
                    mode.mode = False
                self.mode = True
                if not self.custom:
                    mainboard = createnewboard(self.size[0],self.size[1])
                    setcordinates(mainboard)
                    setboardframe(mainboard)
                    self.mainboard = mainboard
                    
        # pygame.draw.rect(WIN, BLACK, self.rect)
        # pygame.draw.rect(WIN, WHITE, self.rect.scale_by(2), 2)

        WIN.blit(self.obraz, self.rect)

    def drawbutton(self):
        self.obraz = self.real_obraz
        self.rect = self.obraz.get_rect()
        currentmode = getcurrentmode(modes)
        if self.restart:
            self.rect.topleft = (WIDTH/2-30,HEIGHT/2-((currentmode.size[0]/2)*25)-100)
        else:
            self.rect.topleft = (self.x,self.y)
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                if self.restart:
                    restart(currentmode)
                if self.exit:
                    restart(currentmode)
                    for mode in modes:
                        mode.mode = False
                    menu.mode = True
        WIN.blit(self.obraz,self.rect)
             
    def drawboard(self):
        for xrow in self.mainboard:
            for cell in xrow:
                if cell.gamestate:
                    cell.drawcell(self.mainboard)
                else:
                    game_defeat(self.mainboard)
                    cell.drawcell(self.mainboard)
                    self.defeat = True
        drawremainingminesandtime(self,self.mainboard)

class InputBox:

    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = WHITE
        self.text = text
        self.txt_surface = font64.render(str(text), True, self.color)
        self.active = False
        self.approved = False

    def drawbox(self):
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos) and pygame.mouse.get_pressed()[0] == 1 and not self.active:
            self.active = not self.active
            time.sleep(0.2)
        if self.active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    custommode.run = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.rect.collidepoint(event.pos):
                        self.active = not self.active
                        try:
                            int(self.text)
                            self.color = GREEN
                            self.approved = True
                        except ValueError:
                            self.color = RED
                            self.approved = False
                        self.active = False
                    else:
                        self.active = False
                if event.type == pygame.KEYDOWN:
                    if self.active:
                        if self.text == '0':
                            self.text = ''
                        if event.key == pygame.K_RETURN:
                            try:
                                int(self.text)
                                self.color = GREEN
                                self.approved = True
                            except ValueError:
                                self.color = RED
                                self.approved = False
                            self.active = False
                        elif event.key == pygame.K_BACKSPACE:
                            self.text = self.text[:-1]
                        else:
                            self.text += event.unicode
        self.txt_surface = font64.render(self.text, True, self.color)
        pygame.draw.rect(WIN, BLACK, self.rect)
        WIN.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        if self.active:
            pygame.draw.rect(WIN, self.color, self.rect, 3)
        else:
            pygame.draw.rect(WIN, self.color, self.rect, 2)

def executeresult(x1,y1,count1):
    recto = ok.get_rect()
    recto.topleft = (WIDTH/2+250,HEIGHT/2)
    WIN.blit(ok,recto)
    if recto.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0] == 1:
        if x1.approved and y1.approved and count1.approved:
            x,y,count = int(x1.text),int(y1.text),int(count1.text)
            if x > 25:
                drawtext('zbyt dluga plansza!!!',font64,RED,100,100)
                
            elif y > 40:
                drawtext('zbyt szeroka plansza!!!',font64,RED,100,100,)
                
            elif (x*y < (count-10)):
                drawtext('za duzo bomb!!!',font64,RED,100,100)
                
            else:
                x1.color,y1.color,count1.color = WHITE,WHITE,WHITE
                custommode.size = [x,y]
                custommode.count = count
                mainboard = createnewboard(x,y)
                setcordinates(mainboard)
                setboardframe(mainboard)
                custommode.mainboard = mainboard
                custommode.customcompleted = True
        else:
            drawtext('nie podano kazdej z wartosci!!!',font64,RED,100,100)

class cell:
    def __init__(self):
        self.obraz = blank_obraz
        self.true_obraz = blank_obraz
        self.visible = False
        self.bomb = False
        self.startcell = False
        self.frame = False
        self.gamestate = True
        self.flag = False
        self.x = 0
        self.y = 0
        self.surroundingbombs = 0
        self.rect = blank_obraz.get_rect(topleft=(self.x,self.y))
        self.xindex = 0
        self.yindex = 0

    def drawcell(self,board):
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if self.frame:
                pass
            elif pygame.mouse.get_pressed()[0] and not self.flag:
                if game_is_started(board):
                    self.startcell = True
                if self.bomb and self.obraz != mine:
                    self.true_obraz = defeat_mine
                    self.gamestate = False
                else:
                    if self.true_obraz == empty_mine:
                        emptymineclick(board,self)
                    elif self.obraz in mine_images:
                        flagsurroundclick(board,self)
                    self.visible = True
                    self.obraz = self.true_obraz
            elif pygame.mouse.get_pressed()[2]:
                if not self.visible:
                    self.flag = not self.flag
                    time.sleep(0.1)
            else:
                pass
        if self.flag:
            WIN.blit(flag,self.rect)
        else:
            WIN.blit(self.obraz,self.rect)

def drawblankboard(currentmode):
    currentmode.drawboard()
    if not game_is_started(currentmode.mainboard):
        startingcell = getstartcellcords(currentmode.mainboard)
        setbombs(currentmode.count,currentmode.mainboard,startingcell)
        setsurroundingbombs(currentmode.mainboard)
        setmineimages(currentmode.mainboard)
        currentmode.completed = True
        currentmode.time = 0

def restart(currentmode):
    mainboard = createnewboard(currentmode.size[0],currentmode.size[1])
    setcordinates(mainboard)
    setboardframe(mainboard)
    currentmode.mainboard = mainboard
    currentmode.completed = False
    currentmode.defeat = False

def drawremainingminesandtime(mode,board):
    xstart = WIDTH/2-((len(board)*25)/2)
    ystart = HEIGHT/2-((len(board[0])*25)/2) - 50
    count = 0
    for xrow in board:
        for cell in xrow:
            if cell.flag:
                count += 1
    count = mode.count - count
    pygame.draw.rect(WIN, BLACK, pygame.Rect(xstart,ystart, 70, 35))
    pygame.draw.rect(WIN, WHITE, pygame.Rect(xstart,ystart, 70, 35),2)
    
    
    drawtext(str(count),font32,WHITE,xstart+5,ystart)
    xstart = WIDTH/2+((len(board)*25)/2)
    ystart = HEIGHT/2-((len(board[0])*25)/2) - 50
    rect = pygame.Rect(xstart,ystart, 70, 35)
    rect.topright = (xstart,ystart)
    pygame.draw.rect(WIN, BLACK, rect)
    pygame.draw.rect(WIN, WHITE, rect ,2)

    if mode.completed and not mode.defeat:
        timer = pygame.time.Clock()
        ticks = timer.tick(13) / 1000
        mode.time = mode.time + ticks

    drawtext(str(round(mode.time)),font32,WHITE,xstart-5,ystart,1)

def game_is_started(board):
    for xrow in board:
        for cell in xrow:
            if cell.startcell:
                return False
    return True

def game_defeat(board):
    for xrow in board:
        for cell in xrow:
            if not cell.frame:
                if cell.flag and not cell.bomb:
                    cell.flag = False
                    cell.true_obraz = flag_wrong
                    cell.obraz = flag_wrong
                else:
                    cell.obraz = cell.true_obraz
                    cell.visible = True

def setcordinates(board):
    xstart = WIDTH/2-((len(board)*25)/2)
    ystart = HEIGHT/2-((len(board[0])*25)/2)
    for xindex, xrow in enumerate(board):
        for yindex, cell in enumerate(xrow):
            cell.x = xstart + xindex*25
            cell.y = ystart + yindex*25
            cell.rect = blank_obraz.get_rect(topleft=(cell.x,cell.y))
    for x in range(1,len(board)-1):
        for y in range(1,len(board[1])-1):
            board[x][y].xindex = x
            board[x][y].yindex = y

def createnewboard(x,y):
    board = [[] for _ in range(y+2)]
    for yrow in board:
        for _ in range(x+2):
            tile = cell()
            yrow.append(tile)
    return board

def setboardframe(board):
    for n in board[0]:
        n.frame = True
        n.obraz = vertical_frame
    for n in board[-1]:
        n.frame = True
        n.obraz = vertical_frame
    for n in board:
        n[-1].frame = True
        n[0].frame = True
        n[-1].obraz = horizontal_frame
        n[0].obraz = horizontal_frame
    board[0][0].obraz = corners[0]
    board[0][-1].obraz = corners[1]
    board[-1][0].obraz = corners[3]
    board[-1][-1].obraz = corners[2]

def setbombs(count,board,startcell):
    i = 0
    freecells = getcellsaround(board,startcell)
    while i < count:
        randomx = random.randint(1,len(board)-2)
        randomy = random.randint(1,len(board[0])-2)

        randomcell = board[randomx][randomy]
        if (not randomcell.bomb) and (not (randomcell in freecells)):
            board[randomx][randomy].bomb = True
            i += 1

def setsurroundingbombs(board):
    for x in range(1,len(board)-1):
        for y in range(1,len(board[1])-1):
            bombcount = 0
            for nx in range(-1,2):
                for ny in range(-1,2):
                    if board[x + nx][y + ny].bomb:
                        bombcount += 1
            board[x][y].surroundingbombs = bombcount

def setmineimages(board):
    for xrow in board:
        for cell in xrow:
            if not cell.frame:
                if cell.bomb:
                    cell.true_obraz = mine
                else:
                    cell.true_obraz = mine_images[cell.surroundingbombs]

def clearboard(board):
    for xrow in board:
        for tile in xrow:
            tile.bomb = 0

def getcurrentmode(modes):
    for n in modes:
        if n.mode == True:
            return n
        
def getcurrentmode(modes):
    for mode in modes:
        if mode.mode:
            return mode
        
def getstartcellcords(board):
    for xrow in board:
        for cell in xrow:
            if cell.startcell:
                return cell

def getcellsaround(board,cell):
    cords = []
    for n in range (-1,2):
        for m in range(-1,2):
            cords.append(board[cell.xindex+n][cell.yindex+m])
    return cords
            
def emptymineclick(board,cell):
    for n in range(-1,2):
        for m in range(-1,2):
            if board[cell.xindex+n][cell.yindex+m].frame:
                continue
            if board[cell.xindex+n][cell.yindex+m].true_obraz == empty_mine and (not board[cell.xindex+n][cell.yindex+m].visible):
                board[cell.xindex+n][cell.yindex+m].visible = True
                board[cell.xindex+n][cell.yindex+m].obraz = board[cell.xindex+n][cell.yindex+m].true_obraz
                emptymineclick(board,board[cell.xindex+n][cell.yindex+m])
            board[cell.xindex+n][cell.yindex+m].visible = True
            board[cell.xindex+n][cell.yindex+m].obraz = board[cell.xindex+n][cell.yindex+m].true_obraz

def flagsurroundclick(board,cell):
    flagcount = 0
    for n in range(-1,2):
        for m in range(-1,2):
            if board[cell.xindex+n][cell.yindex+m].frame:
                continue
            if board[cell.xindex+n][cell.yindex+m].flag:
                flagcount += 1
    if flagcount == board[cell.xindex][cell.yindex].surroundingbombs:
        for n in range(-1,2):
            for m in range(-1,2):
                if not board[cell.xindex+n][cell.yindex+m].flag and not board[cell.xindex+n][cell.yindex+m].frame:
                    if board[cell.xindex+n][cell.yindex+m].true_obraz == empty_mine:
                        board[cell.xindex+n][cell.yindex+m].visible = True
                        emptymineclick(board,cell)
                    if board[cell.xindex+n][cell.yindex+m].bomb:
                        board[cell.xindex+n][cell.yindex+m].gamestate = False
                    board[cell.xindex+n][cell.yindex+m].obraz = board[cell.xindex+n][cell.yindex+m].true_obraz
                    board[cell.xindex+n][cell.yindex+m].visible = True

def drawrules():
    rect = pygame.Rect(43,95,670,370)
    pygame.draw.rect(WIN, BLACK, rect)
    pygame.draw.rect(WIN, WHITE, rect, 2)
    drawtext('1.Klikaj lewym przyciskiem myszy',font32,WHITE,50,100)
    drawtext('   aby odslaniac pola planszy',font32,WHITE,50,130)
    drawtext('2.Unikaj detonacji min, ',font32,WHITE,50,170)
    drawtext('   oznaczajac je flagami',font32,WHITE,50,200)
    drawtext('3.Odslaniaj pola wokól liczb, ',font32,WHITE,50,240)
    drawtext('   aby odkryc wiecej pól',font32,WHITE,50,270)
    drawtext('4.Liczby na planszy oznaczaja liczbe',font32,RED,50,310)
    drawtext('   min sasiadujacych z danym polem',font32,RED,50,340)
    drawtext('5.Gra konczy sie po oznaczeniu wszystkich',font32,WHITE,50,380)
    drawtext('   min lub detonacji jednej z nich.',font32,WHITE,50,410)

def drawcustomtext():
    drawtext('SZEROKOSC',font64,WHITE,WIDTH/2-140, HEIGHT/3-130)
    drawtext('(MAX 25)',font32,RED,WIDTH/2-70, HEIGHT/3-80)
    drawtext('DLUGOSC',font64,WHITE,WIDTH/2-110, HEIGHT/2-80)
    drawtext('(MAX 40)',font32,RED,WIDTH/2-70, HEIGHT/2-30)
    drawtext('ILOSC BOMB',font64,WHITE,WIDTH/2-165, (HEIGHT*2)/3-30)

BLACK = (0,0,0)
WHITE = (255, 255, 255)
YELLOW = (229, 255, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
FPS = 30
WIDTH = 1200
HEIGHT = 790

grid = [[1,0,0],[1,1,0],[0,0,0]]
clock = pygame.time.Clock()
screen = pygame.display.set_mode((320, 200))
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
fontstyle = os.path.join(__location__,'custom_font.ttf')

pygame.font.init()
font16 = pygame.font.Font(fontstyle, 16)
font20 = pygame.font.Font(fontstyle, 20)
font32 = pygame.font.Font(fontstyle, 32)
font48 = pygame.font.Font(fontstyle, 48)
font64 = pygame.font.Font(fontstyle, 64)
font88 = pygame.font.Font(fontstyle, 78)

blank_obraz = pygame.image.load(os.path.join(__location__,'images/blank_mine.png'))
empty_mine = pygame.image.load(os.path.join(__location__,'images/empty_mine.png'))
defeat_mine = pygame.image.load(os.path.join(__location__,'images/defeat_mine.png'))
one_mine = pygame.image.load(os.path.join(__location__,'images/1_mine.png'))
two_mine = pygame.image.load(os.path.join(__location__,'images/2_mine.png'))
three_mine = pygame.image.load(os.path.join(__location__,'images/3_mine.png'))
four_mine = pygame.image.load(os.path.join(__location__,'images/4_mine.png'))
five_mine = pygame.image.load(os.path.join(__location__,'images/5_mine.png'))
six_mine = pygame.image.load(os.path.join(__location__,'images/6_mine.png'))
seven_mine = pygame.image.load(os.path.join(__location__,'images/7_mine.png'))
eight_mine = pygame.image.load(os.path.join(__location__,'images/8_mine.png'))
horizontal_frame = pygame.image.load(os.path.join(__location__,'images/horizontal_frame.png'))
vertical_frame = pygame.image.load(os.path.join(__location__,'images/vertical_frame.png'))
corner_frame = pygame.image.load(os.path.join(__location__,'images/corner_frame.png'))
mine = pygame.image.load(os.path.join(__location__,'images/mine.png'))
exit = pygame.image.load(os.path.join(__location__,'images/exit.png'))
restartimg = pygame.image.load(os.path.join(__location__,'images/restart.png'))
backgroundimage = pygame.image.load(os.path.join(__location__,'images/castle.jpg'))
flag = pygame.image.load(os.path.join(__location__,'images/flag.png'))
flag_wrong = pygame.image.load(os.path.join(__location__,'images/flag_wrong.png'))
ok = pygame.image.load(os.path.join(__location__,'images/ok.png'))
background = backgroundimage.get_rect(topleft=(0,0))
corners = [pygame.transform.rotate(corner_frame, n*90) for n in range(0,4)]
mine_images = [empty_mine,one_mine,two_mine,three_mine,four_mine,five_mine,six_mine,seven_mine,eight_mine]

menu = menubutton('Minesweeper', font88, WHITE, 50, 50,(1,1),0)
beginnermode = menubutton('Beginner', font48, WHITE, 50, 170,(10,10),20)
intermediatemode = menubutton('Intermediate', font48, WHITE, 50, 240,(16,16),40)
expertmode = menubutton('Expert', font48, WHITE, 50, 310,(16,22), 99)
custommode = menubutton('Custom', font48, WHITE, 50, 380,(1,1),1)
rules = menubutton('Rules', font48, WHITE, 50, 450,(1,1),1)
modes = [menu,beginnermode,intermediatemode,expertmode,custommode,rules]
restartmode = menubutton('reset',font16,WHITE,0,0,0,0,True,0,restartimg)
exitmode = menubutton('reset',font16,WHITE,30,30,0,0,0,True,exit)
customx = InputBox(WIDTH/2-200,HEIGHT/3-50,400,75,'0')
customy = InputBox(WIDTH/2-200,HEIGHT/2,400,75,'0')
custombomb = InputBox(WIDTH/2-200,(2*HEIGHT)/3+50,400,75,'0')
menu.mode ,custommode.custom = True, True
defeat = False

def drawtext(text, font, color, x, y, top=0):
    textSurfaceObj = font.render(text, True, color)
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.topleft  = (x,y)
    if top:
        textRectObj.topright  = (x,y)
    WIN.blit(textSurfaceObj, textRectObj)
