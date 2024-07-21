"""
This module is used to hold the Player class. The Player represents the user-
controlled sprite on the screen.
"""
import pygame

import constants

from platforms import MovingPlatform
from spritesheet_functions import SpriteSheet

class Player(pygame.sprite.Sprite):
    """ This class represents the bar at the bottom that the player
    controls. """

    # -- Attributes
    # Set speed vector of player
    change_x = 0
    change_y = 0

    # This holds all the images for the animated walk left/right
    # of our player
    walking_frames_l = []
    walking_frames_r = []

    # What direction is the player facing?
    direction = "R"

    # List of sprites we can bump against
    level = None

    # -- Methods
    def __init__(self):
        """ Constructor function """

        # Call the parent's constructor
        pygame.sprite.Sprite.__init__(self)
        player_w=134-4
        player_h=198+2
        sprite_sheet = SpriteSheet("template_char.png")
        # Load all the right facing images into a list
      
        image = sprite_sheet.get_image(0, 0, player_w, player_h)
        image = pygame.transform.scale(image, (player_w*3,player_h*3))
        self.walking_frames_r.append(image)
        
        image = sprite_sheet.get_image(player_w, 0,player_w, player_h)
        image = pygame.transform.scale(image, (player_w*3,player_h*3))
        self.walking_frames_r.append(image)
        
        image = sprite_sheet.get_image(player_w*2, 0, player_w, player_h)
        image = pygame.transform.scale(image, (player_w*3,player_h*3))
        self.walking_frames_r.append(image)
        
        image = sprite_sheet.get_image(0, player_h, player_w, player_h)
        image = pygame.transform.scale(image, (player_w*3,player_h*3))
        self.walking_frames_r.append(image)
        
        image = sprite_sheet.get_image(player_w, player_h, player_w, player_h)
        image = pygame.transform.scale(image, (player_w*3,player_h*3))
        self.walking_frames_r.append(image)
        
        image = sprite_sheet.get_image(player_w*2, player_h, player_w, player_h)
        image = pygame.transform.scale(image, (player_w*3,player_h*3))
        self.walking_frames_r.append(image)

        image = sprite_sheet.get_image(0, 2*player_h, player_w,player_h)
        image = pygame.transform.scale(image, (player_w*3,player_h*3))
        self.walking_frames_r.append(image)

        #        # Load all the right facing images, then flip them
        # to face left.
        image = sprite_sheet.get_image(0, 0, player_w, player_h)
        image = pygame.transform.scale(image, (player_w*3,player_h*3))
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)
        
        image = sprite_sheet.get_image(player_w, 0,player_w, player_h)
        image = pygame.transform.scale(image, (player_w*3,player_h*3))
        self.walking_frames_l.append(image)
        
        image = sprite_sheet.get_image(player_w*2, 0, player_w, player_h)
        image = pygame.transform.scale(image, (player_w*3,player_h*3))
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)
        
        image = sprite_sheet.get_image(0, player_h, player_w, player_h)
        image = pygame.transform.scale(image, (player_w*3,player_h*3))
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)
        
        image = sprite_sheet.get_image(player_w, player_h, player_w, player_h)
        image = pygame.transform.scale(image, (player_w*3,player_h*3))
        image = sprite_sheet.get_image(player_w*2, player_h, player_w, player_h)
        image = pygame.transform.scale(image, (player_w*3,player_h*3))
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)

        image = sprite_sheet.get_image(0, 2*player_h, player_w,player_h)
        image = pygame.transform.scale(image, (player_w*3,player_h*3))
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)

        # Set the image the player starts with
        self.image = self.walking_frames_r[0]

        # Set a referance to the image rect.
        self.rect = self.image.get_rect()

    def update(self):
        """ Move the player. """
        # Gravity
        self.calc_grav()

        # Move left/right
        self.rect.x += self.change_x
        pos = self.rect.x + self.level.world_shift
        if self.direction == "R":
            frame = (pos // 30) % len(self.walking_frames_r)
            self.image = self.walking_frames_r[frame]
        else:
            frame = (pos // 30) % len(self.walking_frames_l)
            self.image = self.walking_frames_l[frame]

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
     #   if self.change_y>0:
     #      frame = (pos // 30) % len(self.jumping_frames)
     #      self.image = self.jumping_frames   
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
            self.change_y = -10

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
