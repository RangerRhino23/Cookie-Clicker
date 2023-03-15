from ursina import *
import json

with open("data.json", 'r') as data:
    data=json.load(data)

app = Ursina(borderless=False)

window.title = 'Cookie Clicker'
window.icon = 'assets/icon.ico'
window.fullscreen = False
window.exit_button.visible = False
window.fps_counter.enabled = False

cookies=data['cookies']
multiplier = data['multiplier']
multiplier_cost = data['multiplier_cost']
ambient = data['ambient']
ambient_cost = data['ambient_cost']
cookie_cooldown = 0
cookies_text = Text(text=f'Cookies Collected: {cookies}', scale=2, x=-.2,y=.45)

def update():
    global cookies,data, cookie_cooldown, multiplier_button, ambient_button, multiplier_cost, ambient_cost
    cookies_text.text = f'Cookies Colected: {cookies}'
    multiplier_button.tooltip.text=f'Buy Multiplier for <green>${multiplier_cost}'
    ambient_button.tooltip.text=f'Buy Cookie Maker for <green>${ambient_cost}'
    cookie_cooldown = cookie_cooldown + 1
    if cookie_cooldown == 50:
        cookie_cooldown = 0
        cookies += ambient
        data["cookies"] = cookies

def save_data():
    global data
    with open("data.json", "w") as f:
        json.dump(data, f)
    Audio('assets/save_sound.ogg',autoplay=True,loop=False,auto_destroy=True)
    infoText=Text(text='Game saved!',x=-.1)
    destroy(infoText,delay=2)

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
    data["cookies"] = cookies


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

cookie = Entity(model='quad', texture='assets/cookie.png', scale=2, x=-5)
cookie_button = Button(scale=0.25, x=-0.615, on_click=add_cookie, visible=False)
cookie_button.tooltip = Tooltip('Click Me!')

multiplier_button = Button(icon='assets/multiplier.png',scale=0.25, x=0.615, y=0.125, on_click=add_multiplier, visible = True, pressed_color= color.clear, color=color.clear, highlight_color= color.clear)
multiplier_button.tooltip = Tooltip(f'Buy Multiplier for ${multiplier_cost}')

ambient_button = Button(icon='assets/cookiemaker.png',scale=0.25, x=0.615, y=-0.125, on_click=add_ambient, visible = True, pressed_color= color.clear, color=color.clear, highlight_color= color.clear)
ambient_button.tooltip = Tooltip(f'Buy Cookie Maker for ${ambient_cost}')

save_button = Button(icon='assets/floppy.png',scale=0.25, x=-0.7, y=0.4, on_click=save_data, visible = True, pressed_color= color.clear, color=color.clear, highlight_color= color.clear)
save_button.tooltip = Tooltip("<gold>Save progress")



app.run()