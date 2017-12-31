#!/usr/bin/env python3

from tkinter import * 

import random

startingDays = 10
"""int: Documents the amount of days that a cell will have to live"""

landRows = 7
landCols = 5
"""int: The amount of rows and columns the land will span"""

day = 1
labels = []
butt = [""]
landMass = [[]]
"""Default values set for variables used on a global level"""

restart = []
"""list: allows for the simulation to be reset"""

top = Tk( )
top.resizable(False, False)
top.title("Cell Simulation")
"""Initializes the tkinter window that will be used"""

food = -10
"""float: the minimum food that will be needed by the first cell"""

water = 0.1
"""float: the minimum humidity percentage expressed as a decimal which the cell needs"""

minTemp = 32
maxTemp = 200
"""float: the range of temperature values (inclusive) which the cell cal reproduce in"""


detailed = True
"""boolean: Decides whether or not the output will be detailed or not (check the __str__ functions of both classes below)"""



class cellularLife:
    """This class represents a cell"""
    
    def __init__(self, foodNeeded, waterNeeded, tempMinThresh, tempMaxThresh, daysLeft, dayCreated):
        """Initializes a cell with the various attributes a cell has

        Args:
            foodNeeded (float): the minimal amount of sugar needed to reproduced 
            waterNeeded (float): the minimal percentage of humidity needed to reproduce
            tempMinThresh (float): the minimum temperature the cells can reproduce in
            tempMaxThresh (float): the maximum temperature the cells can reproduce in
            daysLeft (int): the amount of time the cell has left
            dayCreated (int): the 'day' which the cell was created on
        """
        self.foodNeeded = foodNeeded
        self.waterNeeded = waterNeeded
        self.tempMinThresh = tempMinThresh
        self.tempMaxThresh = tempMaxThresh
        self.daysLeft = daysLeft
        self.dayCreated = dayCreated

    def birthCertificate(self, dayCreated):
        """Changes the dayCreated value for an individual cell

        Args:
            dayCreated (int): the day the cell was created on
        """
        
        self.dayCreated = dayCreated

    def dayPass(self):
        """Decreases the amount of days that a cell has left to live"""
        
        self.daysLeft-=1

    def __str__(self):
        if(detailed):
            return (str(self.foodNeeded)[:5] + '\n' + str(self.waterNeeded)[:5] + '\n'
                + str(self.tempMinThresh)[:5] + '-' + str(self.tempMaxThresh)[:5] + '\n'
                + str(self.daysLeft))
        return "B"


class landSegment:
    """This class represents a plot of land"""

    def __init__(self, food, water, temp):
        """Initializes a plot of land with the various attributes a plot of land has

        Args:
            food (float): the  amount of sugar on the plot of land 
            water (float): the decimal percentage of humidity on the plot of land
            temp (float): the temperature on the plot of land
        """
        
        self.food = food
        self.water = water
        self.temp = temp

    def __str__(self):
        if(detailed):
            return str(self.food)[:5] + '\n' + str(self.water)[:5] + '\n' + str(self.temp)[:5] + '\n'
        return "L"


def suitable(cell, land):
    """Checks whether or not a cell can reproduce into a plot

    Args:
        cell (:obj:'cellularLife'): The cell which is trying to reproduce
        land (:obj:'landSegment'): The plot of land which the cell is trying to reproduce to

    Returns:
        bool: True if the cell can move onto the plot, False otherwise
    """
    
    if(cell.foodNeeded > land.food):
        return False
    if(cell.waterNeeded > land.water):
        return False
    if(cell.tempMinThresh > land.temp or cell.tempMaxThresh < land.temp):
        return False
    return True


def concentration():
    """Calculates the concentration of cells in a given land map"""
    
    numSpaces = len(landMass) * len(landMass[0])

    infected = 0
    for row in landMass:
        for plot in row:
            if(type(plot).__name__ == 'cellularLife'):
                infected += 1
    return infected / numSpaces


def disableButton(wasSustainable):
    """Disables the day progression button

    Args:
        wasSustainable (bool): True if the bacteria hit a sustainable limit, false otherwise
    """
    
    global butt
    if(wasSustainable):
        butt[0].configure(text='BACTERIA WON', state=DISABLED)
    else:
        butt[0].configure(text='BACTERIA ELIMINATED', state=DISABLED)

    
def generateCell(cell, day):
    """Given a cell this will decide if the cell mutates, and if so whether or not it mutates for the better or worse

    Args:
        cell (:obj:'cellularLife'): The cell which is possibly being mutated
        day (int): The day which the cell was on, for continuity purposes

    Returns:
        cell (:obj:'cellularLife'): The cell mutated to be stronger if the first case is triggered,
            weaker if the second case is triggered, and not mutated at all if the third one is.
    """
    
    if(random.randint(0,30)==0):
        return cellularLife(abs(cell.foodNeeded-.05),abs(cell.waterNeeded-.05),cell.tempMinThresh-5,cell.tempMaxThresh+5, startingDays, day)

    if(random.randint(0,50)==0):
        return cellularLife(cell.foodNeeded+.05,cell.waterNeeded+.05,cell.tempMinThresh+5,cell.tempMaxThresh-5, startingDays, day)
    
    return cellularLife(cell.foodNeeded, cell.waterNeeded, cell.tempMinThresh, cell.tempMaxThresh, startingDays, day)


def act():
    """ Runs all processes which must happen during a day"""
    
    global day

    for x in range(len(landMass)):
        for y in range(len(landMass[0])):
            if(type(landMass[x][y]).__name__ == 'cellularLife' and landMass[x][y].dayCreated != day):
                if(landMass[x][y].daysLeft == 1):
                    landMass[x][y] = landSegment(random.uniform(0,.5),random.uniform(0,.5),random.randint(40,80))
                else:
                    landMass[x][y].dayPass()
                    
                    if(x-1 >= 0 and type(landMass[x-1][y]).__name__ == 'landSegment' and suitable(landMass[x][y], landMass[x-1][y])):
                        landMass[x-1][y] = generateCell(landMass[x][y], day)
                        
                    elif(x+1 < len(landMass) and type(landMass[x+1][y]).__name__ == 'landSegment' and suitable(landMass[x][y], landMass[x+1][y])):
                        landMass[x+1][y] = generateCell(landMass[x][y], day)
                        
                    elif(y-1 >= 0 and type(landMass[x][y-1]).__name__ == 'landSegment' and suitable(landMass[x][y], landMass[x][y-1])):
                        landMass[x][y-1] = generateCell(landMass[x][y], day)
                        
                    elif(y+1 < len(landMass[0]) and type(landMass[x][y+1]).__name__ == 'landSegment' and suitable(landMass[x][y], landMass[x][y+1])):
                        landMass[x][y+1] = generateCell(landMass[x][y], day)
                        
    day += 1
    updateLandMass()


def displayLandMass():
    """Displays the initial window, and adds the buttons along with their functionality at the bottom of the window"""
    
    global day
    global butt
    global labels
    global restart
    labelIndex = 0

    for r in range(len(landMass)):
        for c in range(len(landMass[r])):
            if(type(landMass[r][c]).__name__ == 'cellularLife'):
                labels.append(Label(top, bg='red', text=str(landMass[r][c]), font=("Times, 10")))
                labels[labelIndex].grid(row = r, column = c)
            else:
                labels.append(Label(top, bg='green', text=str(landMass[r][c]), font=("Times, 10")))
                labels[labelIndex].grid(row = r, column = c)
            labelIndex += 1
            
    butt[0] = (Button(top, text='Increment to Day '+str(day), width=25, command = act, font="Times, 10"))
    butt[0].grid(row=len(landMass), columnspan = len(landMass[0]))

    restart.append(Button(top, text = 'Restart', width = 9, command = buildLand, font="Times, 10"))
    restart[0].grid(row = len(landMass)+1, columnspan = len(landMass[0]))
    top.mainloop()
    

def updateLandMass():
    """Updates the labels, as well as incrementing the number on the button and deciding when the user
        should no longer be allowed to increment the day"""
    
    labelIndex = 0

    for r in range(len(landMass)):
        for c in range(len(landMass[r])):
            if(type(landMass[r][c]).__name__ == 'cellularLife'):
                labels[labelIndex].configure(bg='red', text=str(landMass[r][c]))
            else:
                labels[labelIndex].configure(bg='green', text=str(landMass[r][c]))
            labelIndex += 1
    butt[0].configure(text='Increment to Day '+str(day))
    
    if(concentration() == 0):
        disableButton(False)
    if(concentration() >= .8):
        disableButton(True)


def buildLand():
    """Initially builds the land map and inserts the bacteria randomly on it"""
    
    global day
    global landMass
    day = 1
    land = [[0 for x in range(landCols)] for y in range(landRows)]

    for row in range(len(land)):
        for col in range(len(land[0])):
            land[row][col] = landSegment(random.uniform(0,1), random.uniform(0,1), random.uniform(0,100))

    land[random.randint(0,len(landMass)-1)][random.randint(0,len(land[0])-1)] = cellularLife(float(food), float(water), int(minTemp), int(maxTemp), startingDays, 0)
    landMass = land
    displayLandMass()

buildLand()
