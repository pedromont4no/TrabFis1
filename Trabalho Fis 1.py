#Pedro de Almeida Montano - 2658895

import pygame
import sys
import random
import math

# Inicialização do pygame
pygame.init()

# Definição de cores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Configurações da janela
WINDOW_SIZE = (1100, 900)
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption('Trabalho Fis 1')

# Classe para representar as bolas
class Ball:
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = radius  #Para a massa proporcional ao raio
        self.speed_x = random.randint(-5, 5)
        self.speed_y = random.randint(-5, 5)

    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y
        
        # Verifica se a bola atingiu as bordas da janela
        if self.x <= self.radius or self.x >= WINDOW_SIZE[0] - self.radius:
            self.speed_x = -self.speed_x
        if self.y <= self.radius or self.y >= WINDOW_SIZE[1] - self.radius:
            self.speed_y = -self.speed_y

    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

    def check_collision(self, other_ball):
        distance = math.sqrt((self.x - other_ball.x)**2 + (self.y - other_ball.y)**2)
        if distance <= self.radius + other_ball.radius:
            return True
        return False

    def collide(self, other_ball): 
        cv=1 #Coeficiente de restituição

        # Calcula a velocidade do centro de massa
        vcm_x = (self.mass * self.speed_x + other_ball.mass * other_ball.speed_x) / (self.mass + other_ball.mass)
        vcm_y = (self.mass * self.speed_y + other_ball.mass * other_ball.speed_y) / (self.mass + other_ball.mass)
        
        # Aplica a fórmula para as velocidades finais
        self.speed_x = (1+cv) * vcm_x - self.speed_x
        self.speed_y = (1+cv) * vcm_y - self.speed_y
        other_ball.speed_x = 2 * vcm_x - other_ball.speed_x
        other_ball.speed_y = 2 * vcm_y - other_ball.speed_y

def check_overlap(new_x, new_y, new_radius, existing_balls):
    for ball in existing_balls:
        distance = math.sqrt((new_x - ball.x)**2 + (new_y - ball.y)**2)
        if distance < new_radius + ball.radius:
            return True
    return False

def generate_ball(existing_balls):
    radius = random.randint(20, 40)
    while True:
        x = random.randint(radius, WINDOW_SIZE[0] - radius)
        y = random.randint(radius, WINDOW_SIZE[1] - radius)
        if not check_overlap(x, y, radius, existing_balls):
            break
    color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    return Ball(x, y, radius, color)

def main(num_balls):
    # Lista para armazenar as bolas
    balls = []

    # Criando bolas
    for _ in range(num_balls):
        ball = generate_ball(balls)
        balls.append(ball)

    # Loop principal do jogo
    while True:
        screen.fill(BLACK)
        check_events()

        # Movimento e desenho das bolas
        for ball in balls:
            ball.move()
            ball.draw()

        # Detecção e resolução de colisões
        for i in range(len(balls)):
            for j in range(i + 1, len(balls)):
                if balls[i].check_collision(balls[j]):
                    balls[i].collide(balls[j])

        pygame.display.flip()
        pygame.time.Clock().tick(30)

def check_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

if __name__ == '__main__':
    num_balls = int(input("Digite o número de bolas que deseja simular: "))
    main(num_balls)