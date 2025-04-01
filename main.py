import string

import pygame as pg
import pygame_widgets
import functools
from UI import *
from random import *
import time
import threading  # Импортируем модуль threading
from math import *
import datetime
import sys
import os

SCREEN_SIZE = (800, 500)
CONSOLE_HEIGHT = 5  # Максимальное количество строк в консоли
CONSOLE_START_Y = 450  # Начальная Y-координата консоли
CONSOLE_LINE_HEIGHT = 20  # Высота одной строки
CONSOLE_COLOR = "Grey"  # Цвет текста консоли
CONSOLE_FONT_SIZE = 15  # Размер текста консоли
CONSOLE_LOG = []  # Изначально пустой список, содержащий текущую строку консоли
CONSOLE_CURRENT_TEXT = ""  # Переменная для хранения текущего отображаемого текста
CODING_TABLES = string.ascii_letters + string.digits
MODULATIONS = {
    "AM": [["x1 * random() * ZOOM / 48", "red"], ["randint(-255, 255)", None]]
}
LOADING = ["/", "|", "\\", "-"]
SIGNALS = {
    0: {
        "data": "RANDOM_SIGNAL|RANDOM_LENGTH",
        "about": "Strange signal from other galaxy.",
        "type": "UNUSUAL DATA"
    },
    1: {
        "data": "NOW_TIME",
        "about": "GPS satellite broadcasting the time.",
        "type": "GPS SATELITE"
    },
    2: {
        "data": "RANDOM_SIGNAL|2|V2UgaGF2ZSBuZXcgc2lnbmFsIGZyb20gKkRBVEEgV0FTIERFTEVURUQqLCB0aGF0cyBhbWF6aW5nIHdlIGNvdWxkIGRvIGEgbG90IG9mIGRpc2NvdmVyaWVz|RANDOM_SIGNAL|2",
        "about": "Military satellite, transmitting data.",
        "type": "MILITARY SATELLITE"
    },
    3: {
        "data": "RANDOM_SIGNAL|RANDOM_LENGTH",
        "about": "ERROR in your receiver. Dont' mind.",
        "type": "BUG"
    },
    4: {
        "data": "RANDOM_SIGNAL|RANDOM_LENGTH",
        "about": "A asteroid emits electromagnetic waves.",
        "type": "NATURAL EMITTER"
    },
    5: {
        "data": "RANDOM_SIGNAL|RANDOM_LENGTH",
        "about": "The star emits electromagnetic waves.",
        "type": "NATURAL EMITTER"
    },
    999: {
        "data": "Earth time: NOW_TIME",
        "about": "Human-based signal, now press transmit button.",
        "send": "You've finally found earth, and now we can transmit a signal! Trying... YOUR TRANSMITTER IS BROKEN...",
        "type": "EARTH"
    },
}
frames_path = 'clips'
frame_files = sorted(os.listdir(frames_path))

class FrameLoader:
    def __init__(self, frame_files, screen_size):
        self.frame_files = frame_files
        self.screen_size = screen_size
        self.frames = {}
        self.next_frame_to_load = 0

    def load_frame(self, index):
        if index not in self.frames and 0 <= index < len(self.frame_files):
            try:
                image = pg.image.load(os.path.join(frames_path, self.frame_files[index]))
                scaled_image = pg.transform.scale(image, self.screen_size)
                self.frames[index] = scaled_image
            except pg.error as e:
                print(f"Ошибка загрузки кадра {self.frame_files[index]}: {e}")
                self.frames[index] = None

    def get_frame(self, index):
        self.load_frame(index)
        return self.frames.get(index)

    def preload_next_frames(self, count=5):
        for i in range(count):
            index_to_load = (self.next_frame_to_load + i) % len(self.frame_files)
            self.load_frame(index_to_load)

    def update(self):
        self.preload_next_frames()
        self.next_frame_to_load = (self.next_frame_to_load + 1) % len(self.frame_files)


frame_index = 0
pg.mixer.init()
def set_background_music_volume(volume):
    global BACKGROUND_MUSIC
    if BACKGROUND_MUSIC:
        BACKGROUND_MUSIC.set_volume(volume)
pg.mixer.init()
try:
    BACKGROUND_MUSIC = pg.mixer.Sound("sounds/back.mp3")
    WHITE_NOISE = pg.mixer.Sound("sounds/fonov.mp3")
    LOADING_SOUND = pg.mixer.Sound("sounds/load.mp3")
    LOADING_SOUND.set_volume(1.0)
except pg.error as e:
    print(f"Ошибка загрузки звука: {e}")
    BACKGROUND_MUSIC = None
    WHITE_NOISE = None
    LOADING_SOUND = None

def add_to_console(char):
    global CONSOLE_CURRENT_TEXT
    CONSOLE_CURRENT_TEXT += char


# Функция для анимации текста
def animate_text(text, screen, fonts, delay=0.01):
    global CONSOLE_CURRENT_TEXT, CONSOLE_LOG

    words = text.split()
    CONSOLE_CURRENT_TEXT = ""

    for word in words:
        if len(CONSOLE_CURRENT_TEXT) + len(word) + (1 if CONSOLE_CURRENT_TEXT else 0) > 72:
            CONSOLE_LOG.append(CONSOLE_CURRENT_TEXT)
            CONSOLE_CURRENT_TEXT = ""
            if len(CONSOLE_LOG) > CONSOLE_HEIGHT:
                del CONSOLE_LOG[0]

        if CONSOLE_CURRENT_TEXT:
            CONSOLE_CURRENT_TEXT += " "

        for char in word:
            if len(CONSOLE_CURRENT_TEXT) < 70:
                CONSOLE_CURRENT_TEXT += char

                draw_console(screen, fonts)
                time.sleep(delay)

    if CONSOLE_CURRENT_TEXT:
        CONSOLE_LOG.append(CONSOLE_CURRENT_TEXT)
        if len(CONSOLE_LOG) > CONSOLE_HEIGHT:
            CONSOLE_LOG.pop(0)
    CONSOLE_CURRENT_TEXT = ""


def draw_console(screen, fonts):
    fontss = [pg.font.SysFont("monospace", a) for a in range(1, 41)]
    pg.draw.rect(screen, "BLACK",
                 (18, CONSOLE_START_Y - 10, SCREEN_SIZE[0] - 480, 7 * CONSOLE_LINE_HEIGHT))
    for number, text in enumerate(CONSOLE_LOG[-CONSOLE_HEIGHT:]):
        text_surface = fontss[CONSOLE_FONT_SIZE].render(text, True, CONSOLE_COLOR)
        text_rect = text_surface.get_rect(topleft=(30, CONSOLE_START_Y + number * CONSOLE_LINE_HEIGHT))
        screen.blit(text_surface, text_rect)
    # Рисуем текущий текст
    text_surface = fontss[CONSOLE_FONT_SIZE].render(CONSOLE_CURRENT_TEXT, True, CONSOLE_COLOR)
    text_rect = text_surface.get_rect(
        topleft=(30, CONSOLE_START_Y + len(CONSOLE_LOG[-CONSOLE_HEIGHT:]) * CONSOLE_LINE_HEIGHT))
    screen.blit(text_surface, text_rect)


def display_loading(screen, fonts, space):
    global CONSOLE_LOG
    CONSOLE_LOG.clear()
    data = space.research()
    # Проверяем содержит ли вообще space данную позицию
    if "NO SIGNAL" in data:
        CONSOLE_LOG.append(data)
        return
    elif "PRECISION" in data:
        CONSOLE_LOG.append(data)
        return
    draw_console(screen, fonts)

    signal_strength, signal_type = data
    signal_volume = int(signal_strength * 1000)
    bytetrate = randint(100, 1000)
    total_size = signal_volume * bytetrate

    # Форматируем вывод информации о загрузке
    draw_console(screen, fonts)
    if LOADING_SOUND:
        LOADING_SOUND.play(loops=-1)
    count = 0
    while True:
        loading_progress = (count * 100) // (total_size // bytetrate)
        if loading_progress == 100:
            if LOADING_SOUND:
                LOADING_SOUND.stop()
            break

        loading_info = [
            f"Processing signal: {loading_progress:.2f}% | {bytetrate + randint(-20, 20)} bytes/s | {round(bytetrate * count / 1000)}\\{total_size // 1000} KB | {signal_strength:.2f}",
            f"Type of: {LOADING[count % len(LOADING)]}",
            f"About: {LOADING[(count + 3) % len(LOADING)]}",
            f"Decoded {LOADING[(count + 6) % len(LOADING)]}"
        ]
        CONSOLE_LOG.clear()
        CONSOLE_LOG = loading_info
        draw_console(screen, fonts)
        time.sleep(0.001)
        count += 1
    data = SIGNALS[signal_type]['data'].replace("NOW_TIME", str(datetime.datetime.now())).split("|")
    out = []
    for a in range(len(data)):
        if data[a] == "RANDOM_SIGNAL":
            if data[a + 1] == "RANDOM_LENGTH":
                lens = randint(8, 32)
            else:
                lens = int(data[a + 1])
            out.append("".join([CODING_TABLES[randint(0, len(CODING_TABLES) - 1)] for _ in range(lens)]))
        else:
            if data[a-1] != "RANDOM_SIGNAL":
                out.append(data[a])
    print(out)
    data = "".join(out)
    add = ""
    if len(data) > 70:
        add = data[70:140]
        data = data[:70]
    loading_info = [
        f"Processing signal: 100.00% {str(space.antPos)} | 0 bytes/s | {total_size // 1000} KB | {signal_strength:.2f}",
        f"Type of:{SIGNALS[signal_type]['type']}|About: {SIGNALS[signal_type]['about']}",
        f"Decoded data:",
        f"{data}",
        f"{add}"
    ]
    CONSOLE_LOG = loading_info
    draw_console(screen, fonts)


def correctFloat(float_value):
    if float_value > 1:
        float_value = 1
    elif float_value < 0:
        float_value = 0
    return float_value


def updateScreen(screen):
    global space
    pg.draw.rect(screen, [0] * 3, (20, 40, 720, 360))
    datas = [[int(key.split("\\")[0]), int(key.split("\\")[1]), value] for key, value in
             space.space.items()]
    [datas.append([x, y, [data, 3]]) if data else None for x, y, data in
     [[randint(0, space.size), randint(0, space.size), round(random() - 0.25, 2)] for _
      in range(space.size // 2)]]
    [datas.append([x, y, [data, 3]]) if data else None for x, y, data in
     [[randint(0, space.size), randint(0, space.size), 0.2] for _
      in range(space.size // 2)]]
    screenMap = []
    [screenMap.append([x, y, data]) if 30 < x * space.zoom + 20 - space.zoom / 4 + 400 - space.antPos[
        0] * space.zoom < 730 and 50 < y * space.zoom + 40 - space.zoom / 4 + 180 - space.antPos[
                                           1] * space.zoom < 390 and space.sensitivity <= data[0] else None for
     x, y, data in datas]
    [pg.draw.rect(screen, [round(255 * correctFloat(data[0] - space.sensitivity + 0.15))] * 3,
                      (x * space.zoom + 20 - space.zoom / 4 + 360 - space.antPos[0] * space.zoom,
                       y * space.zoom + 40 - space.zoom / 4 + 180 - space.antPos[1] * space.zoom, space.zoom / 2,
                       space.zoom / 2))
     for x, y, data
     in screenMap]


def updateNumber(number, NumOfDigit, negative=False):
    global space
    if number == 1:
        data = list(str(space.antPos[0]).rjust(6, "0"))
    if number == 2:
        data = list(str(space.antPos[1]).rjust(6, "0"))
    if negative:
        out = int(data[NumOfDigit]) - 1
    else:
        out = int(data[NumOfDigit]) + 1
    data[NumOfDigit] = str(out)
    data = list(map(int, data[::-1]))
    for num in range(len(data)):
        if data[num] > 9:
            data[num] = 0
            if num < len(data) - 1:
                data[num + 1] += 1
    for num in range(len(data)):
        if data[num] < 0:
            data[num] = 9
            if num < len(data) - 1:
                data[num + 1] -= 1
    data = data[::-1]
    data = list(map(str, data))
    if number == 1:
        space.antPos[0] = int("".join(data))
    if number == 2:
        space.antPos[1] = int("".join(data))

class Space:
    def __init__(self):
        self.size = 1024
        self.space = {}
        for _ in range(10000):
            self.space[str(randint(0, self.size - 1)) + "\\" + str(randint(0, self.size - 1))] = [random(),
                                                                                                  round(randint(0, 5))]
        self.SignalOfEarth = [randint(0, self.size - 1), randint(0, self.size - 1)]
        self.space[str(self.SignalOfEarth[0]) + "\\" + str(self.SignalOfEarth[1])] = [random(), 999]
        self.antPos = [self.size // 2] * 2
        self.zoom, self.sensitivity = 1, 1
        self.signalMEM = []
        self.graphCount = 0
        self.count = 0

    def research(self):
        pos_str = str(self.antPos[0]) + "\\" + str(self.antPos[1])
        if pos_str not in self.space or self.sensitivity >= self.space[pos_str][0]:
            return "NO SIGNAL. Nothing interesting only cold space..."

        if self.zoom != 38:
            return "PRECISION. Need more precision. Focus on signal by zoom"

        return self.space[pos_str]

    def chgPos(self, pos):
        self.antPos = [*pos]

    def updateGraph(self, screen):
        pg.draw.rect(screen, "white", (780, 360, 400, 200))
        pg.draw.rect(screen, "black", (780, 459, 400, 2))
        pg.draw.rect(screen, "black", (780, 360, 400, 200), 1)
        if self.count > 0:
            pos_str = str(self.antPos[0]) + "\\" + str(self.antPos[1])
            if pos_str not in self.space or self.sensitivity >= self.space[pos_str][0]:
                self.signalMEM.append([(randint(-255, 255) * (1 / self.zoom) * (self.sensitivity), "red")])
            else:
                pre = [data[0].replace("COUNT", str(self.graphCount)) for data in MODULATIONS["AM"]]
                pre = [data[0].replace("ZOOM", str(self.zoom)) for data in MODULATIONS["AM"]]
                for x in range(16):
                    po = []
                    for pr in pre:
                        if x < len(pre):
                            po.append(pr.replace(f"x{x}", pre[x]))
                        else:
                            po.append(pr)
                    pre = po
                self.signalMEM.append(list(zip(list(map(eval, pre)), [data[1] for data in MODULATIONS["AM"]])))
            if len(self.signalMEM) > 100:
                self.signalMEM = self.signalMEM[len(self.signalMEM) - 100:]
            self.graphCount += 0.1
            self.count = 0
        for number, point in enumerate(self.signalMEM):
            try:
                pg.draw.aaline(screen, point[0][1], (782 + number * 4, 460 - round(point[0][0] * (96 / 255))),
                               (782 + (number + 1) * 4, 460 - round(self.signalMEM[number + 1][0][0] * (96 / 255))))
            except:
                pass
            for num, modulFunc in enumerate(point[1:]):
                try:
                    pg.draw.aaline(screen, modulFunc[1], (782 + number * 4, 460 - round(modulFunc[0] * (96 / 255))),
                                   (782 + (number + 1) * 4,
                                    460 - round(self.signalMEM[number + 1][num + 1][0] * (96 / 255))))
                except:
                    pass

        self.count += 1


def ret(newPage):
    global page, updateState
    page = newPage
    updateState = True


def loadSave(name):
    pass


def save():
    pass


def updateGame(scren):
    global updateState, page, space, SCREEN_SIZE, helps, widgets, fonts, text_thread, mousePos, load_thread, screen
    screen = scren
    if updateState:
        mousePos = [360, 180]
        widgets.clear()
        SCREEN_SIZE = [1200, 600]
        pg.font.init()
        font = pg.font.get_default_font()
        fonts = [pg.font.SysFont(font, a) for a in range(1, 41)]
        helps = [
            [fonts[24].render('RadioScannerV1.0 Satelite Edition', True, "BLACK"), [20, 10]],
            [fonts[24].render('Command output:', True, "BLACK"), [20, 410]],
            [fonts[24].render('Settings', True, "BLACK"), [SCREEN_SIZE[0] * 0.6 + 40, 10]],
            [fonts[30].render('X', True, "BLACK"), [SCREEN_SIZE[0] * 0.6 + 40, 69]],
            [fonts[30].render('Y', True, "BLACK"), [SCREEN_SIZE[0] * 0.6 + 40, 158]],
            [fonts[30].render(',', True, "BLACK"), [SCREEN_SIZE[0] * 0.6 + 180, 69]],
            [fonts[30].render(',', True, "BLACK"), [SCREEN_SIZE[0] * 0.6 + 180, 158]],
            [fonts[30].render('Zoom', True, "BLACK"), [SCREEN_SIZE[0] * 0.6 + 40, 220]],
            [fonts[30].render('Sensitivity', True, "BLACK"), [SCREEN_SIZE[0] * 0.6 + 40, 280]],
        ]
        updateState = False
        pg.display.set_mode(SCREEN_SIZE)
        space = Space()
        widgets = InGameSettings(screen)
        widgets[0].setOnClick(lambda: save())
        [widget.setOnClick(functools.partial(lambda x: updateNumber(1, x), number)) for number, widget in
         enumerate(widgets[1:7])]
        [widget.setOnClick(functools.partial(lambda x: updateNumber(1, x, True), number)) for number, widget in
         enumerate(widgets[7:13])]
        [widget.setOnClick(functools.partial(lambda x: updateNumber(2, x), number)) for number, widget in
         enumerate(widgets[13:19])]
        [widget.setOnClick(functools.partial(lambda x: updateNumber(2, x, True), number)) for number, widget in
         enumerate(widgets[19:25])]
        initial_text = (
            'You are the last person on a spaceship, so to ask for help, there’s no one to turn to but yourself.'
            '\nYou need to find EARTH on your own in a cold and not very friendly space…'
            '\nYou have woken up, because ai assistant has do that, before he turned off.'
            '\nHis final message flickers on the console: ‘Find Earth. Humanity depends on you.’'
            '\nThe ship is damaged, resources are dwindling, and the AI’s knowledge of the stars is incomplete. '
            'Good luck. You’ll need it.')
        text_thread = threading.Thread(target=animate_text, args=(initial_text, screen, fonts))
        text_thread.daemon = True  # Поток завершится вместе с основным потоком
        text_thread.start()
        load_thread = None
        widgets[25].setValue(2)
        if BACKGROUND_MUSIC:
            BACKGROUND_MUSIC.play(-1)
        if WHITE_NOISE:
            WHITE_NOISE.play(-1)

    updateScreen(screen)
    set_background_music_volume(0.05)
    pg.draw.rect(screen, "darkGrey", (0, 0, SCREEN_SIZE[0], 40))
    pg.draw.rect(screen, "darkGrey", (0, 0, 20, SCREEN_SIZE[0]))
    pg.draw.rect(screen, "darkGrey", (0, 400, SCREEN_SIZE[0], 40))
    pg.draw.rect(screen, "darkGrey", (0, SCREEN_SIZE[1] - 20, SCREEN_SIZE[0], SCREEN_SIZE[1]))
    pg.draw.rect(screen, "darkGrey", (SCREEN_SIZE[0] * 0.6 + 20, 0, SCREEN_SIZE[0], SCREEN_SIZE[1]))
    [screen.blit(*data) for data in
     [[fonts[35].render(text, True, "BLACK"), [SCREEN_SIZE[0] * 0.6 + 69 + num * 32, 67]] for num, text in
      enumerate(list(str(space.antPos[0]).rjust(6, "0")))]]
    [screen.blit(*data) for data in
     [[fonts[35].render(text, True, "BLACK"), [SCREEN_SIZE[0] * 0.6 + 69 + num * 32, 157]] for num, text in
      enumerate(list(str(space.antPos[1]).rjust(6, "0")))]]
    [screen.blit(*help) for help in helps]
    space.zoom = widgets[25].getValue() + 5
    if space.zoom != 1:
        screen.blit(fonts[30].render("x" + str(space.zoom - 6), True, "BLACK"), [840, 220])
    space.sensitivity = round(1 - widgets[26].getValue() / 1000, 4)
    if WHITE_NOISE:
        WHITE_NOISE.set_volume(space.sensitivity / 2)
    screen.blit(fonts[30].render("x" + str(space.sensitivity).ljust(5, "0"), True, "BLACK"), [890, 280])

    pg.draw.rect(screen, "grey", (20, 40, 720, 360), 5, 1)
    pg.draw.circle(screen, "grey", (380, 220), 10, 1)
    pg.draw.circle(screen, "green", (mousePos[0] + 20, mousePos[1] + 40), 6, 1)
    all_widgets = list(widgets)
    list(map(lambda x: x.draw(), all_widgets))
    draw_console(screen, fonts)
    space.updateGraph(screen)


def eventCheck(events):
    global running, mousePos, screen, fonts, load_thread, space, text_thread
    for event in events:
        if event.type == pg.QUIT:
            save()
            pg.quit()
            exit()
        if not page.isdigit():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    print(f"Antenna position when pressing space: {space.antPos}")
                    if (not load_thread or not load_thread.is_alive()) and not text_thread.is_alive():
                        #space.antPos = space.SignalOfEarth
                        load_thread = threading.Thread(target=display_loading, args=(screen, fonts, space))
                        load_thread.daemon = True
                        load_thread.start()

            if event.type == pg.MOUSEMOTION:
                if 20 < event.pos[0] < 740 and 40 < event.pos[1] < 400:
                    mousePos = [event.pos[0] - 20, event.pos[1] - 40]
                    pg.mouse.set_visible(False)
                else:
                    mousePos = [360, 180]
                    pg.mouse.set_visible(True)
            if event.type == pg.MOUSEWHEEL:
                if not pg.mouse.get_visible():
                    global widgets
                    new_zoom = space.zoom + event.y
                    if new_zoom > 38:
                        new_zoom = 38
                    elif new_zoom < 7:
                        new_zoom = 7
                    widgets[25].setValue(new_zoom - 5)
        pygame_widgets.update(events)


def menu(screen):
    global updateState, widgets, page, frame_index

    if updateState:
        updateState = False
        widgets.clear()

    global frame_index
    frame = frame_loader.get_frame(frame_index)
    if frame:
        screen.blit(frame, (0, 0))
    frame_index = (frame_index + 1) % len(frame_files)

    if page == "0":
        widgets = mainMenu(screen)
        [widgets[a].setOnClick(functools.partial(lambda x: ret(x), str(a + 1))) for a in range(0, 3)]
    elif page == "1":
        ret("GAME")
    elif page == "2":
        widgets = saves(screen)
        widgets[0].setOnClick(lambda: ret("0"))
        if len(widgets) > 1:
            [a.setOnClick(
                functools.partial(lambda x: loadSave(x.string), a)) if a.string != "Пустое сохранение" else None for
             a in widgets[1].buttons]
    elif page == "3":
        widgets = settings(screen)
        widgets[0].setOnClick(lambda: ret("0"))

    pygame_widgets.update(pg.event.get())

    list(map(lambda x: x.draw(), widgets))

    list(map(lambda x: x.draw(), widgets))

def MainGameUpdate(screen):
    global updateState, widgets, page,frame_loader
    page = "0"
    widgets = []
    updateState = True
    clock = pg.time.Clock()

        # Initialize FrameLoader here
    frame_loader = FrameLoader(frame_files, SCREEN_SIZE)

    while True:
        clock.tick(60)
        pg.display.set_caption("SpaceRoutine " + str(round(clock.get_fps(), 1)))
        if page.isdigit():
            menu(screen)
            frame_loader.update()
        else:
            updateGame(screen)
        eventCheck(pg.event.get())
        pg.display.flip()


if __name__ == "__main__":
    clock = pg.time.Clock()
    pg.init()
    MainGameUpdate(pg.display.set_mode(SCREEN_SIZE))
pg.init()