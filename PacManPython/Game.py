import json
from pathlib import Path
import pygame
from player import Player
from board import Board
from ghosts import Ghost
from board_list import new_board,new_board_2
from main_screen import Button
import datetime
import re

class Game():
    def __init__(self):
        self.width_menu = 780
        self.height_menu = 800
        self.width_game = 900
        self.height_game = 950
        self.Player_lives = 3
        self.Player_score = 0
        self.eaten_points = 0 #230
        self.User_name = ""
        self.Ghost_speed = 1
        self.Level = 1
        self.screen = None
        self.run = True
        self.show_scoreboard = False
        self.player_died = True
        self.player_lvl_up = False
        self.board_map = None
        self.which_board = None
        self.board_copy = None
        self.back_menu = False
        self.Game_on = False
        self.board = None
        self.player = None
        self.Ghost_blue = None
        self.Ghost_pink = None
        self.Ghost_red = None
        self.Ghost_orange = None
        self.Ghost_blue_path = Path("ghost_png/blue.png")
        self.Ghost_red_path = Path ("ghost_png/red.png")
        self.Ghost_pink_path = Path ("ghost_png/pink.png")
        self.Ghost_orange_path = Path ("ghost_png/orange.png")
        self.Scoreboard_path = Path("Scoreboard/Scoreboard.json")
        self.Logo_path = Path("Logo/pac_man_bg_image.png")
        self.pattern_length = r"^.{4,12}$"
        self.special_chars_pattern = r"[^\w]+"
        self.map_choosen = False
        self.options = False
        self.first_game = True
        self.coursor = pygame.transform.scale(pygame.image.load("Config/coursor.png") , (25, 25))
        self.Menu()


    def Menu(self):
        clock = pygame.time.Clock ( )
        pygame.init()
        self.screen = pygame.display.set_mode ((self.width_menu, self.height_menu))
        pygame.display.set_caption ('Pac-Man')
        button_start_game = Button (pygame.image.load ("buttons/Button_start_game.png"), (240, 280), self.screen)
        button_scoreboard = Button (pygame.image.load ("buttons/Button_scoreboard.png"), (240, 460), self.screen)
        button_back = Button (pygame.image.load ("buttons/back_small_button.png"), (80, 665), self.screen)
        button_ok = Button( pygame.image.load( "buttons/button_ok.png" ) , (310 , 550) , self.screen )
        button_ok_map_1 = Button (pygame.image.load ("buttons/button_ok.png") , (125 , 600) , self.screen)
        button_ok_map_2 = Button (pygame.image.load ("buttons/button_ok.png") , (500 , 600) , self.screen)
        button_config = Button(pygame.image.load("buttons/button_rules.png"),(600,650),self.screen)
        pygame.mouse.set_visible(False)

        while self.run:
            (x_mouse,y_mouse) = pygame.mouse.get_pos()
            if  not self.show_scoreboard and not self.Game_on and not self.map_choosen and not self.options:
                for event in pygame.event.get ():
                    if event.type == pygame.QUIT:
                        self.run = False
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if button_start_game.png_rect.collidepoint (event.pos):
                            self.map_choosen = True
                            self.screen = pygame.display.set_mode ((self.width_menu , self.height_menu))
                        if button_scoreboard.png_rect.collidepoint (event.pos):
                            self.show_scoreboard = True
                        if button_config.png_rect.collidepoint(event.pos):
                            self.options = True

            if self.show_scoreboard:
                self.screen.fill("black")
                if self.show_scoreboard:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            self.run = False
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if button_back.png_rect.collidepoint(event.pos):
                                self.show_scoreboard = False
                    self.Show_scoreboard()
                    self.Button_back(button_back)
                    self.screen.blit (self.coursor , (x_mouse , y_mouse))
                    pygame.display.update ( )

            elif self.options:
                self.screen.fill ("black")
                if self.options:
                    for event in pygame.event.get ( ):
                        if event.type == pygame.QUIT:
                            self.run = False
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if button_back.png_rect.collidepoint (event.pos):
                                self.options = False
                    self.Button_back (button_back)
                    self.show_options()
                self.screen.blit (self.coursor , (x_mouse , y_mouse))
                pygame.display.update ( )

            elif self.map_choosen:
                self.screen.fill ("black")
                if self.map_choosen:
                    for event in pygame.event.get ( ):
                        if event.type == pygame.QUIT:
                            self.run = False
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if button_ok_map_1.png_rect.collidepoint(event.pos):
                                self.map_choosen = False
                                self.first_game = True
                                self.board_map = new_board
                                self.screen = pygame.display.set_mode ((self.width_game , self.height_game))
                                self.which_board = 1
                                self.board_copy =  [row[ : ] for row in self.board_map ]
                                self.Game_on = True

                            if button_ok_map_2.png_rect.collidepoint(event.pos):
                                self.map_choosen = False
                                self.first_game = True
                                self.board_map = new_board_2
                                self.screen = pygame.display.set_mode ((self.width_game , self.height_game))
                                self.which_board = 2
                                self.board_copy = [ row[ : ] for row in self.board_map ]
                                self.Game_on = True


                    self.choose_map(button_ok_map_1,button_ok_map_2)
                    self.screen.blit (self.coursor , (x_mouse , y_mouse))
                    pygame.display.update ( )

            elif self.Game_on:
                self.Start_game(button_ok)

            else:
                self.buttons_menu(button_start_game,button_scoreboard,button_config)
                pygame.display.update ( )

            clock.tick (60)

    # def game_objects(self):
    #     self.board = Board ( self.screen , self.width_game , self.height_game , self.board_map )
    #     self.player = Player ( self.screen , self.board_map , self.Player_lives , self.Player_score , self.width_game ,
    #                       self.height_game,self.eaten_points )
    #     self.board.count_points_funt()


    def choose_map(self,button_map_1,button_map_2):
        font = pygame.font.Font (None , 75)
        text_surface = font.render ("CHOOSE YOUR MAP" , True , '#fcc92e')
        text_rect = text_surface.get_rect ( )
        text_rect.topleft = (140 , 70)
        self.screen.blit (text_surface , text_rect)
        Map_1 = pygame.transform.scale(pygame.image.load("Maps/map_1.png"), (360,310))
        Map_2 = pygame.transform.scale(pygame.image.load("Maps/map_2.png"), (360,310))
        (x_mouse , y_mouse) = pygame.mouse.get_pos ( )
        button_map_1.enlarge_png (x_mouse , y_mouse , "buttons/big_button_ok.png" , 10 , 5)
        button_map_1.show_button ( )
        button_map_2.enlarge_png (x_mouse , y_mouse , "buttons/big_button_ok.png" , 10 , 5)
        button_map_2.show_button ( )
        self.screen.blit (Map_1 , (20 , 250))
        self.screen.blit (Map_2 , (400 , 250))


    def show_options(self):
        keys = [ "Up" , "Down" , "Left" , "Rigth" ]
        for i,key in enumerate(keys):
            key_arrow = pygame.transform.scale (pygame.image.load (f"Config/{key}.png") , (60 , 60))
            self.screen.blit (key_arrow , (50 , 190 + i *70))

        self.screen.blit(pygame.image.load("Config/Rules.png"),(260,30))

        font = pygame.font.Font (None , 50)

        for i,key in enumerate(keys):
            text_surface = font.render (key , True , 'white')  ##fcc92e'
            text_rect = text_surface.get_rect ( )
            text_rect.topleft = (130 , 205 + i*70)
            self.screen.blit (text_surface , text_rect)

        text_position = [(480 , 205),(380 , 275),(450 , 345),(450 , 415)]
        text_list = ["Player lives :  3","Ghosts speed  :  [1,2,3]","Player speed  :  2", "Power up : "]
        self.screen.blit(pygame.transform.scale(pygame.image.load("Config/cherry.png"), (55,55)),(660,405))
        for i in range(4):
            text_surface = font.render (text_list[i] , True , 'white')  ##fcc92e'
            text_rect = text_surface.get_rect ( )
            text_rect.topleft = text_position[i]
            self.screen.blit (text_surface , text_rect)

        rules_list = ["Player starts game with 3 lives, when he hits ghost without having power",
                      "up, he loses his life. If the player eats all points on the map, he goes up" ,
                      "a level. Game has 3 levels that change the speed of the ghosts. When the ",
                      "player dies or level up, the ghosts and the player reset their position."]

        font = pygame.font.Font (None , 30)

        for i in range(4):
            text_surface = font.render (rules_list[i] , True , 'white')  ##fcc92e'
            text_rect = text_surface.get_rect ( )
            text_rect.topleft = (35,500 + i*40)
            self.screen.blit (text_surface , text_rect)

    def Start_game(self,button):
        self.screen.fill("black")

        if self.first_game:
            self.reset_map()
            self.board = Board(self.screen, self.width_game, self.height_game, self.board_map)
            self.player = Player(self.screen, self.board_map, self.Player_lives, self.Player_score, self.width_game,
                                 self.height_game, self.eaten_points)
            self.board.count_points_funt()
            self.first_game = False

        elif self.Level >=4 :
            self.reset_map()
            self.board = Board(self.screen, self.width_game, self.height_game, self.board_map)
            self.screen = pygame.display.set_mode((self.width_menu, self.height_menu))
            self.save_player(button, self.player.full_score, "You win!")

        else:
            if self.player_died:
                if self.player_lvl_up:
                    eaten_small_balls = 0 #230
                    self.reset_map()
                    self.board = Board(self.screen, self.width_game, self.height_game, self.board_map)
                    self.board.count_points_funt()
                else:
                    eaten_small_balls = self.player.eaten_points

                player_lives = self.player.lives
                player_score = self.player.full_score
                self.player = Player(self.screen,self.board_map,player_lives,player_score, self.width_game ,
                              self.height_game,eaten_small_balls)

                self.Ghost_red = Ghost (self.screen , self.board_map , self.Ghost_red_path, 380 , 48 , self.Ghost_speed ,
                                        self.width_game ,self.height_game,False)
                self.Ghost_pink = Ghost (self.screen , self.board_map , self.Ghost_pink_path , 52 , 48 , self.Ghost_speed ,
                                         self.width_game ,self.height_game,False)
                self.Ghost_blue = Ghost (self.screen , self.board_map , self.Ghost_blue_path , 800 , 48 , self.Ghost_speed ,
                                         self.width_game ,self.height_game,False)
                self.Ghost_orange = Ghost (self.screen , self.board_map , self.Ghost_orange_path , 500 , 384 , self.Ghost_speed ,
                                         self.width_game , self.height_game,True)

                for event in pygame.event.get ( ) :
                    if event.type == pygame.QUIT:
                        pygame.quit ( )
                        quit ( )
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            self.player_lvl_up = False
                            self.player_died = False
                            time_now = datetime.datetime.now ( )
                            self.Ghost_orange.datetime = time_now.second

                self.board.draw_board()
                self.player.score_lives ( )
                self.player.show_animation ( )
                self.Ghost_red.show_ghost()
                self.Ghost_blue.show_ghost()
                self.Ghost_pink.show_ghost()
                self.Ghost_orange.show_ghost()
                self.Space_to_start()
                if self.player_lvl_up:
                    self.player.player_level_up()
                    self.Space_to_start()

            else:

                list_of_objects = self.Update_positions()

                for event in pygame.event.get ( ) :
                    if event.type == pygame.QUIT :
                        self.run = False
                    if event.type == pygame.KEYDOWN :
                        if event.key == pygame.K_DOWN :
                            self.player.set_direction (3)
                        if event.key == pygame.K_LEFT :
                            self.player.set_direction (2)
                        if event.key == pygame.K_UP :
                            self.player.set_direction (1)
                        if event.key == pygame.K_RIGHT :
                            self.player.set_direction (0)

                self.board.draw_board ( )
                self.player.score_lives()
                player_pos = self.player.show_animation()

                if self.Ghost_blue.in_box:
                    if self.player.power_up:
                        pass
                    else:
                        self.Ghost_blue.ghost_in_box()
                if self.Ghost_red.in_box:
                    if self.player.power_up:
                        pass
                    else:
                        self.Ghost_red.ghost_in_box()
                if self.Ghost_pink.in_box:
                    if self.player.power_up:
                        pass
                    else:
                        self.Ghost_pink.ghost_in_box()
                if self.Ghost_orange.in_box:
                    if self.player.power_up:
                        pass
                    else:
                        self.Ghost_orange.ghost_in_box()

                if list_of_objects[0].colliderect(list_of_objects[1]) and self.player.power_up and not self.Ghost_blue.dead:
                    self.Ghost_blue.dead = True
                    self.player.full_score +=100
                if list_of_objects[0].colliderect(list_of_objects[2]) and self.player.power_up and not self.Ghost_red.dead:
                    self.Ghost_red.dead = True
                    self.player.full_score +=100
                if list_of_objects[0].colliderect(list_of_objects[3]) and self.player.power_up and not self.Ghost_pink.dead:
                    self.Ghost_pink.dead = True
                    self.player.full_score +=100
                if list_of_objects[0].colliderect(list_of_objects[4]) and self.player.power_up and not self.Ghost_orange.dead:
                    self.Ghost_orange.dead = True
                    self.player.full_score +=100

                if self.player.power_up:
                    if not self.Ghost_blue.dead:
                        self.Ghost_blue.player_got_power_up()
                    if not self.Ghost_red.dead:
                        self.Ghost_red.player_got_power_up()
                    if not self.Ghost_pink.dead:
                        self.Ghost_pink.player_got_power_up()
                    if not self.Ghost_orange.dead:
                        self.Ghost_orange.player_got_power_up()
                    if self.Ghost_blue.dead:
                        self.Ghost_blue.ghost_is_dead()
                    if self.Ghost_red.dead:
                        self.Ghost_red.ghost_is_dead()
                    if self.Ghost_pink.dead:
                        self.Ghost_pink.ghost_is_dead()
                    if self.Ghost_orange.dead:
                        self.Ghost_orange.ghost_is_dead()

                else:
                    if self.Ghost_blue.dead:
                        self.Ghost_blue.ghost_is_dead()
                    if self.Ghost_red.dead:
                        self.Ghost_red.ghost_is_dead()
                    if self.Ghost_pink.dead:
                        self.Ghost_pink.ghost_is_dead()
                    if self.Ghost_orange.dead:
                        self.Ghost_orange.ghost_is_dead()

                    if 0 <= self.player.score <= 200 or \
                            400 <= self.player.score <= 600 or \
                            800 <= self.player.score <= 1000 or \
                            1200 <= self.player.score <= 1400 or \
                            1600 <= self.player.score <= 1800 or \
                            2000 <= self.player.score <= 2200 or \
                            2400 <= self.player.score <= 2600 :

                        if self.Ghost_blue.dead or self.Ghost_blue.in_box:
                            pass
                        else:
                            self.Ghost_blue.random_walk_whole_map()
                        if self.Ghost_red.dead or self.Ghost_red.in_box:
                            pass
                        else:
                            self.Ghost_red.random_walk_border()
                        if self.Ghost_pink.dead or self.Ghost_pink.in_box:
                            pass
                        else:
                            self.Ghost_pink.random_walk_whole_map()
                        if self.Ghost_orange.dead or self.Ghost_orange.in_box:
                            pass
                        else:
                            self.Ghost_orange.random_walk_border()

                    else:
                        if self.Ghost_blue.dead or self.Ghost_blue.in_box:
                            pass
                        else:
                            self.Ghost_blue.get_pacman(player_pos,self.Ghost_blue.ghost_png)
                        if self.Ghost_red.dead or self.Ghost_red.in_box:
                            pass
                        else:
                            self.Ghost_red.get_pacman(player_pos,self.Ghost_red.ghost_png)
                        if self.Ghost_pink.dead or self.Ghost_pink.in_box:
                            pass
                        else:
                            self.Ghost_pink.get_pacman(player_pos,self.Ghost_pink.ghost_png)
                        if self.Ghost_orange.dead or self.Ghost_orange.in_box:
                            pass
                        else:
                            self.Ghost_orange.get_pacman(player_pos,self.Ghost_orange.ghost_png)

                if not self.player.power_up:
                    if list_of_objects[0].colliderect(list_of_objects[1]) or\
                            list_of_objects[0].colliderect(list_of_objects[2]) or\
                            list_of_objects[0].colliderect(list_of_objects[3]) or \
                            list_of_objects[0].colliderect(list_of_objects[4]):
                        self.player.lives -=1
                        self.player_died = True

                if self.player.lives <1:
                    self.screen = pygame.display.set_mode((self.width_menu,self.height_menu))
                    self.save_player(button,self.player.full_score,"You died!")

                if self.player.eaten_points >= self.board.count_points:
                    self.Level += 1
                    self.Ghost_speed += 1
                    self.player_lvl_up = True
                    self.player_died = True


        pygame.display.update ( )

    def reset_map(self):
        self.board_map = [row[:] for row in self.board_copy]

    def Update_positions(self):
        list = []

        self.player.player_rect.x = self.player.x
        self.player.player_rect.y = self.player.y
        player_hit_box = pygame.draw.circle (self.screen , "black" , self.player.player_rect.center ,
                                                min (self.player.player_rect.width ,
                                                     self.player.player_rect.height) // 3)

        list.append(player_hit_box)

        self.Ghost_blue.ghost_rect.x = self.Ghost_blue.x
        self.Ghost_blue.ghost_rect.y = self.Ghost_blue.y
        ghost_blue_hit_box = pygame.draw.circle (self.screen , "black" , self.Ghost_blue.ghost_rect.center ,
                                                 min (self.Ghost_blue.ghost_rect.width ,
                                                      self.Ghost_blue.ghost_rect.height) // 3)

        list.append(ghost_blue_hit_box)

        self.Ghost_red.ghost_rect.x = self.Ghost_red.x
        self.Ghost_red.ghost_rect.y = self.Ghost_red.y
        ghost_red_hit_box = pygame.draw.circle (self.screen , "black" , self.Ghost_red.ghost_rect.center ,
                                                min (self.Ghost_red.ghost_rect.width ,
                                                     self.Ghost_red.ghost_rect.height) // 3)

        list.append(ghost_red_hit_box)

        self.Ghost_pink.ghost_rect.x = self.Ghost_pink.x
        self.Ghost_pink.ghost_rect.y = self.Ghost_pink.y
        ghost_pink_hit_box = pygame.draw.circle (self.screen , "black" , self.Ghost_pink.ghost_rect.center ,
                                                min (self.Ghost_pink.ghost_rect.width ,
                                                     self.Ghost_pink.ghost_rect.height) // 3)

        list.append (ghost_pink_hit_box)

        self.Ghost_orange.ghost_rect.x = self.Ghost_orange.x
        self.Ghost_orange.ghost_rect.y = self.Ghost_orange.y
        ghost_orange_hit_box = pygame.draw.circle (self.screen , "black" , self.Ghost_orange.ghost_rect.center ,
                                                min (self.Ghost_orange.ghost_rect.width ,
                                                     self.Ghost_orange.ghost_rect.height) // 3)

        list.append (ghost_orange_hit_box)

        return list

    def buttons_menu(self,button_start_game,button_scoreboard,button_config):
        (x_mouse, y_mouse) = pygame.mouse.get_pos()
        button_start_game.enlarge_png(x_mouse, y_mouse, "buttons/big_button_start_game.png", 20, 5)
        button_scoreboard.enlarge_png(x_mouse, y_mouse, "buttons/big_button_scoreboard.png", 20, 5)
        button_config.enlarge_png(x_mouse,y_mouse,"buttons/big_button_rules.png", 10, 3)
        self.screen.fill("black")
        button_start_game.show_logo()
        button_start_game.show_button()
        button_scoreboard.show_button()
        button_config.show_button()
        self.screen.blit (self.coursor , (x_mouse , y_mouse))


    def Show_scoreboard(self,text_x=180,text_y = 45,number=1):
        with self.Scoreboard_path.open("r") as scoreboard_txt:
            content = json.load(scoreboard_txt)

        font = pygame.font.Font(None, 45)
        users_dict = sorted(content, key=lambda x: x['score'], reverse=True)

        for user in users_dict:
            if number <= 8:
                text_surface = font.render(f"{number}.  " + user['nick'], True, (255, 255, 255))
                text_rect = text_surface.get_rect()
                text_rect.topleft = (text_x, text_y)
                self.screen.blit(text_surface, text_rect)
                text_surface = font.render(str(user['score']), True, (255, 255, 255))
                text_rect = text_surface.get_rect()
                text_rect.topleft = (text_x + 330, text_y)
                self.screen.blit(text_surface, text_rect)
                text_surface = font.render("------------------------------------------------------------", True,
                                           '#f8ee39')
                text_rect = text_surface.get_rect()
                text_rect.topleft = (text_x - 100, text_y + 30)
                self.screen.blit(text_surface, text_rect)
                text_y += text_surface.get_height() + 45
                number += 1
            else:
                pass

    def Button_back(self,button_back):
        (x_mouse, y_mouse) = pygame.mouse.get_pos()
        button_back.enlarge_png(x_mouse, y_mouse, "buttons/big_back_button.png",10,5)
        button_back.show_button()
        pac_man_bg_image = pygame.transform.scale(pygame.image.load(self.Logo_path), (340, 140))
        self.screen.blit(pac_man_bg_image, (220, 630))


    def save_player(self,button_ok,player_full_score,win_or_lose):
        self.Level = 1
        self.player_lvl_up = False
        input_rect = pygame.Rect( 280 , 440 , 220 , 32 )
        color_active = pygame.Color( 'white' )
        color_passive = pygame.Color( '#444444' )
        with self.Scoreboard_path.open ("r") as input_file:
            data = json.load (input_file)
        color = color_passive
        good_length = False
        no_special_chars = False
        already_exists = False

        while self.run:
            self.screen.fill( "black" )

            (x_mouse , y_mouse) = pygame.mouse.get_pos( )
            for event in pygame.event.get( ):
                if event.type == pygame.QUIT:
                    self.run = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if button_ok.png_rect.collidepoint( event.pos ):
                        self.Ghost_speed = 1
                        self.Player_lives = 3
                        if self.User_name != "":
                            already_exists = self.check_user (data , self.User_name)
                            if re.match (self.pattern_length , self.User_name):
                                if not re.search (self.special_chars_pattern , self.User_name):
                                    new_player = {"nick": self.User_name , "score": player_full_score}

                                    good_length = False
                                    no_special_chars = False

                                    if already_exists is False:
                                        data.append (new_player)

                                        with self.Scoreboard_path.open ("w") as output_file:
                                            json.dump (data , output_file , indent=4)

                                        self.back_menu = True
                                        self.Game_on = False
                                        self.User_name = ""

                                        return
                                else:
                                    good_length = False
                                    no_special_chars = True
                            else:
                                no_special_chars = False
                                good_length = True
                        else:
                            self.back_menu = True
                            self.Game_on = False
                            return

                    if input_rect.collidepoint( event.pos ):
                        color = color_active
                    else:
                        color = color_passive

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        self.User_name = self.User_name[ :-1 ]
                    elif event.key == pygame.K_RETURN:
                        pass
                    else:
                        self.User_name += event.unicode

            if no_special_chars:
                font = pygame.font.Font (None , 25)

                text_surface = font.render ("No special characters!" , True , '#fcc92e')
                text_rect = text_surface.get_rect ( )
                text_rect.topleft = (300 , 480)
                self.screen.blit (text_surface , text_rect)

            if good_length:
                font = pygame.font.Font (None , 25)

                text_surface = font.render ("Name must contain from 4 to 12 characters! " , True , '#fcc92e')
                text_rect = text_surface.get_rect ( )
                text_rect.topleft = (210 , 480)
                self.screen.blit (text_surface , text_rect)

            if already_exists:
                font = pygame.font.Font (None , 25)

                text_surface = font.render ("Name in use!" , True , '#fcc92e')
                text_rect = text_surface.get_rect ( )
                text_rect.topleft = (330 , 480)
                self.screen.blit (text_surface , text_rect)

            font = pygame.font.Font( None , 75 )

            text_surface = font.render(win_or_lose, True, '#fcc92e')
            text_rect = text_surface.get_rect()
            text_rect.topleft = (265, 70)
            self.screen.blit(text_surface, text_rect)

            text_surface = font.render( "Your score is" , True , '#fcc92e' )
            text_rect = text_surface.get_rect( )
            text_rect.topleft = (220 , 140)
            self.screen.blit( text_surface , text_rect )

            text_surface = font.render( f"{player_full_score}" , True , '#fcc92e' )
            text_rect = text_surface.get_rect( )
            text_rect.topleft = (340 , 245)
            self.screen.blit( text_surface , text_rect )

            font = pygame.font.Font( None , 55 )

            text_surface = font.render( "Write your name " , True , '#fcc92e' )
            text_rect = text_surface.get_rect( )
            text_rect.topleft = (235 , 340)
            self.screen.blit( text_surface , text_rect )

            font = pygame.font.Font( None , 35 )

            pygame.draw.rect( self.screen , color , input_rect )
            text_surface = font.render( self.User_name , True , "black" )
            self.screen.blit( text_surface , (input_rect.x + 5 , input_rect.y + 5) )

            pac_man_bg_image = pygame.transform.scale( pygame.image.load( self.Logo_path ) , (340 , 140) )
            self.screen.blit( pac_man_bg_image , (225 , 640) )

            button_ok.enlarge_png( x_mouse , y_mouse , "buttons/big_button_ok.png" , 10 , 5 )
            button_ok.show_button( )
            self.screen.blit (self.coursor , (x_mouse , y_mouse))
            pygame.display.update( )

    def Space_to_start(self):
        font = pygame.font.Font ( None, 65 )
        text_surface = font.render ("HIT SPACE TO START", True, "#ff914d")
        text_rect = text_surface.get_rect ( )
        text_rect.topleft = (220, 500)
        self.screen.blit ( text_surface, text_rect )


    def check_user(self,data,player):
        for user in data:
            if player == user[ 'nick' ]:
                return True

        return False

