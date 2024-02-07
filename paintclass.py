import pygame
import diy
import math
window_width = 1000
window_height = 800
sidebar_width = 500
bottom_height = 200
screen = pygame.display.set_mode((window_width + sidebar_width, window_height))
pygame.display.set_caption("MND")
# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
# Color for User 2 marker (diy)
USER2_MARKER_COLOR = (130, 80, 255)
USER_MARKER_COLOR = (160, 124, 123)
def draw_mouse(font,sidebar,user1,strongest_station,max_signal_strength,z):
    if strongest_station:
        text = font.render(f"Strongest Base station info (Mouse{user1.x}.{user1.y}):ID:{strongest_station.ID}", True, WHITE)
        sidebar.blit(text, (10, 10))
        text = font.render(f"Signal strength(dbm): {max_signal_strength}", True, WHITE)
        sidebar.blit(text, (10, 40))
        text = font.render(f"Base station position: ({strongest_station.x}, {strongest_station.y})", True, WHITE)
        sidebar.blit(text, (10, 70))
        text = font.render(f"Signal range radius (m): {10*strongest_station.signal_range}", True, WHITE)
        sidebar.blit(text, (10, 100))
        text = font.render(f"Distance from the base station: {z}", True, WHITE)
        sidebar.blit(text, (10, 130))
        text = font.render(f"Channel No. in cluster {strongest_station.cluster}", True, WHITE)
        sidebar.blit(text, (10, 160))
        text = font.render(f"Network Type: {strongest_station.network_type}", True, WHITE)
        sidebar.blit(text, (10, 190))
    else:
        text = font.render("No signal found", True, WHITE)
        sidebar.blit(text, (10, 10))

def draw_user(font,sidebar,users):
    if users is not None:
        for num, user in enumerate(users, start=1):
            if user:
                if user.type==3:
                    pygame.draw.circle(screen, (255,0,0), (user.x, user.y), 3)
                else:
                    pygame.draw.circle(screen, USER_MARKER_COLOR, (user.x, user.y), 2)
                pygame.draw.circle(screen, USER_MARKER_COLOR, (user.x, user.y), 2)
                pygame.draw.line(screen, BLACK, (user.x, user.y + 2), (user.x , user.y + 8), 1)
                pygame.draw.line(screen, BLACK, (user.x-2, user.y + 3), (user.x+2, user.y + 3), 1)

def draw_user_run(font,sidebar,users):
    if users is not None:
        for num, user in enumerate(users, start=1):
            if user:
                if user.type==3:
                    pygame.draw.circle(screen, (255,0,0), (user.x, user.y), 3)
                    if user.cid:
                        pygame.draw.circle(screen, (55, 50, 255), (user.cid.x, user.cid.y), 3)
                else:
                    pygame.draw.circle(screen, USER_MARKER_COLOR, (user.x, user.y), 2)
                pygame.draw.line(screen, BLACK, (user.x, user.y + 2), (user.x , user.y + 5), 1)
                pygame.draw.line(screen, BLACK, (user.x - 2, user.y + 3), (user.x + 2, user.y + 3), 1)
                pygame.draw.line(screen, BLACK, (user.x, user.y + 4), (user.x+3, user.y + 7), 1)
                pygame.draw.line(screen, BLACK, (user.x, user.y + 4), (user.x-3, user.y + 7), 1)
def draw_stationa(base_stations,secang):
    if base_stations is not None:
        for station in base_stations:
            color = (int(station.cluster * 127) % 256, int(station.cluster * 143) % 256, int(station.cluster * 217) % 256)
            distan = min(station.signal_range/10,4)
            points = diy.calculate_hexagon_vertices(station.x, station.y, station.signal_range)
            pygame.draw.polygon(screen, color, points, 1)
            pygame.draw.circle(screen, color, (station.x, station.y), 1.5)
            pygame.draw.line(screen, color, (station.x, station.y+1),(station.x-distan, station.y+2*distan), 1)
            pygame.draw.line(screen, color, (station.x, station.y+1), (station.x + distan, station.y + 2*distan), 1)
            pygame.draw.line(screen, color, (station.x+distan, station.y+2*distan), (station.x - distan, station.y + 2*distan), 1)
            #print(station.ID,station.state())
            if station.state():
                # Drawing the sector lines
                angle1 = station.angl - secang
                angle2 = station.angl + secang

                # Converting angles to radians
                radian1 = math.radians(angle1)
                radian2 = math.radians(angle2)

                # Calculating end points for each line
                end_x1 = station.x + station.signal_range * math.cos(radian1)
                end_y1 = station.y + station.signal_range * math.sin(radian1)
                end_x2 = station.x + station.signal_range * math.cos(radian2)
                end_y2 = station.y + station.signal_range * math.sin(radian2)

                # Drawing lines
                pygame.draw.line(screen, color, (station.x, station.y), (end_x1, end_y1), 1)
                pygame.draw.line(screen, color, (station.x, station.y), (end_x2, end_y2), 1)

def zd(font,sidebar,user):
    if user and user.cid:
        text = font.render(f"Information for the labeled user:", True, WHITE)
        sidebar.blit(text, (10, 310))
        text = font.render(f"User Signal strength (dbm): {user.strength}", True, WHITE)
        sidebar.blit(text, (10, 340))
        text = font.render(f"Base station position: ({user.cid.x}, {user.cid.y})", True, WHITE)
        sidebar.blit(text, (10, 370))
        text = font.render(f"Signal range radius (m): {10*user.cid.signal_range}", True, WHITE)
        sidebar.blit(text, (10, 400))
        text = font.render(f"Distance from the base station(m): {10*math.sqrt((user.cid.x - user.x) ** 2 + (user.cid.y - user.y) ** 2)}", True, WHITE)
        sidebar.blit(text, (10, 430))
        text = font.render(f"Frequency Channel No. {user.channel}", True, WHITE)
        sidebar.blit(text, (10, 460))
        text = font.render(f"Network Type: {user.cid.network_type}", True, WHITE)
        sidebar.blit(text, (10, 490))
        text = font.render(f"Current interference (dbm): {user.interference}", True, WHITE)
        sidebar.blit(text, (10, 520))
        text = font.render(f"Current SINR (Db) : {round(user.strength-max(user.interference,-150),3)}", True, WHITE)
        sidebar.blit(text, (10, 550))
    else:
        text = font.render("No signal found", True, WHITE)
        sidebar.blit(text, (10, 310)) #2030行代码 in total

def draw_car_run(font,sidebar,users,leg):
    if users is not None:
        for num, user in enumerate(users, start=1):
            if user:

                if user.type==3:
                    pygame.draw.circle(screen, (255,0,0), (user.x, user.y), 3)
                    car_rect = pygame.Rect(user.x - 4, user.y - 4, 8, 4)
                    pygame.draw.circle(screen, (125, 125, 125), (user.x - 3, user.y + 2), 2)
                    pygame.draw.circle(screen, (0, 125, 0), (user.x + 3, user.y + 2), 2)
                    pygame.draw.rect(screen, (0, 0, 255), car_rect)
                    if user.cid:
                        pygame.draw.circle(screen, (55, 50, 255), (user.cid.x, user.cid.y), 3)
                else:
                    car_rect = pygame.Rect(user.x - 4, user.y - 4, 8, 4)
                    #wheel1 = pygame.Rect(user.x-3,user.y-2,1,1)
                    #wheel2 = pygame.Rect(user.x + 3, user.y - 2, 1, 1)
                    # 绘制小车
                    #start_angle = math.radians(leg*60)
                    #end_angle = start_angle + 0.6
                    # 绘制圆弧
                    pygame.draw.circle(screen,(125,125,125),(user.x-3,user.y+2),2)
                    pygame.draw.circle(screen, (0, 125, 0), (user.x + 3, user.y + 2), 2)
                    pygame.draw.rect(screen, (0, 0, 255), car_rect)
                    #pygame.draw.arc(screen, (2, 2, 0), wheel1, start_angle, end_angle, 2)
                    #pygame.draw.arc(screen, (2,2,0), wheel2, start_angle, end_angle, 2)