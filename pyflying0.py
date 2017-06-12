import pygame       # pygame 라이브러리 import

WHITE = (255, 255, 255)     # 흰색
pad_width = 1024            # 게임판 폭
pad_height = 512            # 게임판 높이
background_width = 1024     # 배경화면 폭

def back(background, x,y):                                      # 배경이미지 그리는 함수
    global gamepad
    gamepad.blit(background, (x,y))

def airplane(x,y):                                  # 비행기 그리는 함수
    global gamepad, aircraft
    gamepad.blit(aircraft, (x,y))

def runGame():
    # 실제 게임이 구동되는 함수
    global gamepad, aircraft, clock, background1, background2     # 전역변수로 사용 설정

    x = pad_width * 0.05                             # 초기 비행기 위치 x
    y = pad_height * 0.8                             # 초기 비행기 위치 y
    y_change = 0                                     # y축 이동 변수

    background1_x = 0                                # 배경이미지의 좌상단 모서리의 x 좌표
    background2_x = background_width                 # 다음 배경이미지 x좌표는 오른쪽에 붙여서

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
            if event.type == pygame.KEYUP:          # 키가 떼어졌다면
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN: # 위아래 방향키이면
                        y_change = 0                # 이동을 멈춤

        y += y_change                               # y좌표 값을 갱신

        gamepad.fill(WHITE)                         # 게임판을 흰색으로 채우고

        background1_x -= 2
        background2_x -= 2

        if background1_x == -background_width:
            background1_x = background_width

        if background2_x == -background_width:
            background2_x = background_width

        back(background1, background1_x, 0)                       # 배경화면의 위치 초기에는 (0,0)
        back(background2, background2_x, 0)

        airplane(x,y)                               # 비행기 그리기
        pygame.display.update()                     # 게임판을 다시 그림
        clock.tick(60)                              # FPS를 60으로 설정

    pygame.quit()                                   # 초기화한 pygame 종료
    quit()

def initGame():
    # 게임 초기화/시작 함수
    global gamepad, aircraft, clock, background1, background2     # 전역변수로 사용 설정

    pygame.init()                                               # pygame 라이브러리 초기화 (항상 이 함수를 실행해야 함)
    gamepad = pygame.display.set_mode((pad_width, pad_height))  # 게임판 크기를 설정
    pygame.display.set_caption('PyFlying')                    # 게임판 타이틀 설정
    aircraft = pygame.image.load('images/plane.png')         # 비행기 이미지
    background1 = pygame.image.load('images/background_scale.png') # 백그라운드 이미지
    background2 = background1.copy()

    clock = pygame.time.Clock()                                 # 초당프레임(FPS) 설정을 위해 clock 생성
    # 사람 눈에 가장 자연스럽게 보이는 FPS는 30
    runGame()                                                   # 게임 구동

if __name__ == '__main__':
    initGame()