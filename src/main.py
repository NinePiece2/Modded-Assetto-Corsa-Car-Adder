# Imports and setting pygame to use the resolution of the display, not a scaled one
import sys

if sys.platform == 'win32':
    import ctypes
    try:
       ctypes.windll.user32.SetProcessDPIAware()
    except AttributeError:
        pass

# Imports modules from the util.py class
from util import *

import pygame
import datetime
import tkinter as tk
from tkinter import Tk, filedialog, messagebox
import os
from sys import exit
import shutil

# Global Variable Declorations
numbers = []
board = []
boardText = []
entryListFile=[]
serverCfgFile=[]
currentTurn = -1
configFolder='settings'
configFile='settings/config.ini'
savesFolder='saves'
outputFolder='output'
backupFolder='output/Z_Backup'
framerate = 60

base_screen_width = 1100
base_screen_height = 600

scale_factor_x = 1.5
scale_factor_y = 1.5

screen1 = pygame.display.set_mode((1100*scale_factor_x, 600*scale_factor_y), pygame.RESIZABLE)

# Check if the settings and saves folder exists, if it doesn't make the folders
if not os.path.exists(configFolder):
    os.makedirs(configFolder)
if not os.path.exists(outputFolder):
    os.makedirs(outputFolder)
if not os.path.exists(backupFolder):
    os.makedirs(backupFolder)

    
# Check if the config file exisits and if it doesn't one is created
def configFileExists():
    try:
        with open(configFile, 'r') as f:
            return True
    except:
        return False

if configFileExists() == False:
    with open(configFile, 'w') as f:
        f.write('')


# Check if the configFile is empty
def emptyConfigFile():
    try:
        with open(configFile, 'r') as f:
            return f.read() == ''
    except:
        return False

# if emptyConfigFile then add a framerate setting, else read the value of the framerate setting
if emptyConfigFile():
    with open(configFile, 'r') as f:
        lines = f.readlines()
        with open(configFile, 'a') as f:
            f.write('MaxFramerate=' + str(framerate))
else:
    with open(configFile, 'r') as f:
        lines = f.readlines()
        for line in lines:
            if 'MaxFramerate' in line:
                framerate = line.split('=')[1]
                framerate = int(framerate)
        

# Create the Tkinter root window for the messagebox
root = Tk()
root.wm_attributes("-topmost", 1)
root.withdraw()  # Hide the root window

# light shade of the button
color_light = (42,42,42) # Grey

# dark shade of the button
color_dark = (76,175,80) # Green


# Base class for setting up the pygmae application
class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1100*scale_factor_x, 600*scale_factor_y), pygame.RESIZABLE)

        # Setting the name and logo of the window
        pygame.display.set_caption('Car Adder')
        #image = Image.open('resources/bingo_icon.png')
        #Icon = pygame.image.fromstring(image.tobytes(), image.size, image.mode)
        #Icon = pygame.image.load('resources/bingo_icon.png')
        #pygame.display.set_icon(Icon)
        self.clock = pygame.time.Clock()
        self.current_scene = None


    def run(self):
        self.current_scene = MenuScene(self)

        while True:
            # Handle events
            events = pygame.event.get()

            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

            self.current_scene.handle_events(events)

            # Update
            self.current_scene.update()

            # Draw
            self.current_scene.draw()

            # Update the display
            pygame.display.flip()

            # Cap the frame rate
            self.clock.tick(framerate)

    def change_scene(self, scene):
        self.current_scene = scene

# Base Class for all Scenes in the application
class Scene:
    def __init__(self, game):
        self.game = game

    def handle_events(self, events):
        pass

    def update(self):
        pass

    def draw(self):
        pass

# Function that is a child of the Scene Class to make the Main Menu of the Application
class MenuScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        self.font = pygame.font.SysFont('Verdana',int(35*(scale_factor_x+scale_factor_y)/2))

    # Handles Events on the Menu Scene
    def handle_events(self, events):
        for event in events:
            
            # Gets the current height and width of the window
            width = screen1.get_width()
            height = screen1.get_height()
            
            global scale_factor_x, scale_factor_y

            # Sets the scale factors based on the current size of the screen and the inital size
            scale_factor_x = self.game.screen.get_width() / base_screen_width
            scale_factor_y = self.game.screen.get_height() / base_screen_height

            mouse = pygame.mouse.get_pos()

            # Handles when the mouse selects screen elements
            if event.type == pygame.MOUSEBUTTONDOWN:
                if width/2-70*scale_factor_x <= mouse[0] <= width/2+70*scale_factor_x and height/2-80*scale_factor_y <= mouse[1] <= height/2-40*scale_factor_y:
                    # Add Button
                    # Add a car to the files

                    def ask_car_details():
                        root = tk.Tk()
                        root.withdraw()  # Hide the root window

                        model = tk.simpledialog.askstring("Car Details", "Enter car model:")
                        if model is None:
                            return None  # User closed the dialog

                        skin = tk.simpledialog.askstring("Car Details", "Enter car skin:")
                        if skin is None:
                            return None  # User closed the dialog
                        
                        yes = tk.messagebox.askyesnocancel('Add Car', f'Do you want to add the car {model} with the ' +
                                                           f'skin {skin}')

                        return model, skin, yes
                    
                    model, skin, yes = ask_car_details()

                    if model == '' or skin == '' and yes:
                        messagebox.showerror('ERROR','Model or Skin empty - CAR NOT ADDED')
                    elif yes:
                        add_car(model, skin)

                elif width/2-70*scale_factor_x <= mouse[0] <= width/2+70*scale_factor_x and height/2+40*scale_factor_y <= mouse[1] <= height/2+80*scale_factor_y:
                    # Exit Button
                    pygame.quit()
                    exit()
                elif width/2-70*scale_factor_x <= mouse[0] <= width/2+70*scale_factor_x and height/2-20*scale_factor_y <= mouse[1] <= height/2+20*scale_factor_y:
                    # Remove Button
                    # Remove a car to the files

                    def ask_car_details():
                        root = tk.Tk()
                        root.withdraw()  # Hide the root window

                        model = tk.simpledialog.askstring("Car Details", "Enter car model:")
                        if model is None:
                            return None  # User closed the dialog
                        
                        yes = tk.messagebox.askyesnocancel('Remove Car', f'Do you want to remove the car {model}.')

                        return model, yes
                    
                    model, yes = ask_car_details()

                    if model == '' and yes:
                        messagebox.showerror('ERROR','Model Empty - CAR NOT REMOVED')
                    elif yes:
                        remove_car(model)

                elif width - 210*scale_factor_x <= mouse[0] <= width - 10*scale_factor_x and 20*scale_factor_y <= mouse[1] <= 60*scale_factor_y:
                    # Save a copy of the input file in the output folder
                    # Warn the user if this will override a file

                    current = os.getcwd()
                    file_path = filedialog.askopenfilename(initialdir=current + '/output')

                    global entryListFile

                    # Check if a file was selected
                    if file_path:
                        # Read the encoded data from the file
                        try:
                            with open(file_path, "rb") as file:
                                entryListFile = file_path

                            current_time = datetime.datetime.now()
                            newName = current_time.strftime("entry_list-%Y-%m-%d_%H-%M-%S") + '.ini'

                            # Save a backup of the file
                            backup_file_path = os.path.join(backupFolder, newName)
                            shutil.copyfile(file_path, backup_file_path)

                            Tk().wm_withdraw()
                            messagebox.showinfo('Continue', f"Entry List -> {file_path} Loaded")

                        except:
                            print("Wrong File/ Data Corrupted or Tampered with")
                            Tk().wm_withdraw()
                            messagebox.showerror('Error', f"Wrong File/ Data Corrupted or Tampered with")
                            return

                    else:
                        print("No file selected.")
                        return

                elif width - 210*scale_factor_x <= mouse[0] <= width - 10*scale_factor_x and 80*scale_factor_y <= mouse[1] <= 120*scale_factor_y:
                    # Save a copy of the input file in the output folder
                    # Warn the user if this will override a file

                    current = os.getcwd()
                    file_path = filedialog.askopenfilename(initialdir=current + '/output')

                    global serverCfgFile

                    # Check if a file was selected
                    if file_path:
                        # Read the encoded data from the file
                        try:
                            with open(file_path, "rb") as file:
                                serverCfgFile = file_path

                            current_time = datetime.datetime.now()
                            newName = current_time.strftime("server_cfg-%Y-%m-%d_%H-%M-%S") + '.ini'

                            # Save a backup of the file
                            backup_file_path = os.path.join(backupFolder, newName)
                            shutil.copyfile(file_path, backup_file_path)

                            Tk().wm_withdraw()
                            messagebox.showinfo('Continue', f"Server Cfg -> {file_path} Loaded")

                        except:
                            print("Wrong File/ Data Corrupted or Tampered with")
                            Tk().wm_withdraw()
                            messagebox.showerror('Error', f"Wrong File/ Data Corrupted or Tampered with")
                            return

                    else:
                        print("No file selected.")
                        return


    # Displays the user interface
    def draw(self):
        # Gets the current height and width of the window
        width = screen1.get_width()
        height = screen1.get_height()
        mouse = pygame.mouse.get_pos()

        # Sets the default cursor
        hover = False

        # Sets the scale factors based on the current size of the screen and the inital size
        global scale_factor_x, scale_factor_y
        scale_factor_x = self.game.screen.get_width() / base_screen_width
        scale_factor_y = self.game.screen.get_height() / base_screen_height

    
        # Background Colour
        self.game.screen.fill((18,18,18))

        # Checks if the user is hovering the menu options  
        # Delete Menu
        if width/2-70*scale_factor_x <= mouse[0] <= width/2+70*scale_factor_x and height/2-20*scale_factor_y <= mouse[1] <= height/2+20*scale_factor_y:
            pygame.draw.rect(self.game.screen,color_light,[width/2-70*scale_factor_x,height/2-20*scale_factor_y,140*scale_factor_x,40*scale_factor_y])  
            hover = True         
        else:
            pygame.draw.rect(self.game.screen,color_dark,[width/2-70*scale_factor_x,height/2-20*scale_factor_y,140*scale_factor_x,40*scale_factor_y])

        # Exit Button
        if width/2-70*scale_factor_x <= mouse[0] <= width/2+70*scale_factor_x and height/2-80*scale_factor_y <= mouse[1] <= height/2-40*scale_factor_y:
            pygame.draw.rect(self.game.screen,color_light,[width/2-70*scale_factor_x,height/2-80*scale_factor_y,140*scale_factor_x,40*scale_factor_y])
            hover = True
        else:
            pygame.draw.rect(self.game.screen,color_dark,[width/2-70*scale_factor_x,height/2-80*scale_factor_y,140*scale_factor_x,40*scale_factor_y])

        # Add Menu
        if width/2-70*scale_factor_x <= mouse[0] <= width/2+70*scale_factor_x and height/2+40*scale_factor_y <= mouse[1] <= height/2+80*scale_factor_y:
            pygame.draw.rect(self.game.screen,color_light,[width/2-70*scale_factor_x,height/2+40*scale_factor_y,140*scale_factor_x,40*scale_factor_y])
            hover = True
        else: 
            pygame.draw.rect(self.game.screen,color_dark,[width/2-70*scale_factor_x,height/2+40*scale_factor_y,140*scale_factor_x,40*scale_factor_y])

        # Load Entry Button
        if width - 210*scale_factor_x <= mouse[0] <= width - 10*scale_factor_x and 20*scale_factor_y <= mouse[1] <= 60*scale_factor_y:
            pygame.draw.rect(self.game.screen,color_light,[width - 210*scale_factor_x,20*scale_factor_y,200*scale_factor_x,40*scale_factor_y])
            hover = True
        else: 
            pygame.draw.rect(self.game.screen,color_dark,[width - 210*scale_factor_x,20*scale_factor_y,200*scale_factor_x,40*scale_factor_y])

        # Load Cfg Button
        if width - 210*scale_factor_x <= mouse[0] <= width - 10*scale_factor_x and 80*scale_factor_y <= mouse[1] <= 120*scale_factor_y:
            pygame.draw.rect(self.game.screen,color_light,[width - 210*scale_factor_x,80*scale_factor_y,200*scale_factor_x,40*scale_factor_y])
            hover = True
        else: 
            pygame.draw.rect(self.game.screen,color_dark,[width - 210*scale_factor_x,80*scale_factor_y,200*scale_factor_x,40*scale_factor_y])
        
        # Changes the cursor wheather or not the user is hovering an option to select
        if hover:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND) 
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW) 


        # Sets the font size based on the scale factors 
        self.font = pygame.font.SysFont('Verdana',int(35*(scale_factor_x+scale_factor_y)/2))

        # Creates text boxes for the different options and the main manu page title
        text = self.font.render("Car Adder", True, (255, 255, 255))

        # Sets the font size based on the scale factors 
        self.font = pygame.font.SysFont('Verdana',int(24*(scale_factor_x+scale_factor_y)/2))

        # Creates text boxes for the different options and the main manu page title
        addText = self.font.render('ADD', True, (255, 255, 255))
        removeText = self.font.render('REMOVE', True, (255, 255, 255))
        exitText = self.font.render('EXIT', True, (255, 255, 255))
        loadEntryText = self.font.render('LOAD ENTRY', True, (255, 255, 255))
        loadCfgText = self.font.render('LOAD CFG', True, (255, 255, 255))

        # Shows and scales the text boxes based on the scale factors
        self.game.screen.blit(exitText, (width/2-30*scale_factor_x,height/2+43*scale_factor_y))
        self.game.screen.blit(addText, (width/2-28*scale_factor_x,height/2-76*scale_factor_y))
        self.game.screen.blit(removeText, (width/2-52*scale_factor_x,height/2-15*scale_factor_y))
        self.game.screen.blit(text, (10, 10))
        self.game.screen.blit(loadEntryText, (width-185*scale_factor_x, 24*scale_factor_y))
        self.game.screen.blit(loadCfgText, (width-170*scale_factor_x, 83*scale_factor_y))


def add_car(model, skin):
    if entryListFile == []:
        root = tk.Tk()
        root.withdraw()  # Hide the root window
        messagebox.showerror('ERROR','No Entry List File Selected - CAR NOT ADDED')
    elif serverCfgFile ==[]:
        root = tk.Tk()
        root.withdraw()  # Hide the root window
        messagebox.showerror('ERROR','No Cfg File Selected - CAR NOT ADDED')
    else:
        add_car_to_entry(model, skin, entryListFile)
        add_car_to_cfg(model, serverCfgFile)

        root = tk.Tk()
        root.withdraw()  # Hide the root window
        messagebox.showinfo('Continue', f"Car model:{model} with skin:{skin} added.")

def remove_car(model):
    if entryListFile == []:
        root = tk.Tk()
        root.withdraw()  # Hide the root window
        messagebox.showerror('ERROR','No Entry List File Selected - CAR NOT REMOVE')
    elif serverCfgFile ==[]:
        root = tk.Tk()
        root.withdraw()  # Hide the root window
        messagebox.showerror('ERROR','No Cfg File Selected - CAR NOT REMOVE')
    else:
        delete_car_entry(model, entryListFile)
        delete_car_cfg(model, serverCfgFile)

        root = tk.Tk()
        root.withdraw()  # Hide the root window
        messagebox.showinfo('Continue', f"Car model:{model} removed.")

        

# Function that starts the application
if __name__ == "__main__":
    game = Game()
    game.run()