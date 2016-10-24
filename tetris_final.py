# tetris_empty.py

# Name:Jenny, Xiu
# Collaborators: Julia, Katherine
##
from graphics import *
from random import *

############################
######  BLOCK CLASS  #######
############################

class Block(Rectangle):
    BLOCK_SIZE = 30
    OUTLINE_WIDTH = 2

    def __init__(self,point,color):
        self.x = point.x
        self.y = point.y
        x1 = Block.BLOCK_SIZE*self.x+Block.OUTLINE_WIDTH
        x2 = Block.BLOCK_SIZE+self.x*Block.BLOCK_SIZE
        y1 = self.y*Block.BLOCK_SIZE + Block.OUTLINE_WIDTH
        y2 = self.y*Block.BLOCK_SIZE + Block.BLOCK_SIZE
        p1 = Point(x1,y1)
        p2 = Point(x2,y2)
        Rectangle.__init__(self,p1,p2)
        self.color = color
        self.setWidth(Block.OUTLINE_WIDTH)
        self.setFill(color)

    def can_move(self,board,dx,dy):
        if board.can_move(self.x+dx,self.y+dy) == True:
            return  True
        else:
            return False

    def move(self,dx,dy):
        self.x += dx
        self.y += dy
        Rectangle.move(self,dx*Block.BLOCK_SIZE, dy*Block.BLOCK_SIZE)


############################
######  SHAPE CLASS  #######
############################

class Shape(object):
    def __init__(self,coords,color):
        self.blocks = []
        self.rotation_dir = 1
        self.shift_rotation_dir = False

        for pos in coords:
            self.blocks.append(Block(pos,color))

    def draw(self,win):
        for block in self.blocks:
            block.draw(win)

    def move(self,dx,dy):
        for block in self.blocks:
            block.move(dx,dy)

    def get_blocks (self):
        return self.blocks

    def can_move (self, board, dx, dy):
        x=0
        for block in self.blocks:
            if block.can_move(board,dx,dy) == True:
                x = x+1
        if x == 4:
            return True
        else:
            return False

    def can_rotate(self,board):
        x=0
        center_x = self.center_block.x
        center_y = self.center_block.y
        for block in self.blocks:
            dx = center_x - self.rotation_dir*center_y + self.rotation_dir*block.y
            dy = center_y + self.rotation_dir*center_x - self.rotation_dir*block.x
            if block.can_move(board,dx-block.x,dy-block.y) == True: #checking if each block in shape can move to the new position of a distance "dx-block.x" and "dy-block.y"
                x = x+1
        if x == 4:
            return True
        else:
            return False

    def rotate (self, board):
        center_x = self.center_block.x #x-value of the center block
        center_y = self.center_block.y #y-value of the center block
        for block in self.blocks:
            pblock_y=block.y #y-coordinate of the block before rotation
            pblock_x=block.x
            d_x = center_x - self.rotation_dir*center_y + self.rotation_dir*pblock_y
            d_y = center_y + self.rotation_dir*center_x - self.rotation_dir*pblock_x
            block.move(d_x-pblock_x,d_y-pblock_y)
        if self.type == "I" or self.type == "S" or self.type == "Z" and self.rotation_dir == -1:
            self.rotation_dir = 1
        elif self.type == "I" or self.type == "S" or self.type == "Z" and self.rotation_dir == 1:
            self.rotation_dir = -1





class I_shape(Shape):
    def __init__(self, center):
        coords = [Point(center.x - 1, center.y),
                  Point(center.x , center.y),
                  Point(center.x+1  , center.y),
                  Point(center.x + 2, center.y)]
        Shape.__init__(self, coords, "pale turquoise")
        self.center_block = self.blocks[1]
        self.rotation_dir = -1
        self.shift_rotation_dir = True
        self.type = "I"

class J_shape(Shape):
    def __init__(self, center):
        coords = [Point(center.x-1 , center.y),
                  Point(center.x, center.y),
                  Point(center.x +1  , center.y),
                  Point(center.x+1, center.y+1)]
        Shape.__init__(self, coords, "aquamarine")
        self.center_block = self.blocks[1]
        self.rotation_dir = 1
        self.type = "J"

class L_shape(Shape):
    def __init__(self, center):
        coords = [Point(center.x , center.y),
                  Point(center.x+1, center.y),
                  Point(center.x+2 , center.y),
                  Point(center.x, center.y+1)]
        Shape.__init__(self, coords, "medium spring green")
        self.center_block = self.blocks[0]
        self.rotation_dir = 1
        self.type = "L"

class O_shape(Shape):
    def __init__(self, center):
        coords = [Point(center.x , center.y),
                  Point(center.x +1, center.y),
                  Point(center.x, center.y+1),
                  Point(center.x+1, center.y+1)]
        Shape.__init__(self, coords, "deep pink")
        self.center_block = self.blocks[0]
        self.type = "O"

    def rotate(self,board):
        return

class S_shape(Shape):
    def __init__(self, center):
        coords = [Point(center.x +1, center.y),
                  Point(center.x , center.y),
                  Point(center.x  , center.y+1),
                  Point(center.x-1 , center.y+1)]
        Shape.__init__(self, coords, "tomato")
        self.center_block = self.blocks[1]
        self.rotation_dir = 1
        self.shift_rotation_dir = True
        self.type = "S"

class T_shape(Shape):
    def __init__(self, center):
        coords = [Point(center.x - 1, center.y),
                  Point(center.x , center.y),
                  Point(center.x+1  , center.y),
                  Point(center.x , center.y+1)]
        Shape.__init__(self, coords, "violet")
        self.center_block = self.blocks[1]
        self.rotation_dir = 1
        self.type = "T"

class Z_shape(Shape):
    def __init__(self, center):
        coords = [Point(center.x - 1, center.y),
                  Point(center.x , center.y),
                  Point(center.x    , center.y+1),
                  Point(center.x + 1, center.y+1)]
        Shape.__init__(self, coords, "cyan")
        self.center_block = self.blocks[1]
        self.rotation_dir = -1
        self.shift_rotation_dir = True
        self.type = "Z"


############################
######  BOARD CLASS  #######
############################

class Board(object):
    def __init__(self,win,width,height):
        self.width = width
        self.height = height

        self.canvas = CanvasFrame(win,self.width*Block.BLOCK_SIZE,
                                  self.height * Block.BLOCK_SIZE)
        self.canvas.setBackground('black')
        self.grid = {}

    def draw_shape(self,shape):
        if self.can_move(0,0) == True:
            shape.draw(self.canvas)
            return True
        else:
            return False

    def can_move (self,x,y):
        if x <10 and x >= 0 and y < 20 and y >= 0:
            if (x,y) in self.grid:
                return False
            else:
                return True
        else:
            return False

    def add_shape (self,shape):
        for block in shape.get_blocks():
            self.grid[(block.x,block.y)] = block

    def delete_row(self,y):
        x=0
        while x <= 9:
            if (x,y) in self.grid:
                block = self.grid[(x,y)]
                block.undraw()
                del self.grid[(x,y)]
                x = x + 1

    def is_row_complete(self,y):
        x=0
        while x <= 9:
            if (x,y) in self.grid:
                x = x + 1
            else:
                return False
        return True

    def move_down_rows(self,y_start):
        for y in range(y_start,0,-1):
            for x in range (10):
                if (x,y) in self.grid:
                    new_block = self.grid[(x,y)]
                    self.grid[(x,y+1)] = new_block
                    self.grid[(x,y)].move(0,1)
                    del self.grid[(x,y)]

    def remove_complete_rows(self):
        for y in range(20):
            if self.is_row_complete(y) == True:
                self.delete_row(y)
                self.move_down_rows(y-1)

    def game_over(self):
        msg1 = Text(Point(150,300),"GAME OVER!")
        msg1.draw(self.canvas)
        msg1.setSize(30)
        msg1.setTextColor('white')

############################
#### WTP TETRIS GAME  ######
############################

class WTPTetris(object):
    SHAPES = [I_shape, J_shape, L_shape, O_shape, S_shape, T_shape, Z_shape]
    DIRECTION = {'Left':(-1,0),'Right':(1,0),'Down':(0,1)}
    BOARD_WIDTH = 10
    BOARD_HEIGHT = 20

    def __init__(self,win):
        self.board = Board(win, self.BOARD_WIDTH, self.BOARD_HEIGHT)
        self.win = win
        self.delay = 1000 #ms

        self.win.bind_all('<Key>',self.key_pressed)

        self.current_shape = self.create_new_shape()
        self.board.draw_shape(self.current_shape)
        self.gameover = 1
        self.animate_shape()


    def animate_shape(self):
        self.do_move((0,1))
        if self.gameover == 1:
            self.win.after(self.delay,self.animate_shape)


    def create_new_shape(self):
        x = randint(0,6)
        y = self.SHAPES[x](Point(4,0))
        return y

    def do_move(self,direction):
        if self.gameover == 1:
            if self.current_shape.can_move(self.board,direction[0],direction[1]) == True:
                self.current_shape.move(direction[0],direction[1])
            elif self.current_shape.can_move(self.board,0,1) == False:
                self.board.add_shape(self.current_shape)
                self.board.remove_complete_rows()
                self.current_shape = self.create_new_shape()
                self.board.draw_shape(self.current_shape)
                if self.current_shape.can_move(self.board,0,1) == False:
                    self.board.game_over()
                    self.gameover = 0

    def do_rotate(self):
        if self.current_shape.can_rotate(self.board) == True:
            self.current_shape.rotate(self.board)
        else:
            return False


    def key_pressed (self, event):
        key = event.keysym
        if key == 'space':
            while self.current_shape.can_move(self.board,0,1) == True:
                self.do_move((0,1))
        elif key == 'Up':
            if self.current_shape.can_rotate(self.board) == True:
                self.do_rotate()
        else:
            self.do_move(self.DIRECTION[key])



win = Window("WTP Tetris")
game = WTPTetris(win)
win.mainloop()
