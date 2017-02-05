import os, sys
import pygame as pg
import itertools


#array to store current board state
# x correspond to state 2 of arr----ie human
# o correspond to stare 1 of arr----ie AI
# not_fill correspond to 0 of arr
arr = [0 for x in range(9)]


class Game( object ):

    def __init__(self):
        self.size=480
        self.grid=3
        self.box_size=self.size/self.grid
        self.border=5
        self.surface=pg.display.set_mode((self.size+15,self.size+15))
        self.box_width=self.box_size- (2*self.border)
        self.box_height=self.box_size- (2*self.border)
        #self.alpha=-1000000
        #self.beta=1000000
        self.box_coordinates=None
        for i in range(9):
			arr[i]=0


    def create_board(self):
        pg.display.set_caption("Chuckie's TicTacToe")
        self.surface.fill((255,255,255)) 


    def display_msg(self,str):
        self.surface.fill((255,255,255))
        font = pg.font.Font(None, self.size/10)
        text = font.render(str, 1, (10, 10, 10))
        textpos = text.get_rect(centerx=self.surface.get_width()/2)
        self.surface.blit(text, textpos)
        pg.display.update()


    def draw_lines(self):
        for i in xrange(1,3):
            start_position = ((self.box_size * i) + (5 * (i - 1))) + self.border
            width = self.surface.get_width() - (2 * self.border)
            pg.draw.rect(self.surface,((0,0,0)), (start_position, self.border,5, width))
            pg.draw.rect(self.surface,((0,0,0)), (self.border, start_position, width, 5))
        


    def create_boxes(self):        
        top_left_numbers = []
        for i in range(0, 3):
            num = ((i * self.box_size) + self.border + (i * 5))
            top_left_numbers.append(num)
        
        self.box_coordinates = list(itertools.product(top_left_numbers, repeat=2))
       


    def box_index(self,x,y):
        for idx,(a,b) in enumerate(self.box_coordinates):
            tile=pg.Rect(a,b,self.box_width,self.box_height)
            #print a,b,self.box_width,self.box_height,x,y,arr[idx],tile
            if tile.collidepoint((x,y))==1 and arr[idx]==0:
				#print tile,arr[idx],tile.collidepoint((x,y))
				#print idx
				return idx
        return -1   



    def mark_x(self,idx):
        (x,y)=self.box_coordinates[idx]
        pg.draw.line(self.surface,(25,25,200),((x+5),(y+5)),((x+5+self.box_width),(y+5+self.box_height)),4)
        pg.draw.line(self.surface,(25,25,200),((x+5),(y+5+self.box_height)),((x+5+self.box_width),(y+5)),4)
        arr[idx]=2
        sound=load_sound('mark_x.ogg')
        sound.play()
        pg.time.delay(200)


    def mark_o(self,idx):
        (x,y)=self.box_coordinates[idx]
        pg.draw.circle(self.surface,(200,25,25),((x+(self.box_width/2)),(y+(self.box_height/2))),self.box_width/2-self.box_width/8,4)
        arr[idx]=1
        sound=load_sound('mark_o.ogg')
        sound.play()
        pg.time.delay(200)

    def human_turn(self,x,y):
		#for idx,(a,b) in enumerate(self.box_coordinates):
			#print a,b
		idx=self.box_index(x,y)
		if idx==-1:
			return False
		self.mark_x(idx)
		return True

    def check_status(self):
        
        # any vertical combination
        for i in range(0,9,3):
            if arr[i]!=0 and arr[i]==arr[i+1]==arr[i+2]:
                return arr[i]
        
        # any horizontal combination    
        for i in range(3):
            if arr[i]!=0 and arr[i]==arr[i+3]==arr[i+6]:
                return arr[i]    
        
        #for diagonal combination
        if arr[0]!=0 and arr[0]==arr[4]==arr[8]:
            return arr[0]
        if arr[2]!=0 and arr[2]==arr[4]==arr[6]:
            return arr[2]

        #if more moves possible
        for i in range(0,9):
            if arr[i]==0:
                return -1
        
        #if no winner---tie
        return 0
        

	#minimax algorithm with apha beta cuts
    def minimax(self,isMax,alpha,beta):
        status=self.check_status()
        if status==1:
            return 10
        elif status==2:
            return -10
        elif status==0:
            return 0

        if(isMax):
            best=-1000000
            for i in range(0,9):
                if arr[i]==0:
                    arr[i]=1
                    val=self.minimax(not isMax,alpha,beta)
                    arr[i]=0
                    best=max(best,val)
                    alpha=max(alpha,best)

                    if beta<=alpha:
                        return alpha

            return alpha

        else:
            best=1000000
            for i in range(0,9):
                if arr[i]==0:
                    arr[i]=2
                    val=self.minimax(not isMax,alpha,beta)
                    arr[i]=0
                    best=min(best,val)
                    beta=min(beta,best)

                    if beta<=alpha:
                        return beta

            return beta



    def alphabeta(self):
		bestval=-1000000
		move=-1
		for i in range(9):
			if arr[i]==0:
				#for val in arr:
					#print arr
				arr[i]=1
				moveval=self.minimax(False,-1000000,1000000)
				#print arr
				arr[i]=0

				if moveval > bestval:
					bestval=moveval
					move=i
		return move



    def AI_turn(self):
        idx= self.alphabeta()
        self.mark_o(idx)

#predefined functions to load sounds and images on screen

def load_image(name, colorkey=None):
	fullname = os.path.join('/home/chucki/games/tictactoe/images', name)
	try:
		image = pg.image.load(fullname)
	except pg.error, message:
		print 'Cannot load image:', name
		raise SystemExit, message
	image = image.convert()
	if colorkey is not None:
		if colorkey is -1:
			colorkey = image.get_at((0,0))
		image.set_colorkey(colorkey, RLEACCEL)
	return image, image.get_rect()


def load_sound(name):
	class NoneSound:
		def play(self): pass
	if not pg.mixer:
		return NoneSound()
	fullname = os.path.join('/home/chucki/games/tictactoe/sounds', name)
	try:
		sound = pg.mixer.Sound(fullname)
	except pg.error, message:
		print 'Cannot load sound:', wav
		raise SystemExit, message
	return sound



# pygame.display.set_caption('Monkey Fever')
# my_image=load_image('index.png')
# my_sound=load_sound('bgmusic.ogg')
# print my_image[1]
# screen.blit(my_image[0],my_image[1])
# pygame.display.update()
# my_sound.play()
# pygame.time.delay(1000)
