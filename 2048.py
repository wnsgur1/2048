import pygame
import random

# 4x4의 판 생성
board = [[0 for i in range(4)]for j in range(4)]



def board_reset():
    # 보드 초기화
    for i in range(4):
        for j in range(4):
            board[i][j] = 0

# pygame초기화 및 화면 크기 설정
pygame.init()
screen_width = 400
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))

# 게임 타이틀
pygame.display.set_caption("2048")

# 색상 정의
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
BLUE = (0,0,255)



# 타일 색상 매핑
tile_colors = {
    0: GRAY,
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46)
}
# 게임 폰트 설정
font = pygame.font.Font(None,50)

# 총시간
total_time=15
# 시작 시간 정보
strt_ticks=pygame.time.get_ticks()


# 메인화면 글자
def main_text():
    main_text=font.render("2048", True, BLACK)
    # 글자 위치
    main_text_rect = main_text.get_rect(center=(screen_width // 2, screen_height // 4))
    # 게임 오버 글자 출력
    screen.blit(main_text, main_text_rect)


def reset_text():
    reset_text=font.render("RESET(r)", True, BLACK)
    screen.blit(reset_text, (10,10))

# 난이도 선택
def choice_text():
    choice_text=font.render("nonarl(n)   or   hard(h)", True, BLACK)
    speed_text=font.render("speed(s)", True, BLACK)
    # 글자 위치
    choice_text_rect = choice_text.get_rect(center=(screen_width // 2, screen_height // 2))
    speed_text_rect = speed_text.get_rect(center=(screen_width // 2, 350))
    # 게임 오버 글자 출력
    screen.blit(choice_text, choice_text_rect)
    screen.blit(speed_text, speed_text_rect)

# 숫자의 랜덤 좌표 생성
def random_coor():
    none_tiles = []
    for i in range(4):
        for j in range(4):
            if board[i][j] == 0:
                none_tiles.append((i,j))
    if none_tiles:
        i, j=random.choice(none_tiles)
        board[i][j]=random.choice([2,4])

def zero_tile(x,y):
    pygame.draw.rect(screen, GRAY, (x, y, 90, 90))

def tile(x,y,value):
    pygame.draw.rect(screen, tile_colors[value], (x, y, 90, 90))
    if value != 0:
        text = font.render(str(value), True, BLACK)
        text_rect = text.get_rect(center=(x + 45, y + 45))
        screen.blit(text, text_rect)

#판을 그릴 위치 구하는 함수
def darw_tiles():
    for i in range(4):
        for j in range(4):
            value=board[i][j]
            x=j*100+5
            y=i*100+75
            # 만약 판 위치의 값이 0이면
            if value==0:
                # 0의 타일을 그리는 함수 실행
                zero_tile(x,y)
            else:
                tile(x,y,value)

# 위쪽으로 움직이는 함수
def up():
    for j in range(4):
        for i in range(1,4):
            if board[i][j] != 0:
                for k in range(i, 0, -1):
                    if board[k - 1][j] == 0:
                        board[k - 1][j] = board[k][j]
                        board[k][j] = 0
                    elif board[k - 1][j] == board[k][j]:
                        board[k - 1][j] *= 2
                        board[k][j] = 0

# 아래쪽으로 움직이는 함수
def down():
    for j in range(4):
        for i in range(2, -1, -1):
            if board[i][j] != 0:
                for k in range(i, 3):
                    if board[k + 1][j] == 0:
                        board[k + 1][j] = board[k][j]
                        board[k][j] = 0
                    elif board[k + 1][j] == board[k][j]:
                        board[k + 1][j] *= 2
                        board[k][j] = 0

# 왼쪽으로 움직이는 함수
def left():
    for i in range(4):
        for j in range(1, 4):
            if board[i][j] != 0:
                for k in range(j, 0, -1):
                    if board[i][k - 1] == 0:
                        board[i][k - 1] = board[i][k]
                        board[i][k] = 0
                    elif board[i][k - 1] == board[i][k]:
                        board[i][k - 1] *= 2
                        board[i][k] = 0

# 오른쪽으로 움직이는 함수
def right():
    for i in range(4):
        for j in range(1,4):
            if board[i][j] != 0 :
                for k in range(j, -1, -1):
                    if board[i][k-1]==board[i][k]:
                        board[i][k-1]*=2
                        board[i][j]=0
                    elif board[i][k-1]==0:
                        board[i][k-1]=board[i][k]
                        board[i][k]=0

#게임 오버 판단 함수
def jud_game_over():
    for i in range(4):
        for j in range(4):
            if board[i][j]==0:
                return False
            if i > 0 and board[i][j] == board[i - 1][j]:
                return False
            if i < 3 and board[i][j] == board[i + 1][j]:
                return False
            if j > 0 and board[i][j] == board[i][j - 1]:
                return False
            if j < 3 and board[i][j] == board[i][j + 1]:
                return False
    return True

# 시간계산 시간 출력
def time_limit(elapsed_time):
    timer = font.render(str(int(total_time - elapsed_time)), True, BLUE)
    screen.blit(timer, (350,10))

def game_over_print():
    text=font.render("Game Over", True, RED)
    # 글자 위치
    text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2))
    # 게임 오버 글자 출력
    screen.blit(text, text_rect)



def main_screen(screen):
    main_running = True
    board_reset()
    while main_running:
        for event in pygame.event.get():
            # 종료 버튼을 눌렀는가?
            if event.type == pygame.QUIT:
                main_running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_n:
                    nonarl(screen)
                    main_running = False
                elif event.key == pygame.K_s:
                    speed(screen)
                    main_running = False
                elif event.key == pygame.K_h:
                    hard(screen)
                    main_running = False
                   

        screen.fill((255, 255, 255))
        main_text()
        choice_text()
        pygame.display.flip()



def main():
    try:
        main_screen(screen)
    except pygame.error as e:
        print("An error occurred:", str(e))
    finally:
        pygame.quit()




def nonarl(screen):
    # 게임을 계속 지속하는지 판단하는 변수
    running = True
    game_over = False

    # 숫자의 랜덤 좌표 2개 생성
    random_coor()
    random_coor()
    # 게임 실행
    while running:
        # 게임 종료 프로그램
        for event in pygame.event.get():
            # 종료 버튼을 눌렀는가?
            if event.type == pygame.QUIT:
                running = False
            # 키보드를 눌렀는가?
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    main_screen(screen)
                # 게임오버가 False면
                if not game_over:
                    # 누른 버튼이 위쪽 화살표이면
                    if event.key == pygame.K_UP:
                        # 위쪽으로 이동하는 함수 실행
                        up()
                    # 누른 버튼이 아래쪽 화살표이면
                    elif event.key == pygame.K_DOWN:
                        # 아래쪽으로 이동하는 함수 실행
                        down()
                    # 누른 버튼이 왼쪽 화살표이면
                    elif event.key == pygame.K_LEFT:
                        # 왼쪽으로 이동하는 함수 실행
                        left()
                    # 누른 버튼이 오른쪽 화살표이면
                    elif event.key == pygame.K_RIGHT:
                        # 오른쪽으로 이동하는 함수 실행
                        right()
                    # elif event.key == pygame.K_r:
                    #     main_screen()
                    # 만약 움직여도 게임 오버가 아니라면 랜덤 타일 1개 생성
                    # jud_game_over = 게임이 끝나는지 아닌지 판단하는 함수
                    if not jud_game_over():
                        # 랜덤 타일 1개 생성
                        random_coor()       
                    # 게임 오버라면 끝    
                    else:
                        game_over = True
        #배경 화면 색
        screen.fill(WHITE)
        # 리셋 버튼
        reset_text()
        # 판 출력
        darw_tiles()
        if game_over:
            # 게임 오버 글자 출력 함수
            game_over_print()
        # 게임 업데이트
        pygame.display.flip()
    # 게임 창 종료
    pygame.quit()


def hard(screen):
    running = True
    game_over = False
    end=True

    start_ticks = pygame.time.get_ticks()

    # 숫자의 랜덤 좌표 2개 생성
    random_coor()
    random_coor()
    # 게임 실행
    while running:
        # 게임 종료 프로그램
        for event in pygame.event.get():
            # 종료 버튼을 눌렀는가?
            if event.type == pygame.QUIT:
                running = False
            # 키보드를 눌렀는가?
            elif event.type ==  pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    main_screen(screen)
                # 게임오버가 False면
                if not game_over:
                    # 누른 버튼이 위쪽 화살표이면
                    if event.key == pygame.K_UP:
                        # 위쪽으로 이동하는 함수 실행
                        up()
                        start_ticks += 500
                    # 누른 버튼이 아래쪽 화살표이면
                    elif event.key == pygame.K_DOWN:
                        # 아래쪽으로 이동하는 함수 실행
                        down()
                        start_ticks += 500
                    # 누른 버튼이 왼쪽 화살표이면
                    elif event.key == pygame.K_LEFT:
                        # 왼쪽으로 이동하는 함수 실행
                        left()
                        start_ticks += 500
                    # 누른 버튼이 오른쪽 화살표이면
                    elif event.key == pygame.K_RIGHT:
                        # 오른쪽으로 이동하는 함수 실행
                        right()
                        start_ticks += 500
                    # 만약 움직여도 게임 오버가 아니라면 랜덤 타일 1개 생성
                    # jud_game_over = 게임이 끝나는지 아닌지 판단하는 함수
                    if not jud_game_over():
                        # 랜덤 타일 1개 생성
                        random_coor()    
                    # 게임 오버라면 끝    
                    else:
                        game_over = True

        # 배경 화면 색
        screen.fill(WHITE)
        # 리셋 버튼
        reset_text()
        # 판 출력
        darw_tiles()
        if game_over:
            # 게임 오버 글자 출력 함수
            game_over_print()

        elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000
        if elapsed_time >= total_time:
            # 게임 시간 종료 처리
            game_over = True
        else:
            time_limit(elapsed_time)
            
        
        # 게임 업데이트
        pygame.display.flip()
    # 게임 창 종료
    pygame.quit()


def speed(screen):
    running = True
    game_over = False

    start_ticks = pygame.time.get_ticks()

    # 숫자의 랜덤 좌표 2개 생성
    random_coor()
    random_coor()
    # 게임 실행
    while running:
        # 게임 종료 프로그램
        for event in pygame.event.get():
            # 종료 버튼을 눌렀는가?
            if event.type == pygame.QUIT:
                running = False
            # 키보드를 눌렀는가?
            elif event.type ==  pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    main_screen(screen)
                # 게임오버가 False면
                if not game_over:
                    # 누른 버튼이 위쪽 화살표이면
                    if event.key == pygame.K_UP:
                        # 위쪽으로 이동하는 함수 실행
                        up()
                        
                    # 누른 버튼이 아래쪽 화살표이면
                    elif event.key == pygame.K_DOWN:
                        # 아래쪽으로 이동하는 함수 실행
                        down()
                      
                    # 누른 버튼이 왼쪽 화살표이면
                    elif event.key == pygame.K_LEFT:
                        # 왼쪽으로 이동하는 함수 실행
                        left()
                        
                    # 누른 버튼이 오른쪽 화살표이면
                    elif event.key == pygame.K_RIGHT:
                        # 오른쪽으로 이동하는 함수 실행
                        right()
                       
                    # 만약 움직여도 게임 오버가 아니라면 랜덤 타일 1개 생성
                    # jud_game_over = 게임이 끝나는지 아닌지 판단하는 함수
                    if not jud_game_over():
                        # 랜덤 타일 1개 생성
                        random_coor()    
                    # 게임 오버라면 끝    
                    else:
                        game_over = True

        # 배경 화면 색
        screen.fill(WHITE)
        # 리셋 버튼
        reset_text()
        # 판 출력
        darw_tiles()
        if game_over:
            # 게임 오버 글자 출력 함수
            game_over_print()

        elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000
        if elapsed_time >= total_time:
            # 게임 시간 종료 처리
            game_over = True
        else:
            time_limit(elapsed_time)
            
        
        # 게임 업데이트
        pygame.display.flip()
    # 게임 창 종료
    pygame.quit()


if __name__ == "__main__":
    main()