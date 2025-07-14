'''
This program emulates the 1978 video game Space Invaders, which was originally
an arcade cabinet and later released for Atari and Nintendo consoles, 
among others. 
It reads in information from a companion file. 
'''

#imports
from pgl import GWindow, GRect, GLabel, GImage
from SpaceInvadersClasses import Ship, Bulwark, Player
from tokenscanner import TokenScanner

def SpaceInvaders(file):
    '''
    The main function of the Space Invaders program. 
    It sets up the board and runs the game. 
    '''

    '''DEFINING FUNCTIONS:'''

    def read_file(f):
        '''Reads in the information in the starting setup file. 
        Returns a dictionary.'''
        file = {}
        finished = False
        while not finished:
            line = f.readline().rstrip()
            if line == "":
                finished = True
                pass
            else:
                colon = line.find(":")
                key = line[:colon]
                data = line[colon+1:]
                if len(data) > 1:
                    info = []
                    scanner = TokenScanner(data)
                    scanner.addWordCharacters("-")
                    while scanner.hasMoreTokens():
                        token = scanner.nextToken()
                        #extracts data, using dashes to seperate values
                        if token != " " and token != "":
                            dash = token.find("-")
                            #if the data is a single number:
                            if dash == -1:
                                info.append(int(token))
                            #if the data has more than one value:
                            else: 
                                x = int(token[:dash])
                                dash2 = token.rfind("-")
                                #for two-digit coordinates:
                                if dash2 == dash:
                                    y = int(token[dash+1:])
                                    z = 0
                                #for three-digit coordinates:
                                else:
                                    y = int(token[dash+1:dash2])
                                    z = int(token[dash2+1:])
                                coord = (x,y,z)
                                info.append(coord)
                file[key] = info
        return file

    def start_aliens_moving(e):
        '''This function is activated when the player clicks on the screen. 
        It adds timers so the aliens will move and shoot automatically.'''
        #remove instructions
        gw.remove(click_prompt)
        gw.remove(controls)
        #cycles through and initializes aliens 
        for i in range(5):
            for j in alienlocs[i]:
                x = j[0] + 1
                y = j[1] + 1
                alien = gw.get_element_at(x,y)
                if alien != background:
                    #odd-numbered rows start with negative dx
                    if i == 1 or i == 3:
                        alien.dx = -alien.dx
                    #timers
                    gw.set_interval(alien.shoot, 3000)
                    gw.set_interval(alien.move_horizontal, 30)
                    gw.set_interval(alien.move_vertical, 2000)

    def key_action(e):
        '''This function is called when a key is pressed. 
        It is the foundation of player interactivity in the game.'''
        char = e.get_key()
        #move left: a
        if char == "a":
            player.set_speed(-20)
            player.move_horizontal()
        #move right: d
        if char == "d":
            player.set_speed(20)
            player.move_horizontal()
        #firing a bullet 
        if char == "w":
            #gun time
            player.create_bullet(-5)
            player.fire_bullet()

    def remove_all():
        '''This function removes all bulwarks and the player from the screen. 
        It is called when the player loses the game.'''
        for x in range(0,700,50):
            for y in range(500,700,50):
                obj = gw.get_element_at(x,y)
                if obj != background:
                    gw.remove(obj)

    def check_points():
        '''This function maintains the points counter.'''
        #checks points
        points = player.get_points()
        #label creation
        points_label = GLabel(f"SCORE: {points:>5}")
        points_label.set_font('20px "sans-serif"')
        points_label.set_color('white')
        points_x = 10
        points_y = points_label.get_ascent() + 10
        obj = gw.get_element_at(points_x, points_y)
        #removes previous label
        if obj != background:
            gw.remove(obj)
        #adds new label
        gw.add(points_label, points_x, points_y)
        #win condition and announcement:
        if points == (30*7 + 20*14 + 10*14):
            win_label = GLabel("CONGRATULATIONS!")
            win_label.set_font('50px "sans-serif"')
            win_x = (700 - win_label.get_width()) / 2
            win_y = 250
            win_label.set_color('white')
            gw.add(win_label, win_x, win_y)
            lives = player.get_lives()
            result_to_file("win", lives, points)

    def check_lives():
        '''This function maintains the life counter.'''
        #checks lives
        lives = player.get_lives()
        #label creation
        lives_label = GLabel(f"LIVES: {lives:>2}")
        lives_label.set_font('20px "sans-serif"')
        lives_label.set_color('white')
        lives_x = 700 - (lives_label.get_width() + 10)
        lives_y = lives_label.get_ascent() + 10
        obj = gw.get_element_at(lives_x, lives_y)
        #removes previous label
        if obj != background:
            gw.remove(obj)
        #adds new label 
        gw.add(lives_label, lives_x, lives_y)
        #lose condition and announcement:
        if lives == 0:
            remove_all()
            lose_label = GLabel("BETTER LUCK NEXT TIME.")
            lose_label.set_font('50px "sans-serif"')
            lose_x = (700 - lose_label.get_width()) / 2
            lose_y = 500
            lose_label.set_color('white')
            gw.add(lose_label, lose_x, lose_y)
            points = player.get_points()
            result_to_file("lose", lives, points)

    def result_to_file(condition, lives, points):
        '''This function takes the final conditions of the game and prints them to a file.'''
        with open("Results.txt", "w") as fh:
            if condition == "win":
                result = "Congratulations! You vanquished the alien threat."
                string = f"You earned {points} points and had {lives} lives left."
            if condition == "lose":
                result = "You fell to the alien invaders. Better luck next time."
                string = f"You earned {points} points before you fell."
            fh.write(result + '\n')
            fh.write(string)


    '''MAIN PROGRAM: INITIALIZATION AND RUNNING'''
    #try statement enables file names defined incorrectly
    try: 
        with open(file) as f:
            '''READ IN CONSTANTS'''
            data = read_file(f)
            playerstart = data["player position"]
            bulwarklocs = data["bulwark locations"]
            alienlocs = [data["row" + str(i+1)] for i in range(5)]
            alienpoints = [data["alien" + str(i+1) + " points"] for i in range(3)] #this is a nested list!
            bulwark_lives = data["bulwark lives"]

            '''WINDOW AND OBJECT CREATION'''
            #window creation
            gw = GWindow(700,700)
            background = GRect(700,700)
            background.set_filled(True)
            gw.add(background)

            #prompt to click to start
            click_prompt = GLabel("CLICK ANYWHERE TO BEGIN")
            click_prompt.set_font('30px "sans-serif"')
            label_x = (700 - click_prompt.get_width()) / 2
            label_y = 440
            click_prompt.set_color('#54f7d0')
            gw.add(click_prompt, label_x, label_y)

            #controls label
            controls = GLabel("Use A and D to move, and W to shoot.")
            controls_x = (700 - controls.get_width()) / 2
            controls_y = 480
            controls.set_color('white')
            gw.add(controls, controls_x, controls_y)
    
            #defining aliens
            for i in range(5):
                for j in alienlocs[i]:
                    x = j[0]
                    y = j[1]
                    #first two rows
                    if i == 0 or i == 1:
                        img = "alien1.png"
                        points = alienpoints[0][0]
                        alien = Ship(img, x, y,points)
                        alien.set_alternate_image("alien1.red.png")
                    #second set of rows
                    elif i == 2 or i == 3:
                        img = "alien2.png"
                        points = alienpoints[1][0]
                        alien = Ship(img, x, y,points)
                        alien.set_alternate_image("alien2.red.png")
                    #final rows
                    else:
                        img = "alien3.png"
                        points = alienpoints[2][0]
                        alien = Ship(img, x, y,points)
                        alien.set_alternate_image("alien3.red.png")
                    alien.set_gw(gw)
                    alien.set_background(background)
                    #add them
                    gw.add(alien)

            #defining and adding bulwarks
            for i in bulwarklocs:
                x = i[0]
                y = i[1]
                bulwark = Bulwark("bulwark.png",bulwark_lives[0],x,y)
                bulwark.set_alternate_image("bulwark.red.png")
                bulwark.set_gw(gw)
                gw.add(bulwark)

            #defining and adding player
            player_x = playerstart[0][0]
            player_y = playerstart[0][1]
            player = Player("player.png",3,player_x,player_y)
            player.set_alternate_image("player.red.png")
            player.set_gw(gw)
            player.set_background(background)
            gw.add(player)

            #points and lives label timers
            gw.set_interval(check_points, 1000)
            gw.set_interval(check_lives, 1000)

            #animation / playing:
            #alien movement 
            gw.add_event_listener("click", start_aliens_moving)
            #ship movement 
            gw.add_event_listener("key", key_action)
            
    #error message if the file name is invalid
    except IOError:
        print("That isn't a valid file name. Please try again.")


if __name__ == "__main__":
    info = "StartingInformation.txt"
    SpaceInvaders(info)