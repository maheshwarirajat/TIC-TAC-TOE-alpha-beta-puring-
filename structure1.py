#Modules
import pygame as pg
import sys
import tictactoelib as lib

#initializations
pg.init()
frames = pg.time.Clock()
human =0
AI=0
status=-1


while True:

	Board=lib.Game()
	Board.create_board()
	Board.create_boxes()

	pg.mixer.stop()
	sound=lib.load_sound('start.ogg')
	sound.play()
	#choose turn
	Board.display_msg("Do you want to start first [y/n]")
	response =raw_input()
	pg.time.delay(2000)
	Board.surface.fill((255,255,255))

	
	#set initial turns
	if(response=='y' or response=='Y'):
		human=1
		AI=0
	else:
		human=0
		AI=1;
	
	#set initial status
	status=-1

	#draw lines
	Board.draw_lines()


	while True:
		for event in pg.event.get():

			if event.type==pg.QUIT:
				pg.quit()
				sys.exit()
			
			if  AI==1:
				Board.AI_turn()
				AI=0
				human=1
				status=Board.check_status()
			
			elif event.type==pg.MOUSEBUTTONUP:
				if human==1:
					x,y = event.pos
					valid=Board.human_turn(x,y)
					#print valid
					if valid==True:
						AI=1
						human=0
						status=Board.check_status()

			if  status!=-1:
				break

		pg.display.update()
		frames.tick(30)
		if  status!=-1:
			break

	pg.mixer.stop()
	
	if  status==2:
		Board.display_msg('YOU WON THE GAME')
		sound=lib.load_sound("won_sound.ogg")
		sound.play()
		pg.time.delay(4000)	
	if  status==1:
		Board.display_msg('YOU LOSE THE GAME')
		sound=lib.load_sound("lose_sound.ogg")
		sound.play()
		pg.time.delay(4000)
	if  status==0:
		Board.display_msg("IT'S A TIE")
		sound=lib.load_sound("lose_sound.ogg")
		sound.play()
		pg.time.delay(4000)

	Board.surface.fill((255,255,255))
	Board.display_msg('want to play another game [y/n]')
	restart=raw_input()

	if(restart=='n' or restart=='N'):
		break





	

