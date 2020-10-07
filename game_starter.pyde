from game_controller import GameController

SPACE = {'w': 700, 'h': 700}
filename = "scores.txt"

gc = GameController(SPACE, filename)


def setup():
    size(SPACE['w'], SPACE['h'])
    colorMode(RGB, 1)


def draw():
    background(0.7, 0.7, 0.7)
    gc.update()
    if mousePressed:
        gc.prepare_to_drop(mouseX, mouseY)


def mouseReleased():
    gc.start_drop(mouseX, mouseY)


def keyTyped():
    global gc
    if key == 'y' or key == 'Y':
        gc = GameController(SPACE, filename)
    if key == 'n' or key == 'N':
        exit()
