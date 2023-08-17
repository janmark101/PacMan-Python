import pygame
import random
from board import Board
import datetime

class Ghost(Board):
    def __init__(self,screen,board,img_path,x_pos,y_pos,speed,width,height,in_box):
        super().__init__(screen,width,height,board)
        self.ghost_png = pygame.transform.scale(pygame.image.load(img_path), (45, 45))
        self.dead_ghost_png = pygame.transform.scale(pygame.image.load("ghost_png/dead.png"), (45,45))
        self.power_up_ghost = pygame.transform.scale(pygame.image.load("ghost_png/powerup.png"), (45,45))
        self.in_box = in_box
        self.x = x_pos
        self.y = y_pos
        self.dead = False
        self.avaible_moves = [False,False,False,False]
        self.direction = 0
        self.padding_walls = 16
        self.random_direction = 0
        self.list_of_directions = []
        self.speed = speed
        self.next_direction = None
        self.is_next_direction = False
        self.datetime = None
        self.cooldown = False
        self.ghost_rect = self.ghost_png.get_rect()
        self.ghost_rect.center = (x_pos,y_pos)
        self.dead_speed = 1


    def availableMoves(self):
        center_x = self.x +22
        center_y = self.y +22
        self.avaible_moves = [False,False,False,False]
        self.list_of_directions = []

        if 1 < center_x // self.temp_width < 29:

            if 13 <= center_x % self.temp_width <= 17:
                if self.board[(center_y - self.padding_walls) // self.temp_height][center_x // self.temp_width] < 3:
                    self.avaible_moves[1] = True
                if self.dead and self.board[(center_y + self.padding_walls) // self.temp_height][center_x // self.temp_width] == 9:
                    self.avaible_moves[3] = True
                if self.dead and self.board[(center_y + self.padding_walls) // self.temp_height][center_x // self.temp_width] <3:
                    self.avaible_moves[3] = True
                if not self.dead:
                    if self.board[(center_y + self.padding_walls) // self.temp_height][center_x // self.temp_width] < 3:
                        self.avaible_moves[3] = True
                    if self.cooldown and self.board[(center_y - self.padding_walls) // self.temp_height][center_x // self.temp_width] == 9:
                        self.avaible_moves[1] = True
            if 12 <= center_y % self.temp_height <= 16:
                if self.board[center_y // self.temp_height][(center_x - self.temp_width) // self.temp_width] < 3:
                    self.avaible_moves[2] = True
                if self.board[center_y // self.temp_height][(center_x + self.temp_width) // self.temp_width] < 3:
                    self.avaible_moves[0] = True
            if 13 <= center_x % self.temp_width <= 17:
                if self.board[(center_y - self.temp_height) // self.temp_height][center_x // self.temp_width] < 3:
                    self.avaible_moves[1] = True
                if self.dead and self.board[(center_y + self.temp_height) // self.temp_height][center_x // self.temp_width] == 9:
                    self.avaible_moves[3] = True
                if self.dead and self.board[(center_y + self.padding_walls) // self.temp_height][center_x // self.temp_width] <3:
                    self.avaible_moves[3] = True
                if not self.dead:
                    if self.board[(center_y + self.temp_height) // self.temp_height][center_x // self.temp_width] < 3:
                        self.avaible_moves[3] = True
                    if self.cooldown and self.board[(center_y - self.temp_height) // self.temp_height][center_x // self.temp_width] == 9:
                        self.avaible_moves[1] = True
            if 12 <= center_y % self.temp_height <= 16:
                if self.board[center_y // self.temp_height][(center_x - self.padding_walls) // self.temp_width] < 3:
                    self.avaible_moves[2] = True
                if self.board[center_y // self.temp_height][(center_x + self.padding_walls) // self.temp_width] < 3:
                    self.avaible_moves[0] = True
        else:
            self.avaible_moves = [True, False, True, False]
            if (center_x // self.temp_width) == 0:
                self.x = 875
            elif (center_x // self.temp_width) == 30:
                self.x = 8

        if self.avaible_moves[0]:
            self.list_of_directions.append(0)
        if self.avaible_moves[1]:
            self.list_of_directions.append(1)
        if self.avaible_moves[2]:
            self.list_of_directions.append(2)
        if self.avaible_moves[3]:
            self.list_of_directions.append(3)

    def random_walk_whole_map(self):

        self.availableMoves()
        center_x = self.x + 22
        center_y = self.y + 22

        if len(self.list_of_directions) ==0:
             pass
        else:

            if self.random_direction == 0 and len(self.list_of_directions) >=3 and not self.is_next_direction:
                if 2 in self.list_of_directions:
                    self.list_of_directions.remove(2)
                self.next_direction = random.choice(self.list_of_directions)
                self.is_next_direction = True

            elif self.random_direction == 2 and len(self.list_of_directions) >=3 and not self.is_next_direction:
                if 0 in self.list_of_directions:
                    self.list_of_directions.remove(0)
                self.next_direction = random.choice(self.list_of_directions)
                self.is_next_direction = True

            elif self.random_direction == 1 and len(self.list_of_directions) >=3 and not self.is_next_direction:
                if 3 in self.list_of_directions:
                    self.list_of_directions.remove(3)
                self.next_direction = random.choice(self.list_of_directions)
                self.is_next_direction = True

            elif self.random_direction == 3 and len(self.list_of_directions) >=3 and not self.is_next_direction:
                if 1 in self.list_of_directions:
                    self.list_of_directions.remove(1)
                self.next_direction = random.choice(self.list_of_directions)
                self.is_next_direction = True

            elif len(self.list_of_directions) <3 :
                self.is_next_direction = False

            if self.speed == 1:
                if not self.next_direction is None:
                    if self.avaible_moves[self.next_direction] and  (center_x%self.temp_width == 15 and center_y%self.temp_height == 14):
                        self.random_direction = self.next_direction
                        self.next_direction = None

            if self.speed == 2 :
                if not self.next_direction is None:
                    if self.avaible_moves[self.next_direction] and (14 <= center_x%self.temp_width <=16 and center_y%self.temp_height == 14):
                        self.random_direction = self.next_direction
                        self.next_direction = None

            if self.speed == 3 :
                if not self.next_direction is None:
                    if self.avaible_moves[self.next_direction] and (center_x%self.temp_width == 15 and 13 <=center_y%self.temp_height <= 15):
                        self.random_direction = self.next_direction
                        self.next_direction = None

            if self.random_direction == 0 and not self.avaible_moves[0]:
                if 2 in self.list_of_directions:
                    self.list_of_directions.remove(2)
                self.random_direction = random.choice(self.list_of_directions)

            if self.random_direction == 2 and not self.avaible_moves[2]:
                if 0 in self.list_of_directions:
                    self.list_of_directions.remove(0)
                self.random_direction = random.choice(self.list_of_directions)

            if self.random_direction == 1 and not self.avaible_moves[1]:
                if 3 in self.list_of_directions:
                    self.list_of_directions.remove(3)
                self.random_direction = random.choice(self.list_of_directions)

            if self.random_direction == 3 and not self.avaible_moves[3]:
                if 1 in self.list_of_directions:
                    self.list_of_directions.remove(1)
                self.random_direction = random.choice(self.list_of_directions)



        self.screen.blit(self.ghost_png, (self.x, self.y))
        self.move_ghost()


    def random_walk_border(self):

        self.availableMoves()

        if len (self.list_of_directions) == 0 :
            pass
        else :

            if self.random_direction == 2 :
                if self.avaible_moves[2]:
                    self.random_direction = 2
                else:
                    if 0 in self.list_of_directions:
                        self.list_of_directions.remove(0)
                    self.random_direction = random.choice(self.list_of_directions)

            elif self.random_direction == 0 :
                if self.avaible_moves[0]:
                    self.random_direction = 0
                else:
                    if 2 in self.list_of_directions:
                        self.list_of_directions.remove(2)
                    self.random_direction = random.choice(self.list_of_directions)

            elif self.random_direction == 1 :
                if self.avaible_moves[1]:
                    self.random_direction = 1
                else:
                    if 3 in self.list_of_directions:
                        self.list_of_directions.remove(3)
                    self.random_direction = random.choice(self.list_of_directions)

            elif self.random_direction == 3 :
                if self.avaible_moves[3]:
                    self.random_direction = 3
                else:
                    if 1 in self.list_of_directions:
                        self.list_of_directions.remove(1)
                    self.random_direction = random.choice(self.list_of_directions)

            if not self.avaible_moves[self.random_direction] :
                self.random_direction = random.choice(self.list_of_directions)


        self.move_ghost()


    def move_ghost(self):

        if self.random_direction == 0 and self.avaible_moves[0]:
                self.x += self.speed
        if self.random_direction == 2 and self.avaible_moves[2]:
                self.x -= self.speed
        if self.random_direction == 1 and self.avaible_moves[1]:
                self.y -= self.speed
        if self.random_direction == 3 and self.avaible_moves[3]:
                self.y += self.speed

        self.screen.blit(self.ghost_png, (self.x, self.y))



    def get_pacman(self,player_pos,image):

        self.availableMoves()

        if self.direction == 0:
            if player_pos[0] > self.x and self.avaible_moves[0]:
                self.x += self.speed
            elif not self.avaible_moves[0]:
                if player_pos[1] > self.y and self.avaible_moves[3]:
                    self.direction = 3
                    self.y += self.speed
                elif player_pos[1] < self.y and self.avaible_moves[1]:
                    self.direction = 1
                    self.y -= self.speed
                elif player_pos[0] < self.x and self.avaible_moves[2]:
                    self.direction = 2
                    self.x -= self.speed
                elif self.avaible_moves[3]:
                    self.direction = 3
                    self.y += self.speed
                elif self.avaible_moves[1]:
                    self.direction = 1
                    self.y -= self.speed
                elif self.avaible_moves[2]:
                    self.direction = 2
                    self.x -= self.speed
            elif self.avaible_moves[0]:
                if player_pos[1] > self.y and self.avaible_moves[3]:
                    self.direction = 3
                    self.y += self.speed
                elif player_pos[1] < self.y and self.avaible_moves[1]:
                    self.direction = 1
                    self.y -= self.speed
                else:
                    self.x += self.speed
        elif self.direction == 2:
            if player_pos[1] > self.y and self.avaible_moves[3]:
                self.direction = 3
            elif player_pos[0] < self.x and self.avaible_moves[2]:
                self.x -= self.speed
            elif not self.avaible_moves[2]:
                if player_pos[1] > self.y and self.avaible_moves[3]:
                    self.direction = 3
                    self.y += self.speed
                elif player_pos[1] < self.y and self.avaible_moves[1]:
                    self.direction = 1
                    self.y -= self.speed
                elif player_pos[0] > self.x and self.avaible_moves[0]:
                    self.direction = 0
                    self.x += self.speed
                elif self.avaible_moves[3]:
                    self.direction = 3
                    self.y += self.speed
                elif self.avaible_moves[1]:
                    self.direction = 1
                    self.y -= self.speed
                elif self.avaible_moves[0]:
                    self.direction = 0
                    self.x += self.speed
            elif self.avaible_moves[2]:
                if player_pos[1] > self.y and self.avaible_moves[3]:
                    self.direction = 3
                    self.y += self.speed
                elif player_pos[1] < self.y and self.avaible_moves[1]:
                    self.direction = 1
                    self.y -= self.speed
                else:
                    self.x -= self.speed
        elif self.direction == 1:
            if player_pos[0] < self.x and self.avaible_moves[2]:
                self.direction = 2
                self.x -= self.speed
            elif player_pos[1] < self.y and self.avaible_moves[1]:
                self.direction = 2
                self.y -= self.speed
            elif not self.avaible_moves[1]:
                if player_pos[0] > self.x and self.avaible_moves[0]:
                    self.direction = 0
                    self.x += self.speed
                elif player_pos[0] < self.x and self.avaible_moves[2]:
                    self.direction = 2
                    self.x -= self.speed
                elif player_pos[1] > self.y and self.avaible_moves[3]:
                    self.direction = 3
                    self.y += self.speed
                elif self.avaible_moves[2]:
                    self.direction = 2
                    self.x -= self.speed
                elif self.avaible_moves[3]:
                    self.direction = 3
                    self.y += self.speed
                elif self.avaible_moves[0]:
                    self.direction = 0
                    self.x += self.speed
            elif self.avaible_moves[1]:
                if player_pos[0] > self.x and self.avaible_moves[0]:
                    self.direction = 0
                    self.x += self.speed
                elif player_pos[0] < self.x and self.avaible_moves[2]:
                    self.direction = 2
                    self.x -= self.speed
                else:
                    self.y -= self.speed
        elif self.direction == 3:
            if player_pos[1] > self.y and self.avaible_moves[3]:
                self.y += self.speed
            elif not self.avaible_moves[3]:
                if player_pos[0] > self.x and self.avaible_moves[0]:
                    self.direction = 0
                    self.x += self.speed
                elif player_pos[0] < self.x and self.avaible_moves[2]:
                    self.direction = 2
                    self.x -= self.speed
                elif player_pos[1] < self.y and self.avaible_moves[1]:
                    self.direction = 1
                    self.y -= self.speed
                elif self.avaible_moves[1]:
                    self.direction = 1
                    self.y -= self.speed
                elif self.avaible_moves[2]:
                    self.direction = 2
                    self.x -= self.speed
                elif self.avaible_moves[0]:
                    self.direction = 0
                    self.x += self.speed
            elif self.avaible_moves[3]:
                if player_pos[0] > self.x and self.avaible_moves[0]:
                    self.direction = 0
                    self.x += self.speed
                elif player_pos[0] < self.x and self.avaible_moves[2]:
                    self.direction = 2
                    self.x -= self.speed
                else:
                    self.y += self.speed
        
        self.screen.blit(image, (self.x, self.y))


    def player_got_power_up(self):

        self.availableMoves()

        if len(self.list_of_directions) ==0:
             pass
        else:
            if self.random_direction == 2:
                if self.avaible_moves[2]:
                    self.random_direction = 2
                else:
                    if 0 in self.list_of_directions:
                        self.list_of_directions.remove(0)
                    self.random_direction = random.choice(self.list_of_directions)
            elif self.random_direction == 0:
                if self.avaible_moves[0]:
                    self.random_direction = 0
                else:
                    if 2 in self.list_of_directions:
                        self.list_of_directions.remove(2)
                    self.random_direction = random.choice(self.list_of_directions)
            elif self.random_direction == 1:
                if self.avaible_moves[1]:
                    self.random_direction = 1
                else:
                    if 3 in self.list_of_directions:
                        self.list_of_directions.remove(3)
                    self.random_direction = random.choice(self.list_of_directions)
            elif self.random_direction == 3:
                if self.avaible_moves[3]:
                    self.random_direction = 3
                else:
                    if 1 in self.list_of_directions:
                        self.list_of_directions.remove(1)
                    self.random_direction = random.choice(self.list_of_directions)

            if not self.avaible_moves[self.random_direction]:
                self.random_direction = random.choice(self.list_of_directions)

            if self.random_direction == 0 and self.avaible_moves[0]:
                    self.x += 1
            if self.random_direction == 2 and self.avaible_moves[2]:
                    self.x -= 1
            if self.random_direction == 1 and self.avaible_moves[1]:
                    self.y -= 1
            if self.random_direction == 3 and self.avaible_moves[3]:
                    self.y += 1

        self.screen.blit(self.power_up_ghost, (self.x, self.y))



    def show_ghost(self):
        self.screen.blit(self.ghost_png, (self.x, self.y))



    def ghost_dead_walk(self , box ) :
        self.availableMoves ( )

        if self.x < box[0]:
            self.x += self.dead_speed
            if self.y < box[1]:
                self.y += self.dead_speed
            if self.y > box[1]:
                self.y -= self.dead_speed
        if self.x > box[0]:
            self.x -= self.dead_speed
            if self.y < box[1]:
                self.y += self.dead_speed
            if self.y > box[1]:
                self.y -= self.dead_speed
        if self.x == box[0]:
            if self.y < box[1]:
                self.y += self.dead_speed
            if self.y > box[1]:
                self.y -= self.dead_speed

    def ghost_is_dead(self):
        self.ghost_rect.x = self.x
        self.ghost_rect.y = self.y
        ghost_blue_hit_box = pygame.draw.circle (self.screen , "black" , self.ghost_rect.center ,
                                                 min (self.ghost_rect.width ,
                                                      self.ghost_rect.height) // 2 , 1)

        box = [ 435 , 434]
        box_place = pygame.draw.circle (self.screen , "black" , (box[ 0 ] , box[ 1 ]) , 10)
        self.ghost_dead_walk (box)

        if (350 <= self.x <= 520) and (380 <= self.y <= 450):
            image = self.ghost_png
            self.dead_speed = 1
        else:
            image = self.dead_ghost_png

        if ghost_blue_hit_box.colliderect (box_place):
            self.in_box = True
            time_now = datetime.datetime.now ( )
            self.datetime = time_now.second
            image = self.ghost_png
            self.dead = False

        self.screen.blit (image , (self.x , self.y))



    def ghost_in_box(self):

        if self.cooldown:
            self.get_pacman((360,320), self.ghost_png)
        else:
            self.random_walk_border()

        time_now = datetime.datetime.now()
        time_now_second = time_now.second

        if time_now.second <= 5:
            if self.datetime + 5 <= time_now_second + 60:
                self.cooldown = True

        else:
            if self.datetime + 5 <= time_now_second:
                self.cooldown = True

        if not (350 <= self.x <= 560) and not (370 <= self.y <= 500) and self.cooldown:
            self.in_box = False
            self.cooldown = False
