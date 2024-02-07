import math
import os
import random
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

class User:
    def __init__(self, x, y):
        self.id = None
        self.x = x
        self.y = y
        self.channel = None
        self.cid = None            #for finding the former cluster and get current cluster
        self.strength = None       #in Dbm
        self.interference = 0      # in mW
        self.speed = 0
        self.ang = 0

# Function to read base station data from data.txt
def read_base_stations(filename,n):
    stat_1 = []
    stat_2 = []
    network_types = ["LTE", "GSM", "2G", "WiFi"]
    try:
        with open(filename, 'r') as file:
            for line in file:
                parts = line.strip().split(',')
                if len(parts) == 10:
                    ID, x, y, signal_strength, signal_range, network_type, cluster,c,clas,link = parts
                    base_station = BaseStation(int(ID), int(x),int(y) , int(signal_strength), int(signal_range), int(network_type), int(cluster), int(int(n)/int(c)))
                    base_station.layer = int(c)
                    base_station.clas = clas
                    base_station.linkage = link
                    if network_type !='0':
                        base_station.network_type = network_types[int(network_type)-1]
                    elif network_type =='0':
                        base_station.network_type = 'Nr5G'
                    if clas == '1' :
                        stat_1.append(base_station)
                    elif clas =='2' or clas =='3':
                        for stst in stat_1:
                            if int(stst.ID) == int(base_station.linkage):
                                x=int(min(stst.avC.keys()))
                                y=int(int(n) /base_station.layer)
                                base_station.avC = None
                                base_station.avC = {i + x + (base_station.cluster - 1) * y: False for i in range(y)}
                                #print(min(base_station.avC.keys()))
                        stat_2.append(base_station)
    except FileNotFoundError:
        pass
    print(len(stat_1),len(stat_2))
    return stat_1,stat_2
# Read base station data from data.txt
#read before doit
def read_base_stations_sp(filename,n):
    base_stations = []
    sp = []
    layer3 = []
    network_types = ["LTE", "GSM", "2G", "WiFi"]
    try:
        with open(filename, 'r') as file:
            for line in file:
                parts = line.strip().split(',')
                if len(parts) == 10:
                    ID, x, y, signal_strength, signal_range, network_type, cluster, c, clas, link = parts
                    base_station = BaseStation(int(ID), int(x), int(y), int(signal_strength), int(signal_range),
                                               int(network_type), int(cluster), int(int(n) / int(c)))
                    base_station.layer = int(c)
                    base_station.clas = clas
                    base_station.linkage = link

                    if clas == '2':
                        base_stations.append(base_station)
                    elif clas == '1':
                        sp.append(base_station)
                    elif clas == '3':
                        layer3.append(base_station)

    except FileNotFoundError:
        pass
    #print(len(base_stations))
    return sp,base_stations,layer3

def find_strongest_base_station(user, base_stations):
    best_station = None
    best_signal_strength = float("-inf")
    x = int(user.x)
    y = int(user.y)
    for station in base_stations:
        distance = math.sqrt((x - station.x) ** 2 + (y - station.y) ** 2)
        if distance <= station.signal_range:
            # 计算用户在该基站处的信号强度，考虑距离因素
            station_signal_strength = station.signal_strength-loss(user,station)
            if station_signal_strength > best_signal_strength:
                best_signal_strength = station_signal_strength
                best_station = station
    return best_station, best_signal_strength

#8wei
def save(filename, base_stations):
    x = len(base_stations)
    num = 0
    with open(filename, 'w') as file:
        for station in base_stations:
            num = num+1
            station.ID= num
            file.write(f"{station.ID},{station.x},{station.y},{station.signal_strength},{station.signal_range},{station.network_type},{station.cluster},{station.layer},{station.clas},{station.linkage}\n")
def read_base_stations_and_create_clusters(H_stations, i, j):
    stations = H_stations.copy()
    temp = H_stations.copy()
    num = i**2+i*j+j**2
    for station in stations:
        station.cluster = None
    while stations:
        base_station = stations.pop(0)
        if base_station.cluster is None:
            base_station.cluster = find_min(temp)

        find_same(i, j, base_station, temp)

def find_same(i, j, station, stations):
    diameter = station.signal_range * math.sqrt(3)
    for a in range(6):
        radi = math.radians(60 * a + 30)  # Calculate the angle for each vertex i, with a 60-degree interval
        radj = math.radians(60 * a + 90)  # Calculate the angle for each vertex j, with a 60-degree interval
        x = station.x + i * diameter * math.cos(radi) + j * diameter * math.cos(radj)
        y = station.y - i * diameter * math.sin(radi) - j * diameter * math.sin(radj)
        for stat in stations:
            distance = math.sqrt((stat.x - x) ** 2 + (stat.y - y) ** 2)
            if distance <= station.signal_range:
                if stat.cluster is None:
                    stat.cluster = station.cluster
                elif stat.cluster is not None:
                    stat.cluster = min(station.cluster,stat.cluster)
                    station.cluster = min(station.cluster, stat.cluster)

def find_min(stations):
    # 创建一个集合，用于存储 stations 中存在的 cid 值
    existing_cids = set()
    # 遍历 stations 列表，将每个 station 的 cid 加入 existing_cids 集合
    for station in stations:
        existing_cids.add(station.cluster)
    num = 1# 初始化 num 为 1
    # 不断增加 num 直到它不在 existing_cids 集合中
    while num in existing_cids:
        num += 1
    # 返回找到的最小的 num
    return num

def retchl(stat, user):
    try:
        if user.channel is not None:
            if stat:
                # 假设频道是一个标记已使用或未使用的字典
                stat.avC[user.channel] = False  # 将频道标记为未使用
                stat.state()
                user.channel = None
            else:
                print("找不到指定ID的基站。")
    except ValueError:
        print("输入无效。")
    except TypeError:
        print("输入无效。")

def delchl(stat, user):
    try:
        if stat:
            # 寻找第一个标记为未使用的频道
            for channel, in_use in stat.avC.items():
                if not in_use:
                    user.channel = channel
                    user.cid = stat
                    stat.avC[channel] = True  # 将频道标记为已使用
                    break
            else:
                print("基站没有可用的频道。")
        else:
            print("找不到指定ID的基站或基站没有可用的频道。")
    except ValueError:
        print("输入无效。")

def loss(user,stst):
    distance = 10*math.sqrt((int(stst.x) - int(user.x)) ** 2 + (int(stst.y) - int(user.y)) ** 2)#/70
    if distance==0:
        return 0.0001
    else:
       return 20*math.log(distance, 10)

def affect(user,users):
        station = user.cid
        if station is not None:
            for user_old in users:
                if user_old.channel == user.channel:
                    ang = calculate_angle(station, user_old)
                    ang2 = calculate_angle(user_old.cid, user)
                    if station.angl - 30 <= ang < station.angl + 30:
                        user_old.interference = user_old.interference + round(1.5*station.signal_strength - (loss(user_old, station)), 3)
                        user.interference = user.interference + round(user_old.cid.signal_strength - (loss(user, user_old.cid)), 3)
                    elif user_old.cid.angl-30<=ang2<user_old.cid.angl + 30:
                         user_old.interference = user_old.interference + round(station.signal_strength - (loss(user_old, station)), 3)
                         user.interference = user.interference + round(1.5*user_old.cid.signal_strength - (loss(user, user_old.cid)), 3)
                    else:
                        user_old.interference = user_old.interference + round(station.signal_strength - (loss(user_old, station)), 3)
                        user.interference = user.interference + round(user_old.cid.signal_strength - (loss(user, user_old.cid)), 3)

                else:
                    continue
def unaff(user,users):
        station = user.cid
        if station is not None:
            for user_old in users:
                if user_old.channel == user.channel:
                    ang = calculate_angle(station,user_old)
                    if station.angl - 30 <= ang < station.angl + 30:
                        user_old.interference = round(user_old.interference - 1.5*station.signal_strength - (loss(user_old, station)), 3)
                    else:
                        user_old.interference = round(user_old.interference - station.signal_strength - (loss(user_old, station)), 3)
                else:
                    continue
        else:
            print('station is none')

# 计算六边形的顶点的函数
def calculate_hexagon_vertices(center_x, center_y, radius):
    vertices = []
    for i in range(6):
        angle_rad = math.radians(60 * i)
        x = center_x + (radius - 1) * math.cos(angle_rad)
        y = center_y - (radius - 1) * math.sin(angle_rad)
        vertices.append((x, y))
    return vertices

def generate_random_base_stations(num_stations, window_width, window_height,m,n,clas):
    base_stations = []
    # 计算基站的信号范围，以便占满整个屏幕
    base_station_radius = max(window_width, window_height) / (math.sqrt(2)*math.ceil(math.sqrt(3 * num_stations / 2)))
    base_station_radius = round(base_station_radius)

    # 计算蜂巢布局的参数
    horizontal_spacing = 3 * base_station_radius
    vertical_spacing = math.sqrt(3) * base_station_radius

    # 初始化位置参数
    x = horizontal_spacing / 3
    y = base_station_radius / 2
    l=1
    a=1
    b=1
    for i in range(num_stations):
        if y > window_height:
            break

        # 随机信号强度
        signal_strength =0
        if clas == '1':
            signal_strength = random.randint(50, 60)
        elif clas == '2':
            signal_strength = random.randint(35, 45)


        network_type = random.randint(1,4)
        new_station = BaseStation(len(base_stations) + 1, int(x), int(y), (signal_strength - 20*(3-clas)), base_station_radius, network_type,0,0)
        new_station.layer = m ** 2 + m * n + n ** 2
        new_station.clas = clas
        #print(a,b)
        base_stations.append(new_station)
        a =a+1

        # 更新坐标位置，实现蜂巢布局
        x += horizontal_spacing
        if x > window_width:
            b = b+1
            a=1
            if l == 0:
                x = horizontal_spacing / 3
                y += vertical_spacing/2
                l=1
            elif l==1:
                x = 2.5*horizontal_spacing / 3
                y += vertical_spacing/2
                l=0
    print(f"生成了{len(base_stations)}个基站")
    read_base_stations_and_create_clusters(base_stations, m, n)
    return base_stations
'''
def generate_random_base_stations_hexagon(num_stations, station, m, n, c):
    hexagon_side = station.signal_range#2
    base_stations = []
    hexagon_height = math.sqrt(3) * hexagon_side#2rt3
    base_station_radius = math.sqrt(1.8)*hexagon_side / (math.ceil(math.sqrt(3 * (num_stations) / 2)))
    base_station_radius = round(base_station_radius)
    #base_station_radius = 20

    horizontal_spacing = 3 * base_station_radius #3a
    vertical_spacing = math.sqrt(3) * base_station_radius
    #horizontal_spacing = 2 * base_station_radius
    #vertical_spacing = 2*math.sqrt(3) * base_station_radius

    x = (- hexagon_side)/2
    y = (-hexagon_height) / 2

    l = 0
    a = 1
    b = 1
    for i in range(100):
        if y > hexagon_height/2:
            break

        # 更新坐标位置，实现蜂巢布局
        x = x + horizontal_spacing# 3a
        distance = math.sqrt(x ** 2 + y ** 2)
        if distance >= hexagon_side:
            b = b + 1
            a = 1

            if l == 0:
                x = horizontal_spacing / 2 - hexagon_side/2
                y += vertical_spacing / 2
                l = 1
            elif l == 1:
                x = - hexagon_side/2
                y += vertical_spacing / 2
                l = 0

        # 随机信号强度
        if i !=0 and len(base_stations) < num_stations :
            signal_strength = random.randint(30, 120)
            network_type = random.randint(1, 4)
            new_station = BaseStation(len(base_stations) + 1, int(x + station.x), int(y + station.y), signal_strength,
                                      base_station_radius, network_type, 0, 0)
            new_station.layer = c
            print(a, b)
            base_stations.append(new_station)
        a = a + 1

    print(f"生成了{len(base_stations)}个基站")
    read_base_stations_and_create_clusters(base_stations, m, n)
    return base_stations
'''
#layer 此处指的是第几层，其他stat.layer只多少份公用
def generate_er(stations, m, n, x,y,layer):
    station = None
    line = 0
    term = 0
    previousx = 0
    previousy = 0
    for stat in stations:
        term+=1
        if stat.y != previousy:
            line +=1
            term = 1
        if line == y and term ==x:
            station = stat
            break
        previousy=stat.y

    if station is not None:
        hexagon_side = station.signal_range  # 2
        base_stations = []
        hexagon_height = math.sqrt(3) * hexagon_side  # 2rt3
        base_station_radius = hexagon_side / 4
        base_station_radius = round(base_station_radius)
        # base_station_radius = 20

        horizontal_spacing = 3 * base_station_radius  # 3a
        vertical_spacing = math.sqrt(3) * base_station_radius / 2

        x = (base_station_radius - hexagon_side) / 2 + station.x
        y = vertical_spacing + (-hexagon_height) / 2 + station.y
        a, b = find_points_20_hex(x, y, horizontal_spacing, vertical_spacing)

        for i in range(int(19)):
            signal_strength = random.randint(35, 45)
            network_type = random.randint(1, 4)
            new_station = BaseStation(len(base_stations+stations) + 1, int(a[i]), int(b[i]), signal_strength,
                                      base_station_radius, network_type, 0, 0)
            new_station.layer = (m ** 2 + m * n + n ** 2)*station.layer
            new_station.clas = layer
            new_station.linkage = station.ID
            base_stations.append(new_station)

        print(f"生成了{len(base_stations)}个基站")
        read_base_stations_and_create_clusters(base_stations, m, n)
        return base_stations
    else:
        print('Not found Station ')
        return None

def generate_san(stations, m, n,Num,layer):
    station = None
    term = 0
    for stat in stations:
        term+=1
        if stat.ID == Num:
            station = stat
            break

    if station is not None:
        hexagon_side = station.signal_range  # 2
        base_stations = []
        hexagon_height = math.sqrt(3) * hexagon_side  # 2rt3
        base_station_radius = hexagon_side / 4
        base_station_radius = round(base_station_radius)
        # base_station_radius = 20

        horizontal_spacing = 3 * base_station_radius  # 3a
        vertical_spacing = math.sqrt(3) * base_station_radius / 2

        x = (base_station_radius - hexagon_side) / 2 + station.x
        y = vertical_spacing + (-hexagon_height) / 2 + station.y
        a, b = find_points_12_hex(x, y, horizontal_spacing, vertical_spacing)

        for i in range(int(12)):
            signal_strength = 30
            network_type = random.randint(1, 4)
            new_station = BaseStation(len(base_stations+stations) + 1, int(a[i]), int(b[i]), signal_strength,
                                      base_station_radius, network_type, 0, 0)
            new_station.layer = (m ** 2 + m * n + n ** 2)*station.layer
            new_station.clas = layer
            new_station.linkage = station.ID
            base_stations.append(new_station)

        print(f"生成了{len(base_stations)}个基站")
        read_base_stations_and_create_clusters(base_stations, m, n)
        return base_stations
    else:
        print('Not found Station ')

def find_points_12_hex(x,y,r,h):
    a = [x,x+r,x+r/2,x,x+r,x+r*3/2,x-r/2,x,x+r,x+r/2,x,x+r]
    b = [y,y,y+h,y+2*h,y+2*h,y+3*h,y+3*h,y+4*h,y+4*h,y+5*h,y+6*h,y+6*h]
    return a,b

def find_points_20_hex(x,y,r,h):
    a = [x,x+r,x+r/2,x,x+r,x+r*3/2,x+r/2,x-r/2,x,x+r,x+r/2,x,x+r,x+r/2,x+r/2,x+r*3/2,x-r/2,x+r*3/2,x-r/2]
    b = [y,y,y+h,y+2*h,y+2*h,y+3*h,y+3*h,y+3*h,y+4*h,y+4*h,y+5*h,y+6*h,y+6*h,y-h,y+7*h,y+h,y+h,y+5*h,y+5*h]
    return a,b

def calculate_angle(base_station, user):
    # 计算基站和用户之间的角度
    dx = user.x - base_station.x
    dy = user.y - base_station.y
    angle = math.atan2(dy, dx) * 180 / math.pi
    return angle % 360

def find_best_sector(base_station, users, sector_angle):
    best_angle = 0
    max_count = 0

    for angle in range(0, 360):
        count = 0
        for user in users:
            if user.cid is not None:
                if user.cid.ID == base_station.ID:
                    user_angle = calculate_angle(base_station, user)
                    if angle - sector_angle <= user_angle < angle + sector_angle:
                        count += 1

        if count > max_count:
            max_count = count
            best_angle = angle

    return best_angle

def read_map_data(filename):
    with open(filename, 'r') as file:
        nodes = []
        for line in file:
            parts = line.strip().split(',')
            if len(parts) == 6:
                x, y, up,down,right,left = parts
                ups = parts[2].strip().lower() == 'true'
                downs = parts[3].strip().lower() == 'true'
                rights = parts[4].strip().lower() == 'true'
                lefts = parts[5].strip().lower() == 'true'
                nod=Nod(x,y,ups,downs,rights,lefts)
                nodes.append(nod)
    return nodes

def createcar(x,y,nodes):
    a=0
    b=0
    mi = 10000
    for node in nodes :
        distance = math.sqrt((x - int(node.x)) ** 2 + (y - int(node.y)) ** 2)
        if distance < mi:
            mi=distance
            a=node.x
            b=node.y
    return a,b

def initialize(filename):
    ini = []
    try:
        with open(filename, 'r') as file:
            for line in file:
                parts = line.strip().split(',')
                if len(parts) == 6:
                    channel,secang,user_s,car_s,file_pic,file_node = parts


    except TypeError:
        print("输入无效。")

    print(channel, secang, user_s, car_s, file_pic, file_node)
    return int(channel),int(secang),float(user_s),float(car_s),str(file_pic),str(file_node)