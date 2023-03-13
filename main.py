from ursina import *

app = Ursina()
window.title = 'Cookie Clicker'
window.icon = 'assets/icon.ico'
window.borderless = False
window.fullscreen = False
window.exit_button.visible = False
window.fps_counter.enabled = False

cookies = 0
multiplier = 1
multiplier_cost = 100
ambient = 1
ambient_cost = 100
cookie_cooldown = 0
cookies_text = Text(text=f'Cookies Collected: {cookies}', scale=2, y=.45)

def update():
    global cookies, cookie_cooldown, multiplier_button, ambient_button, multiplier_cost, ambient_cost
    cookies_text.text = f'Cookies Colected: {cookies}'
    multiplier_button.text = (f'Buy Multiplier: ${multiplier_cost}')
    ambient_button.text = (f'Buy Cookie Maker: ${ambient_cost}')
    cookie_cooldown = cookie_cooldown + 1
    if cookie_cooldown == 50:
        cookie_cooldown = 0
        cookies += ambient

def input(key):
    global cookies, multiplier, ambient
    if key == 'q':
        quit()
    if key == 'space':
        add_cookie()

def add_cookie():
    global cookies
    cookies = cookies + 1 * multiplier

def add_multiplier():
    global cookies, multiplier_cost, multiplier
    if cookies >= multiplier_cost:
        cookies = cookies - multiplier_cost
        multiplier = multiplier + 1
        multiplier_cost = multiplier_cost + round(multiplier_cost * 0.125)
    else:
        print_on_screen("Not Enough Cookies to Buy Multiplier!")

def add_ambient():
    global cookies, ambient_cost, ambient
    if cookies >= ambient_cost:
        cookies = cookies - ambient_cost
        ambient = ambient + 1
        ambient_cost = ambient_cost + round(ambient_cost * 0.125)
    else:
        print_on_screen('Not Enough Cookies to Buy Cookie Maker!')


cookie = Entity(model='quad', texture='assets/cookie.png', scale=2, x=-5)
cookie_button = Button(scale=0.25, x=-0.615, on_click=add_cookie, visible=False)
cookie_button.tooltip = Tooltip('Click Me!')

multiplier_img = Entity(model='quad', texture='assets/multiplier.png', scale=2, x=5, y=1.25)
multiplier_button = Button(scale=0.25, x=0.615, y=0.125, on_click=add_multiplier, visible = True, pressed_color= color.clear, highlight_color= color.clear)
multiplier_button.tooltip = Tooltip(f'Buy Multiplier')

ambient_img = Entity(model='quad', texture='assets/cookiemaker.png', scale=2, x=5, y=-0.9)
ambient_button = Button(scale=0.25, x=0.615, y=-0.125, on_click=add_ambient, visible = True, pressed_color= color.clear, highlight_color= color.clear)
ambient_button.tooltip = Tooltip(f'Buy Cookie Maker')





app.run()