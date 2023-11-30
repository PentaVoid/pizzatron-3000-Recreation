#ideas!
#use a dictionary for orders, that way it's easier to pull up info about each one
#might be worth making a physical sketch of how it's going to look, just so i know coords regarding bins, edges, and sizes
#conveyor belt will be a loop of drawing things, just a grey rect with diagonal lines that update across
#used an external varible with the dough sprite to cchange appearance
#import the pygame module and random
import pygame
import random

#import pygame locals for easy access to key coordinates
from pygame.locals import (K_ESCAPE, KEYDOWN, QUIT)

#initialize pygame
pygame.init()

#Define constants for screen width and height
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

#Create the screen object (size determined by width and height)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

#as a note, user gets 10-11 seconds to do a pizza at the start

#Start a count of how many pizzas have gone by in total
loop_count = 0

#set up some custom events that replenish toppings and dough base
ADDDOUGH = pygame.USEREVENT + 1
pygame.time.set_timer(ADDDOUGH, 11400)
ADDTOPPING = pygame.USEREVENT + 2
pygame.time.set_timer(ADDTOPPING, 100)

#variable to keep the main loop running
running = True

#define the dough object by extending pygame.sprite.Sprite
#The surface drawn on screen is now an attribute of 'dough'
class Dough(pygame.sprite.Sprite):
  def __init__(self):
    super(Dough, self).__init__()
    self.surf = pygame.Surface((175, 100))
    self.surf.fill((209, 160, 96))
    #randomly generate start position and speed
    self.rect = self.surf.get_rect(center = (-100, 350, ))

  #move sprite based on completion and delete once it goes off the right edge of the screen
  def update(self, x_speed):
    self.rect.move_ip(x_speed, 0)
    if self.rect.left > 800:
      self.kill()

#define the topping class (it's a blueprint for all the basic topics)
class Topping(pygame.sprite.Sprite):
  def __init__(self, type, size, colour, start):
    super(Topping, self).__init__()
    self.surf = pygame.Surface(size)
    self.surf.fill(colour)
    self.type = type
    #draw at right position
    self.rect = self.surf.get_rect(center = start)

  #move sprite based on where it is and delete once it goes off the right edge of the screen
  def update(self, x_speed, y_speed):
    self.rect.move_ip(x_speed, y_speed)
    if self.rect.left > 800 or self.rect.top > 600:
      self.kill()

#might need a new class for the bins, so that i can check collisions and then generate a new topping based on that

#Set up the variable for the drag and drop system
active_box = None

#the big list of orders, brace yo self
possible_orders = [[0, 0, 1, 0, 0, 0, 0], [0, 0, 1, 1, 0, 0, 0], [0, 0, 1, 2, 0, 0, 0], [0, 0, 2, 2, 0, 0, 0]]

#initialize some lists and counter variables
#order is as follows: [sauce, hot sauce, cheese, seaweed, shrimp, squid, fish]
order = [0, 0, 0, 0, 0, 0, 0]
on_pizza = [0, 0, 0, 0, 0, 0, 0]
score = 0
mistakes = 0
order_done = False

#create groups to hold  all sprites
#groups are for collision detection and position updates
#all_sprites is used for rendering
doughs = pygame.sprite.Group()
cheeses = pygame.sprite.Group()
seaweeds = pygame.sprite.Group()
shrimps = pygame.sprite.Group()
squids = pygame.sprite.Group()
fish = pygame.sprite.Group()
toppings_on = pygame.sprite.Group()
fallen = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()

#Setup clock for a decent framerate
clock = pygame.time.Clock()

#main loop
while running:
  #Get and print mouse position
  pos = pygame.mouse.get_pos()
  print(pos)

  #look at every event in the queue
  for event in pygame.event.get():

    #did the user hit a key?
    if event.type == KEYDOWN:
      #if escape key, stop loop
      if event.key == K_ESCAPE:
        running = False

    #stop the loop if the user closes the window    
    elif event.type == QUIT:
      running = False

    #Add a new dough?
    elif event.type == ADDDOUGH:
      #create the new dough and add it to sprite groups
      new_dough = Dough()
      doughs.add(new_dough)
      all_sprites.add(new_dough)
      #if it's not the first pizza, check for mistakes: if mistakes reaches 5, the game ends
      if loop_count != 0:
        if order_done == False:
          mistakes += 1
          if mistakes == 5:
            running = False
      #reset other variables for the new pizza, like order and what's on it
      on_pizza = [0, 0, 0, 0, 0, 0, 0]
      order_done = False
      loop_count += 1
      #randomly pick an order based on how many pizzas the user has completed
      if score < 5:
        order_num = random.randint(0, 1)
        order = possible_orders[order_num]
      else:
        order_num = random.randint(0, 3)
        order = possible_orders[order_num]

    #replenish all toppings (self, type, size, colour, start), then add them to their respective groups
    elif event.type == ADDTOPPING:
      new_cheese = Topping("CHEESE", (75, 35), (255, 255, 0), (300,100, ))
      cheeses.add(new_cheese)
      all_sprites.add(new_cheese)

      new_seaweed = Topping("SEAWEED", (75, 35), (0, 100, 0), (600, 100, ))
      seaweeds.add(new_seaweed)
      all_sprites.add(new_seaweed)

    #the user clicks down
    elif event.type == pygame.MOUSEBUTTONDOWN:
      if event.button == 1:
        #check what the user clicked on
        for cheese in cheeses:
          if cheese.rect.collidepoint(pos) == True:
            active_box = cheese

        for seaweed in seaweeds:
          if seaweed.rect.collidepoint(pos) == True:
            active_box = seaweed

    #the user moves the mouse
    elif event.type == pygame.MOUSEMOTION:
      if active_box != None:
        #move the held topping with the mouse
        active_box.rect.move_ip(event.rel)

    #the user lets go of the mouse button
    elif event.type == pygame.MOUSEBUTTONUP:
      if event.button == 1:
        if active_box != None:
          #check if a topping was placed on the dough, if so then update what's on the pizza
          if pygame.sprite.spritecollideany(active_box, doughs):
            if order_done != True:
              toppings_on.add(active_box)
              if active_box.type == "CHEESE":
                on_pizza[2] += 1
              elif active_box.type == "SEAWEED":
                on_pizza[3] += 1
              active_box = None

              #if the user successfully completes the order, add to the score
              if on_pizza == order:
                score += 1
                order_done = True
              else:
                order_done = False

            #if the order is done, don't let any more toppings go on the pizza    
            else:
              fallen.add(active_box)
              active_box = None

          #if the user drops the topping on nothing, it falls down and can't be used again
          else:
            fallen.add(active_box)
            active_box = None

  #get the set of keys pressed and check for user input
  pressed_keys = pygame.key.get_pressed()

  #move the pizza based on completion
  if order_done == False:
    doughs.update(2)
    toppings_on.update(2, 0)
  else:
    doughs.update(9)
    toppings_on.update(9, 0)

  

  #make all dropped toppings fall down
  for topping in fallen:
    topping.update(0, 5)

  #fill the screen with dark blue
  screen.fill((0, 0, 30))

  # Select the font to use, size, bold, italics
  #display the score, mistakes, what's on the pizza, and what needs to go on the pizza
  font = pygame.font.SysFont('Comic Sans MS', 25, True, False)
  text = font.render("Score: {0}".format(score), True, (0, 255, 255))
  screen.blit(text, [350, 250])
  text2 = font.render("{0} : {1}".format(on_pizza, order), True, (0, 255, 255))
  screen.blit(text2, [350, 200])
  text2 = font.render("Mistakes: {0}".format(mistakes), True, (0, 255, 255))
  screen.blit(text2, [350, 150])

  #draw all sprites on the screen
  for entity in all_sprites:
    screen.blit(entity.surf, entity.rect)

  #Update the display
  pygame.display.flip()

  #ensure program maintains a rate of 60 frames per second
  clock.tick(60)
