import glob
import pygame
import datetime
from board import Board


class Player(Board):
    def __init__(self,screen,board,lives,score_,width,height,eaten_points):
        super().__init__(screen,width,height,board)
        self.player_list = [pygame.transform.scale(pygame.image.load(i), (45, 45)) for i in glob.glob("player_png/*.png")]
        self.counter = 0
        self.angle = 0
        self.direction = -1
        self.x=430
        self.y=664
        self.can_move = [False,False,False,False]
        self.score = 0
        self.lives = lives
        self.padding_walls = 15
        self.detect_walls = 23
        self.kontrolka = None
        self.power_up = False
        self.datetime = None
        self.full_score = score_
        self.player_rect = self.player_list[0].get_rect()
        self.player_rect.center = (430,664)
        self.player_speed = 2
        self.eaten_points = eaten_points


    def set_direction(self,direct):
        center_x = self.x + 22
        center_y = self.y + 22

        if direct == 0 :
            if self.can_move[direct] and 12 <= center_y % self.temp_height <= 18 \
                    and self.board[center_y//self.temp_height][(center_x // self.temp_width)+1] < 3 :
                self.direction = direct
                self.kontrolka = None
            else:
                self.kontrolka = direct
        if direct == 2 :
            if self.can_move[direct] and 12 <= center_y % self.temp_height <= 18 \
                    and self.board[center_y//self.temp_height][(center_x // self.temp_width)-1] <3 :
                self.direction = direct
                self.kontrolka = None
            else:
                self.kontrolka = direct
        if direct == 1 :
            if self.can_move[direct] and 12 < center_x % self.temp_width < 18 \
                    and self.board[(center_y//self.temp_height)-1][center_x // self.temp_width] <3 :
                self.direction = direct
                self.kontrolka = None
            else:
                self.kontrolka = direct
        if direct == 3:
            if self.can_move[direct] and 12 < center_x % self.temp_width < 18 \
                    and self.board[(center_y//self.temp_height)+1][center_x // self.temp_width] <3 :
                self.direction = direct
                self.kontrolka = None
            else:
                self.kontrolka = direct


    def move_player(self):
        center_x = self.x + 22
        center_y = self.y + 22

        if self.kontrolka == 0 and self.can_move[0] and self.board[center_y//self.temp_height][(center_x // self.temp_width)+1] <3  :
            self.direction = self.kontrolka
            self.kontrolka = None
        elif self.kontrolka == 1 and self.can_move[1] and self.board[(center_y//self.temp_height)-1][center_x // self.temp_width] <3:
            self.direction = self.kontrolka
            self.kontrolka = None
        elif self.kontrolka == 2 and self.can_move[2] and self.board[center_y//self.temp_height][(center_x // self.temp_width)-1] <3:
            self.direction = self.kontrolka
            self.kontrolka = None
        elif self.kontrolka == 3 and self.can_move[3] and self.board[(center_y//self.temp_height)+1][center_x // self.temp_width] <3:
            self.direction = self.kontrolka
            self.kontrolka = None

        elif self.direction == 0 and self.can_move[0]:
            self.x += self.player_speed
            self.angle = 0
        elif self.direction == 2 and self.can_move[2]:
            self.x -= self.player_speed
            self.angle = 180
        elif self.direction == 1 and self.can_move[1]:
            self.y -= self.player_speed
            self.angle = 90
        elif self.direction == 3 and self.can_move[3]:
            self.y += self.player_speed
            self.angle = 270

    def show_animation(self):
        if self.counter >= len(self.player_list):
            self.counter = 0

        self.detect_collision()
        self.points_eaten()
        self.move_player()


        self.screen.blit(pygame.transform.rotate(self.player_list[int(self.counter)], self.angle), (self.x,self.y))
        #pygame.display.update()

        self.counter +=0.2
        return (self.x, self.y)


    def detect_collision(self):
        self.can_move = [False, False, False, False]
        center_x = self.x + 22
        center_y = self.y + 22

        if 1< center_x // self.temp_width <29:

            if 12 < center_x % self.temp_width < 18:
                if self.board[(center_y - self.padding_walls) // self.temp_height][center_x // self.temp_width] < 3:
                    self.can_move[1] = True
                if self.board[(center_y + self.padding_walls) // self.temp_height][center_x // self.temp_width] < 3:
                    self.can_move[3] = True
            if 13 <= center_y % self.temp_height <= 17:
                if self.board[center_y // self.temp_height][(center_x - self.temp_width) // self.temp_width] < 3:
                    self.can_move[2] = True
                if self.board[center_y // self.temp_height][(center_x + self.temp_width) // self.temp_width] < 3:
                    self.can_move[0] = True
            if 12 < center_x % self.temp_width < 18:
                if self.board[(center_y - self.temp_height) // self.temp_height][center_x // self.temp_width] < 3:
                    self.can_move[1] = True
                if self.board[(center_y + self.temp_height) // self.temp_height][center_x // self.temp_width] < 3:
                    self.can_move[3] = True
            if 13 <= center_y % self.temp_height <= 17:
                if self.board[center_y // self.temp_height][(center_x - self.padding_walls) // self.temp_width] < 3:
                    self.can_move[2] = True
                if self.board[center_y // self.temp_height][(center_x + self.padding_walls) // self.temp_width] < 3:
                    self.can_move[0] = True
        else:
            self.can_move = [True,False,True,False]
            if (center_x // self.temp_width) == 0:
                self.x = 875
            elif (center_x // self.temp_width) == 30:
                self.x = 8

    def points_eaten(self):
        center_x = self.x + 22
        center_y = self.y + 22

        if self.board[center_y //  self.temp_height][center_x  // self.temp_width] == 1:
            self.board[center_y //  self.temp_height][center_x  // self.temp_width] = 0
            self.score+=10
            self.eaten_points +=1
            self.full_score +=10
        elif self.board[center_y //  self.temp_height][center_x  // self.temp_width] == 2:
            self.board[center_y //  self.temp_height][center_x  // self.temp_width] = 0
            self.power_up = True
            time_now = datetime.datetime.now()
            self.datetime = time_now.second


        if self.power_up :
            time_now = datetime.datetime.now()
            if time_now.second <= 5:
                if self.datetime + 5 == time_now.second + 60:
                    self.power_up = False
                    self.datetime = None
            else:
                if self.datetime + 5 == time_now.second:
                    self.power_up = False
                    self.datetime = None



    def score_lives(self):
        x = 100
        y = 910
        pygame.font.init()
        my_font = pygame.font.SysFont('Comic Sans MS', 25)
        text_surface_score = my_font.render(f"Score : {self.full_score}", False, "white")

        self.screen.blit(text_surface_score, (x,y))

        x_lives = 600
        for i in range (self.lives):
            self.screen.blit(pygame.transform.scale(pygame.image.load("player_png/1.png"), (25, 25)),(x_lives,y+5))
            x_lives +=30


    def player_level_up(self):
        font = pygame.font.Font(None, 65)
        text_surface = font.render ("LEVEL UP", True, "#ff914d")
        text_rect = text_surface.get_rect ()
        text_rect.topleft = (350, 440)
        self.screen.blit (text_surface, text_rect)

