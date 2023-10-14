import pygame as pg
import random as rand
import os


class BlockOfField(pg.sprite.Sprite):

    def __init__(self, i, j, mine):
        self.position = [int(i), int(j)]
        self.status = 0
        self.is_mine = mine
        self.is_activated = False
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(os.path.join(sprites_folder, "block_of_field.jpg")).convert()
        self.image = pg.transform.scale(self.image, (mine_size, mine_size))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = i * mine_size + menu_width, j * mine_size + 2*menu_width + menu_height

    def update(self, button):

        timer.start_time()

        if button == "left":
            if self.is_activated is False:
                self.is_activated = True
                global not_activated_block
                not_activated_block -= 1
                if self.is_mine is True:
                    self.image = pg.image.load(os.path.join(sprites_folder, "mine_field_activated.jpg")).convert()
                    self.image = pg.transform.scale(self.image, (mine_size, mine_size))
                    pg.time.set_timer(timer.TICK, 0)
                    global win, lose, running
                    open_field(False, self.position[0], self.position[1])
                    ResetButton.image = pg.image.load(os.path.join(sprites_folder, "reset_button_lose.jpg")).convert()
                    ResetButton.image = pg.transform.scale(ResetButton.image, (0.9*menu_height, 0.9*menu_height))
                    win, lose, running = False, True, False
                else:
                    file_name = "blank_field_" + str(field_nums[self.position[0]][self.position[1]]) + ".jpg"
                    self.image = pg.image.load(os.path.join(sprites_folder, file_name)).convert()
                    self.image = pg.transform.scale(self.image, (mine_size, mine_size))
                if field_nums[self.position[0]][self.position[1]] == 0:
                    self.update("left")

            else:
                count_of_flags = 0
                for i in range(self.position[0]-1, self.position[0]+2):
                    for j in range(self.position[1] - 1, self.position[1] + 2):
                        if (i >= 0) & (i < field_width) & (j >= 0) & (j < field_height):
                            if (field_data[i][j].is_activated is False) & (field_data[i][j].status == 1):
                                count_of_flags += 1
                if count_of_flags == field_nums[self.position[0]][self.position[1]]:
                    for i in range(self.position[0] - 1, self.position[0] + 2):
                        for j in range(self.position[1] - 1, self.position[1] + 2):
                            if (i >= 0) & (i < field_width) & (j >= 0) & (j < field_height):
                                if (field_data[i][j].is_activated is False) & (field_data[i][j].status != 1):
                                    field_data[i][j].update("left")
                else:
                    for i in range(self.position[0] - 1, self.position[0] + 2):
                        for j in range(self.position[1] - 1, self.position[1] + 2):
                            if (i >= 0) & (i < field_width) & (j >= 0) & (j < field_height) & ((i != self.position[0]) | (j != self.position[1])):
                                if field_data[i][j].is_activated is False:
                                    if field_data[i][j].status == 0:
                                        field_data[i][j].image = pg.image.load(
                                            os.path.join(sprites_folder, "block_of_field.jpg")).convert()
                                        field_data[i][j].image = pg.transform.scale(field_data[i][j].image, (mine_size, mine_size))
                                    elif field_data[i][j].status == 1:
                                        field_data[i][j].image = pg.image.load(os.path.join(sprites_folder, "flag.jpg")).convert()
                                        field_data[i][j].image = pg.transform.scale(field_data[i][j].image, (mine_size, mine_size))
                                    else:
                                        field_data[i][j].image = pg.image.load(
                                            os.path.join(sprites_folder, "question.jpg")).convert()
                                        field_data[i][j].image = pg.transform.scale(field_data[i][j].image, (mine_size, mine_size))


        if button == "right":
            if self.is_activated is False:
                self.status = (self.status + 1) % 3
                if self.status == 0:
                    self.image = pg.image.load(os.path.join(sprites_folder, "block_of_field.jpg")).convert()
                    self.image = pg.transform.scale(self.image, (mine_size, mine_size))
                elif self.status == 1:
                    bomb_counter.update(-1)
                    self.image = pg.image.load(os.path.join(sprites_folder, "flag.jpg")).convert()
                    self.image = pg.transform.scale(self.image, (mine_size, mine_size))
                else:
                    bomb_counter.update(1)
                    self.image = pg.image.load(os.path.join(sprites_folder, "question.jpg")).convert()
                    self.image = pg.transform.scale(self.image, (mine_size, mine_size))


class Counter(pg.sprite.Sprite):

    def __init__(self, pos, type):
        self.status = 0
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(os.path.join(sprites_folder, "counter_0.jpg")).convert()
        self.image = pg.transform.scale(self.image, (counter_width, counter_height))
        self.rect = self.image.get_rect()
        if type == 0:
            self.rect.center = (pos * counter_width + menu_width + 2 * counter_width, menu_width + menu_height//2)
        elif type == 1:
            self.rect.center = (screen_width - (pos * counter_width + menu_width + 2*counter_width), menu_width + menu_height//2)

    def tick(self):
        self.status = (self.status + 1) % 10
        s = "counter_" + str(self.status) + ".jpg"
        self.image = pg.image.load(os.path.join(sprites_folder, s)).convert()
        self.image = pg.transform.scale(self.image, (counter_width, counter_height))

    def update(self, num):
        self.status = num
        s = "counter_" + str(self.status) + ".jpg"
        self.image = pg.image.load(os.path.join(sprites_folder, s)).convert()
        self.image = pg.transform.scale(self.image, (counter_width, counter_height))


class Timer:

    def __init__(self, first):
        self.time_count = 0
        self.is_started = False
        self.TICK = first

    def start_time(self):
        if self.is_started is False:
            pg.time.set_timer(self.TICK, 1 * 1000)
            self.is_started = True


class BombCounter:

    def __init__(self, first, second, third, num_of_bombs):
        self.num = num_of_bombs
        self.BombCounter_1 = first
        self.BombCounter_10 = second
        self.BombCounter_100 = third

    def update(self, delta=0):
        self.num += delta
        if self.num >= 0:
            _ = self.num
            self.BombCounter_1.update(_ % 10)
            _ //= 10
            self.BombCounter_10.update(_ % 10)
            _ //= 10
            bomb_counter_100.update(_)


class SpriteFromFile(pg.sprite.Sprite):

    def __init__(self, file_name, size):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(os.path.join(sprites_folder, file_name)).convert()
        self.image = pg.transform.scale(self.image, size)
        self.rect = self.image.get_rect()


class BasicSprite(pg.sprite.Sprite):

    def __init__(self, color, size):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface(size)
        self.image.fill(color)
        self.rect = self.image.get_rect()


class ResetButton(pg.sprite.Sprite):

    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(os.path.join(sprites_folder, "reset_button_" + str(difficulty) + ".jpg")).convert()
        self.image = pg.transform.scale(self.image, (0.9*menu_height, 0.9*menu_height))
        self.rect = self.image.get_rect()
        self.rect.center = (screen_width/2, menu_width + menu_height/2)

    def next_difficulty(self):
        global difficulty
        difficulty = (difficulty + 1) % 3
        file_name = "reset_button_" + str(difficulty) + ".jpg"
        self.image = pg.image.load(os.path.join(sprites_folder, file_name)).convert()
        self.image = pg.transform.scale(self.image, (0.9*menu_height, 0.9*menu_height))


def search_sort(arr, indexes):
    for i in range(len(arr)):

        min_ = i

        for j in range(i, len(arr)):

            if arr[j] < arr[min_]:
                min_ = j

        buffer = arr[i]
        arr[i] = arr[min_]
        arr[min_] = buffer
        buffer = indexes[i]
        indexes[i] = indexes[min_]
        indexes[min_] = buffer


def print_wallpaper():
    #ортисовка фона
    #углы
    menu_sprite = SpriteFromFile("angle_2.jpg", (menu_width, menu_width))
    menu_sprite.rect.bottomleft = (0, screen_height)
    all_sprites.add(menu_sprite)
    menu_sprite = SpriteFromFile("angle_1.jpg", (menu_width, menu_width))
    menu_sprite.rect.topright = (screen_width, 0)
    all_sprites.add(menu_sprite)
    #горизонтальные
    menu_sprite = BasicSprite("gray", (screen_width - 2*menu_width/4, 2*menu_width/4))
    menu_sprite.rect.x, menu_sprite.rect.y = menu_width/4, menu_width/4
    all_sprites.add(menu_sprite)
    menu_sprite = BasicSprite((207, 207, 207), (screen_width - menu_width/4, menu_width/4))
    menu_sprite.rect.x, menu_sprite.rect.y = 0, 0
    all_sprites.add(menu_sprite)
    menu_sprite = BasicSprite((99, 99, 99), (screen_width - 7*menu_width/4, menu_width/4))
    menu_sprite.rect.x, menu_sprite.rect.y = 3*menu_width/4, 3*menu_width/4
    all_sprites.add(menu_sprite)
    menu_sprite = BasicSprite("gray", (screen_width - 2*menu_width/4, 2*menu_width/4))
    menu_sprite.rect.bottomleft = (menu_width/4, screen_height - menu_width/4)
    all_sprites.add(menu_sprite)
    menu_sprite = BasicSprite((99, 99, 99), (screen_width - menu_width, menu_width/4))
    menu_sprite.rect.bottomleft = (menu_width, screen_height)
    all_sprites.add(menu_sprite)
    menu_sprite = BasicSprite((207, 207, 207), (screen_width - 7*menu_width/4, menu_width/4))
    menu_sprite.rect.bottomleft = (menu_width, screen_height - 3*menu_width/4)
    all_sprites.add(menu_sprite)
    #вертикальные
    menu_sprite = BasicSprite("gray", (2*menu_width/4, screen_height - 2*menu_width/4))
    menu_sprite.rect.x, menu_sprite.rect.y = menu_width/4, menu_width/4
    all_sprites.add(menu_sprite)
    menu_sprite = BasicSprite((207, 207, 207), (menu_width/4, screen_height - menu_width))
    menu_sprite.rect.x, menu_sprite.rect.y = 0, 0
    all_sprites.add(menu_sprite)
    menu_sprite = BasicSprite((99, 99, 99), (menu_width/4, screen_height - 7*menu_width/4))
    menu_sprite.rect.x, menu_sprite.rect.y = 3*menu_width/4, 3*menu_width/4
    all_sprites.add(menu_sprite)
    menu_sprite = BasicSprite("gray", (2*menu_width/4, screen_height - 2*menu_width/4))
    menu_sprite.rect.bottomright = (screen_width - menu_width/4, screen_height - menu_width/4)
    all_sprites.add(menu_sprite)
    menu_sprite = BasicSprite((99, 99, 99), (menu_width/4, screen_height - menu_width/4))
    menu_sprite.rect.bottomright = (screen_width, screen_height)
    all_sprites.add(menu_sprite)
    menu_sprite = BasicSprite((207, 207, 207), (menu_width/4, screen_height - 2*menu_width))
    menu_sprite.rect.bottomright = (screen_width - 3*menu_width/4, screen_height - menu_width)
    all_sprites.add(menu_sprite)
    #центральнай гранца
    #углы
    menu_sprite = SpriteFromFile("board_inside.jpg", (menu_width/4, menu_width/4))
    menu_sprite.rect.x, menu_sprite.rect.y = 3*menu_width/4, menu_height + menu_width
    all_sprites.add(menu_sprite)
    menu_sprite = SpriteFromFile("board_inside.jpg", (menu_width/4, menu_width/4))
    menu_sprite.rect.bottomright = (screen_width - 3 * menu_width/4, menu_height + 2*menu_width)
    all_sprites.add(menu_sprite)
    #полосы
    menu_sprite = BasicSprite("gray", (screen_width - 2*menu_width/4, 2 * menu_width / 4))
    menu_sprite.rect.x, menu_sprite.rect.y = (menu_width/4, menu_height + 5 * menu_width / 4)
    all_sprites.add(menu_sprite)
    menu_sprite = BasicSprite((99, 99, 99), (screen_width - 2*menu_width, menu_width/4))
    menu_sprite.rect.topright = (screen_width - menu_width, menu_height + 7 * menu_width / 4)
    all_sprites.add(menu_sprite)
    menu_sprite = BasicSprite((207, 207, 207), (screen_width - 2*menu_width, menu_width/4))
    menu_sprite.rect.bottomright = (screen_width - menu_width, menu_height + 5 * menu_width / 4)
    all_sprites.add(menu_sprite)


def open_field(is_win, i_=0, j_=0):
    for j in range(field_height):
        for i in range(field_width):
            if field_data[i][j].is_mine is True:
                if (is_win is False) & ((i != i_) | (j != j_)):
                    field_data[i][j].image = pg.image.load(os.path.join(sprites_folder, "mine_field.jpg")).convert()
                    field_data[i][j].image = pg.transform.scale(field_data[i][j].image,(mine_size, mine_size))
                elif is_win is True:
                    field_data[i][j].image = pg.image.load(os.path.join(sprites_folder, "mine_field_deffused.jpg")).convert()
                    field_data[i][j].image = pg.transform.scale(field_data[i][j].image, (mine_size, mine_size))
            else:
                file_name = "blank_field_" + str(field_nums[field_data[i][j].position[0]][field_data[i][j].position[1]]) + ".jpg"
                field_data[i][j].image = pg.image.load(os.path.join(sprites_folder, file_name)).convert()
                field_data[i][j].image = pg.transform.scale(field_data[i][j].image, (mine_size, mine_size))


def logs_file_to_list():
    file = open(os.path.join(records_folder, "logs.txt"), 'r')
    string_list = []
    file.readline()
    for line in file:
        string_list.append(line)
    return string_list


def write_logs():
    if difficulty == 0:
        string_list = logs_file_to_list()
        file = open(os.path.join(records_folder, "logs.txt"), 'w')
        for line in string_list:
            file.write(line)
        file.write("easy - " + str(timer.time_count) + " seconds\n")
        file.close()

    elif difficulty == 1:
        string_list = logs_file_to_list()
        file = open(os.path.join(records_folder, "logs.txt"), 'w')
        for line in string_list:
            file.write(line)
        file.write("normal - " + str(timer.time_count) + " seconds\n")
        file.close()

    elif difficulty == 2:
        string_list = logs_file_to_list()
        file = open(os.path.join(records_folder, "logs.txt"), 'w')
        for line in string_list:
            file.write(line)
        file.write("hard - " + str(timer.time_count) + " seconds\n")
        file.close()


def write_stats():
    list_stats = []
    file = open(os.path.join(records_folder, "stats.txt"), 'r')
    for _ in range(3):
        file.readline()
        s = file.readline().split()
        list_stats.append(int(s[0]))
    list_stats[difficulty] += 1
    file.close()
    file = open(os.path.join(records_folder, "stats.txt"), 'w')
    file.write("Easy\n")
    file.write(str(list_stats[0]) + "\n")
    file.write("Normal\n")
    file.write(str(list_stats[1]) + "\n")
    file.write("Hard\n")
    file.write(str(list_stats[2]) + "\n")


def write_time_and_field(file_name, field_size):
    file = open(os.path.join(records_folder, file_name), 'a')
    file.write(str(timer.time_count) + '\n')
    for i in range(field_height):
        for j in range(field_width):
            if field_data[j][i].is_mine is True:
                file.write("0")
            else:
                file.write("+")
        file.write("\n")
    file.close()
    field_list = []
    time_list = []
    file = open(os.path.join(records_folder, file_name), 'r')
    for _ in range(11):
        time = file.readline()
        field_row = ""
        for pos in range(field_size):
            str_ = file.readline()
            field_row += str_
        time_list.append(int(time))
        field_list.append(field_row)
    file.close()
    search_sort(time_list, field_list)
    file = open(os.path.join(records_folder, file_name), 'w')
    for _ in range(10):
        file.write(str(time_list[_]))
        file.write("\n")
        file.write(field_list[_])
    file.close()


def write_data():
    write_logs()
    write_stats()
    if difficulty == 0:
        write_time_and_field("Easy_difficulty.txt", difficulty_list[0][1])
    elif difficulty == 1:
        write_time_and_field("Normal_difficulty.txt", difficulty_list[1][1])
    elif difficulty == 2:
        write_time_and_field("Hard_difficulty.txt", difficulty_list[2][1])


def generate_mines(i_pos=-1, j_pos=-1):
    counter = num_of_mines
    while True:
        if counter <= 0:
            break
        i = rand.randint(0, field_width - 1)
        j = rand.randint(0, field_height - 1)
        if (i != i_pos) | (j != j_pos):
            if field_data[i][j].is_mine is False:
                field_data[i][j].is_mine = True
                counter -= 1
                for i_ in range(i - 1, i + 2):
                    for j_ in range(j - 1, j + 2):
                        if (i_ >= 0) & (i_ < field_width) & (j_ >= 0) & (j_ < field_height):
                            field_nums[i_][j_] += 1



#окно
pg.init()
pg.display.set_caption("Minesweeper")

#директории
game_folder = os.path.dirname(__file__)
sprites_folder = os.path.join(game_folder, "sprites")
records_folder = os.path.join(game_folder, "records")

difficulty = 0
difficulty_list = [[9, 9, 10],
                   [16, 16, 40],
                   [30, 16, 99]]

while True:

    #параметры экрана/настройки игры
    not_activated_block = int(difficulty_list[difficulty][0]) * int(difficulty_list[difficulty][1])
    num_of_mines = int(difficulty_list[difficulty][2])
    menu_width, menu_height = 4 * 6, 100
    counter_width, counter_height = 40, 80
    field_width, field_height = int(difficulty_list[difficulty][0]), int(difficulty_list[difficulty][1])
    mine_size = min(1400 // field_width, 600 // field_height)
    screen_width, screen_height = mine_size * field_width + 2 * menu_width, mine_size * field_height + 3 * menu_width + menu_height
    screen = pg.display.set_mode((screen_width, screen_height))

    #группа всех спрайтов
    all_sprites = pg.sprite.Group()

    print_wallpaper()

    #данные об игровом поле
    field_data = [] #спрайты
    field_nums = [] #числа

    reset_button = ResetButton()
    all_sprites.add(reset_button)

    #отрисовка поля
    for i in range(field_width):
        field_line = []
        sub_data = []
        for j in range(field_height):
            spr = BlockOfField(i, j, False)
            all_sprites.add(spr)
            field_line.append(spr)
            sub_data.append(int(0))
        field_data.append(field_line)
        field_nums.append(sub_data)

    #таймер
    TICK = pg.USEREVENT + 1
    timer_1 = Counter(2, 0)
    timer_10 = Counter(1, 0)
    timer_100 = Counter(0, 0)
    timer = Timer(TICK)
    all_sprites.add(timer_1)
    all_sprites.add(timer_10)
    all_sprites.add(timer_100)

    #счётчик бомб
    bomb_counter_1 = Counter(0, 1)
    bomb_counter_10 = Counter(1, 1)
    bomb_counter_100 = Counter(2, 1)
    all_sprites.add(bomb_counter_1)
    all_sprites.add(bomb_counter_10)
    all_sprites.add(bomb_counter_100)
    bomb_counter = BombCounter(bomb_counter_1, bomb_counter_10, bomb_counter_100, num_of_mines)
    bomb_counter.update()

    running, win, lose, is_mine_generate = True, False, False, False
    fps = 60

    clock = pg.time.Clock()

    #сновной цикл
    while running:

        clock.tick(fps)

        if not_activated_block == num_of_mines:
            open_field(True)
            pg.time.set_timer(timer.TICK, 0)
            bomb_counter.num = 0
            bomb_counter.update()
            write_data()
            running, win, lose = False, True, False

        for event in pg.event.get():

            if event.type == pg.MOUSEBUTTONDOWN:
                # определение ячейки
                x, y, i_pos, j_pos = int(menu_width), int(menu_height+2*menu_width), int(-1), int(-1)
                while x < int(event.pos[0]):
                    x += mine_size
                    i_pos += 1
                while y < int(event.pos[1]):
                    y += mine_size
                    j_pos += 1
                if (i_pos < 0) | (j_pos < 0):
                    i_pos, j_pos = field_width + 1, field_height + 1
                if (i_pos < field_width) & (j_pos < field_height):
                    if event.button == 3:
                        field_data[i_pos][j_pos].update("right")

                    if (event.button == 1) & (field_data[i_pos][j_pos].status == 0) & (field_data[i_pos][j_pos].is_activated is False):
                        field_data[i_pos][j_pos].image = pg.image.load(os.path.join(sprites_folder, "blank_field_0.jpg")).convert()
                        field_data[i_pos][j_pos].image = pg.transform.scale(field_data[i_pos][j_pos].image, (mine_size, mine_size))
                    elif (event.button == 1) & (field_data[i_pos][j_pos].is_activated is True):
                        for i in range(i_pos - 1, i_pos + 2):
                            for j in range(j_pos - 1, j_pos + 2):
                                if (i >= 0) & (i < field_width) & (j >= 0) & (j < field_height) & ((i != i_pos) | (j != j_pos)):
                                    if (field_data[i][j].is_activated is False) & (field_data[i][j].status != 1):
                                        field_data[i][j].image = pg.image.load(os.path.join(sprites_folder, "blank_field_0.jpg")).convert()
                                        field_data[i][j].image = pg.transform.scale(field_data[i][j].image,(mine_size, mine_size))
                elif (event.pos[0] >= screen_width / 2 - 0.45*menu_height) & (event.pos[0] < screen_width / 2 + 0.45*menu_height) & (event.pos[1] >= menu_width + menu_height / 2 - 0.45*menu_height) & (event.pos[1] < menu_width + menu_height / 2 + 0.45*menu_height):
                    reset_button.image = pg.image.load(os.path.join(sprites_folder, "pushed_reset_button_" + str(difficulty) + ".jpg")).convert()
                    reset_button.image = pg.transform.scale(reset_button.image,(0.9*menu_height, 0.9*menu_height))

            if event.type == pg.MOUSEBUTTONUP:
                if (i_pos < field_width) & (j_pos < field_height):
                    if (event.button == 1) & (field_data[i_pos][j_pos].status == 0):
                        if is_mine_generate is False:
                            generate_mines(i_pos, j_pos)
                            is_mine_generate = True
                        field_data[i_pos][j_pos].update("left")
                elif (event.pos[0] >= screen_width / 2 - 0.45 * menu_height) & (event.pos[0] < screen_width / 2 + 0.45 * menu_height) & (event.pos[1] >= menu_width + menu_height / 2 - 0.45 * menu_height) & (event.pos[1] < menu_width + menu_height / 2 + 0.45 * menu_height):
                    pg.time.set_timer(timer.TICK, 0)
                    if event.button == 3:
                        reset_button.next_difficulty()
                    running, win, lose = False, False, False

            if event.type == TICK:
                timer.time_count += 1
                if timer_1.status == 9:
                    if timer_10.status == 9:
                        timer_100.tick()
                    timer_10.tick()
                timer_1.tick()

            if event.type == pg.QUIT:
                pg.quit()

        screen.fill("gray")
        all_sprites.draw(screen)
        pg.display.flip()

    # победа
    while win:

        clock.tick(fps)

        for event in pg.event.get():

            if event.type == pg.MOUSEBUTTONDOWN:
                # определение ячейки
                x, y, i_pos, j_pos = int(menu_width), int(menu_height + 2*menu_width), int(-1), int(-1)
                while x < int(event.pos[0]):
                    x += mine_size
                    i_pos += 1
                while y < int(event.pos[1]):
                    y += mine_size
                    j_pos += 1
                if (i_pos < 0) | (j_pos < 0):
                    i_pos, j_pos = field_width + 1, field_height + 1
                if (i_pos >= field_width) | (j_pos >= field_height):

                    if (event.pos[0] >= screen_width / 2 - 0.45 * menu_height) & (event.pos[0] < screen_width / 2 + 0.45 * menu_height) & (event.pos[1] >= menu_width + menu_height / 2 - 0.45 * menu_height) & (event.pos[1] < menu_width + menu_height / 2 + 0.45 * menu_height):
                        reset_button.image = pg.image.load(os.path.join(sprites_folder, "pushed_reset_button_" + str(difficulty) + ".jpg")).convert()
                        reset_button.image = pg.transform.scale(reset_button.image,(0.9 * menu_height, 0.9 * menu_height))

            if event.type == pg.MOUSEBUTTONUP:
                if (i_pos >= field_width) | (j_pos >= field_height):
                    if (event.pos[0] >= screen_width / 2 - 0.45 * menu_height) & (event.pos[0] < screen_width / 2 + 0.45 * menu_height) & (event.pos[1] >= menu_width + menu_height / 2 - 0.45 * menu_height) & (event.pos[1] < menu_width + menu_height / 2 + 0.45 * menu_height):
                        pg.time.set_timer(timer.TICK, 0)
                        if event.button == 3:
                            reset_button.next_difficulty()
                        running, win, lose = False, False, False

            if event.type == pg.QUIT:
                pg.quit()

        screen.fill("gray")
        all_sprites.draw(screen)
        pg.display.flip()

    # поражение
    while lose:

        clock.tick(fps)

        for event in pg.event.get():

            if event.type == pg.MOUSEBUTTONDOWN:
                # определение ячейки
                x, y, i_pos, j_pos = int(menu_width), int(menu_height + 2*menu_width), int(-1), int(-1)
                while x < int(event.pos[0]):
                    x += mine_size
                    i_pos += 1
                while y < int(event.pos[1]):
                    y += mine_size
                    j_pos += 1
                if (i_pos < 0) | (j_pos < 0):
                    i_pos, j_pos = field_width + 1, field_height + 1
                if (i_pos >= field_width) | (j_pos >= field_height):

                       if (event.pos[0] >= screen_width / 2 - 0.45 * menu_height) & (event.pos[0] < screen_width / 2 + 0.45 * menu_height) & (event.pos[1] >= menu_width + menu_height / 2 - 0.45 * menu_height) & (event.pos[1] < menu_width + menu_height / 2 + 0.45 * menu_height):
                        reset_button.image = pg.image.load(os.path.join(sprites_folder, "pushed_reset_button_" + str(difficulty) + ".jpg")).convert()
                        reset_button.image = pg.transform.scale(reset_button.image, (0.9 * menu_height, 0.9 * menu_height))

            if event.type == pg.MOUSEBUTTONUP:
                if (i_pos >= field_width) | (j_pos >= field_height):
                    if (event.pos[0] >= screen_width / 2 - 0.45 * menu_height) & (event.pos[0] < screen_width / 2 + 0.45 * menu_height) & (event.pos[1] >= menu_width + menu_height / 2 - 0.45 * menu_height) & (event.pos[1] < menu_width + menu_height / 2 + 0.45 * menu_height):
                        pg.time.set_timer(timer.TICK, 0)
                        if event.button == 3:
                            reset_button.next_difficulty()
                        running, win, lose = False, False, False

            if event.type == pg.QUIT:
                pg.quit()

        screen.fill("gray")
        all_sprites.draw(screen)
        pg.display.flip()
