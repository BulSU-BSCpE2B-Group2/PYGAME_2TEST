import pygame as pg
import random
from os import path
from settings import *
from sprites import *
from start_screen import *
from game_over_screen import *
from pause_screen import *

RESET_SPEED_EVENT = pg.USEREVENT + 1

class Game:
    def __init__(self):
        # initialize game window, etc.
        pg.init()
        pg.mixer.init()
        self.screen = screen # add pg.FULLSCREEN if you want to full screen
        pg.display.set_caption(title)
        self.newPlatformInterval = 50
        self.currentInterval = 0
        self.highscore = load_hs_data()
        self.running = True

    def new(self):
        # starting a new game
        self.score = 0
        self.running = True
        self.multiplier = 1
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.slowplatformpowerup = pg.sprite.Group()
        self.player = Player(self)
        self.all_sprites.add(self.player)
        self.run()

    def run(self):
        # Game loop
        while self.running:
            clock.tick(fps)
            self.events()
            self.update()
            self.draw()

    def update(self):
        # game loop update
        # initialize variables needed for the function
        self.multiplier += 0.0008
        self.score += 1
        self.height_platform = 2
        self.speed = 2 * self.multiplier
        # if speed is more than 4, speed multiplier goes back to 0
        if self.speed > 4:
            self.multiplier = 1
        # gaps spawn function
        self.gaps = random.randint(1, 6)
        self.generate = random.randint(0, 4)
        self.currentInterval += 1
        if (self.currentInterval + self.speed) > self.newPlatformInterval:
            if not self.height_platform > 6:
                self.height_platform += 1
            sequence, rect = add_platform(self.gaps, self.height_platform)
            for x in sequence:
                if x == 1:
                    p = Platform(rect.center, (67, 20))
                    self.platforms.add(p)
                    self.all_sprites.add(p)
                    rect.width += 134
                else:
                    rect.width += 134
            self.currentInterval = 0
        # slow platform power up function spawn
            power_up, power_up_rect = spawn_power_up(self.generate, self.height_platform)
            for n in power_up:
                if n == 1:
                    slowplatform_powerup = SlowPlatformPowerUp(power_up_rect.center)
                    self.slowplatformpowerup.add(slowplatform_powerup)
                    self.all_sprites.add(slowplatform_powerup)
                    power_up_rect.width += 134
                else:
                    power_up_rect.width += 134

        # update number of platforms, update the player position
        self.player.update()
        self.platforms.update()
        self.slowplatformpowerup.update()

        # if power up leaves the screen, kill it.
        for slowdown_platform in self.slowplatformpowerup:
            slowdown_platform.rect.y -= self.speed
            if slowdown_platform.rect.top <= -20:
                slowdown_platform.kill()

        # if platform leaves the screen, kill it.
        for platform in self.platforms:
            platform.rect.y -= self.speed
            if platform.rect.top <= -20:
                platform.kill()

        # check if player hits a power_up
        slow_down_hit = pg.sprite.spritecollide(self.player, self.slowplatformpowerup, True)
        if slow_down_hit:
            self.multiplier = 0.5
            pg.time.set_timer(RESET_SPEED_EVENT, 6000)

        # check if player hits a platform - only if falling!
        if self.player.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                self.player.pos.y = hits[0].rect.top - self.speed
                self.player.vel.y = 0

        # if player reaches 1/4 from the bottom of the screen, camera should follow the player position
        if self.player.rect.bottom > (height / 4) * 3:
            self.score += 1
            self.currentInterval += 4
            for sprite in self.all_sprites:
                sprite.rect.y -= max(self.player.vel.y, 20)
                if sprite.rect.bottom < 10:
                    sprite.kill()

        # if player reaches spike, player dies.
        if self.player.rect.top < 0:
            self.running = False

        # for debugging purposes, do not remove yet.
        """print("Speed is: {}".format(self.speed))
        print("Speed multiplier is: {}".format(self.multiplier))
        print("Current interval is: {}".format(self.currentInterval))"""

    def events(self):
        # Game loop - EVENTS
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                self.running = False
            if event.type == RESET_SPEED_EVENT:
                self.multiplier = 1
                pg.time.set_timer(RESET_SPEED_EVENT, 0)
            if event.type == pg.KEYDOWN:
                # if escape it should go to the game over screen
                if event.key == pg.K_ESCAPE:
                    self.running = False
                elif event.key == pg.K_e:
                    # pressing 'e' should reset the game
                    self.platforms.empty()
                    self.new()
                # soon! pause feature.
                elif event.key == pg.K_SPACE:
                    self.pause_screen()
                    pass

    def draw(self):
        # Game loop for drawing graphics
        # the background is gray, will add animated background soon!
        self.screen.fill(gray)
        # draw and update all existing sprites on screen
        self.all_sprites.draw(self.screen)
        # draw and update the score
        draw_text(str(self.score), 22, white, WIDTH / 2, 50)
        # *after* drawing everything, flip the display for changes to take effect on the window
        pg.display.flip()

    def pause_screen(self): # does not work yet, will edit soon!
        clock.tick(fps)
        self.pause = fade_pause_animation()
        return self.pause


# turn 'g' into an object of Game class, essentially initializing pygame
g = Game()
# loop that makes restarting work. will only be broken by break statements
while True:
    # assign show_start_screen() to run variable to tell whether the return value of show_start_screen()/
    # / is true or false
    run = show_start_screen()
    # if show_start_screen() returned false, break the loop, ending the program.
    if not run:
        break
    # else, initialize the game loop (which is the 'new' function) inside the Game class
    else:
        while run:
            start_game_animation_sequence()
            g.new()
            # if player dies, game over screen shows, show_go_screen tells restart whether or not it wants to
            # restart or not (True or False statement gate again)
            restart = show_go_screen(g.score, g.highscore)
            # if you want to restart, run sets to true then loop happens all over again.
            if restart:
                run = True
            # it puts you back to the outer loop, showing you the start_screen and giving you another choice to
            # start the game or completely exit.
            else:
                break
pg.quit()
