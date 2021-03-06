import pygame       # pygame 라이브러리 import
import random       # random 라이브러리 import
from time import sleep

WHITE = (255, 255, 255)     # 흰색
pad_width = 1024            # 게임판 폭
pad_height = 512            # 게임판 높이
background_width = 1024     # 배경화면 폭
bat_width = 110
bat_height = 67
aircraft_width = 90
aircraft_height = 55

def drawObject(obj, x, y):      # 화면에 객체를 그리는 함수(비행기, 적 등)
    global gamepad
    gamepad.blit(obj, (x, y))

# def back(background, x, y):                                      # 배경이미지 그리는 함수
#     global gamepad
#     gamepad.blit(background, (x,y))
#
# def airplane(x,y):                                  # 비행기 그리는 함수
#     global gamepad, aircraft
#     gamepad.blit(aircraft, (x,y))

def runGame():
    # 실제 게임이 구동되는 함수
    global gamepad, aircraft, clock, background1, background2     # 전역변수로 사용 설정
    global bat, fires, bullet, boom

    isShotBat = False
    boom_count = 0

    bullet_xy = []                                   # 왼쪽 컨트롤 키를 누를때마다 총알의 위치를 저장할 리스트

    x = pad_width * 0.05                             # 초기 비행기 위치 x
    y = pad_height * 0.8                             # 초기 비행기 위치 y
    y_change = 0                                     # y축 이동 변수

    background1_x = 0                                # 배경이미지의 좌상단 모서리의 x 좌표
    background2_x = background_width                 # 다음 배경이미지 x좌표는 오른쪽에 붙여서

    bat_x = pad_width                                # 박쥐 위치
    bat_y = random.randrange(0, pad_height)

    fire_x = pad_width                               # 불덩어리 위치
    fire_y = random.randrange(0, pad_height)

    random.shuffle(fires)
    fire = fires[0]

    crashed = False                                 # 게임을 종료하기 위한 Flag 변수
    while not crashed:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:           # 종료 이벤트인 경우, loop를 빠져 나옴
                crashed = True

            if event.type == pygame.KEYDOWN:        # 키가 눌러졌다면
                if event.key == pygame.K_UP:        # 눌러진 키가 화살표 위 키이면
                   y_change = -5
                elif event.key == pygame.K_DOWN:    # 눌러진 키가 화살표 아래 키이면
                    y_change = 5
                elif event.key == pygame.K_LCTRL:   # 왼쪽 컨트롤 키가 눌러졌다면
                    bullet_x = x + aircraft_width    # 비행기의 앞부분에서
                    bullet_y = y + aircraft_height / 2  # 비행기의 중간 정도의 높이에서
                    bullet_xy.append([bullet_x, bullet_y])  # 총알 좌표 설정
                elif event.key == pygame.K_SPACE:   # 스페이스 키가 눌러지면
                    sleep(5)                         # 5초간 정지지
            if event.type == pygame.KEYUP:          # 키가 떼어졌다면
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN: # 위아래 방향키이면
                        y_change = 0                # 이동을 멈춤

        gamepad.fill(WHITE)                         # 게임판을 흰색으로 채우고

        background1_x -= 2
        background2_x -= 2

        if background1_x == -background_width:
            background1_x = background_width

        if background2_x == -background_width:
            background2_x = background_width

        # back(background1, background1_x, 0)                       # 배경화면의 위치 초기에는 (0,0)
        # back(background2, background2_x, 0)
        #
        # airplane(x,y)                               # 비행기 그리기

        drawObject(background1, background1_x, 0)
        drawObject(background2, background2_x, 0)

        # 비행기 위치
        y += y_change  # 비행기의 y좌표 값을 갱신
        if y < 0:       # 비행기가 화면을 벗어나지 않도록 설정
            y = 0
        elif y > pad_height - aircraft_height:
            y = pad_height - aircraft_height

        # 박쥐 위치
        bat_x -= 7                                  # 박쥐가 비행기 쪽으로 날아오게 x좌표를 감소
        if bat_x <= 0:                              # 왼쪽 끝까지 오면
            bat_x = pad_width                       # 박쥐 위치를 다시 오른쪽 끝으로
            bat_y = random.randrange(0, pad_height) # 높이는 랜덤

        # 불덩어리 위치
        if fire == None:                           # 불덩어리가 None이면 속도는 -30
            fire_x -= 30
        else:
            fire_x -= 15                            # 진짜 불덩어리면 속도는 -15

        if fire_x <= 0:
            fire_x = pad_width
            fire_y = random.randrange(0, pad_height)
            random.shuffle(fires)
            fire = fires[0]

        # 총알 위치
        if len(bullet_xy) != 0:                     # 총알이 있는 동안에
            for i, bxy in enumerate(bullet_xy):     # 하나씩 가져 옵시다.
                bxy[0] += 15                         # 총알속도는 15픽셀
                bullet_xy[i][0] = bxy[0]

                # 총알이 박쥐와 부딪혔는지 체크
                if bxy[0] > bat_x:
                    if bxy[1] > bat_y and bxy[1] < bat_y + bat_height:
                        bullet_xy.remove(bxy)
                        isShotBat = True

                if bxy[0] >= pad_width:             # 총알이 화면을 벗어나면
                    try:
                        bullet_xy.remove(bxy)           # 총알 삭제
                    except:
                        pass

        drawObject(aircraft, x, y)
        #drawObject(bat, bat_x, bat_y)

        if fire != None:
            drawObject(fire, fire_x, fire_y)

        if len(bullet_xy) != 0:
            for bx, by in bullet_xy:
                drawObject(bullet, bx, by)

        if not isShotBat:
            drawObject(bat, bat_x, bat_y)
        else:
            drawObject(boom, bat_x, bat_y)
            boom_count += 1
            if boom_count > 5:
                boom_count = 0
                bat_x = pad_width
                bat_y = random.randrange(0, pad_height - bat_height)
                isShotBat = False

        pygame.display.update()                     # 게임판을 다시 그림
        clock.tick(60)                              # FPS를 60으로 설정

    pygame.quit()                                   # 초기화한 pygame 종료
    quit()

def initGame():
    # 게임 초기화/시작 함수
    global gamepad, aircraft, clock, background1, background2     # 전역변수로 사용 설정
    global bat, fires, bullet, boom

    fires = []                                                  # 불덩어리 2개와 None 객체 5개를 담을 리스트

    pygame.init()                                               # pygame 라이브러리 초기화 (항상 이 함수를 실행해야 함)
    gamepad = pygame.display.set_mode((pad_width, pad_height))  # 게임판 크기를 설정
    pygame.display.set_caption('PyFlying')                    # 게임판 타이틀 설정
    aircraft = pygame.image.load('images/plane.png')         # 비행기 이미지
    background1 = pygame.image.load('images/background_scale.png') # 백그라운드 이미지
    background2 = background1.copy()
    bat = pygame.image.load('images/bat.png')
    fires.append(pygame.image.load('images/fireball.png'))
    fires.append(pygame.image.load('images/fireball2.png'))
    bullet = pygame.image.load('images/bullet.png')
    boom = pygame.image.load('images/boom.png')

    for i in range(5):
        fires.append(None)

    clock = pygame.time.Clock()                                 # 초당프레임(FPS) 설정을 위해 clock 생성
    # 사람 눈에 가장 자연스럽게 보이는 FPS는 30
    runGame()                                                   # 게임 구동

if __name__ == '__main__':
    initGame()