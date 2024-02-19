import pygame
import math
import diy
import random

import time
import paintclass
# Initialize Pygame
pygame.init()

# Set window size, title, and sidebar width
window_width = 1000
window_height = 800
sidebar_width = 500
bottom_height = 100
screen = pygame.display.set_mode((window_width + sidebar_width, window_height))
pygame.display.set_caption("Mobile Network Demonstrator")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
# Color for User 2 marker (diy)
USER2_MARKER_COLOR = (130, 80, 255)
USER_MARKER_COLOR = (160, 124, 123)
# Create BaseStation class
class BaseStation:
    def __init__(self,ID, x, y, signal_strength, signal_range, network_type, cluster,n):
        self.ID = ID
        self.x = x
        self.y = y
        self.signal_strength = signal_strength
        self.signal_range = signal_range
        self.network_type = network_type
        self.cluster = cluster
        self.avC = {i+1 + (self.cluster-1) * n: False for i in range(n)}  # 初始化频道字典，所有频道都标记为未使用(False)
        self.layer = 1
        self.clas = 0
        self.linkage = None
        self.angl = 0
    def state(self):
        return any(self.avC.values())


# Create User class to represent user positions and information
class User:
    def __init__(self, x, y):
        self.id = None
        self.x = x
        self.y = y
        self.channel = None
        self.cid = None            #for finding the former cluster and get current cluster
        self.strength = None       #in Dbm
        self.interference = -999      # in mW
        self.speed = user_s           # should be changeable
        self.ang = random.uniform(0, 2 * math.pi)  # Random angle in radians
        self.type = None

class Nod:
    def __init__(self, x, y,ups,downs,rights,lefts):
        self.x = x
        self.y = y
        self.available = {
            90: ups,
            270: downs,
            0: rights,
            180: lefts
        }
def spmove(temp):
    New_user = []
    New_sp = []
    for user in temp[:]:
        if user.cid:
            diy.unaff(user, temp,secang)
            diy.retchl(user.cid, user)
        if user.type ==1:
            user.x = user.x + user.speed * math.cos(user.ang)
            user.y = user.y - user.speed * math.sin(user.ang)
            if 0.0 < user.x < 1000.0 and 0.0 < user.y < 800.0:
                new_user = User(user.x, user.y)
                new_user.type = 1
                new_user.ang = user.ang + random.uniform(-0.2, 0.2)
                New_user.append(new_user)
            temp.remove(user)
        elif user.type == 2:
            new_user = User(user.x, user.y)
            new_user.speed = car_s
            new_user.type = 2
            new_user.ang = user.ang
            for node in nodes:
                distance = math.sqrt((user.x - int(node.x)) ** 2 + (user.y - int(node.y)) ** 2)
                if distance <= 2:
                    new_user.x = node.x
                    new_user.y = node.y
                    # 筛选出为True的方向
                    true_directions = [direction for direction, state in node.available.items() if state ]#and int(direction) != user.ang - 180 and int(direction) != user.ang + 180]
                    # 如果有一个或多个方向为True，随机选择一个
                    if true_directions:
                        new_user.ang = int(random.choice(true_directions))
                        print(new_user.ang)
                        break
            if new_user.ang == 0:
                new_user.x = user.x + user.speed
                new_user.y = user.y
            elif new_user.ang == 90:
                new_user.x = user.x
                new_user.y = user.y - user.speed
            elif new_user.ang == 180:
                new_user.x = user.x - user.speed
                new_user.y = user.y
            elif new_user.ang == 270:
                new_user.x = user.x
                new_user.y = user.y + user.speed
            if 0.0 < new_user.x < 1000.0 and 0.0 < new_user.y < 800.0:
                New_sp.append(new_user)
            temp.remove(user)
        elif user.type == 3:
            if 0.0 < user.x < 1000.0 and 0.0 < user.y < 800.0 and user.speed !=car_s:
                user.x = user.x + user.speed * math.cos(user.ang)
                user.y = user.y - user.speed * math.sin(user.ang)
                new_user = User(user.x, user.y)
                new_user.ang = user.ang + random.uniform(-0.2, 0.2)
                new_user.type = 3
                New_user.append(new_user)
            elif 0.0 < user.x < 1000.0 and 0.0 < user.y < 800.0 and user.speed ==car_s:
                new_user = User(user.x, user.y)
                new_user.speed = car_s
                new_user.type = 3
                new_user.ang = user.ang
                for node in nodes:
                    distance = math.sqrt((user.x - int(node.x)) ** 2 + (user.y - int(node.y)) ** 2)
                    if distance <= 2:
                        new_user.x = node.x
                        new_user.y = node.y
                        # 筛选出为True的方向
                        true_directions = [direction for direction, state in node.available.items() if
                                           state]  # and int(direction) != user.ang - 180 and int(direction) != user.ang + 180]
                        # 如果有一个或多个方向为True，随机选择一个
                        if true_directions:
                            new_user.ang = int(random.choice(true_directions))
                            print(new_user.ang)
                            break
                if new_user.ang == 0:
                    new_user.x = user.x + user.speed
                    new_user.y = user.y
                elif new_user.ang == 90:
                    new_user.x = user.x
                    new_user.y = user.y - user.speed
                elif new_user.ang == 180:
                    new_user.x = user.x - user.speed
                    new_user.y = user.y
                elif new_user.ang == 270:
                    new_user.x = user.x
                    new_user.y = user.y + user.speed
                if 0.0 < new_user.x < 1000.0 and 0.0 < new_user.y < 800.0:
                    New_sp.append(new_user)
            temp.remove(user)
    result = []
    for user in New_user:
        user_station, user.strength = diy.find_strongest_base_station(user, sp+base_stations,secang)
        if user_station:
            diy.delchl(user_station, user)
        diy.affect(user, result,secang)
        result.append(user)
    for user in New_sp:
        user_station, user.strength = diy.find_strongest_base_station(user,base_stations,secang)
        if user_station:
            diy.delchl(user_station, user)
        diy.affect(user, result,secang)
        result.append(user)


    for station in sp+base_stations:
        station.angl = diy.find_best_sector(station,result,secang/2) # sector angle 60 degree(should be changeable)

    return New_user,New_sp

def randgen(users,users_sp):
    num = len(users+users_sp)
    if num <=50:
        n = random.randint(0, 10)
        if n == 1:
            x = random.randint(0, 1000)
            y = random.randint(0, 800)
            user = User(x, y)
            user.type = 1
            user_station, user.strength = diy.find_strongest_base_station(user, base_stations + sp,secang)  # 行人使用大基站和小基站
            if user_station:
                diy.delchl(user_station, user)
            diy.affect(user, users + users_sp,secang)
            users.append(user)
        elif n == 2:
            x = random.randint(0, 1000)
            y = random.randint(0, 800)
            a, b = diy.createcar(x, y, nodes)
            user = User(int(a), int(b))
            user.type = 2
            user.ang = 45
            user_station, user.strength = diy.find_strongest_base_station(user, base_stations,secang)  # 特殊载具使用大基站
            if user_station:
                diy.delchl(user_station, user)
            diy.affect(user, users_sp + users,secang)
            user.speed = car_s
            users_sp.append(user)
            # pygame.display.update()





running = True
# Initialize the sidebar
sidebar = pygame.Surface((sidebar_width, window_height))
sidebar.fill(BLACK)

clusters = []
channum,secang,user_s,car_s,file_pic,file_node = diy.initialize('initial.txt')
base_stations,sp = diy.read_base_stations("data.txt",int(channum))  #Total of 100 channels(should be changeable)
nodes = diy.read_map_data(file_node)
# Create InputBoxes
font = pygame.font.Font(None, 32)
#加载导入的图片
# 背景图像路径
background_image_path = file_pic  # 使用双反斜杠 shold be changeable

# 加载背景图像
background_image = pygame.image.load(background_image_path)
background_image = pygame.transform.scale(background_image, (1000,800))  # 调整图像大小以适应窗口

def main():
    global running
    font = pygame.font.Font(None, 24)
    # Initialize user data
    user1 = User(0, 0)
    user1.cid = 0
    users = []
    users_sp =[]
    total =[]
    # Flag to control pause/resume
    pause = True
    state = 0
    add = True
    leg = 0
    # Use pygame's clock to control time
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if add == True:
                        x, y = event.pos
                        user = User(x, y)
                        user.type=1
                        user_station, user.strength = diy.find_strongest_base_station(user, base_stations+sp,secang) #行人使用大基站和小基站
                        if user_station:
                            diy.delchl(user_station, user)
                        diy.affect(user, users+users_sp,secang)
                        users.append(user)
                        pygame.display.update()
                    else:
                        x, y = event.pos
                        a,b = diy.createcar(x,y,nodes)
                        user = User(int(a),int(b))
                        user.type = 2
                        user.ang = 45
                        user_station, user.strength = diy.find_strongest_base_station(user, base_stations,secang) #特殊载具使用大基站
                        if user_station:
                            diy.delchl(user_station, user)
                        diy.affect(user,users_sp+users,secang)
                        user.speed = car_s
                        users_sp.append(user)
                        pygame.display.update()

                elif event.button == 3:
                    if add == True:
                        x, y = event.pos
                        for user in users:
                            distance = math.sqrt((x - user.x) ** 2 + (y - user.y) ** 2)
                            if distance <= 10:  # 判断点击是否在用户附近
                                if user.cid:
                                    diy.unaff(user, users+users_sp,secang)
                                    diy.retchl(user.cid, user)
                                users.remove(user)
                                break
                    else:
                        x, y = event.pos
                        for user in users_sp:
                            distance = math.sqrt((x - user.x) ** 2 + (y - user.y) ** 2)
                            if distance <= 10:  # 判断点击是否在用户附近
                                if user.cid:
                                    diy.unaff(user, users_sp+users,secang)
                                    diy.retchl(user.cid, user)
                                users_sp.remove(user)
                                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pause = not pause  # Toggle pause flag
                if event.key == pygame.K_1:
                    state = 1
                if event.key == pygame.K_2:
                    state = 2
                if event.key == pygame.K_0:
                    state = 0
                if event.key == pygame.K_3:
                    state = 3
                if event.key == pygame.K_q:
                    add = not add
                if event.key == pygame.K_6:
                    x, y = pygame.mouse.get_pos()
                    for user in users+users_sp:
                        distance = math.sqrt((x - user.x) ** 2 + (y - user.y) ** 2)
                        if distance <= 10:  # 判断点击是否在用户附近
                            if user.cid and user.type!=3:
                                user.type = 3
                            elif user.cid and user.type == 3 and user.speed==user_s:
                                user.type = 1
                            elif user.cid and user.type == 3 and user.speed!=user_s:
                                user.type = 2

        screen.fill(WHITE)
        #screen.blit(background_image, (0, 0))
        sidebar.fill(BLACK)
        #inputbar.fill(BLACK)

        #randgen(users,users_sp)

        if state ==1:
            screen.blit(background_image, (0, 0))
            paintclass.draw_car_run(font, sidebar, users_sp, leg)
            for user in users+users_sp:
                if user.type ==3:
                    paintclass.zd(font, sidebar, user)
                    break
            if leg <=3:
                paintclass.draw_user_run(font, sidebar, users)
                leg +=1
            elif leg ==6:
                paintclass.draw_user(font, sidebar, users)
                leg=0
            else:
                paintclass.draw_user(font, sidebar, users)
                leg+=1

            paintclass.draw_stationa(base_stations,secang/2)
        elif state ==2:
            for user in users+users_sp:
                if user.type ==3:
                    paintclass.zd(font, sidebar, user)
                    break
            if leg <= 3:
                paintclass.draw_user_run(font, sidebar, users)
                leg += 1
            elif leg == 6:
                paintclass.draw_user(font, sidebar, users)
                leg = 0
            else:
                paintclass.draw_user(font, sidebar, users)
                leg += 1

            paintclass.draw_stationa(sp,secang/2)
        elif state == 0:
            screen.blit(background_image, (0, 0))
            paintclass.draw_car_run(font,sidebar,users_sp,leg)
            for user in users+users_sp:
                if user.type ==3:
                    paintclass.zd(font, sidebar, user)
                    break
            if leg <= 3:
                paintclass.draw_user_run(font, sidebar, users)
                leg += 1
            elif leg == 6:
                paintclass.draw_user(font, sidebar, users)
                leg = 0
            else:
                paintclass.draw_user(font, sidebar, users)
                leg += 1
            paintclass.draw_stationa(base_stations+sp,secang/2)
        elif state == 3:
            paintclass.draw_car_run(font, sidebar, users_sp, leg)
            for user in users+users_sp:
                if user.type ==3:
                    paintclass.zd(font, sidebar, user)
                    break
            if leg <= 2:
                paintclass.draw_user_run(font, sidebar, users)
                leg += 1
            elif leg == 4:
                paintclass.draw_user(font, sidebar, users)
                leg = 0
            else:
                paintclass.draw_user(font, sidebar, users)
                leg += 1
            paintclass.draw_stationa(base_stations+sp,secang/2)

        # 鼠标点绘制
        x, y = pygame.mouse.get_pos()
        user1 = User(x, y)
        strongest_station, max_signal_strength = diy.find_strongest_base_station(user1, base_stations+sp,secang)
        z = 10*math.sqrt(
            (x - strongest_station.x) ** 2 + (y - strongest_station.y) ** 2) if strongest_station else None

        #detect if users are paused(change or not)
        if pause is False:
            users,users_sp = spmove(users+users_sp)
        else:
            users = users
            users_sp = users_sp
        paintclass.draw_mouse(font, sidebar,user1, strongest_station, max_signal_strength, z)

        text = font.render(f"Pause? (use space key): {pause}/ current user:{len(users),len(users_sp)}", True, WHITE)
        sidebar.blit(text, (10, 210))
        screen.blit(sidebar, (window_width, 0))
        text = font.render(f"current drawing state(0/1/2/3): {state}", True, WHITE)
        sidebar.blit(text, (10, 225))
        screen.blit(sidebar, (window_width, 0))
        if add == True:
            text = font.render(f"Now adding normal users ", True, WHITE)
        else:
            text = font.render(f"Now adding special users ", True, WHITE)
        sidebar.blit(text, (10, 240))
        screen.blit(sidebar, (window_width, 0))

        clock.tick(10)
        pygame.display.flip()
    pygame.quit()

if __name__ == "__main__":
    main()