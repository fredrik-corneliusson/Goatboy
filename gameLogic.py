'''
	Goatboy : The jumpin' jackass
	
@note: hejhej    
@author: Mikael					    
'''

import os, pygame, string, getpass, time, operator
from pygame.locals import RLEACCEL

def loadvisible(gameState):
    gs = gameState
    gs.allsprites = pygame.sprite.RenderPlain(sum([gs.map.shots, gs.map.blocks, gs.map.enemies, gs.map.doors, [gs.leveleditor, gs.thor]], [])) # Alla sprites som ska ritas

def reset(gameState):
    gs = gameState
    '''
    Reset everything but the current level and current weapon
	'''
    gs.scrollx, gs.scrolly, gs.thor.dx, gs.thor.ddx, gs.thor.dy, = 0, 0, 0, 0, 0
    gameState.scoore = gameState.scoreFromPreviousLevel
    gs.map.reset()
    gs.thor.setposition(300, 150)
    gs.background.blit(gs.back_surface, (0, 0))
    loadvisible(gs)

def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error, message:
        print "Cannot load image:", name
        raise SystemExit, message
    image = image.convert()
    if colorkey is not None:
        if colorkey is - 1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()

def highscore(score):
    '''
    Appends new score to high score file, reads in the highscore file to a list, sorts
    the	list on score and prints it to the terminal.
    '''
    if score < 1: # Score zero doesn't count
        print "You suck. Gain at least one point in order to reveal the high score list."
        return

    f = open(os.path.join('data', 'highscore.csv'), 'a')
    scoreLine = ("%s, %s, %s \n") % ( score, str(getpass.getuser()), str(time.strftime('%x %X')) )
    f.write(scoreLine)
    f.close()
    
    highscoreList = []
    f = open(os.path.join('data', "highscore.csv"), 'r')
    for line in f:
        entry = string.split(line, ',')
        highscoreList.append( (entry[0], entry[1], entry[2] ) )
    f.close()
    sortedHighscores = sorted(highscoreList, key=lambda score: int(score[0]), reverse=True)
    
    print " Rank | Score  |       Name        |     Time/date    "
    print "------------------------------------------------------"
    
    lowestOnList = 0
    for rank, scoreLine in enumerate(sortedHighscores):
        print str(rank).rjust(5) + scoreLine[0].rjust(8) + scoreLine[1].rjust(20) + scoreLine[2].rjust(23)
        if rank == 9:
            lowestOnList = scoreLine[0]
            break
        
    if score < lowestOnList:
        print "\nSorry pal, a score of just %i points doesn't cut it anymore." % score
       
def getHighestMapNumber():
    ''' Raden nedan gor foljande:
    1. Plockar fram en lista pa alla filer med  i katalogen 'data' med andelsen '.map'
    2. Plockar bort prefix och suffix runt kart-nummret i varje filnamn
    3. Sorterar i storleksordning
    4. Returnerar sista elementet i den sorterade listan
    '''
    return sorted( int( file.lstrip('map').rstrip('.map') ) for file in os.listdir('data') if file.endswith('.map') )[-1]
    