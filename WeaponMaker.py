#imports
import ctypes
import os
import sys
import random
import time
from datetime import datetime

import customtkinter as ctk
from CTkToolTip import CTkToolTip
from tkinter import messagebox, filedialog
import pywinstyles
from PIL import Image, ImageGrab, ImageDraw, ImageOps
from ctypes import wintypes

def resource_path(relative_part):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_part)

#vars
first_time = True
picked_merc = "All"
max_num = 8
created_attribute_label = []
order = {"=": 0, "+": 1, "-": 2}
allowed_letters_list = ["-", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
mercs = ["Demoman", "Engineer", "Heavy", "Medic", "Pyro", "Scout", "Sniper", "Soldier", "Spy"]
mercs_list_for_the_class_button = ["All", "Scout", "Soldier", "Pyro", "Demoman", "Heavy", "Engineer", "Medic", "Sniper", "Spy"]
all_weapons = [
    # Primary
    "Scattergun",
    "Rocket Launcher",
    "Flamethrower",
    "Grenade Launcher",
    "Minigun",
    "Shotgun",
    "Syringe Gun",
    "Medigun",
    "Sniper Rifle",
    "Huntsman",
    "Revolver",
    # Secondary
    "Pistol",
    "Buff Banner",
    "Flare Gun",
    "Stickybomb Launcher",
    "Chargin' Shield",
    "Lunchbox Item",
    "SMG",
    "Jarate",
    "Mad Milk",
    # Melee
    "Bat",
    "Shovel",
    "Fire Axe",
    "Bottle",
    "Sword",
    "Fists",
    "Wrench",
    "Bonesaw",
    "Kukri",
    "Butterfly Knife",
    "Sapper",
    #PDA
    "Construction PDA",
    "Destruction PDA",
    "Invis Watch",
]
qualities = ["All", "Unique", "Strange", "Vintage", "Genuine", "Australium", "Unusual"]
quality_colors = ["#FFD700", "#CF6A32", "#476291", "#4D7455", "#E5C158", "#8650AC"]
quality_weights = [85, 10, 3, 2, 2, 0.66]

    #paths
if hasattr(sys, "_MEIPASS"):
    attributes_folder_path = sys._MEIPASS
else:
    attributes_folder_path = os.path.dirname(os.path.abspath(__file__))
logo_file_path = os.path.join(attributes_folder_path, "Images/Logo.ico")
my_logo_path = os.path.join(attributes_folder_path, "Images/MyLogo.png")
class_images_folder_path = os.path.join(attributes_folder_path, "Images/ClassIcons")
weapon_images_folder_path = os.path.join(attributes_folder_path, "Images/Weapons")
attributes_file_path = os.path.join(attributes_folder_path, "Texts/attributes.txt")
nouns_file_path = os.path.join(attributes_folder_path, "Texts/nouns.txt")
adjs_file_path = os.path.join(attributes_folder_path, "Texts/adjectives.txt")
font_file_path = os.path.join(attributes_folder_path, "Assets/tf2build.ttf")
        #mercs attributes paths
demo_attributes_path = os.path.join(attributes_folder_path, "Texts/ClassAttributes/DemomanAttributes.txt")
engineer_attributes_path = os.path.join(attributes_folder_path, "Texts/ClassAttributes/EngineerAttributes.txt")
heavy_attributes_path = os.path.join(attributes_folder_path, "Texts/ClassAttributes/HeavyAttributes.txt")
medic_attributes_path = os.path.join(attributes_folder_path, "Texts/ClassAttributes/MedicAttributes.txt")
pyro_attributes_path = os.path.join(attributes_folder_path, "Texts/ClassAttributes/PyroAttributes.txt")
scout_attributes_path = os.path.join(attributes_folder_path, "Texts/ClassAttributes/ScoutAttributes.txt")
sniper_attributes_path = os.path.join(attributes_folder_path, "Texts/ClassAttributes/SniperAttributes.txt")
soldier_attributes_path = os.path.join(attributes_folder_path, "Texts/ClassAttributes/SoldierAttributes.txt")
spy_attributes_path = os.path.join(attributes_folder_path, "Texts/ClassAttributes/SpyAttributes.txt")
        #icons
team_icon_paths = []
for i in os.listdir(class_images_folder_path):
    full_path = os.path.join(class_images_folder_path, i)
    team_icon_paths.append(full_path)

primary_wep_path = os.path.join(weapon_images_folder_path, "Primary")
primary_wep_paths = []
for i in os.listdir(primary_wep_path):
    full_path = os.path.join(primary_wep_path, i)
    primary_wep_paths.append(full_path)
secondary_wep_path = os.path.join(weapon_images_folder_path, "Secondary")
secondary_wep_paths = []
for i in os.listdir(secondary_wep_path):
    full_path = os.path.join(secondary_wep_path, i)
    secondary_wep_paths.append(full_path)
melee_wep_path = os.path.join(weapon_images_folder_path, "Melee")
melee_wep_paths = []
for i in os.listdir(melee_wep_path):
    full_path = os.path.join(melee_wep_path, i)
    melee_wep_paths.append(full_path)
PDA_wep_path = os.path.join(weapon_images_folder_path, "PDA")
PDA_wep_paths = []
for i in os.listdir(PDA_wep_path):
    full_path = os.path.join(PDA_wep_path, i)
    PDA_wep_paths.append(full_path)

#the window
ctk.set_window_scaling(0.9)
ctk.set_widget_scaling(0.9)
window = ctk.CTk()
window_width = 540
window_height = 285
window.title("THE TF2 Weapons Generator")
window.iconbitmap(logo_file_path)
window.resizable(False, False)
window.config(background="#24201b")
pywinstyles.change_header_color(window, color="#24201b")

option_window = ctk.CTkToplevel(window)
option_window.title("THE TF2 Weapons Generator Options")
option_window.geometry("440x230")
option_window.iconbitmap(logo_file_path)
option_window.resizable(False, False)
option_window.configure(fg_color="#24201b")
option_window.protocol("WM_DELETE_WINDOW", option_window.withdraw)
option_window.withdraw()

def clean_custom():
    custom_window.withdraw()
    if changed_weapon_label.cget("image"):
        changed_weapon_label.configure(text="", image=None)
        changed_weapon_label.update_idletasks()
    name_changer.delete("0", "end")
    level_changer.delete("0", "end")
    class_changer.set("All")
    type_changer._entry.delete("0", "end")
    num_changer.set("The classic")
    quality_changer.set("All")
    attributes_changer.delete("0.0", "end")

custom_window = ctk.CTkToplevel(window)
custom_window.title("THE TF2 Custom Weapons Generator")
custom_window.geometry("540x750")
custom_window.iconbitmap(logo_file_path)
custom_window.resizable(False, False)
custom_window.configure(fg_color="#24201b")
custom_window.protocol("WM_DELETE_WINDOW", clean_custom)
custom_window.withdraw()

ctypes.windll.gdi32.AddFontResourceExW(font_file_path, 0x10, 0)

frame = ctk.CTkFrame(window, width=200, height=180, corner_radius=20, fg_color="#3c362f", border_color="#ffd700", border_width=2, bg_color="#24201b")
frame.place(x=170, y=15)
frame.pack_propagate(False)

name_label = ctk.CTkLabel(window, font=("TF2 BUILD", 33), text_color="#ffd700", fg_color="#24201b", bg_color="#24201b", wraplength=window_width)
level_label = ctk.CTkLabel(window, font=("TF2 BUILD", 20), text_color="#756b5e", fg_color="#24201b", bg_color="#24201b")

weapon_label = ctk.CTkLabel(frame, image=None, text="", bg_color="#3c362f")
weapon_label.place(relx=0.5, rely=0.5, anchor="center")

merc_label = ctk.CTkLabel(window, image=None, text="", bg_color="#24201b")
merc_label.place(x=15, y=15)

pixel = ctk.CTkFrame(window, width=10, height=10, fg_color="#24201b", bg_color="#24201b", cursor="question_arrow")
pixel.place(relx=0.0, rely=1.0, anchor="sw")
CTkToolTip(pixel, message="Yo, what's up.")
    #tools
line = ctk.CTkFrame(window, width=5, height=1000, fg_color="#3c362f", bg_color="#24201b")
line.place(x=540, y=-10)
line.pack_propagate(False)
        #buttons
more_Button = ctk.CTkButton(window, text=">", font=("TF2 BUILD", 20), width=50, height=180, corner_radius=20, fg_color="#3c362f", bg_color="#24201b", border_width=2, hover_color="#99ccff", command=lambda: more_tools())
more_Button.place(x=550, y=10)
CTkToolTip(more_Button, message="More tools.\n(You can press <Escape> instead.)")

buttons_frame = ctk.CTkFrame(option_window, width=200, height=150, corner_radius=20, fg_color="#3c362f", border_color="#ffd700", border_width=2, bg_color="#24201b")
buttons_frame.grid(row=0, column=0, padx=10, pady=5, sticky="n")
buttons_frame.grid_propagate(False)

generate_Button = ctk.CTkButton(buttons_frame, text="Generate", font=("TF2 BUILD", 20), width=180, height=50, corner_radius=20, fg_color="#3c362f", bg_color="#3c362f", border_width=2, hover_color="#99ccff", command=lambda: generate())
generate_Button.grid(row=0, column=0, padx=10, pady=10)
CTkToolTip(generate_Button, message="Randomly generate a weapon.\n(You can press <Space> instead.)")

screen_shot_Button = ctk.CTkButton(buttons_frame, text="Save Image", font=("TF2 BUILD", 20), width=180, height=50, corner_radius=20, fg_color="#3c362f", bg_color="#3c362f", border_width=2, hover_color="#99ccff", command=lambda: screenshot())
screen_shot_Button.grid(row=3, column=0, padx=10, pady=10)
CTkToolTip(screen_shot_Button, message="Dont worry it wont capture the buttons.\n(All images will be in the Pictures folder.)")
        #menus
menus_frame = ctk.CTkFrame(option_window, width=200, height=150, corner_radius=20, fg_color="#3c362f", border_color="#ffd700", border_width=2, bg_color="#24201b")
menus_frame.grid(row=0, column=1, padx=10, pady=5, sticky="n")
menus_frame.grid_propagate(False)

        #custom
custom_Button = ctk.CTkButton(option_window, text="Custom Weapon", font=("TF2 BUILD", 20), width=180, height=50, corner_radius=20, fg_color="#3c362f", bg_color="#24201b", border_width=2, border_color="#ffd700", hover_color="#99ccff", command=lambda: custom())
custom_Button.grid(row=1, column=0, columnspan=2, padx=10, pady=5)
CTkToolTip(custom_Button, message="Import your own attribute and images.")

image_changer_label = ctk.CTkLabel(custom_window, text="Image: ", font=("TF2 BUILD", 20), text_color="#ffd700", fg_color="#24201b", bg_color="#24201b")
image_changer_label.grid(row=0, column=0, padx=10, pady=5, sticky="n")
CTkToolTip(image_changer_label, message="Choose your weapon's look.")
image_changer = ctk.CTkFrame(custom_window, width=200, height=180, corner_radius=20, fg_color="#1D1E1E", border_color="#ffd700", border_width=2, bg_color="#24201b")
image_changer.grid(row=0, column=1, padx=10, pady=5, sticky="n")
image_changer.pack_propagate(False)
changed_weapon_label = ctk.CTkLabel(image_changer, text="", bg_color="#1D1E1E")

name_changer_label = ctk.CTkLabel(custom_window, text="Name: ", font=("TF2 BUILD", 20), text_color="#ffd700", fg_color="#24201b", bg_color="#24201b")
name_changer_label.grid(row=1, column=0, padx=10, pady=5, sticky="n")
CTkToolTip(name_changer_label, message="Just type a name...")
name_changer = ctk.CTkEntry(custom_window, font=("TF2 BUILD", 30), width=360, height=90, corner_radius=20, border_color="#ffd700", border_width=2, bg_color="#24201b", fg_color="#1D1E1E")
name_changer.grid(row=1, column=1, padx=10, pady=5, sticky="n")

level_changer_label = ctk.CTkLabel(custom_window, text="Level: ", font=("TF2 BUILD", 20), text_color="#ffd700", fg_color="#24201b", bg_color="#24201b")
level_changer_label.grid(row=2, column=0, padx=10, pady=5, sticky="n")
CTkToolTip(level_changer_label, message=f"Choose your weapon's level\nThe list of characters you can use is {allowed_letters_list}.")
level_changer = ctk.CTkEntry(custom_window, font=("TF2 BUILD", 30), width=360, height=90, corner_radius=20, border_color="#ffd700", border_width=2, bg_color="#24201b", fg_color="#1D1E1E")
level_changer.grid(row=2, column=1, padx=10, pady=5, sticky="n")

type_changer_label = ctk.CTkLabel(custom_window, text="Type: ", font=("TF2 BUILD", 20), text_color="#ffd700", fg_color="#24201b", bg_color="#24201b")
type_changer_label.grid(row=3, column=0, padx=10, pady=5, sticky="n")
CTkToolTip(type_changer_label, message=f"What is your weapon?")
type_changer = ctk.CTkComboBox(custom_window, values=all_weapons, font=("TF2 BUILD", 20), width=30, height=30, corner_radius=20, fg_color="#1D1E1E", bg_color="#24201b", button_color="#1D1E1E", button_hover_color="#3c362f", border_width=2)
type_changer.grid(row=3, column=1, padx=10, pady=10, sticky="nesw")
type_changer.set("")

class_changer_label = ctk.CTkLabel(custom_window, text="Class: ", font=("TF2 BUILD", 20), text_color="#ffd700", fg_color="#24201b", bg_color="#24201b")
class_changer_label.grid(row=4, column=0, padx=10, pady=5, sticky="n")
CTkToolTip(class_changer_label, message=f"Choose which class shall wield the weapon.")
class_changer = ctk.CTkOptionMenu(custom_window, values=mercs_list_for_the_class_button, font=("TF2 BUILD", 20), width=30, height=30, corner_radius=20, fg_color="#1D1E1E", bg_color="#24201b", button_color="#1D1E1E", button_hover_color="#3c362f")
class_changer.grid(row=4, column=1, padx=10, pady=10, sticky="nesw")
class_changer.set("All")
class_changer.grid_propagate(False)

num_changer_label = ctk.CTkLabel(custom_window, text="Number: ", font=("TF2 BUILD", 20), text_color="#ffd700", fg_color="#24201b", bg_color="#24201b")
num_changer_label.grid(row=5, column=0, padx=10, pady=5, sticky="n")
CTkToolTip(num_changer_label, message=f"Choose how many attributes can a weapon have.\n(Gud luck figuring it out tho...)\n(And it wont work if you have custom attributes because why.)")
num_changer = ctk.CTkOptionMenu(custom_window, values=["Why are you like this?", "TF2 updates...", "Bread size" , "The classic" , "Mann SIZE!"], font=("TF2 BUILD", 20), width=180, height=30, corner_radius=10, fg_color="#1D1E1E", bg_color="#24201b", button_color="#1D1E1E", button_hover_color="#3c362f", anchor="w")
num_changer.grid(row=5, column=1, padx=10, pady=10, sticky="nesw")
num_changer.set("The classic")

quality_changer_label = ctk.CTkLabel(custom_window, text="Quality: ", font=("TF2 BUILD", 20), text_color="#ffd700", fg_color="#24201b", bg_color="#24201b")
quality_changer_label.grid(row=6, column=0, padx=10, pady=5, sticky="n")
CTkToolTip(quality_changer_label, message=f"Choose how fancy is your weapon.")
quality_changer = ctk.CTkOptionMenu(custom_window, values=qualities, font=("TF2 BUILD", 20), width=30, height=30, corner_radius=20, fg_color="#1D1E1E", bg_color="#24201b", button_color="#1D1E1E", button_hover_color="#3c362f")
quality_changer.grid(row=6, column=1, padx=10, pady=10, sticky="nesw")
quality_changer.set("All")
quality_changer.grid_propagate(False)

attributes_changer_label = ctk.CTkLabel(custom_window, text="Attributes: ", font=("TF2 BUILD", 20), text_color="#ffd700", fg_color="#24201b", bg_color="#24201b")
attributes_changer_label.grid(row=7, column=0, padx=10, pady=5, sticky="n")
CTkToolTip(attributes_changer_label, message="In order to color your attributes you need to type between the [ ]:\n[=]: For white\n[+]: For blue\n[-]: For red")
attributes_changer = ctk.CTkTextbox(custom_window, font=("TF2 BUILD", 20), width=360, height=150, corner_radius=20, border_color="#ffd700", border_width=2, bg_color="#24201b", activate_scrollbars=True)
attributes_changer.grid(row=7, column=1, padx=10, pady=5, sticky="n")

my_frame = ctk.CTkFrame(option_window, width=50, height=50, fg_color="#3c362f", border_color="#ffd700", border_width=2, bg_color="#24201b")
my_frame2 = ctk.CTkFrame(custom_window, width=50, height=50, fg_color="#3c362f", border_color="#ffd700", border_width=2, bg_color="#24201b")
my_frame.place(relx=0.0, rely=1.0, anchor="sw")
my_frame2.place(relx=0.0, rely=1.0, anchor="sw")
raw_image = Image.open(my_logo_path)
my_icon = ctk.CTkImage(light_image=raw_image, dark_image=raw_image, size=(44, 44))
my_label = ctk.CTkLabel(my_frame, image=my_icon, text="", bg_color="#24201b")
my_label2 = ctk.CTkLabel(my_frame2, image=my_icon, text="", bg_color="#24201b")
my_label.place(x=25, y=25, anchor="center")
my_label2.place(x=25, y=25, anchor="center")
CTkToolTip(my_label, message="THAT Snowy")
CTkToolTip(my_label2, message="THAT Snowy")
    #lists
with open(attributes_file_path, "r", encoding="utf-8") as f:
    all_attributes = [line.strip() for line in f if line.strip()]
with open(nouns_file_path, "r", encoding="utf-8") as f:
    nouns = [line.strip() for line in f if line.strip()]
with open(adjs_file_path, "r", encoding="utf-8") as f:
    adjs = [line.strip() for line in f if line.strip()]
        #mercs attributes lists
with open(demo_attributes_path, "r", encoding="utf-8") as f:
    demo_attributes = [line.strip() for line in f if line.strip()]
with open(engineer_attributes_path, "r", encoding="utf-8") as f:
    engineer_attributes = [line.strip() for line in f if line.strip()]
with open(heavy_attributes_path, "r", encoding="utf-8") as f:
    heavy_attributes = [line.strip() for line in f if line.strip()]
with open(medic_attributes_path, "r", encoding="utf-8") as f:
    medic_attributes = [line.strip() for line in f if line.strip()]
with open(pyro_attributes_path, "r", encoding="utf-8") as f:
    pyro_attributes = [line.strip() for line in f if line.strip()]
with open(scout_attributes_path, "r", encoding="utf-8") as f:
    scout_attributes = [line.strip() for line in f if line.strip()]
with open(sniper_attributes_path, "r", encoding="utf-8") as f:
    sniper_attributes = [line.strip() for line in f if line.strip()]
with open(soldier_attributes_path, "r", encoding="utf-8") as f:
    soldier_attributes = [line.strip() for line in f if line.strip()]
with open(spy_attributes_path, "r", encoding="utf-8") as f:
    spy_attributes = [line.strip() for line in f if line.strip()]

def generate(event=None):
    global window_height, window_width, first_time, created_attribute_label, new_window_height
    #resets
    try:
        name_label.configure(font=("TF2 BUILD", 33))
        window.bind("<space>", generate)
        option_window.bind("<space>", generate)
        window_height = 285
        y_offset = 0
        if not first_time:
            for i in created_attribute_label:
                i.destroy()
        #merc, type and kind choice
        if class_changer.get():
            picked_merc = class_changer.get()
        else:
            picked_merc = "All"
        if picked_merc == "All":
            mercs_choice = random.randint(0, 8)
        elif picked_merc == "Scout":
            mercs_choice = 5
        elif picked_merc == "Soldier":
            mercs_choice = 7
        elif picked_merc == "Pyro":
            mercs_choice = 4
        elif picked_merc == "Demoman":
            mercs_choice = 0
        elif picked_merc == "Heavy":
            mercs_choice = 2
        elif picked_merc == "Engineer":
            mercs_choice = 1
        elif picked_merc == "Medic":
            mercs_choice = 3
        elif picked_merc == "Sniper":
            mercs_choice = 6
        elif picked_merc == "Spy":
            mercs_choice = 8
        if type_changer.get():
            weapons = type_changer.get()
        else:
            if mercs_choice == 0:
                weapons = ["Grenade Launcher", "Stickybomb Launcher", "Chargin' Shield", "Bottle", "Sword"]
            elif mercs_choice == 1:
                weapons = ["Shotgun", "Pistol", "Wrench", "Construction PDA", "Destruction PDA"]
            elif mercs_choice == 2:
                weapons = ["Minigun", "Shotgun", "Lunchbox Item", "Fists"]
            elif mercs_choice == 3:
                weapons = ["Syringe Gun", "Medigun", "Bonesaw"]
            elif mercs_choice == 4:
                weapons = ["Flamethrower", "Shotgun", "Flare Gun", "Fire Axe"]
            elif mercs_choice == 5:
                weapons = ["Scattergun", "Pistol", "Mad Milk", "Bat"]
            elif mercs_choice == 6:
                weapons = ["Sniper Rifle", "Huntsman", "SMG", "Jarate", "Kukri"]
            elif mercs_choice == 7:
                weapons = ["Rocket Launcher", "Shotgun", "Buff Banner", "Shovel"]
            elif mercs_choice == 8:
                weapons = ["Revolver", "Butterfly Knife", "Sapper", "Invis Watch"]
        if type_changer.get():
            Type = type_changer.get()
        else:
            Type = random.choice(weapons)
        if Type in all_weapons[0:11]:
            kind = "Primary"
        elif Type in all_weapons[11:20]:
            kind = "Secondary"
        elif Type in all_weapons[20:31]:
            kind = "Melee"
        elif Type in all_weapons[31:34]:
            kind = "PDA"
        else:
            kind = "all"
        #mec icon
        raw_image = Image.open(team_icon_paths[mercs_choice])
        merc_icon = ctk.CTkImage(light_image=raw_image, dark_image=raw_image, size=(44, 44))
        merc_label.configure(image=merc_icon)
        if mercs_choice == 0:
            CTkToolTip(merc_label, message="Soup can!!!!!!")
        elif mercs_choice == 1:
            CTkToolTip(merc_label, message="Engineer gaming.")
        elif mercs_choice == 2:
            CTkToolTip(merc_label, message="It is gud day to be not dead!")
        elif mercs_choice == 3:
            CTkToolTip(merc_label, message="I am going to saw through your bones!")
        elif mercs_choice == 4:
            CTkToolTip(merc_label, message="hmmmmph hmmmph!!!")
        elif mercs_choice == 5:
            CTkToolTip(merc_label, message="Next time eat a salad.")
        elif mercs_choice == 6:
            CTkToolTip(merc_label, message="Mental sickness.")
        elif mercs_choice == 7:
            CTkToolTip(merc_label, message="STAND ON THE POINT, MAGGOT!\nTHIS POINT IS MINE!\nDO YOU UNDERSTAND THAT?\nGOT ANYTHING FUNNY TO SAY ABOUT THAT, FUNNY MAN?")
        elif mercs_choice == 8:
            CTkToolTip(merc_label, message="Your mother!")
        #weapon kind and image
        if changed_weapon_label.cget("image"):
            weapon_icon = changed_weapon_label.cget("image")
        else:
            max_width2, max_height2 = 190, 170
            if kind == "Primary":
                raw_image2 = Image.open(random.choice(primary_wep_paths))
                raw_size = ImageOps.contain(raw_image2, (max_width2, max_height2))
                weapon_icon = ctk.CTkImage(light_image=raw_image2, dark_image=raw_image2, size=raw_size.size)
            elif kind == "Secondary":
                raw_image2 = Image.open(random.choice(secondary_wep_paths))
                raw_size = ImageOps.contain(raw_image2, (max_width2, max_height2))
                weapon_icon = ctk.CTkImage(light_image=raw_image2, dark_image=raw_image2, size=raw_size.size)
            elif kind == "Melee":
                raw_image2 = Image.open(random.choice(melee_wep_paths))
                raw_size = ImageOps.contain(raw_image2, (max_width2, max_height2))
                weapon_icon = ctk.CTkImage(light_image=raw_image2, dark_image=raw_image2, size=raw_size.size)
            elif kind == "PDA":
                raw_image2 = Image.open(random.choice(PDA_wep_paths))
                raw_size = ImageOps.contain(raw_image2, (max_width2, max_height2))
                weapon_icon = ctk.CTkImage(light_image=raw_image2, dark_image=raw_image2, size=raw_size.size)
            elif kind == "all":
                raw_image2 = Image.open(random.choice(random.choice([primary_wep_paths, secondary_wep_paths, melee_wep_paths, PDA_wep_paths])))
                raw_size = ImageOps.contain(raw_image2, (max_width2, max_height2))
                weapon_icon = ctk.CTkImage(light_image=raw_image2, dark_image=raw_image2, size=raw_size.size)
        weapon_label.configure(image=weapon_icon)
        #name and level
            #name rarety
        if quality_changer.get():
            if quality_changer.get() == "All":
                quality_choice = random.choices(quality_colors, weights=quality_weights, k=1)[0]
                name_label.configure(text_color=quality_choice)
            elif quality_changer.get() == "Unique":
                quality_choice = quality_colors[0]
                name_label.configure(text_color=quality_choice)
            elif quality_changer.get() == "Strange":
                quality_choice = quality_colors[1]
                name_label.configure(text_color=quality_choice)
            elif quality_changer.get() == "Vintage":
                quality_choice = quality_colors[2]
                name_label.configure(text_color=quality_choice)
            elif quality_changer.get() == "Genuine":
                quality_choice = quality_colors[3]
                name_label.configure(text_color=quality_choice)
            elif quality_changer.get() == "Australium":
                quality_choice = quality_colors[4]
                name_label.configure(text_color=quality_choice)
            elif quality_changer.get() == "Unusual":
                quality_choice = quality_colors[5]
                name_label.configure(text_color=quality_choice)
        else:
            quality_choice = random.choices(quality_colors, weights=quality_weights, k=1)[0]
            name_label.configure(text_color=quality_choice)
        quality_index = quality_colors.index(quality_choice)
        quality_name = qualities[quality_index + 1]
            #name
        if name_changer.get():
            name = name_changer.get()
        else:
            name = random.choice(nouns)
            adj = random.choice(adjs)
            chance = random.randint(0, 3)
            if chance == 0:
                if quality_name == qualities[0] or quality_name == qualities[1]:
                    name = "The" + " " + name
                else:
                    name = "The" + " " + quality_name + " " + name
            elif chance == 1:
                if quality_name == qualities[0] or quality_name == qualities[1]:
                    name = name + "er"
                else:
                    name = quality_name + " " + name + "er"
            elif chance == 2:
                if quality_name == qualities[0] or quality_name == qualities[1]:
                    name = adj + " " + name
                else:
                    name = quality_name + " " + adj + " " + name
            elif chance == 3:
                if quality_name == qualities[0] or quality_name == qualities[1]:
                    name = adj
                else:
                    name = quality_name + " " + adj
        name_changer.configure(placeholder_text=name)
        if level_changer.get():
            level = level_changer.get()
        else:
            level = int(round(min(random.randint(1, 100), random.randint(1, 100)))/10)*10
        level_changer.configure(placeholder_text=level)
        name_label.configure(text=name)
        window.update_idletasks()
        placment_space = 210
        name_label.place(x=window_width/2, y=placment_space, anchor="n")
        placment_space += name_label.winfo_reqheight()
        level_label.configure(text=f"Level {level} {Type}")
        level_label.place(x=window_width/2, y=placment_space + 15, anchor="center")
        window.update_idletasks()
        placment_space += level_label.winfo_reqheight() + 10
        #attributes
        if not attributes_changer.get("1.0", "end-1c"):
            if mercs_choice == 0:
                attributes = demo_attributes
            elif mercs_choice == 1:
                attributes = engineer_attributes
            elif mercs_choice == 2:
                attributes = heavy_attributes
            elif mercs_choice == 3:
                attributes = medic_attributes
            elif mercs_choice == 4:
                attributes = pyro_attributes
            elif mercs_choice == 5:
                attributes = scout_attributes
            elif mercs_choice == 6:
                attributes = sniper_attributes
            elif mercs_choice == 7:
                attributes = soldier_attributes
            elif mercs_choice == 8:
                attributes = spy_attributes
            if num_changer.get():
                if num_changer.get() == "Why are you like this?":
                    max_num = 1
                elif num_changer.get() == "TF2 updates...":
                    max_num = 2
                elif num_changer.get() == "Bread size":
                    max_num = 4
                elif num_changer.get() == "The classic":
                    max_num = 8
                elif num_changer.get() == "Mann SIZE!":
                    max_num = 16
            else:
                max_num = 8
            num_of_attributes = random.randint(0, max_num)
            chosen_attributes = random.sample(attributes, min(num_of_attributes, len(attributes)))
        else:
            chosen_attributes = attributes_changer.get("1.0", "end-1c").splitlines()

        chosen_attributes.sort(key= lambda attrib: order.get(attrib[1], 3))
        try:
            for i in range(len(chosen_attributes)):
                if "##" in chosen_attributes[i]:
                    inx = chosen_attributes[i].index("##")
                    if chosen_attributes[i][inx:].startswith("##(percentage)"): #percentage
                        if chosen_attributes[i][1] == "+":
                            value = random.randint(5, 300)
                        else:
                            value = random.randint(5, 100)
                        value = str(round(value / 5) * 5) + "%"
                        chosen_attributes[i] = chosen_attributes[i].replace("##(percentage)", value)
                    elif chosen_attributes[i][inx:].startswith("##(particle_index)"): #particle
                        value = str(random.randint(1, 300))
                        chosen_attributes[i] = chosen_attributes[i].replace("##(particle_index)", value)
                    elif chosen_attributes[i][inx:].startswith("##(additive)"): #additive
                        if chosen_attributes[i][1] == "+":
                            value = random.randint(5, 300)
                        else:
                            value = random.randint(5, 80)
                        value = str(round(value / 5) * 5)
                        chosen_attributes[i] = chosen_attributes[i].replace("##(additive)", value)
                    elif chosen_attributes[i][inx:].startswith("##(additive_percentage)"): #additive_percentage
                        value = random.randint(5, 100)
                        value = str(round(value / 5) * 5) + "%"
                        chosen_attributes[i] = chosen_attributes[i].replace("##(additive_percentage)", value)
                    elif chosen_attributes[i][inx:].startswith("##(inverted_percentage)"): #inverted_percentage
                        if chosen_attributes[i][1] == "+":
                            value = random.randint(5, 250)
                        else:
                            value = random.randint(5, 80)
                        value = str(round(value / 5) * 5) + "%"
                        chosen_attributes[i] = chosen_attributes[i].replace("##(inverted_percentage)", value)
                    elif chosen_attributes[i][inx:].startswith("##(integer)"): #integer
                        value = str(random.randint(0, 4))
                        chosen_attributes[i] = chosen_attributes[i].replace("##(integer)", value)
                    elif chosen_attributes[i][inx:].startswith("##(or_equal)"): #or_equal
                        value = random.choice(["0", "1"])
                        chosen_attributes[i] = chosen_attributes[i].replace("##(or_equal)", value)
                    elif chosen_attributes[i][inx:].startswith("##(date)"): #date
                        month = random.choice(["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sept", "Oct", "Nov", "Dec"])
                        if month == "Feb":
                            day = str(random.randint(1, 28))
                        elif month in ["Apr", "Jun", "Sept", "Nov"]:
                            day = str(random.randint(1, 30))
                        else:
                            day = str(random.randint(1, 31))
                        year = str(random.randint(2007, 2038))
                        value = f"{month} {day}, {year}"
                        chosen_attributes[i] = chosen_attributes[i].replace("##(date)", value)
                    elif chosen_attributes[i][inx:].startswith("##(account_id)"): #account_id
                        value = random.choice(["THAT_Snowy", "Valve", "Heavy's right eyebrow", "Archimedes", "Toby Fox", "You", "No one", "Wikipedia", "Some guy called Alan", "Freddy Fazbear", "Sun Tzu"])
                        chosen_attributes[i] = chosen_attributes[i].replace("##(account_id)", value)

            for i in range(len(chosen_attributes)):
                if chosen_attributes[i][1] == "=":
                    color = "#ebe2ca"
                elif chosen_attributes[i][1] == "+":
                    color = "#99ccff"
                elif chosen_attributes[i][1] == "-":
                    color = "#ff4040"
                chosen_attributes[i] = chosen_attributes[i][4:]
                attribute_label = ctk.CTkLabel(window, text=chosen_attributes[i], font=("TF2 BUILD", 20), text_color=color, fg_color="#24201b", bg_color="#24201b", wraplength=450, justify="center")
                attribute_label.place(x=window_width/2, y=placment_space + y_offset, anchor="n")
                created_attribute_label.append(attribute_label)
                window.update_idletasks()
                y_offset += attribute_label.winfo_height() + 6
        except Exception:
            messagebox.showerror("Error", "You typed the [ ] wrong :[\n(Read the help? label for more info.)")

        placment_space += y_offset + 25
        new_window_height = window_height
        more_Button.configure(height=placment_space - 20)
        window.geometry(f"{window_width + 65}x{placment_space}")
        first_time = False
    except Exception:
        messagebox.showerror("Error", "Something went wrong :[")

def more_tools(event=None):
    if not option_window.winfo_ismapped():
        option_window.deiconify()
        option_window.transient(window)
        pywinstyles.change_header_color(option_window, color="#24201b")
        option_window.lift()
        option_window.focus_force()
    else:
        option_window.withdraw()
def custom():
    if not custom_window.winfo_ismapped():
        custom_window.deiconify()
        custom_window.transient(window)
        pywinstyles.change_header_color(custom_window, color="#24201b")
        custom_window.lift()
        custom_window.focus_force()
        attributes_changer.insert("0.0", "[=] White Placeholder\n[+] Blue Placeholder\n[-] Red Placeholder")
    else:
        custom_window.withdraw()
        clean_custom()

def screenshot():
    try:
        option_window_open = False if not option_window.winfo_ismapped() else True
        custom_window_open = False if not custom_window.winfo_ismapped() else True
        option_window.withdraw()
        custom_window.withdraw()
        time.sleep(0.5)
        bbox = (window.winfo_rootx(), window.winfo_rooty(), window.winfo_rootx() + (window.winfo_width() - 75), window.winfo_rooty() + window.winfo_height())
        window.deiconify()
        window.lift()
        window.focus_force()
        img = ImageGrab.grab(bbox=bbox)
        img.convert("RGBA")
        mask = Image.new("L", img.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.rounded_rectangle((0, 0, img.size[0], img.size[1]), radius=30, fill=255)
        img.putalpha(mask)
        buf = ctypes.create_unicode_buffer(wintypes.MAX_PATH)
        ctypes.windll.shell32.SHGetFolderPathW(None, 0x0027, None, 0, buf)
        path = buf.value
        date = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        img.save(os.path.join(path, f"Weapon({date}).png"))
        messagebox.showinfo("NOT Error", "Check your images folder :]")
    except Exception:
        messagebox.showerror("Error", f"Something went wrong :[")
    if option_window_open:
        more_tools()
    if custom_window_open:
        custom()

def choose_image(event):
    global  changed_weapon_label
    file_path = filedialog.askopenfilename(title="Choose an image", filetypes=[("Image files", "*.png *.jpg")])
    if file_path:
        raw_image = Image.open(file_path)
        max_width, max_height = 190, 170
        raw_size = ImageOps.contain(raw_image, (max_width, max_height))
        weapon_icon = ctk.CTkImage(light_image=raw_image, dark_image=raw_image, size=raw_size.size)
        changed_weapon_label.configure(image=weapon_icon,)
        changed_weapon_label.place(relx=0.5, rely=0.5, anchor="center")

def attributes_changer_on_enter_pressed(event):
    event.widget.insert("insert", "\n[=]")
    return "break"

def level_and_type_done(event):
    if level_changer.get():
        level_text = level_changer.get()
        level_changer.delete("0", "end")
        level_text = "".join(char for char in level_text if char in allowed_letters_list)
        if "-" in level_text:
            if not level_text.startswith("-"):
                level_text = level_text.replace("-", "")
        level_changer.insert("0", level_text[:7])
    if type_changer.get():
        type_text = type_changer.get()
        type_changer.configure(require_redraw=True)
        type_entry = type_changer._entry
        type_entry.delete(0, "end")
        type_entry.insert("0", type_text[:20])

def on_windows_restore(event):
    pywinstyles.change_header_color(option_window, color="#24201b")
    pywinstyles.change_header_color(custom_window, color="#24201b")

generate()
#binds
window.bind("<space>", generate)
window.bind("<Escape>", more_tools)
option_window.bind("<space>", generate)
option_window.bind("<Escape>", more_tools)
option_window.bind("<Map>", on_windows_restore)
custom_window.bind("<Map>", on_windows_restore)
attributes_changer.bind("<Return>", attributes_changer_on_enter_pressed)
level_changer.bind("<Return>", level_and_type_done)
level_changer.bind("<FocusOut>", level_and_type_done)
type_changer.bind("<Return>", level_and_type_done)
type_changer.bind("<FocusOut>", level_and_type_done)
image_changer.bind("<Button-1>", choose_image)
changed_weapon_label.bind("<Button-1>", choose_image)

window.mainloop()