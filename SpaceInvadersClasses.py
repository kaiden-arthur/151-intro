'''
This file holds the code for all the classes the SpaceInvaders program runs on. 
'''

#imports
from pgl import GImage, GRect

class Ship(GImage):
    '''
    A generic ship, which uses a GImage as the base. 
    '''
    def __init__(self, image, x=0, y=0, points=0):
        '''Creates a Ship object with the specified attributes.'''
        GImage.__init__(self, image,x,y)
        self.x = x
        self.y = y
        self.dx = 1
        self.dy = 2
        self.points = points

    def __str__(self):
        '''Returns a string representation of the object.'''
        return f"A Ship object worth {self.points} points, which starts at {self.x}, {self.y}."

    def is_hit(self):
        '''Tells the ship how to react when it's hit by a bullet.'''
        self.use_alternate_image()
        self.gw.set_timeout(self.remove_self_action, 50)
    
    def use_alternate_image(self):
        '''Overlays the alternate image on the ship's location.'''
        x = self.get_x()
        y = self.get_y()
        self.gw.add(self.alt,x,y)
        

    def remove_self_action(self):
        '''Called by the timer to remove the ship from the screen.'''
        self.gw.remove(self.alt)
        self.gw.remove(self)

    def set_alternate_image(self, alt):
        '''Sets the alternate image file of the ship.'''
        self.alt = GImage(alt)

    def remove_alt(self):
        '''Removes the alternate image file from the screen.
        A seperate function so it can be called by a timer.'''
        self.gw.remove(self.alt)
    
    def move_horizontal(self):
        '''Moves the ship in the horizontal direction, by the self.dx variable.'''
        self.move(self.dx,0)
        if self.get_x() <= 10 or self.get_x() >= 640:
            self.dx = -self.dx

    def move_vertical(self):
        '''Moves the ship in the vertical direction, by the self.dy variable.'''
        self.move(0, self.dy)
        self.dx = -self.dx

    def shoot(self):
        '''Fires a Bullet-type object, if there are no other ships in the way of the bullet.'''
        if self.no_obstructions() == True:
            bullet_x = self.get_x() + self.get_width()/2
            bullet_y = self.get_y() + (self.get_height()- 5)
            #bullet creation 
            self.bullet = Bullet(2, 5)
            self.bullet.set_color("white")
            self.bullet.set_filled(True)
            self.bullet.set_gw(self.gw)
            self.bullet.set_background(self.background)
            self.bullet.set_type("alien")
            self.gw.add(self.bullet, bullet_x, bullet_y)
            #start bullet moving 
            self.bullet.set_firing(True)
            self.gw.set_interval(self.bullet.firing, 30)

    def no_obstructions(self):
        '''Determines if there are any objects (other than the background) 
        below the ship; stops checking at the level of the bulwarks.'''
        i = self.get_y() + self.get_height() + 2
        x = self.get_x() + self.get_width()/2
        state = True
        while i < 510:
            obstruction = self.gw.get_element_at(x,i)
            if obstruction != self.background:
                state = False
            i += 10
        return state

    def set_gw(self,gw):
        '''Sets the GWindow the ship can affect.'''
        self.gw = gw
    
    def set_speed(self,speed):
        '''Sets the horizontal speed of the ship.'''
        self.dx = speed

    def set_background(self, background):
        '''Sets the object used as the background 
        (typically used so detections will ignore it when looking for objects).'''
        self.background = background

    def get_array(self):
        '''Returns the pixel array of the image.'''
        self.array = self.get_pixel_array()
        return self.array

    def get_points(self):
        '''Returns the number of points associated with the ship.'''
        return self.points

    def add_points(self, points):
        '''Adds a desgnated number of points to the ship's point count.'''
        self.points += points 
                

class Bulwark(Ship):
    '''
    This class inherits from the generic Ship class. 
    It forms the barricades near the base of the screen.
    '''
    def __init__(self, image,lives,x=0,y=0,):
        '''Creates a Bulwark object with the given attributes.'''
        Ship.__init__(self, image,x,y)
        self.lives = lives

    def __str__(self):
        '''Returns a string representation of the object.'''
        return f"A Bulwark object with {self.lives} lives, at {self.x}, {self.y}."

    def is_hit(self):
        '''Tells the Bulwark what to do when hit by a bullet.'''
        self.lives -=1
        self.use_alternate_image()
        self.gw.set_timeout(self.remove_alt, 100)
        if self.lives == 0:
            self.gw.remove(self)

    def get_lives(self):
        '''Returns the number of lives the Bulwark has.'''
        return self.lives


class Player(Bulwark):
    '''
    This class inherits from the Bulwark class, since it has a relevant number of lives. 
    It is the type of Ship controlled by the player. 
    '''
    def __init__(self, image,lives=3,x=0,y=0,):
        '''Creates a Player object with the given attributes.'''
        Bulwark.__init__(self, image,lives,x,y)

    def __str__(self):
        '''Returns a string representation of the object.'''
        return f"A Player-ship object with {self.lives} lives, at {self.x}, {self.y}."

    def create_bullet(self, speed):
        '''Creates a Bullet-type object and adds it to the screen.'''
        #create a bullet 
        bullet_x = self.get_x() + self.get_width()/2
        bullet_y = self.get_y() - (self.get_height() - 5)
        self.bullet = Bullet(2, 5)
        self.bullet.set_color("white")
        self.bullet.set_filled(True)
        self.bullet.set_gw(self.gw)
        self.bullet.set_type("player")
        self.bullet.set_ship(self)
        self.bullet.set_background(self.background)
        self.gw.add(self.bullet, bullet_x, bullet_y)
        self.bullet.set_speed(speed)

    def fire_bullet(self):
        '''Takes a previously-created Bullet-type object and sets an interval timer
        so it fires.'''
        #it goes
        self.bullet.set_firing(True)
        self.gw.set_interval(self.bullet.firing, 30)


class Bullet(GRect):
    '''
    BULLET CLASS, SO THE SHIPS CAN HAVE GUNS
    This class inherits from the GRectangle class, 
    and is what is created when a ship fires.
    '''
    def __init__(self, width, height, x=0, y=0, speed=5):
        '''Creates a Bullet object with the designated attributes.'''
        GRect.__init__(self,width, height)
        self.dy = speed
        self.count = 0

    def __str__(self):
        '''Returns a string representation of the object.'''
        return f"A Bullet object with a speed of {self.dy}."

    def set_gw(self, gw):
        '''Sets the GWindow the bullet can affect.'''
        self.gw = gw

    def set_background(self, background):
        '''Sets the object used as the background 
        (typically used so detections will ignore it when looking for objects).'''
        self.background = background

    def set_speed(self, speed):
        '''Sets the firing speed of the Bullet object.'''
        self.dy = speed

    def set_type(self, type):
        '''Sets the type of the bullet:
        in this project either "alien" or "player"'''
        self.type = type

    def set_ship(self, ship):
        '''Sets which ship the Bullet object is associated with.'''
        self.ship = ship

    def get_ship(self):
        '''Returns the Ship object the Bullet is associated with.'''
        return self.ship

    def set_firing(self, state):
        '''Sets the firing state of the Bullet, either True or False.'''
        self.is_firing = state
    
    def firing(self):
        '''Function called when the bullet is moving.
        Checks for objects in contact, and triggers said object's is_hit function.'''
        if self.is_firing:
            #move, check for 
            self.move(0, self.dy)
            if self.get_y() >= 700 or self.get_y() <= 0:
                self.set_speed(0)
                self.gw.remove(self)
            #effects of alien bullet 
            if self.type == "alien":
                if self.get_y() >= 510:
                    x = self.get_x()
                    y = self.get_y() + self.get_height()
                    obj = self.gw.get_element_at(x,y)
                    try:
                        #effects on object if present
                        if obj != self.background and obj is not None:
                            self.set_firing(False)
                            self.gw.remove(self)
                            obj.is_hit()
                    #It kept running into None-type objects, for some reason, 
                    #so this bypasses that. 
                    except AttributeError:
                        pass
            #effects of player ship bullets
            if self.type == "player":
                if self.get_y() <= 510:
                    x = self.get_x()
                    y = self.get_y() + self.get_height()
                    obj = self.gw.get_element_at(x,y)
                    try:
                        #effects on object if present 
                        if obj != self.background and obj is not None:
                            self.points = obj.get_points()
                            ship = self.get_ship()
                            ship.add_points(self.points)
                            obj.is_hit()
                            self.set_firing(False)
                            self.gw.remove(self)
                    #(as above)
                    except AttributeError:
                        pass
                