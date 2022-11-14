from tkgpio import TkCircuit
# hellloo
# initialize the circuit inside the GUI

configuration = {
    "width": 500,
    "height": 200,
    "leds": [
        {"x": 300, "y": 80, "name": "RED", "pin": 5},
        {"x": 350, "y": 80, "name": "YELLOW", "pin": 6},
        {"x": 400, "y": 80, "name": "BLUE", "pin": 13},
        {"x": 450, "y": 80, "name": "GREEN", "pin": 19}
    ],
    "buttons": [
        {"x": 50, "y": 80, "name": "Button 1", "pin": 2},
        {"x": 100, "y": 80, "name": "Button 2", "pin": 3},
        {"x": 150, "y": 80, "name": "Button 3", "pin":4},
        {"x": 200, "y": 80, "name": "Button 4", "pin": 17},
        {"x": 250, "y": 120, "name": "Button 5", "pin": 27}
    ]
}

circuit = TkCircuit(configuration)
@circuit.run
def main ():
    
    #------------------------------------#    
    # STUDENT CODE GOES BELOW THIS LINE
    #------------------------------------#
    
    # importing necessary tools for the code to work
    from time import sleep # allows sleep() function which can delay program
    from gpiozero import LED # allows code to work with LEDs
    from gpiozero import Button # allows code to work with Buttons
    import sys # for exit() function
    import random # for random.randint() function

    # global allows me to change the contents of the variable within methods
    
    # time delay for each round to input the sequence of LEDs
    global difficultyTime
    difficultyTime = 7
    
    # time delay for how long LEDs should be on 
    global lightFlashTime
    lightFlashTime = 1

    # False: Player has not lost, True: Player has lost

    global fail
    fail = False

    # True: Player can use buttons to input LED sequence,
    # False: Pressing buttons does nothing
    global allowButtonInput
    allowButtonInput = False
    # The order in which the sequence of LEDs is at currently
    # eg. 0 is the first LED that flashed, 1 is the 2nd, 2 is the 3rd, etc.
    global sequenceNum
    sequenceNum = 0
    # Total input time to press buttons
    global inputTime
    inputTime = 0
    # True: game can start, False: game does not start
    global gameLoop
    gameLoop = False

    # stores the sequence of LEDs that must be inputted
    # r is red, y is yellow, b is blue, g is green
    # eg. "rgby" means that the lights flashed red, green, blue, yellow in that order
    global colorSequence
    colorSequence = ""

    # variables for setting buttons to GPIO
    redButton = Button(2) # corresponds to red LED
    yellowButton = Button(3) # corresponds to yellow LED
    blueButton = Button(4) # corresponds to blue LED
    greenButton = Button(17) # corresponds to green LED
    controlButton = Button(27) # starts game
    # variables for setting LEDs to GPIO
    redLight = LED(5)
    yellowLight = LED(6)
    blueLight = LED(13)
    greenLight = LED(19)
    
    # turns off all lights
    def lights_off():
        redLight.off()
        yellowLight.off()
        blueLight.off()
        greenLight.off()

    # chooses a random light and stores it in the colorSequence variable 
    def randomLight():
        global colorSequence 
        global inputTime
        
        colorNum = random.randint(0, 3)
        
        if colorNum == 0:
            colorSequence += "r"
        elif colorNum == 1:
            colorSequence += "y"
        elif colorNum == 2:
            colorSequence += "b"
        elif colorNum == 3:
            colorSequence += "g"
        # each new LED that flashes in the sequence, there is more time added
        # difficultyTime changes based on the difficulty of the game,
        # meaning harder difficulty is less time to input sequence
        inputTime += difficultyTime
        
    # starts the main game loop
    def startGame():
        global gameLoop
        if gameLoop == False:
            lights_off()
            gameLoop = True
            
    # Below are 4 methods that run when each corresponding button is pressed,
    # Red, Green, Yellow, and Blue
    
    def redInput():
        global i
        global fail
        global gameLoop
        global sequenceNum
        global difficultyTime
        global lightFlashTime

        if gameLoop == False: # Checks if main game has started
            # changes the timing of the lights flashing,
            # and the time to input the sequence of LEDs
            # Red is the easiest, with 7 sec to input each LED and
            # the LEDs turns on for 1.5 sec before turning off
            lights_off()
            redLight.on() # light indicates current difficulty
            difficultyTime = 7
            lightFlashTime = 1.5
            
        if allowButtonInput: # checks if buttons should do anything
            # flashes corresponding light
            sleep(0.2)
            redLight.off()
            redLight.on()
            sleep(lightFlashTime)
            redLight.off()
            # checks if the button pressed matches the sequence
            # if the red light flashed, it would be correct
            if "r" == colorSequence[sequenceNum]:
                # adds 1 so that the next letter
                # in the colorSequence variable will be checked
                sequenceNum += 1
                # checks if the end of the sequence of lights is reached
                if sequenceNum == len(colorSequence):
                    # if true, the timer is cut short and next round starts
                    i = 99999
            # if the red light did not flash, game over
            else:
                gameLoop = False
                fail = True
                i = 99999 
    
    def yellowInput():
        global i
        global fail
        global gameLoop
        global sequenceNum
        global difficultyTime
        global lightFlashTime
        if gameLoop == False: # Checks if main game has started
            # changes the timing of the lights flashing,
            # and the time to input the sequence of LEDs
            # Yellow is the 2nd easiest, with 5 sec to input each LED and
            # the LEDs turns on for 1 sec before turning off
            lights_off()
            yellowLight.on() # light indicates current difficulty
            difficultyTime = 5
            lightFlashTime = 1
        if allowButtonInput: # checks if buttons should do anything
            # flashes corresponding light
            sleep(0.2)
            yellowLight.on()
            sleep(lightFlashTime)
            yellowLight.off()
            # checks if the button pressed matches the sequence
            # if the yellow light flashed, game continues
            if "y" == colorSequence[sequenceNum]:
                sequenceNum += 1
                # checks if the end of the sequence of lights is reached
                if sequenceNum == len(colorSequence):
                    # if true, the timer is cut short and next round starts
                    i = 99999
            # if the yellow light did not flash, game over
            else:
                gameLoop = False
                fail = True
                i = 99999
                
    def blueInput():
        global i
        global fail
        global gameLoop
        global sequenceNum
        global difficultyTime
        global lightFlashTime
        if gameLoop == False: # Checks if main game has started
            # changes the timing of the lights flashing,
            # and the time to input the sequence of LEDs
            # Yellow is the 2nd easiest, with 5 sec to input each LED and
            # the LEDs turns on for 1 sec before turning off
            lights_off()
            blueLight.on()
            difficultyTime = 3.5
            lightFlashTime = 0.5

        if allowButtonInput:
            sleep(0.2)
            blueLight.off()
            blueLight.on()
            sleep(lightFlashTime)
            blueLight.off()
            if "b" == colorSequence[sequenceNum]:
                sequenceNum += 1
                if sequenceNum == len(colorSequence):
                    i = 9999999999
            else:
                gameLoop = False
                fail = True
                i = 9999999999
                
    def greenInput():
        global i
        global fail
        global gameLoop
        global sequenceNum
        global difficultyTime
        global lightFlashTime
        if gameLoop == False:
            lights_off()
            greenLight.on()
            difficultyTime = 1.5
            lightFlashTime = 0.25
        if allowButtonInput:
            sleep(0.2)
            greenLight.off()
            greenLight.on()
            sleep(lightFlashTime)
            greenLight.off()
            if "g" == colorSequence[sequenceNum]:
                sequenceNum += 1
                if sequenceNum == len(colorSequence):
                    i = 99999
            else:
                gameLoop = False
                fail = True
                i = 99999


    controlButton.when_pressed = startGame
    redButton.when_pressed = redInput
    yellowButton.when_pressed = yellowInput
    blueButton.when_pressed = blueInput
    greenButton.when_pressed = greenInput
    
    while True:
        if gameLoop:
            global i
            i = 0 
            randomLight()
            for x in colorSequence:
                if x == "r":
                    redLight.on()
                    sleep(lightFlashTime)
                    redLight.off()
                    sleep(0.2)
                if x == "y":
                    yellowLight.on()
                    sleep(lightFlashTime)
                    yellowLight.off()
                    sleep(0.2)
                if x == "b":
                    blueLight.on()
                    sleep(lightFlashTime)
                    blueLight.off()
                    sleep(0.2)
                if x == "g":
                    greenLight.on()
                    sleep(lightFlashTime)
                    greenLight.off()
                    sleep(0.2)
            allowButtonInput = True
            while i < inputTime:
                sleep(1)
                i+= 1
                if inputTime == i:
                    fail = True
            sequenceNum = 0
            allowButtonInput = False
        if fail:
            for x in range(0, 8):
                redLight.off()
                sleep(0.5)
                redLight.on()
                sleep(0.5)
            exit()

            
    
    #------------------------------------#
    # STUDENT CODE GOES ABOVE THIS LINE
    #------------------------------------#


            

main()
