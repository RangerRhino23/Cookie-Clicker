from ursina import *
import json #used for reading the json file (built in with every python)

with open("data.json", 'r') as data: # this opens the file data.json as data, it doesn't have to be data it can be anything and opens it as read 'r'
    data=json.load(data) # this then loads all the data as a dict in the data variable
'''
The with statement is used to open the "data.json" file in read mode ('r')
and assigns it to the variable data. The open() function returns a file 
object that represents the opened file. The with statement ensures that 
the file object is closed automatically when the block of code within the 
with statement is exited. The json.load() function is used to read the 
contents of the opened file object (data) and load it as a Python 
dictionary object. The resulting dictionary object is assigned to the 
variable data. Therefore, this block of code opens the "data.json" file 
and loads its contents into a Python dictionary object, which is 
assigned to the data variable.
'''
app = Ursina(borderless=False)

window.title = 'Cookie Clicker'
window.icon = 'assets/icon.ico'
window.fullscreen = False
window.exit_button.visible = False
window.fps_counter.enabled = False

volume=1
cookies=data['cookies'] #This takes the value of cookies from the json file and sets the json value to the game value
multiplier = data['multiplier'] 
multiplier_cost = data['multiplier_cost']
ambient = data['ambient']
ambient_cost = data['ambient_cost']
Autosave=data['Autosave']
'''
This line of code retrieves the value of the "cookies" key from 
the data dictionary using dictionary indexing (data['cookies']) 
and assigns that value to the variable cookies. In other words, cookies 
is set to the value of the "cookies" key in the data dictionary.
This code does not modify the data dictionary or the "data.json" 
file itself. It only retrieves a value from the dictionary and assigns 
it to a variable in the local Python script.
'''
bg_music=Audio('assets/bg_music.ogg',autoplay=True,loop=True)

cookie_cooldown = 0
cookies_text = Text(text=f'Cookies Collected: {cookies}', scale=2, x=-.2,y=.45)

def update():
    global Autosave,cookies,data, cookie_cooldown, multiplier_button, ambient_button, multiplier_cost, ambient_cost
    cookies_text.text = f'Cookies Colected: {cookies}'
    multiplier_button.tooltip.text=f'Buy Multiplier for <green>${multiplier_cost}'
    ambient_button.tooltip.text=f'Buy Cookie Maker for <green>${ambient_cost}'
    cookie_cooldown = cookie_cooldown + 1
    if cookie_cooldown == 50:
        cookie_cooldown = 0
        cookies += ambient
        data["cookies"] = cookies #This changes the json variable locally so its saved in this python file but not the json file
    if Autosave:
        with open("data.json", "w") as f:
            json.dump(data, f)
'''
The code data["cookies"] = cookies adds a new key-value pair to the data 
dictionary, where the key is "cookies" and the value is the value of the 
cookies variable. This code updates the data dictionary locally 
within the Python script, but does not modify the "data.json" file itself. 
In order to persist the updated data dictionary to the "data.json" file
you would need to call the save_data(). refer to line 69-74 (noice)
'''

def save_data():
    global data #not sure if you need to globally define it but just in case
    with open("data.json", "w") as f: #same as before execpt this time it writes to the json file 'w' as 'f' this time (again doesnt matter what you set it too)
        json.dump(data, f) #This dumps/transfers all the data from the local variables to the json file
    Audio('assets/save_sound.ogg',autoplay=True,loop=False,auto_destroy=True)
    infoText=Text(text='Game saved!',x=-.1)
    destroy(infoText,delay=2)
'''
This function saves the contents of the data variable to a JSON file 
named "data.json" The global keyword is used to indicate that data is 
defined outside of the function. The file "data.json" is opened in write 
mode using the with statement, and assigned to the variable f. The 
json.dump method is used to write the contents of the data variable to 
the file object f in JSON format.
'''
def input(key):
    global cookies, multiplier, ambient
    if key == 'q':
        quit()
    if key == 'space':
        add_cookie()

def add_cookie():
    global cookies,multiplier
    cookies += 1 * multiplier
    Audio('assets/crush.ogg',autoplay=True,loop=False,auto_destroy=True,volume=2)
    cookie.scale = [e*1.25 for e in [1.5,1.5]]
    cookie.animate('scale_x', 2, duration=.1)
    cookie.animate('scale_y', 2, duration=.1)
    data["cookies"] = cookies #changes the data locally again


def add_multiplier():
    global cookies, multiplier_cost, multiplier, num_calls
    if cookies >= multiplier_cost:
        cookies -= multiplier_cost
        multiplier += 1
        multiplier_cost = multiplier_cost + round(multiplier_cost * 0.125)
        data["multiplier"] +=1
        data['multiplier_cost'] = multiplier_cost
        data["cookies"] = cookies

    else:
        print_on_screen("Not Enough Cookies to Buy Multiplier!")



def add_ambient():
    global cookies, ambient_cost, ambient
    if cookies >= ambient_cost:
        cookies -= ambient_cost
        ambient += 1
        ambient_cost = ambient_cost + round(ambient_cost * 0.125)
        data["ambient"] += 1
        data["ambient_cost"] = ambient_cost
        data["cookies"] = cookies

    else:
        print_on_screen('Not Enough Cookies to Buy Cookie Maker!')


def set_volume():
    global volume_slider,volume
    volume = volume_slider.value/100
    app.sfxManagerList[0].setVolume(volume)
    volume = volume

cookie = Entity(model='quad', texture='assets/cookie.png', scale=2, x=-5)
cookie_button = Button(scale=0.25, x=-0.615, on_click=add_cookie, visible=False)
cookie_button.tooltip = Tooltip('Click Me!')

multiplier_button = Button(icon='assets/multiplier.png',scale=0.25, x=0.615, y=0.125, on_click=add_multiplier, visible = True, pressed_color= color.clear, color=color.clear, highlight_color= color.clear)
multiplier_button.tooltip = Tooltip(f'Buy Multiplier for ${multiplier_cost}')

ambient_button = Button(icon='assets/cookiemaker.png',scale=0.25, x=0.615, y=-0.125, on_click=add_ambient, visible = True, pressed_color= color.clear, color=color.clear, highlight_color= color.clear)
ambient_button.tooltip = Tooltip(f'Buy Cookie Maker for ${ambient_cost}')

if not Autosave:
    save_button = Button(icon='assets/floppy.png',scale=0.25, x=-0.7, y=0.4, on_click=save_data, visible = True, pressed_color= color.clear, color=color.clear, highlight_color= color.clear)
    save_button.tooltip = Tooltip("<gold>Save progress")

volume_slider = Slider(min=0, max=100, default=volume*100, dynamic=True,position=(-.1, -.4),text='Master volume:',on_value_changed = set_volume)


app.run()