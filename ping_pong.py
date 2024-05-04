from pygame import *
'''Необходимые классы'''
#TODO score counter
#TODO time limit + counter
#TODO win condition
'''A game shall be won by the player first scoring 11 points unless both players score 10 points, 
when the game shall be won by the first player subsequently gaining a lead of 2 points. 
A match shall consist of the best of any odd number of games.
In competition play, matches are typically best of five or seven games.'''

#класс-родитель для спрайтов
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, width, height):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (width, height)) #вместе 55,55 - параметры
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y


    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def update_r(self):
        keys = key.get_pressed()
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.bottom < win_height:
            self.rect.y += self.speed
    def update_l(self):
        keys = key.get_pressed()
        if keys[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.bottom < win_height:
            self.rect.y += self.speed
            


            

class Ball(GameSprite):
    def __init__(self, player_image, player_x, player_y, width, height, setting, speed_x, speed_y):
        super().__init__(player_image, player_x, player_y, setting, width, height)  #!Добавил setting для скорости мяча в будущем
        self.speed_x = speed_x
        self.speed_y = speed_y
    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
    
    def hit(self, paddle):
        if sprite.collide_rect(paddle, self):
            angle = section(paddle, self)
            #print(angle)
            if abs(angle) == 20:
                self.speed_y = 1
                self.speed_x = 3
            elif abs(angle) == 40:
                self.speed_y = 3
                self.speed_x = 3
            elif abs(angle) == 0:
                self.speed_y = 0
                self.speed_x = 4

            if angle < 0:
                self.speed_y *= -1


            #!Делаем нужное направление от(!) ракетки
            if self.rect.x > win_width/2:
                self.speed_x = abs(self.speed_x) * -1
            else:
                self.speed_x = abs(self.speed_x)


#! В какую часть ракетки попал мяч? Считаем угол отскока
def section(paddle, pong):
    height = paddle.rect.bottom - paddle.rect.top
    if pong.rect.centery <= (paddle.rect.y + height * 3/14):
        return -40
    elif pong.rect.centery <= (paddle.rect.y + height * 6.5/14):
        return -20
    elif pong.rect.centery <= (paddle.rect.y + height * 7.5/14):
        return 0
    elif pong.rect.centery <= (paddle.rect.y + height * 11/14):
        return 20
    else:
        return 40
    


#игровая сцена:
back = (200, 255, 255) #цвет фона (background)
win_width = 600
win_height = 500
window = display.set_mode((win_width, win_height))
window.fill(back)


#флаги, отвечающие за состояние игры
game = True
finish = False
clock = time.Clock()
FPS = 60
setting = 1

#создания мяча и ракетки   
racket1 = Player('racket.png', 30, 200, 4, 50, 150) 
racket2 = Player('racket.png', 520, 200, 4, 50, 150)
ball = Ball('tenis_ball.png', 200, 200, 50, 50, setting, 3, 3) #!Тоже настройка скорости


font.init()
font = font.Font(None, 35)
lose1 = font.render('PLAYER 1 LOSE!', True, (180, 0, 0))
lose2 = font.render('PLAYER 2 LOSE!', True, (180, 0, 0))

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
  
    if finish != True:
        window.fill(back)
        racket1.update_l()
        racket2.update_r()
        ball.update()
        ball.hit(racket1)
        ball.hit(racket2)
      
        #если мяч достигает границ экрана, меняем направление его движения
        if ball.rect.y > win_height-50 or ball.rect.y < 0:
            ball.speed_y *= -1


        #если мяч улетел дальше ракетки, выводим условие проигрыша для первого игрока
        if ball.rect.x < 0:
            finish = True
            window.blit(lose1, (200, 200))
            game_over = True


        #если мяч улетел дальше ракетки, выводим условие проигрыша для второго игрока
        if ball.rect.x > win_width:
            finish = True
            window.blit(lose2, (200, 200))
            game_over = True


        racket1.reset()
        racket2.reset()
        ball.reset()


    display.update()
    clock.tick(FPS)


