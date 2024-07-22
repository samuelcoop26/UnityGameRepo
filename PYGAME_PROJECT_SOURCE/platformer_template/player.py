"""
This module is used to hold the Player class. The Player represents the user-
controlled sprite on the screen.
"""
import pygame

import constants

from platforms import MovingPlatform
from spritesheet_functions import SpriteSheet

player_scale=2

def sprite_parse_walk(self,sprite_sheet, player_bounds):
    #Right facing:
    right_facing_list=[]
    left_facing_list=[]
    walking_frames_r=[]
    walking_frames_l=[]
    for i in range(0, len(player_bounds)):
        image = sprite_sheet.get_image(player_bounds[i][0], player_bounds[i][1], player_bounds[i][2], player_bounds[i][3])
        image = pygame.transform.scale(image, (player_bounds[i][2]*player_scale,player_bounds[i][3]*player_scale))
          #  self.walking_frames_r.append(image)
        right_facing_list.append(image)
        self.walking_frames_r.append(image)
        image = pygame.transform.flip(image, True, False)
        left_facing_list.append(image)
        self.walking_frames_l.append(image)
    return [right_facing_list, left_facing_list]

def sprite_parse_jump(self,sprite_sheet, player_bounds):
    #Right facing:
    right_facing_list=[]
    left_facing_list=[]
    #jumping_frames_r=[]
    #jumping_frames_l=[]
    for i in range(0, len(player_bounds)):
        image = sprite_sheet.get_image(player_bounds[i][0], player_bounds[i][1], player_bounds[i][2], player_bounds[i][3])
        image = pygame.transform.scale(image, (player_bounds[i][2]*player_scale,player_bounds[i][3]*player_scale))
          #  self.walking_frames_r.append(image)
        right_facing_list.append(image)
        self.jumping_frames_r.append(image)
        image = pygame.transform.flip(image, True, False)
        left_facing_list.append(image)
        self.jumping_frames_l.append(image)
    return [self.jumping_frames_l, self.jumping_frames_r]


class Player(pygame.sprite.Sprite):
    """ This class represents the bar at the bottom that the player
    controls. """

    # -- Attributes
    # Set speed vector of player
    change_x = 0
    change_y = 0
    frameh=0
    # This holds all the images for the animated walk left/right
    # of our player
    walking_frames_l = []
    walking_frames_r = []
    jumping_frames_l=[]
    jumping_frames_r=[]
    # What direction is the player facing?
    direction = "R"
    jump_switch=0
    # List of sprites we can bump against
    level = None
    
    # -- Methods
    def __init__(self):
        """ Constructor function """
        frameh=0
        # Call the parent's constructor
        pygame.sprite.Sprite.__init__(self)
        player_w=134-4
        player_h=198+2
        sprite_sheet = SpriteSheet("template_char.png")
        jumping_sprite_sheet=SpriteSheet("jumping_char.png")
        # Load all the right facing images into a list
        #Right facing running animiations:
        player_bounds=[[0,0,player_w,player_h],[player_w, 0, player_w,player_h],[player_w*2,0,player_w,player_h],[0, player_h, player_w, player_h],[player_w,player_h,player_w,player_h],[player_w*2, player_h, player_w, player_h],[0,2*player_h,player_w,player_h],[player_w,2*player_h,player_w,player_h],[2*player_w,2*player_h, player_w, player_h],[0,3*player_h,player_w, player_h],[player_w,3*player_h,player_w, player_h]]
       
        jumping_bounds=[[0,19,133,171],[125,0,142,190],[265,0,126,190],[0,200,124,200],[124,200,124,200],[257,190,134,210],[257,190,134,210],[257,190,134,210],[257,190,134,210],[257,190,134,210],[257,190,134,210]]
        
        walking_frames_r=sprite_parse_walk(self,sprite_sheet,player_bounds)[0]
        walking_frames_l=sprite_parse_walk(self,sprite_sheet,player_bounds)[1]
        self.jumping_frames_r=sprite_parse_jump(self, jumping_sprite_sheet, jumping_bounds)[1]
        self.jumping_frames_l=sprite_parse_jump(self, jumping_sprite_sheet, jumping_bounds)[0]
        # Set the image the player starts with
        self.image = self.walking_frames_r[0]
        # Set a referance to the image rect.
        self.rect = self.image.get_rect()

    def update(self):
        """ Move the player. """
        # Gravity`
        self.calc_grav()
        # Move left/right
        self.rect.x += self.change_x
        pos = self.rect.x + self.level.world_shift
        height= constants.SCREEN_HEIGHT  - self.rect.y

        if self.jump_switch==0:
            frameh=0
            if self.direction == "R":
                frame = (pos // 30) % len(self.walking_frames_r)
                self.image = self.walking_frames_r[frame]
            elif self.direction=="L":
                frame = (pos // 30) % len(self.walking_frames_l)
                self.image = self.walking_frames_l[frame]
        #if self.jump_switch==1:
            #for frame in range(0,len(self.jumping_frames_r)):
            
            #frameh=(height // 15) % len(self.jumping_frames_r)
        if self.jump_switch==1:
            frameh=0
            if self.direction=="L":
                #print(self.frameh)
                frameh = (height // 40) % len(self.jumping_frames_l)
                #print(frame)
                self.image=self.jumping_frames_l[frameh]
            elif self.direction=="R":
                frameh = (height // 40) % len(self.jumping_frames_r)
                #print(frame)
                self.image=self.jumping_frames_r[frameh]
            elif self.change_x==0:
                frameh = (height // 40) % len(self.jumping_frames_r)
                self.image=self.jumping_frames_r[frameh]
            
            print(frameh)

        #if self.frameh==6: self.frameh=0
        if self.change_y==0: 
            self.jump_switch=0
            frameh=0
        if self.change_x==0 and self.direction=="R": self.image=self.walking_frames_r[0]
        if self.change_x==0 and self.direction=="L": self.image=self.walking_frames_l[0]
        # See if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            # If we are moving right,
            # set our right side to the left side of the item we hit
            if self.change_x > 0:
                self.rect.right = block.rect.left
            elif self.change_x < 0:
                # Otherwise if we are moving left, do the opposite.
                self.rect.left = block.rect.right

        # Move up/down
        self.rect.y += self.change_y
        # Check and see if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:

            # Reset our position based on the top/bottom of the object.
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom

            # Stop our vertical movement
            self.change_y = 0
            if isinstance(block, MovingPlatform):
                self.rect.x += block.change_x
    def calc_grav(self):
        """ Calculate effect of gravity. """
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += .35

        # See if we are on the ground.
        if self.rect.y >= constants.SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = constants.SCREEN_HEIGHT - self.rect.height

    def jump(self):
        """ Called when user hits 'jump' button. """
               # move down a bit and see if there is a platform below us.
        # Move down 2 pixels because it doesn't work well if we only move down 1
        # when working with a platform moving down.
        self.rect.y += 4
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.rect.y -= 4
    
        # If it is ok to jump, set our speed upwards
        if len(platform_hit_list) > 0 or self.rect.bottom >= constants.SCREEN_HEIGHT:
            self.change_y = -20
            self.jump_switch=1
                       # Player-controlled movement:
    def go_left(self):
        """ Called when the user hits the left arrow. """
        self.change_x = -9
        self.direction = "L"

    def go_right(self):
        """ Called when the user hits the right arrow. """
        self.change_x = 9
        self.direction = "R"

    def stop(self):
        """ Called when the user lets off the keyboard. """
        self.change_x = 0
