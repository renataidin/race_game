import pygame
import random
import mysql.connector

pygame.init()

FPS = 60
WIDTH = 800
HEIGHT = 450
SPEED = 10
ACCELERATION = 0.5  


RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
ORANGE = (255, 165, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

dbconfig = {'host': '127.0.0.1',
            'user': 'root',
            'password': '4152',
            'database': 'game_results'}


speed_x = 0
speed_y = 0

game_mode = "game"
start_btn = pygame.Rect(400, 300, 100, 50)
exit_btn = pygame.Rect(280, 240, 250, 80) 

window = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
run = True

distance = 0
frame_count = 0
damage = 0
repair_score = 0

car_set = ["lamborgini", "porsche", "ferrari"]
choosed_car = random.choice(car_set)
index_car = car_set.index(choosed_car)

ferrari = pygame.image.load("background.jpeg")
fon = pygame.image.load("background.jpeg")
asphalt = pygame.image.load("asphalt.jpg")
car = pygame.image.load(choosed_car + ".png")
block = pygame.image.load("image.png")
repairTools = pygame.image.load("repair_tools.png")
repairTools.set_colorkey(WHITE)
gameover_bg = pygame.image.load("game_over.png")
score_fon = pygame.image.load("score_fon.jpg")

car_rect = car.get_rect()
gamemode = "menu"
font_menu = pygame.font.SysFont("arial", 60, bold=True)
rect_start = pygame.Rect(280, 120, 250, 80)
rect_exit = pygame.Rect(280, 240, 250, 80)
rect_lamborgini = pygame.Rect(280, 110, 250, 80)
rect_porsche = pygame.Rect(280, 230, 250, 80)
rect_ferrari = pygame.Rect(280, 350, 250, 80)
font_style = pygame.font.SysFont("arial", 20)
start_btn = font_menu.render("START", True, BLACK)
exit_btn = font_menu.render("EXIT", True, BLACK)
ferrari_btn = font_menu.render("ferrari", True, BLACK)
lamborgini_btn = font_menu.render("lamborgini", True, BLACK)
porsche_btn = font_menu.render("porsche", True, BLACK)
block_rect = block.get_rect(top = random.choice([20, 120]))
repairTools_rect = repairTools.get_rect(top = random.choice([20, 120]))
font_status = pygame.font.SysFont("arial", 20, bold=True)

pygame.mixer.music.load('NFS2_Remix.ogg')
pygame.mixer.music.play()
pygame.mixer.music.set_volume(0.3)


kickSound = pygame.mixer.Sound('kick.mp3')
bonusSound = pygame.mixer.Sound('bonus1.wav')
healthRecharge = pygame.mixer.Sound('health-recharge.wav')

road = []
for i in range(10, WIDTH, 100):
    road.append([i, 220, 50, 10])

font =pygame.font.SysFont('Arial', 32)
input_box = pygame.Rect(330, 150, 140, 50)
active = False
player_name = ''
color = 'red'

while run:
    if gamemode == "menu":
        reg = False
        player_name = ''
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                run = False
            elif i.type == pygame.MOUSEBUTTONDOWN:
                if i.button == 1 and rect_start.collidepoint(i.pos):
                    gamemode = "user"
                elif i.button == 1 and rect_exit.collidepoint(i.pos):
                    run = False
        window.blit(fon,(0,0))
        pygame.draw.rect(window, YELLOW, rect_start)
        window.blit(start_btn, rect_start)
        pygame.draw.rect(window, YELLOW, rect_exit)
        window.blit(exit_btn, rect_exit)
        car_rect.top = 20
        car_rect.left = 20
        block_rect.left = WIDTH

    elif gamemode == "user":
        window.fill((0, 0, 0))

        tabel = font_status.render("Добро пожаловать в игру: ", True, RED)
        window.blit (tabel, (280, 50))

        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                run = False
            if i.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(i.pos):
                    active = True
                    color = 'green'
                else:
                    active = False
                    color = 'red'
            if i.type == pygame.KEYDOWN:
                if active:
                    if i.key == pygame.K_RETURN:
                        conn = mysql.connector.connect(**dbconfig)
                        cursor = conn.cursor()
                        SQL = '''select * from users where name_user= (%s)'''
                        cursor.execute( SQL, (player_name,))
                        current_user = cursor.fetchone()
                        if current_user:
                            reg = True
                        else:
                            SQL = '''insert into users (name_user) values (%s)'''
                            cursor.execute(SQL, (player_name,))
                            conn.commit()
                            SQL = '''select * from users where name_user= (%s)'''
                            cursor.execute( SQL, (player_name,))
                            current_user = cursor.fetchone()

                        cursor.close()
                        conn.close()
                        gamemode = "game"
                    elif i.key == pygame.K_BACKSPACE:
                        player_name = player_name[:-1]
                    else:
                        player_name += i.unicode
        txt_surface = font.render(player_name, True, 'green')
        width = max(200, txt_surface.get_width()+10)
        input_box.w = width
        input_box.x = (WIDTH - width) / 2
        window.blit(txt_surface, (input_box.x+5, input_box.y+5))
        pygame.draw.rect(window, color, input_box, 2)
    
    # elif gamemode == "choose_car":
    #     for i in pygame.event.get():
    #         if i.type == pygame.QUIT:
    #             run = False
    #         elif i.type == pygame.MOUSEBUTTONDOWN:
    #             if i.button == 1 and rect_porsche.collidepoint(i.pos):
    #                 gamemode = "game"
    #             elif i.button == 1 and rect_exit.collidepoint(i.pos):
    #                 run = False
    #     window.blit(fon,(0,0))
    #     pygame.draw.rect(window, YELLOW, rect_start)
    #     window.blit(start_btn, rect_start)
    #     pygame.draw.rect(window, YELLOW, rect_exit)
    #     window.blit(exit_btn, rect_exit)
    #     car_rect.top = 20
    #     car_rect.left = 20
    #     block_rect.left = WIDTH

    elif gamemode == "game":
        window.blit(asphalt,(0,0))
        frame_count += 1
        distance = frame_count//FPS
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                run = False
        keys = pygame.key.get_pressed()

        ## Управление движением ##
        if keys[pygame.K_LEFT]:
            speed_x -= ACCELERATION
        elif keys[pygame.K_RIGHT]:
            speed_x += ACCELERATION
        else:
            # Плавное замедление, если клавиша не нажата
            speed_x *= 0.9

        if keys[pygame.K_UP]:
            speed_y -= ACCELERATION
        elif keys[pygame.K_DOWN]:
            speed_y += ACCELERATION
        else:
            # Плавное замедление, если клавиша не нажата
            speed_y *= 0.9

        # Обновление позиции феррари с учетом скорости
        car_rect.x += speed_x
        car_rect.y += speed_y

        # Ограничение движения феррари в пределах экрана
        car_rect.x = max(0, min(car_rect.x, WIDTH - car_rect.width))
        car_rect.y = max(0, min(car_rect.y, HEIGHT - car_rect.height))

        for i in road:
            if i[0] < 0:
                i[0] = WIDTH
            else:
                i[0] -=2
            pygame.draw.rect(window, WHITE, i)

        if block_rect.left > 0:
            block_rect.left -= SPEED
        else:
            block_rect.left = WIDTH
            block_rect.top = random.choice([20, 120, 240, 360])
        window.blit(block, block_rect)

        if repairTools_rect.left > 0:
            repairTools_rect.left -= SPEED - 3
        elif random.randint(1, 200) == 5:
            repairTools_rect.left = WIDTH
            repairTools_rect.top = random.choice([20, 120, 240, 360])
        else: 
            repairTools_rect.left = -100
        window.blit(repairTools, repairTools_rect)

        if car_rect.colliderect(block_rect):
            kickSound.play()
            damage += 1
            block_rect.left = WIDTH
            block_rect.top = random.choice([20, 120, 240, 360])

        if car_rect.colliderect(repairTools_rect):
            bonusSound.play()
            repair_score += 1
            repairTools_rect.left = -100


        if damage >= 3:
            gamemode = "gameover"
            damage=0
            frame_count = 0

            conn = mysql.connector.connect(**dbconfig)
            cursor = conn.cursor()
            _SQL = '''insert into scores (scores, user_id) values (%s, %s)'''
            cursor.execute(_SQL, (distance, current_user[0]))
            conn.commit()
            cursor.close()
            conn.close()
            
        else:
            window.blit(block, block_rect)
            window.blit(car,car_rect)

        if  repair_score >= 10:
            healthRecharge.play()
            damage = 0
            repair_score = 0
        else:
            window.blit(block, block_rect)
            window.blit(car,car_rect)

        pygame.draw.rect(window, WHITE, (0, 420, WIDTH, 30))

        label = font_status.render("Пройденное растояния: " + str(distance), True, BLACK)
        damage_label = font_status.render("Повреждения: " + str(damage), True, BLACK)
        repair_score_label = font_status.render("Починка: " + str(repair_score), True, BLACK)

        window.blit (label, (10, 420))
        window.blit(damage_label, (300, 420))
        window.blit (repair_score_label, (500, 420))

        if not reg:
            user_hello_text = font.render("WELCOME IN THE GAME, " + player_name, True,
        YELLOW)
            window.blit(user_hello_text, (250, 330))
        else:
            user_hello_text = font.render("Рады приветствовать Вас, " +
        player_name, True, YELLOW)
            window.blit(user_hello_text, (250, 330))

    elif gamemode == "gameover":
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                run = False
            elif i.type == pygame.KEYDOWN:
                if i.key == pygame.K_SPACE:
                    gamemode = "result_score_screen"
        window.blit(gameover_bg, (0, 0))

    elif gamemode == "result_score_screen":
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                run = False
            elif i.type == pygame.KEYDOWN:
                if i.key == pygame.K_SPACE:
                    gamemode = "menu"
        window.blit(score_fon, (0, 0))

        # # show last 5 tries
        # # window.fill(BLACK)
        # scores = []
        # with open("total_score.txt", "r") as file:
        #     for line in file:
        #         scores.append(line)
        
        # last_scores = scores[-5:]
        
        # font = pygame.font.SysFont("arial", 20, bold=True)
        # y = 50
        # for score in last_scores:
        #     player_name = font.render(score[:-1], True, BLACK)
        #     player_name_rect = player_name.get_rect(center=(400, y))
        #     pygame.draw.rect(window, YELLOW, player_name_rect)
        #     window.blit(player_name, player_name_rect)
        #     y += 40  

        conn = mysql.connector.connect(**dbconfig)
        cursor = conn.cursor()
        SQL = '''SELECT scores.scores, users.name_user FROM scores JOIN users ON scores.user_id = users.id_user ORDER BY scores DESC LIMIT 5;'''
        cursor.execute(SQL)
        records = cursor.fetchall()
        # list_records = []
        # for i in records:
        #     list_records.append(i)
        y_pos = 150
        for i in records:
            score_surf = font_style.render(str(i[0]) + " " + str(i[1]), True, WHITE)
            window.blit(score_surf, (80, y_pos))
            y_pos += 30
        


    pygame.display.update()
    clock.tick(FPS)