import pygame, sys, random, hashlib, assets.ranking, assets.user_password, assets.topic, assets.answer, os
from pygame.math import Vector2

def source_path(relative_path):
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS

    else:
        base_path = os.path.abspath(".")

    return os.path.join (base_path, relative_path)

cd = source_path('')
os.chdir(cd)

user_password = assets.user_password.user_password

def update_ranking(mode, player_name, score):
    player_lis = assets.ranking.player_dic[f'{mode}_player_lis']

    if player_name in player_lis:
        if assets.ranking.score_dic[f'{mode}_score_lis'][player_lis.index(player_name)] < score:
            assets.ranking.score_dic[f'{mode}_score_lis'][player_lis.index(player_name)] = score
    else:
        player_lis.append(player_name)
        assets.ranking.score_dic[f'{mode}_score_lis'].append(score)

    assets.ranking.player_dic[f'{mode}_player_lis'] = player_lis
    game_window.mode = mode
    game_window.sort_ranking()

    with open('assets/ranking.py', mode='w', encoding='utf-8') as f:
        f.write('player_dic = '+str(assets.ranking.player_dic)+'\nscore_dic = '+str(assets.ranking.score_dic))

def login_window_init(change=False):
    global Cursor_Text, display_time
    screen.blit(background, (0, 0))

    screen.blit(Login_Text, (Login_Text_x, Login_Text_y))
    screen.blit(Sign_Up_Text, (Sign_Up_Text_x, Sign_Up_Text_y))

    screen.blit(Name_Text, (pix/2-pix/13-Name_Text.get_width(), pix/2-pix*5/39))
    screen.blit(Word_Text, (pix/2-pix/13-Word_Text.get_width(), pix/2-pix*5/156))

    help_text_x = (pix-help_text.get_width())/2
    help_text_y = pix/2-pix*5/39-help_text.get_height()

    if display_time <= 20:
        prov_name_text = font.render('*'*len(username)+' ', True, (0, 0, 0)) if change else font.render(username+' ', True, (0, 0, 0))
        prov_word_text = font.render('*'*len(password)+' ', True, (0, 0, 0))
        if mode == 'name':
            cursor_text_x = Rect_x+prov_name_text.get_width()
            cursor_text_y = Name_Rect_y+(pix*5/78-user_name_text.get_height())/2
        elif mode == 'word':
            cursor_text_x = Rect_x+prov_word_text.get_width()
            cursor_text_y = Word_Rect_y+(pix*5/78-pass_word_text.get_height())/2
        else:
            cursor_text_x = display # 屏幕外
            cursor_text_y = display # 屏幕外

        screen.blit(Cursor_Text, (cursor_text_x, cursor_text_y))
    
    screen.blit(help_text, (help_text_x, help_text_y))
    
    if display_time <= 0:
        display_time = 30

    pygame.draw.rect(screen, (0, 0, 0), (Rect_x, Name_Rect_y, pix*23/76, pix*5/76), 2)
    pygame.draw.rect(screen, (0, 0, 0), (Rect_x, Word_Rect_y, pix*23/76, pix*5/76), 2)

    display_time -= 1

def login(change=False):
    global help_text, blit_help_time
    if username == '' or password == '':
        help_text = font.render('新密码或再次输入的密码为空！' if change else '用户名或密码为空！', True, (255, 0, 0))
        blit_help_time = 120

    elif change:
        if username != password:
            help_text = font.render('两次输入密码不同', True, (255, 0, 0))
            blit_help_time = 120
        elif len(password) <= 5:
            help_text = font.render('密码过短，安全性低！', True, (255, 0, 0))
            blit_help_time = 120

    else:
        if username not in user_password:
            help_text = font.render('用户名不存在或不正确！', True, (255, 0, 0))
            blit_help_time = 120
        elif hashlib.pbkdf2_hmac('sha512', str.encode(password), 
                                 hashlib.pbkdf2_hmac('sha512', str.encode(password), 
                                                     str.encode(password), 5), 20) != user_password[username]:
            help_text = font.render('密码不正确！', True, (255, 0, 0))
            blit_help_time = 120

def sign_up():
    global help_text, blit_help_time
    if username == '' or password == '':
        help_text = font.render('用户名或密码为空！', True, (255, 0, 0))
        blit_help_time = 120

    elif username in user_password or user_password in ['admin', 'Admin', 'ADMIN', 'root', 'Root', 'ROOT', 'Guest', 'guest', 'GUEST']:
        help_text = font.render('用户名已存在！', True, (255, 0, 0))
        blit_help_time = 120

    elif len(password) <= 5:
        help_text = font.render('密码过短，安全性低！', True, (255, 0, 0))
        blit_help_time = 120

def login_window(change=False, again=False):
    global Login_Text, Sign_Up_Text, Name_Text, Word_Text, Login_Text_x, Login_Text_y, Sign_Up_Text_x, Sign_Up_Text_y, Rect_x
    global user_name_text, pass_word_text, help_text, blit_help_time, username, password, mode, display_time

    #全局变量
    help_text = font.render('', True, (255, 0, 0))
    blit_help_time = 120
    password = ''
    mode = 'name'
    display_time = 30
    
    #内部变量
    shut_down = False
    check = False

    if change:
        real_username = username
        username = ''

        Login_Text = font.render('确定', True, (0, 0, 0))
        Sign_Up_Text = font.render('取消', True, (0, 0, 0))

        Name_Text = font.render('新密码：', True, (0, 0, 0))
        Word_Text = font.render('再次输入密码：', True, (0, 0, 0))
        Login_Text_x = (pix-Login_Text.get_width())/2-pix/13

    else:
        username = ''

        Name_Text = font.render('用户名：', True, (0, 0, 0))
        Word_Text = font.render('密码：', True, (0, 0, 0))
        Login_Text_x = (pix-Login_Text.get_width())/2-pix/13

        if again:
            Login_Text = font.render('登录', True, (0, 0, 0))
            Sign_Up_Text = font.render('取消', True, (0, 0, 0))
            help_text = font.render('请重新登录以验证！', True, (255, 0, 0))
            blit_help_time = 120

        else:
            Login_Text = font.render('登录', True, (0, 0, 0))
            Sign_Up_Text = font.render('注册', True, (0, 0, 0))

    Login_Text_y = (pix-Login_Text.get_height())/2+pix/13
    Sign_Up_Text_x = (pix-Sign_Up_Text.get_width())/2+pix/13
    Sign_Up_Text_y = (pix-Sign_Up_Text.get_height())/2+pix/13
    Rect_x = pix/2-pix*19/76+Name_Text.get_width()
    
    #主循环
    bgm.play(-1)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if mode == 'down':
                if (event.type == pygame.MOUSEBUTTONDOWN) or check:
                    if (pygame.mouse.get_pos()[0] > Rect_x and pygame.mouse.get_pos()[0] < Rect_x+230
                        and pygame.mouse.get_pos()[1] > Name_Rect_y and pygame.mouse.get_pos()[1] < Name_Rect_y+50):
                        mode = 'name'
                    
                    elif (pygame.mouse.get_pos()[0] > Rect_x and pygame.mouse.get_pos()[0] < Rect_x+230
                        and pygame.mouse.get_pos()[1] > Word_Rect_y and pygame.mouse.get_pos()[1] < Word_Rect_y+50):
                        mode = 'word'
                    
                    elif (pygame.mouse.get_pos()[0] > Login_Text_x and pygame.mouse.get_pos()[0] < Login_Text_x+Login_Text.get_width()
                        and pygame.mouse.get_pos()[1] > Login_Text_y and pygame.mouse.get_pos()[1] < Login_Text_y+Login_Text.get_height()):
                        login(change) # change情况下代表确定
                        if blit_help_time != 120:
                            shut_down = True
                            break

                    elif (pygame.mouse.get_pos()[0] > Sign_Up_Text_x and pygame.mouse.get_pos()[0] < Sign_Up_Text_x+Sign_Up_Text.get_width()
                        and pygame.mouse.get_pos()[1] > Sign_Up_Text_y and pygame.mouse.get_pos()[1] < Sign_Up_Text_y+Sign_Up_Text.get_height()):
                        if change:
                            return
                        if again:
                            return 0
                        sign_up()
                        if blit_help_time != 120:
                            shut_down = True
                            break
                    check = False

            elif mode == 'name':
                if event.type == pygame.MOUSEBUTTONDOWN and not (pygame.mouse.get_pos()[0] > Rect_x
                                                                 and pygame.mouse.get_pos()[0] < Rect_x+230
                                                                 and pygame.mouse.get_pos()[1] > Name_Rect_y
                                                                 and pygame.mouse.get_pos()[1] < Name_Rect_y+50):
                    check = True
                    mode = 'down'

                else:
                    if event.type == pygame.KEYDOWN: # 上限10
                        if event.key == pygame.K_RETURN:
                            if password:
                                login(change)
                                if blit_help_time != 120:
                                    shut_down = True
                                    break
                                
                            else:
                                mode = 'word'
                                
                        elif event.key == pygame.K_BACKSPACE:
                            username = username[:-1]
                            if change:
                                user_name_text = font.render('*'*len(username), True, (0, 0, 0))
                            else:
                                user_name_text = font.render(username, True, (0, 0, 0))

                        elif len(username) >= 10:
                            if change:
                                if len(username) >= 16:
                                    help_text = font.render('密码长度超出范围！', True, (255, 0, 0))
                                    blit_help_time = 120
                                else:
                                    username += event.unicode
                                    user_name_text = font.render('*'*len(username), True, (0, 0, 0))

                            else:
                                help_text = font.render('用户名长度超出范围！', True, (255, 0, 0))
                                blit_help_time = 120

                        else:
                            username += event.unicode
                            if change:
                                user_name_text = font.render('*'*len(username), True, (0, 0, 0))
                            else:
                                user_name_text = font.render(username, True, (0, 0, 0))

            elif mode == 'word':
                if event.type == pygame.MOUSEBUTTONDOWN and not (pygame.mouse.get_pos()[0] > Rect_x
                                                                 and pygame.mouse.get_pos()[0] < Rect_x+230
                                                                 and pygame.mouse.get_pos()[1] > Word_Rect_y
                                                                 and pygame.mouse.get_pos()[1] < Word_Rect_y+50):
                    check = True
                    mode = 'down'
                    
                else:
                    if event.type == pygame.KEYDOWN: # 上限16
                        if event.key == pygame.K_RETURN:
                            if username:
                                login(change)
                                if blit_help_time != 120:
                                    shut_down = True
                                    break
                                
                            else:
                                mode = 'name'

                        elif event.key == pygame.K_BACKSPACE:
                            if password == '':
                                mode = 'name'
                            password = password[:-1]
                            pass_word_text = font.render('*'*len(password), True, (0, 0, 0))

                        elif len(password) >= 16:
                            help_text = font.render('密码长度超出范围！', True, (255, 0, 0))
                            blit_help_time = 120

                        else:
                            password += event.unicode
                            pass_word_text = font.render('*'*len(password), True, (0, 0, 0))

        if not username:
            if change:
                user_name_text = font.render('新密码 password', True, (176, 176, 176))
            else:
                user_name_text = font.render('用户名 username', True, (176, 176, 176))

        if not password:
            if change:
                pass_word_text = font.render('新密码 password', True, (176, 176, 176))
            else:
                pass_word_text = font.render('密码 password', True, (176, 176, 176))

        if shut_down:
            break

        if blit_help_time <= 0:
            help_text = font.render('', True, (255, 0, 0))
        blit_help_time -= 1

        login_window_init(change)
        screen.blit(user_name_text, (Rect_x+pix/78, Name_Rect_y+(pix*5/78-user_name_text.get_height())/2))
        screen.blit(pass_word_text, (Rect_x+pix/78, Word_Rect_y+(pix*5/78-pass_word_text.get_height())/2))

        pygame.display.update()
        clock.tick(30)
    
    if change:
        username = real_username

    user_password[username] = hashlib.pbkdf2_hmac('sha512', str.encode(password), 
                                                  hashlib.pbkdf2_hmac('sha512', str.encode(password), 
                                                                      str.encode(password), 5), 20)
        
    with open('assets/user_password.py', mode='w', encoding='utf-8') as f:
        f.write('user_password = '+str(user_password))

class SNAKE:
    def __init__(self):
        self.reset()
        self.crunch_sound = pygame.mixer.Sound('assets/sound/贪知蛇吃食物.wav')
        
        self.head_image = pygame.transform.smoothscale(pygame.image.load('assets/image/头.png').convert_alpha(), (size, size))
        self.body_image = pygame.transform.smoothscale(pygame.image.load('assets/image/身体.png').convert_alpha(), (size, size))
        self.tail_image = pygame.transform.smoothscale(pygame.image.load('assets/image/尾巴.png').convert_alpha(), (size, size))
        self.convert_image = pygame.transform.smoothscale(pygame.image.load('assets/image/转接处.png').convert_alpha(), (size, size))
    
    def draw_snake(self):
        self.update_head()
        self.update_tail()
        
        for i, block in enumerate(self.body):
            self.x_pos = int(block.x * size)
            self.y_pos = int(block.y * size)
            self.block_rect = pygame.Rect(self.x_pos, self.y_pos, size, size)

            if i == 0:
                screen.blit(self.head, self.block_rect)

            elif i == len(self.body) - 1:
                screen.blit(self.tail, self.block_rect)

            else:
                last_block = self.body[i + 1] - block
                next_block = self.body[i - 1] - block
                if last_block.x == next_block.x:
                    screen.blit(pygame.transform.rotate(self.body_image, 90), self.block_rect)

                if last_block.y == next_block.y:
                    screen.blit(self.body_image, self.block_rect)

                else:
                    if last_block.x == next_block.y == -1 or last_block.y == next_block.x == -1:
                        screen.blit(pygame.transform.rotate(self.convert_image, -90), self.block_rect)

                    elif last_block.x == next_block.y == 1 or last_block.y == next_block.x == 1:
                        screen.blit(pygame.transform.rotate(self.convert_image, 90), self.block_rect)

                    elif last_block.x == -1 and next_block.y == 1 or last_block.y == 1 and next_block.x == -1:
                        screen.blit(self.convert_image, self.block_rect)

                    elif last_block.x == 1 and next_block.y == -1 or last_block.y == -1 and next_block.x == 1:
                        screen.blit(pygame.transform.rotate(self.convert_image, 180), self.block_rect)

    
    def update_head(self):
        self.head_location = self.body[1] - self.body[0]
        if self.head_location == Vector2(1, 0):
            self.head = pygame.transform.rotate(self.head_image, 90)

        elif self.head_location == Vector2(-1, 0):
            self.head = pygame.transform.rotate(self.head_image, -90)

        elif self.head_location == Vector2(0, 1):
            self.head = self.head_image
            
        elif self.head_location == Vector2(0, -1):
            self.head = pygame.transform.rotate(self.head_image, 180)
            
    def update_tail(self):
        self.tail_location = self.body[-2] - self.body[-1]
        if self.tail_location == Vector2(1, 0):
            self.tail = pygame.transform.rotate(self.tail_image, 90)

        elif self.tail_location == Vector2(-1, 0):
            self.tail = pygame.transform.rotate(self.tail_image, -90)

        elif self.tail_location == Vector2(0, 1):
            self.tail = self.tail_image

        elif self.tail_location == Vector2(0, -1):
            self.tail = pygame.transform.rotate(self.tail_image, -180)
            
    def move_snake(self):
        if self.new_block:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0]+self.direction)
            self.body = body_copy[:]
            self.new_block = False

        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0]+self.direction)
            self.body = body_copy[:]
        
    def add_block(self):
        self.new_block = True
        self.crunch_sound.play()

    def reset(self):
        self.body = [Vector2(number/2, number/2-1), 
                        Vector2(number/2, number/2), 
                        Vector2(number/2, number/2+1)]
        self.direction = Vector2(1, 0)
        self.new_block = False

class FRUIT:
    def __init__(self, snake_body, reset_fruit=False, teach=True, fruit_num=0):
        self.snake_body = snake_body
        self.reset_fruit = reset_fruit
        self.teach = teach
        self.reset_fruit_time = 0
        self.fruit_num = fruit_num
        self.reset_fruit_place()
    
    def draw_fruit(self):
        self.fruit_rect = pygame.Rect(int(self.pos.x), int(self.pos.y), size, size)
        screen.blit(apple, self.fruit_rect)
        if self.teach:
            self.draw_answer()
        
    def draw_answer(self):
        global answer_lis
        self.answer = str(answer_lis[self.fruit_num])
        self.answer_text = num_font.render(self.answer, True, (0, 0, 0))
        screen.blit(self.answer_text, (int(self.pos.x)+size/2-self.answer_text.get_width()/2, int(self.pos.y)))
        
    def reset_fruit_place(self):
        global fruit_place_lis
        while True:
            if self.teach:
                while True:
                    self.x = random.randint(1, number-2)
                    self.y = random.randint(1, number-2)
                    self.pos = Vector2(self.x * size, self.y * size)
                    if (self.pos not in fruit_place_lis) and (self.pos.y > pix/5 or self.pos.y < ((pix-font_size)/5+font_size/3*7)):
                        fruit_place_lis.append(self.pos)
                        break

            else:
                self.x = random.randint(0, number-1)
                self.y = random.randint(0, number-1)
                self.pos = Vector2(self.x * size, self.y * size)

            lis = []
            try:
                for block in game_window.main_game.snake.body:
                    for j in range(-1, 2):
                        for i in range(-1, 2):
                            lis.append([block[0] + j, block[1] + i])

                if Vector2(self.pos.x/size, self.pos.y/size) not in lis:
                    break
                else:
                    continue

            except NameError:
                for block in self.snake_body:
                    for j in range(-1, 2):
                        for i in range(-1, 2):
                            lis.append([block[0] + j, block[1] + i])

                if Vector2(self.pos.x/size, self.pos.y/size) not in lis:
                    break
                else:
                    continue

        if self.reset_fruit:
            self.reset_fruit_time = 0

class MAIN:
    def __init__(self, mode='class', fast=False, reset_fruit=False, teach=True, only_add_sub=False
                 , only_mul_div=False, wiki=False, all_oper=False, divisor=10):
        global fruit_place_lis
        self.fast = fast
        self.reset_fruit = reset_fruit
        self.teach = teach
        self.only_add_sub = only_add_sub
        self.only_mul_div = only_mul_div
        self.wiki = wiki
        self.all_oper = all_oper
        self.divisor = divisor
        self.mode = mode

        self.choose_rgb = (22, 167, 43)
        self.snake = SNAKE()
        self.fruit = FRUIT(self.snake.body, reset_fruit=self.reset_fruit, teach=self.teach)

        if self.teach:
            self.fruit = FRUIT(self.snake.body, teach=True, fruit_num=0)
            self.second_fruit = FRUIT(self.snake.body, teach=True, fruit_num=1)
            self.third_fruit = FRUIT(self.snake.body, teach=True, fruit_num=2)
            fruit_place_lis = [self.fruit.pos, self.second_fruit.pos, self.third_fruit.pos]

        self.over_music = pygame.mixer.Sound('assets/sound/贪知蛇死亡.wav')
        self.play_bgm()

        self.move_snake = 1
        self.die = False
        self.two_lines = False
        self.num = 0
        self.score = 0

        if self.all_oper and self.wiki:
            if random.randint(0, 1):
                self.create_wiki_topic()
            else:
                self.create_topic()

        elif self.wiki:
            self.create_wiki_topic()

        elif teach:
            self.create_topic()
        
    def update(self):
        self.snake.move_snake()

        if self.fast:
            if self.move_snake == 2:
                self.snake.move_snake()
                self.move_snake = 1

        self.check_place()
        self.check_die()
        
    def draw_elements(self):
        screen.fill((167, 209, 61))
        self.draw_grass()
        self.snake.draw_snake()
        self.draw_score()
        self.fruit.draw_fruit()

        if self.teach:
            self.second_fruit.draw_fruit()
            self.third_fruit.draw_fruit()
            if not self.die:
                self.blit_topic()
                
        pygame.display.update()
        
    def check_place(self):
        global answer_lis
        if self.fruit.pos/size == self.snake.body[0]:
            self.fruit.reset_fruit_place()
            self.snake.add_block()
            if self.all_oper and self.wiki:
                if random.randint(0,  1):
                    self.reset_wrong_fruit()
                    self.create_topic()
                else:
                    self.reset_wrong_fruit()
                    self.create_wiki_topic()

            else:
                if self.teach:
                    self.reset_wrong_fruit()
                    self.create_topic()
                if self.wiki:
                    self.reset_wrong_fruit()
                    self.create_wiki_topic()

        if self.teach:
            if self.second_fruit.pos/size == self.snake.body[0]:
                self.game_over()
            elif self.third_fruit.pos/size == self.snake.body[0]:
                self.game_over()

    def check_die(self):
        if not 0 <= self.snake.body[0].x < number or not 0 <= self.snake.body[0].y < number:
            self.game_over()

        if self.snake.body[0] in self.snake.body[1:]:
            self.game_over()
            
    def game_over(self):
        global max_score
        self.die = True

        if self.score > max_score[self.mode]:
            max_score[self.mode] = self.score
            if max_score[self.mode] != 0:
                update_ranking(self.mode, username, max_score[self.mode])

        self.over_music.play()
        self.reset()

        if self.reset_fruit:
            self.fruit.reset_fruit_time = 0
        self.die = False
        
    def reset(self):
        global game_window
        bgm.stop()
        self.score_text = chinese_title_font.render(str(self.score)+' 分', True, (0, 0, 0))
        self.shut_down = False
        self.round = False
        self.choose_index = 0

        while True:
            self.click = False

            game_window.draw_init_window()
            self.choose_exit_text()
            self.blit_all_text()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if (pygame.mouse.get_pos()[0] > (pix-self.choose_text1.get_width())/2 and pygame.mouse.get_pos()[0] < pix/2+self.choose_text1.get_width()/2 and 
                        pygame.mouse.get_pos()[1] > (pix-self.choose_text1.get_height())/3+pix*2/13 and pygame.mouse.get_pos()[1] < pix/3+self.choose_text1.get_height()*2/3+pix*2/13):
                        self.choose_index = 0
                        self.click = True

                    if (pygame.mouse.get_pos()[0] > (pix-self.choose_text2.get_width())/2 and pygame.mouse.get_pos()[0] < pix/2+self.choose_text2.get_width()/2 and 
                        pygame.mouse.get_pos()[1] > (pix-self.choose_text2.get_height())/3+pix*3/13 and pygame.mouse.get_pos()[1] < pix/3+self.choose_text2.get_height()*2/3+pix*3/13):
                        self.choose_index = 1
                        self.click = True

                if event.type == pygame.KEYDOWN or self.click:
                    if self.click or (event.key == pygame.K_SPACE or event.key == pygame.K_RETURN):
                        self.click = False

                        if self.choose_index == 0:
                            self.draw_elements()
                            bgm.play(-1)
                            self.snake.reset()
                            self.shut_down = True
                            break

                        else:
                            bgm.play(-1)
                            game_window.draw_start_window()
                            self.shut_down = True

                    elif event.key == pygame.K_w or event.key == pygame.K_UP:
                        if self.choose_index == 0:
                            self.choose_index = 1
                        else:
                            self.choose_index -= 1

                    elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                        if self.choose_index == 1:
                            self.choose_index = 0
                        else:
                            self.choose_index += 1

            if self.shut_down:
                break

            pygame.display.update()
                
    def blit_all_text(self):
        screen.blit(self.score_text, ((pix-self.score_text.get_width())/2, 
                                      (pix-self.score_text.get_height())/3))
        screen.blit(self.choose_text1, ((pix-self.choose_text1.get_width())/2, 
                                        (pix-self.choose_text1.get_height())/3+pix*2/13))
        screen.blit(self.choose_text2, ((pix-self.choose_text2.get_width())/2, 
                                        (pix-self.choose_text2.get_height())/3+pix*3/13))
                
    def choose_exit_text(self):
        self.choose_text1 = chinese_font.render('再来一轮', True, self.choose_rgb if self.choose_index == 0 else (0, 0, 0))
        self.choose_text2 = chinese_font.render('返回菜单', True, self.choose_rgb if self.choose_index == 1 else (0, 0, 0))
            
    def reset_wrong_fruit(self):
        self.second_fruit.reset_fruit_place()
        self.third_fruit.reset_fruit_place()                

    def create_wiki_topic(self):
        global answer_lis
        self.wiki_num = random.randint(0, len(assets.topic.wiki_topic_lis))
        answer_lis = assets.answer.wiki_answer_lis[self.wiki_num*3-3:self.wiki_num*3]
        self.topic = assets.topic.wiki_topic_lis[self.wiki_num-1]
        self.two_lines = False

    def create_topic(self):
        self.two_lines = False
        while True:
            self.num1 = random.randint(-10, 10)/self.divisor
            if self.divisor == 1:
                self.num1 = random.randint(-10, 10)
            if self.num1 != 0:
                break

        while True:
            self.num2 = random.randint(-10, 10)/self.divisor
            if self.divisor == 1:
                self.num2 = random.randint(-10, 10)
            if self.num1 != self.num2 != 0:
                break
        
        if self.only_mul_div:
            self.create_mul_div_topic()
        elif self.only_add_sub:
            self.create_add_sub_topic()
        elif random.randint(0, 1):
            self.create_mul_div_topic()
        else:
            self.create_add_sub_topic()
            
    def create_mul_div_topic(self):
        global answer_lis
        if random.randint(0, 1):
            self.topic_num1 = random.randint(-100, 100)/self.divisor
            self.topic_num2 = random.randint(-100, 100)/self.divisor

            if self.divisor == 1:
                self.topic_num1 = random.randint(-100, 100)
                self.topic_num2 = random.randint(-100, 100)
            if self.topic_num2 < 0:
                self.topic = f'{self.topic_num1}*({self.topic_num2})'
            else:
                self.topic = f'{self.topic_num1}*{self.topic_num2}'

            answer_lis = [round(self.topic_num1*self.topic_num2, 2), 
                        round((self.topic_num1+self.num1)*self.topic_num2, 2), 
                        round(self.topic_num1*(self.topic_num2+self.num2), 2)]
            
        else:
            self.topic_num1 = random.randint(-100, 100)/self.divisor

            if self.divisor == 1:
                self.topic_num1 = random.randint(-100, 100)

            while True:
                self.double = random.randint(-10, 10)/self.divisor
                self.topic_num2 = round(self.topic_num1*self.double, 2)
                if self.divisor == 1:
                    self.double = random.randint(-10, 10)
                    self.topic_num2 = self.topic_num1*self.double
                if self.topic_num2 != 0:
                    break

            if self.topic_num2 < 0:
                self.topic = f'{self.topic_num2}/({self.topic_num1})'
            else:
                self.topic = f'{self.topic_num2}/{self.topic_num1}'

            while True:
                self.num1 = random.randint(-5, 5)
                if self.num1 != 0:
                    break

            while True:
                self.num2 = random.randint(-5, 5)
                if self.num1 != self.num2 != 0:
                    break

            answer_lis = [round(self.topic_num2/self.topic_num1, 2), 
                          round((self.topic_num2*(self.double+self.num1))/self.topic_num2, 2), 
                          round((self.topic_num2*(self.double+self.num2))/self.topic_num2, 2)]
                
    def create_add_sub_topic(self):
        global answer_lis
        self.topic_num1 = random.randint(-1000, 1000)/self.divisor
        self.topic_num2 = random.randint(-1000, 1000)/self.divisor

        if self.divisor == 1:
            self.topic_num1 = random.randint(-1000, 1000)
            self.topic_num2 = random.randint(-1000, 1000)
        if random.randint(0, 1):
            if self.topic_num2 < 0:
                self.topic = f'{self.topic_num1}+({self.topic_num2})'
            else:
                self.topic = f'{self.topic_num1}+{self.topic_num2}'
            answer_lis = [round(self.topic_num1+self.topic_num2, 1), 
                          round(self.topic_num1+self.topic_num2+self.num1, 1), 
                          round(self.topic_num1+self.topic_num2+self.num2, 1)]
            
        else:
            if self.topic_num2 < 0:
                self.topic = f'{self.topic_num1}-({self.topic_num2})'
            else:
                self.topic = f'{self.topic_num1}-{self.topic_num2}'
            answer_lis = [round(self.topic_num1-self.topic_num2, 1), 
                          round(self.topic_num1-self.topic_num2+self.num1, 1), 
                          round(self.topic_num1-self.topic_num2+self.num2, 1)]
    
    def blit_topic(self):
        self.topic_text = chinese_font.render(self.topic, True, (0, 0, 0))
        if self.topic_text.get_width() >= size*(number-2):
            self.last_topic = self.topic[int(len(self.topic)/2+1):]
            self.topic = self.topic.split(self.last_topic)[0]
            self.topic_text = chinese_font.render(self.topic, True, (0, 0, 0))
            self.last_topic_text = chinese_font.render(self.last_topic, True, (0, 0, 0))
            self.two_lines = True

        if self.two_lines:
            screen.blit(self.last_topic_text, ((pix-self.last_topic_text.get_width())/2, 
                                          (pix-self.last_topic_text.get_height())/5+font_size/3*4))
            
        screen.blit(self.topic_text, ((pix-self.topic_text.get_width())/2, 
                                      (pix-self.topic_text.get_height())/5))
                
    def play_bgm(self):
        bgm.play(-1)

    def draw_score(self):
        self.score = len(self.snake.body)-3
        score_surface = english_font.render(str(self.score), True, (56, 74, 21))
        score_rect = score_surface.get_rect(center=(int(pix - 35), int(pix - 25)))
        apple_rect = apple.get_rect(midright=(score_rect.left, score_rect.centery))
        screen.blit(apple, apple_rect)
        screen.blit(score_surface, score_rect)
        
    def draw_grass(self):
        grass_color = (157, 199, 51)
        for row in range(number):
            if row % 2:
                for col in range(number):
                    if col % 2 != 0:
                        grass_rect = pygame.Rect(col*size, row*size, size, size)
                        pygame.draw.rect(screen, grass_color, grass_rect)

            else:
                for col in range(number):
                    if col % 2 == 0:
                        grass_rect = pygame.Rect(col*size, row*size, size, size)
                        pygame.draw.rect(screen, grass_color, grass_rect)

class GAME_WINDOW:
    def __init__(self):
        self.choose_rgb = (22, 167, 43)
        self.all_clear = True
        self.zero_clear()
        self.draw_start_window()

    def zero_clear(self):
        self.shut_down = False
        self.round = False
        self.click = False

        if self.all_clear:
            self.reset_fruit = False
            self.fast = False
            self.only_add_sub = False
            self.only_mul_div = False
            self.wiki = False
            self.all_oper = False
            self.divisor = 10
            self.mode = None

    def draw_init_window(self):
        screen.blit(background, (0, 0))
        self.all_clear = True
        self.zero_clear()
        self.title_text = chinese_title_font.render('贪知蛇', True, (0, 0, 0))
        self.help_text = chinese_help_font.render('通过W/A或上箭头/下箭头来选择  空格确定', True, (255, 0, 0))

    def draw_ranking_init(self):
        self.all_clear = False
        self.zero_clear()
        screen.fill((215,233,214))
        self.header_text = font.render('名次       玩家名称       分数 | 名次       玩家名称       分数', True, (0, 0, 0))
        self.ranking_title = chinese_font.render('贪知蛇排行榜', True, (0, 0, 0))
        screen.blit(self.ranking_title, ((pix-self.ranking_title.get_width())/2, 0))
        screen.blit(self.header_text, (pix/26, self.ranking_title.get_height()))
        
        index = 1
        self.num = int(((pix*49/52) - (self.ranking_title.get_height() + pix/26))/(pix/26))
        for i in range(1, self.num+1):
            self.ranking_text = font.render(f'  {index}.', True, (0, 0, 0))
            screen.blit(self.ranking_text, (pix/26, self.ranking_title.get_height()+i*(pix/26)))
            index += 1
            
        for i in range(1, self.num+1):
            self.ranking_text = font.render(f'  {index}.', True, (0, 0, 0))
            screen.blit(self.ranking_text, (pix*7/13, 
                                            self.ranking_title.get_height()+i*(pix/26)))
            index += 1

    def blit_all_text(self):
        self.choose_text_lis = []

        title_x = (pix-self.title_text.get_width())/2
        help_x = (pix-self.help_text.get_width())/2

        lines_space = font_size/8*7
        box_to_choose = lines_space*4
        Choose_To_Help = font_size + lines_space + font_size/2
        title_to_box = (pix-(box_to_choose + font_size*(self.choose_num+1) + \
                             lines_space*self.choose_num + Choose_To_Help + self.help_text.get_height()))/2
        Help_To_Box = title_to_box + self.help_text.get_height()
        help_to_choose = pix-Help_To_Box-self.help_text.get_height()
        all_height = box_to_choose - title_to_box + Choose_To_Help + font_size + (lines_space + font_size) * self.choose_num

        if all_height >= pix/8*7:
            difference = (all_height - pix/8*7)/(self.choose_num+1)
            lines_space -= difference
            Choose_To_Help -= difference
            Help_To_Box += difference

            box_to_choose = lines_space*4
            title_to_box = (pix-(box_to_choose + font_size*(self.choose_num+1) + \
                                lines_space*self.choose_num + Choose_To_Help + self.help_text.get_height()))/2
            help_to_choose = pix-Help_To_Box-self.help_text.get_height()
            
        screen.blit(self.title_text, (title_x, title_to_box))
        for i in range(1, self.choose_num+2):
            prev_mode_text = eval(f'self.mode_text{i}')
            place = eval(f'((pix-self.mode_text{i}.get_width())/2, title_to_box + self.title_text.get_height() + lines_space * {i} + font_size*({i-1}))')
            eval(f'screen.blit(self.mode_text{i}, {place})')
            self.choose_text_lis.append((place[0], place[1], place[0]+prev_mode_text.get_width(), place[1]+prev_mode_text.get_height()))
        screen.blit(self.help_text, (help_x, help_to_choose))

        pygame.display.update()

    def choose_text(self):
        self.choose_num = 6
        lis = ['数学运算', '百科知识', '综合知识', '轻松一刻', '排行榜', '个人中心', '退出游戏']
        for i in range(self.choose_num+1):
            exec(f'self.mode_text{i+1} = chinese_font.render("{lis[i]}", True, self.choose_rgb if self.choose_index == {i} else (0, 0, 0))')

    def choose_math_text(self):
        self.choose_num = 3
        lis = ['加减运算', '乘除运算', '加减乘除', '返回']
        for i in range(self.choose_num+1):
            exec(f'self.mode_text{i+1} = chinese_font.render("{lis[i]}", True, self.choose_rgb if self.choose_index == {i} else (0, 0, 0))')

    def choose_snake_text(self):
        self.choose_num = 3
        lis = ['经典模式', '加速模式', '限时挑战', '返回']
        for i in range(self.choose_num+1):
            exec(f'self.mode_text{i+1} = chinese_font.render("{lis[i]}", True, self.choose_rgb if self.choose_index == {i} else (0, 0, 0))')
            
    def choose_decimal_mode(self):
        self.choose_num = 2
        self.mode_text1 = chinese_font.render('整数模式', True, self.choose_rgb if self.choose_index == 0 else (0, 0, 0))
        self.mode_text2 = chinese_font.render('小数模式', True, self.choose_rgb if self.choose_index == 1 else (0, 0, 0))
        self.mode_text3 = chinese_font.render('返回', True, self.choose_rgb if self.choose_index == 2 else (0, 0, 0))

    def choose_up_down_page(self):
        self.choose_num = 2
        self.choose_text1 = font.render('返回', True, self.choose_rgb if self.choose_index == 0 else (0, 0, 0))
        self.choose_text2 = font.render('下一模式', True, self.choose_rgb if self.choose_index == 1 else (0, 0, 0))
        self.choose_text3 = font.render('上一模式', True, self.choose_rgb if self.choose_index == 2 else (0, 0, 0))

    def choose_personal_text(self):
        self.choose_num = 3
        lis = ['个人排行', '更改密码', '切换用户', '返回']
        for i in range(self.choose_num+1):
            exec(f'self.mode_text{i+1} = chinese_font.render("{lis[i]}", True, self.choose_rgb if self.choose_index == {i} else (0, 0, 0))')

    def choose_cancel(self):
        self.choose_num = 0
        self.choose_text1 = font.render('返回', True, self.choose_rgb if self.choose_index == 0 else (0, 0, 0))

    def traverse_choose_index(self):
        if self.event.key == pygame.K_w or self.event.key == pygame.K_UP or self.event.key == pygame.K_a or self.event.key == pygame.K_LEFT:
            if self.choose_index == 0:
                self.choose_index = self.choose_num
            else:
                self.choose_index -= 1

        elif self.event.key == pygame.K_s or self.event.key == pygame.K_DOWN or self.event.key == pygame.K_d or self.event.key == pygame.K_RIGHT:
            if self.choose_index == self.choose_num:
                self.choose_index = 0
            else:
                self.choose_index += 1

    def traverse_choose(self):
        for self.event in pygame.event.get():
            if self.event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            self.traverse_mouse_choose()

            if self.event.type == pygame.KEYDOWN or self.click:
                if self.click or (self.event.key == pygame.K_SPACE or self.event.key == pygame.K_RETURN):
                    self.click = False
                    self.shut_down = True
                    break

                self.traverse_choose_index()

    def traverse_mouse_choose(self):
        if self.event.type == pygame.MOUSEBUTTONDOWN:
            for choose in self.choose_text_lis:
                if (pygame.mouse.get_pos()[0] > choose[0] and pygame.mouse.get_pos()[0] < choose[2]
                    and pygame.mouse.get_pos()[1] > choose[1] and pygame.mouse.get_pos()[1] < choose[3]):
                    self.choose_index = self.choose_text_lis.index(choose)
                    self.click = True
    
    def draw_start_window(self):
        global max_score
        
        self.choose_index = 0
        self.choose_text_lis = []

        while True: # 主循环
            self.draw_init_window()
            self.choose_text()
            self.blit_all_text()
            for self.event in pygame.event.get(): # 检查输入循环
                self.click = False

                if self.event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                self.traverse_mouse_choose()

                if self.event.type == pygame.KEYDOWN or self.click:
                    if self.click == False:
                        self.traverse_choose_index()

                    if (self.click and self.event.type == pygame.MOUSEBUTTONDOWN) or (self.event.key == pygame.K_SPACE or self.event.key == pygame.K_RETURN):
                        self.click = False
                        
                        if self.choose_index == 0: # math
                            self.choose_index = 0

                            while True: # math模式下的主循环
                                self.draw_init_window()
                                self.choose_math_text()
                                self.blit_all_text()
                                self.traverse_choose()
                                if self.shut_down:
                                    break

                            if self.choose_index == 0: # +-
                                self.choose_index = 0

                                while True: # +-模式下的主循环
                                    self.draw_init_window()
                                    self.choose_decimal_mode()
                                    self.blit_all_text()
                                    self.traverse_choose()
                                    if self.shut_down:
                                        break

                                self.shut_down = False
                                self.round = False

                                if self.choose_index == 0:
                                    self.teach = True
                                    self.divisor = 1
                                    self.only_add_sub = True
                                    self.mode = 'only_add_sub_integer'
                                    self.shut_down = True
                                    break

                                elif self.choose_index == 1:
                                    self.teach = True
                                    self.divisor = 10
                                    self.only_add_sub = True
                                    self.mode = 'only_add_sub_decimal'
                                    self.shut_down = True
                                    break

                                elif self.choose_index == 2:
                                    self.draw_init_window()
                                    self.choose_index = 0 # 重置为主菜单选项
                                    break

                            elif self.choose_index == 1: # */
                                self.choose_index = 0

                                while True:
                                    self.draw_init_window()
                                    self.choose_decimal_mode()
                                    self.blit_all_text()
                                    self.traverse_choose()
                                    if self.shut_down:
                                        break

                                self.shut_down = False
                                self.round = False
                                
                                if self.choose_index == 0:
                                    self.teach = True
                                    self.divisor = 1
                                    self.only_mul_div = True
                                    self.mode = 'only_mul_div_integer'
                                    self.shut_down = True
                                    break

                                elif self.choose_index == 1:
                                    self.teach = True
                                    self.divisor = 10
                                    self.only_mul_div = True
                                    self.mode = 'only_mul_div_decimal'
                                    self.shut_down = True
                                    break

                                elif self.choose_index == 2:
                                    self.draw_init_window()
                                    self.choose_index = 1 # 重置为主菜单选项
                                    break

                            elif self.choose_index == 2: # +-*/
                                self.choose_index = 0

                                while True:
                                    self.draw_init_window()
                                    self.choose_decimal_mode()
                                    self.blit_all_text()
                                    self.traverse_choose()
                                    if self.shut_down:
                                        break

                                self.shut_down = False
                                self.round = False

                                if self.choose_index == 0:
                                    self.teach = True
                                    self.divisor = 1
                                    self.mode = 'all_oper_integer'
                                    self.shut_down = True
                                    break

                                elif self.choose_index == 1:
                                    self.teach = True
                                    self.divisor = 10
                                    self.mode = 'all_oper_decimal'
                                    self.shut_down = True
                                    break

                                elif self.choose_index == 2:
                                    self.draw_init_window()
                                    self.choose_index = 2 # 重置为主菜单选项
                                    break

                            else:
                                self.draw_init_window()
                                self.choose_index = 0
                                break
                        
                        elif self.choose_index == 1: # wiki
                            self.teach = True
                            self.wiki = True
                            self.mode = 'wiki'
                            self.shut_down = True
                            break
                        
                        elif self.choose_index == 2: # all
                            self.teach = True
                            self.wiki = True
                            self.all_oper = True
                            self.mode = 'comp'
                            self.shut_down = True
                            break
                        
                        elif self.choose_index == 3: # more games
                            self.choose_index = 0

                            while True:
                                self.draw_init_window()
                                self.choose_snake_text()
                                self.blit_all_text()
                                self.traverse_choose()
                                if self.shut_down:
                                    break

                            self.shut_down = False
                            self.round = False

                            if self.choose_index == 0:
                                self.teach = False
                                self.mode = 'class'
                                self.shut_down = True
                                break

                            elif self.choose_index == 1:
                                self.teach = False
                                self.fast = True
                                self.mode = 'fast'
                                self.shut_down = True
                                break

                            elif self.choose_index == 2:
                                self.teach = False
                                self.reset_fruit = True
                                self.mode = 'time_move'
                                self.shut_down = True
                                break

                            elif self.choose_index == 3:
                                self.draw_init_window()
                                self.choose_index = 3
                                break
                        
                        elif self.choose_index == 4: # ranking
                            mode = mode_lis[0]
                            self.choose_index = 1

                            while True:
                                while True:
                                    self.draw_ranking_init()
                                    self.mode_text = font.render(mode_text_lis[mode_lis.index(mode)], True, (0, 0, 0))
                                    screen.blit(self.mode_text, (pix/26, pix/26-self.mode_text.get_height()/2))
                                    self.choose_up_down_page()

                                    screen.blit(self.choose_text1, ((pix-self.choose_text1.get_width())/2, 
                                                                    pix*25/26-self.choose_text2.get_height()/2))
                                    screen.blit(self.choose_text2, (pix*25/26-self.choose_text2.get_width(), 
                                                                    pix*25/26-self.choose_text2.get_height()/2))
                                    screen.blit(self.choose_text3, (pix/26, pix*25/26-self.choose_text3.get_height()/2))
                                    
                                    self.choose_text_lis = (((pix-self.choose_text1.get_width())/2, pix*25/26-self.choose_text1.get_height()/2, pix/2+self.choose_text1.get_width()/2, pix*25/26+self.choose_text1.get_height()/2), 
                                                            (pix*25/26-self.choose_text2.get_width(), pix*25/26-self.choose_text2.get_height()/2, pix*25/26, pix*25/26+self.choose_text2.get_height()/2), 
                                                            (pix/26, pix*25/26-self.choose_text3.get_height()/2, pix/26+self.choose_text3.get_width(), pix*25/26+self.choose_text3.get_height()/2))
                                    
                                    self.traverse_choose()

                                    self.mode = mode
                                    self.sort_ranking()

                                    index = 0
                                    for name in assets.ranking.player_dic[f'{mode}_player_lis']:
                                        if name == username:
                                            self.name_text = font.render(name, True, (255, 0, 0))
                                        else:
                                            self.name_text = font.render(name, True, (0, 0, 0))
                                        x = pix*5/26+(pix/6.5-self.name_text.get_width())/2
                                        y = self.ranking_title.get_height()+(index+1)*(pix/26)
                                        if index > self.num-1:
                                            x = pix*9/13+(pix/6.5-self.name_text.get_width())/2
                                            y = self.ranking_title.get_height()+(index+1-self.num)*(pix/26)
                                        screen.blit(self.name_text, (x, y))
                                        index += 1
                                    
                                    index = 0
                                    for score in assets.ranking.score_dic[f'{mode}_score_lis']:
                                        if assets.ranking.player_dic[f'{mode}_player_lis'][index] == username:
                                            self.score_text = font.render(str(score), True, (255, 0, 0))
                                        else:
                                            self.score_text = font.render(str(score), True, (0, 0, 0))
                                        x = pix*5/13+(pix/12-self.score_text.get_width())/2
                                        y = self.ranking_title.get_height()+(index+1)*(pix/26)
                                        if index > self.num-1:
                                            x = pix*9/13+(pix/12-self.score_text.get_width())/2
                                            y = self.ranking_title.get_height()+(index+1-self.num)*(pix/26)
                                        screen.blit(self.score_text, (x, y))
                                        index += 1
                                    
                                    pygame.display.update()

                                    if self.shut_down:
                                        break
                                if self.choose_index == 0:
                                    self.choose_index = 4
                                    break

                                elif self.choose_index == 1:
                                    if mode == mode_lis[-1]:
                                        mode = mode_lis[0]
                                    else:
                                        mode = mode_lis[mode_lis.index(mode)+1]

                                elif self.choose_index == 2:
                                    if mode == mode_lis[0]:
                                        mode = mode_lis[-1]
                                    else:
                                        mode = mode_lis[mode_lis.index(mode)-1]

                                elif self.shut_down:
                                    break

                            self.shut_down = False

                        elif self.choose_index == 5: # personal
                            self.choose_index = 0
                            self.title_text = chinese_title_font.render(username, True, (0, 0, 0))

                            while True:
                                screen.blit(background, (0, 0))
                                self.choose_personal_text()
                                self.blit_all_text()
                                self.traverse_choose()

                                if self.shut_down:
                                    self.shut_down = False

                                    if self.choose_index == 0: # personal ranking
                                        self.ranking_title = chinese_title_font.render('贪知蛇个人排行榜', True, (0, 0, 0))
                                        
                                        while True:
                                            screen.fill((215,233,214))
                                            self.choose_cancel()

                                            for event in pygame.event.get():
                                                if event.type == pygame.QUIT:
                                                    pygame.quit()
                                                    sys.exit()
                                                if event.type == pygame.KEYDOWN:
                                                    if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                                                        self.shut_down = True
                                                        break
                                                if event.type == pygame.MOUSEBUTTONDOWN:
                                                    x = pix/78*76-self.choose_text1.get_width()*1.5
                                                    y = pix/78*76-self.choose_text1.get_height()*1.5
                                                    if (pygame.mouse.get_pos()[0] > x and pygame.mouse.get_pos()[0] < (x+self.choose_text1.get_width()*3)
                                                        and pygame.mouse.get_pos()[1] > y and pygame.mouse.get_pos()[1] < (x+self.choose_text1.get_height()*3)):
                                                        self.shut_down = True
                                                        break
                                            
                                            screen.blit(self.ranking_title, ((pix-self.ranking_title.get_width())/2, 0))
                                            screen.blit(self.choose_text1, (pix/78*76-self.choose_text1.get_width(), pix/78*76-self.choose_text1.get_height()))
                                            
                                            count = 0
                                            for mode in mode_text_lis:
                                                if username in assets.ranking.player_dic[f'{mode_lis[mode_text_lis.index(mode)]}_player_lis']:
                                                    count += 1
                                            
                                            first_line_y = self.ranking_title.get_height() + (pix-self.ranking_title.get_height())/(count*1.1+3)
                                            index = 0
                                            for mode in mode_text_lis:
                                                if username in assets.ranking.player_dic[f'{mode_lis[mode_text_lis.index(mode)]}_player_lis']:
                                                    mode_name = font.render(f'{mode}: ', True, (0, 0, 0))
                                                    rank = assets.ranking.player_dic[f'{mode_lis[mode_text_lis.index(mode)]}_player_lis'].index(username) + 1
                                                    rank_text = ' 第' + str(rank) + '名'
                                                    score = str(assets.ranking.score_dic[f'{mode_lis[mode_text_lis.index(mode)]}_score_lis'][assets.ranking.player_dic[f'{mode_lis[mode_text_lis.index(mode)]}_player_lis'].index(username)]) + rank_text
                                                    score_text = font.render(score, True, (255, 0, 0) if rank == 1 else (0, 0, 0))
                                                    screen.blit(mode_name, ((pix-mode_name.get_width()-score_text.get_width())/2, first_line_y*(1+0.1*index) + mode_name.get_height()*index))
                                                    screen.blit(score_text, ((pix+mode_name.get_width()-score_text.get_width())/2, first_line_y*(1+0.1*index) + mode_name.get_height()*index))
                                                    index += 1
                                            
                                            if self.shut_down:
                                                self.shut_down = False
                                                break
                                                
                                            pygame.display.update()
                                    elif self.choose_index == 1: # change password
                                        bgm.stop()
                                        again = login_window(again=True)
                                        if again != 0:
                                            bgm.stop()
                                            login_window(change=True)
                                    elif self.choose_index == 2: # change user
                                        bgm.stop()
                                        login_window()
                                        self.title_text = chinese_title_font.render(username, True, (0, 0, 0))
                                        max_score = dict(zip(mode_lis, [0 for i in range(len(mode_lis))]))
                                    else: # cancel
                                        self.choose_index = 5
                                        break
                        
                        else:
                            pygame.quit()
                            sys.exit()

            if self.round:
                continue

            elif self.shut_down:
                break

        bgm.stop()
        self.main_game = MAIN(fast=self.fast, reset_fruit=self.reset_fruit, 
                              teach=self.teach, only_add_sub=self.only_add_sub, 
                              only_mul_div=self.only_mul_div, wiki=self.wiki, 
                              all_oper=self.all_oper, divisor=self.divisor, mode=self.mode)
        
    def sort_ranking(self):
        if assets.ranking.player_dic[f'{self.mode}_player_lis']:
            dic = dict(zip(assets.ranking.score_dic[f'{self.mode}_score_lis'], assets.ranking.player_dic[f'{self.mode}_player_lis']))
            assets.ranking.score_dic[f'{self.mode}_score_lis'].sort(reverse=True)

            for i in range(len(assets.ranking.score_dic[f'{self.mode}_score_lis'])):
                assets.ranking.player_dic[f'{self.mode}_player_lis'][i] = dic[assets.ranking.score_dic[f'{self.mode}_score_lis'][i]]



pygame.mixer.init()
pygame.init()

infoobject = pygame.display.Info()
display = min(infoobject.current_w, infoobject.current_h)
size = 30
number = int(round(display/4*3/size, 0))
if number % 2:
    number += 1
pix = size * number

screen = pygame.display.set_mode((pix, pix))
pygame.display.set_caption('贪知蛇—贪知无厌、智博行远')

clock = pygame.time.Clock()

apple = pygame.image.load('assets/image/apple20_20.png').convert_alpha()
apple = pygame.transform.smoothscale(apple, (size, size))
background = pygame.image.load('assets/image/background.jpg').convert_alpha()
background = pygame.transform.smoothscale(background, (pix, pix))
bgm = pygame.mixer.Sound('assets/sound/贪知蛇背景音乐.mp3')

font_size = int(round(pix / 19.5, 0))
english_font = pygame.font.Font('assets/font/Brush Script.ttf', font_size)
chinese_font = pygame.font.Font('assets/font/Chinese regular script.ttf', font_size)
chinese_title_font = pygame.font.Font('assets/font/Chinese regular script.ttf', font_size*2)
chinese_help_font = pygame.font.Font('assets/font/Regular Script.ttf', int(round(font_size/8*5, 0)))
num_font = pygame.font.Font('assets/font/Chinese regular script.ttf', size)
font = pygame.font.Font('assets/font/Chinese regular script.ttf', int(round(pix/26, 0)))

fruit_place_lis = [None]
answer_lis = []

mode_lis = ['only_add_sub_integer', 'only_mul_div_integer', 'all_oper_integer', 
            'only_add_sub_decimal', 'only_mul_div_decimal', 'all_oper_decimal', 
            'wiki', 'comp', 'class', 'fast', 'time_move']
mode_text_lis = ['加减运算-整数', '乘除运算-整数', '加减乘除-整数', 
                 '加减运算-小数', '乘除运算-小数', '加减乘除-小数', 
                 '百科知识', '综合知识', '经典模式', '加速模式', '限时挑战']

max_score = dict(zip(mode_lis, [0 for i in range(len(mode_lis))]))

Login_Text = font.render('登录', True, (0, 0, 0))
Sign_Up_Text = font.render('注册', True, (0, 0, 0))

Name_Text = font.render('用户名：', True, (0, 0, 0))
Word_Text = font.render('密码：', True, (0, 0, 0))
Cursor_Text = font.render('|', True, (0, 0, 0))

Login_Text_x = (pix-Login_Text.get_width())/2-pix/13
Login_Text_y = (pix-Login_Text.get_height())/2+pix/13
Sign_Up_Text_x = (pix-Sign_Up_Text.get_width())/2+pix/13
Sign_Up_Text_y = (pix-Sign_Up_Text.get_height())/2+pix/13

Rect_x = pix/2-pix*19/76+Name_Text.get_width()
Name_Rect_y = pix/2-pix/7.6
Word_Rect_y = pix/2-pix/30.4

login_window()

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)

game_window = GAME_WINDOW()
game_window.main_game.fruit.reset_fruit_time = 0

update = False
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if not game_window.main_game.fast:
            if event.type == SCREEN_UPDATE:
                game_window.main_game.update()
                update = True

        if event.type == pygame.KEYDOWN:
            if update and (event.key == pygame.K_w or event.key == pygame.K_UP) and game_window.main_game.snake.direction.y != 1:
                game_window.main_game.snake.direction = Vector2(0, -1)
                update = False
            elif update and (event.key == pygame.K_s or event.key == pygame.K_DOWN) and game_window.main_game.snake.direction.y != -1:
                game_window.main_game.snake.direction = Vector2(0, 1)
                update = False
            elif update and (event.key == pygame.K_a or event.key == pygame.K_LEFT) and game_window.main_game.snake.direction.x != 1:
                game_window.main_game.snake.direction = Vector2(-1, 0)
                update = False
            elif update and (event.key == pygame.K_d or event.key == pygame.K_RIGHT) and game_window.main_game.snake.direction.x != -1:
                game_window.main_game.snake.direction = Vector2(1, 0)
                update = False
            elif event.key == pygame.K_r:
                game_window.main_game.snake.reset()

    game_window.main_game.draw_elements()

    if game_window.main_game.fast:
        clock.tick(12)
        game_window.main_game.update()

    if not game_window.main_game.fast:
        clock.tick(60)

    if game_window.main_game.fruit.reset_fruit:
        if game_window.main_game.fruit.reset_fruit_time == 300:
            game_window.main_game.fruit.reset_fruit_place()
        game_window.main_game.fruit.reset_fruit_time += 1
