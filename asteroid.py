import pygame, os, math
from random import random, randint, uniform
WIDTH= 700
HEIGHT = 700
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

BLACK = (0,0,0)
WHITE = (255,255,255)
level_speed = 1
level = 1
clock = pygame.time.Clock()

pygame.font.init()

font = pygame.font.SysFont('sans', 50, bold = True)
class asteroid_class:
    def __init__(self):
        self.x = randint(0, 1)*WIDTH
        self.y = randint(0, 1)*HEIGHT
        self.rotating_angle = 0
        self.rotating_speed = uniform(0,2)
        
        if self.x == 0 and self.y == 0:  
            self.asteroid_angle = uniform(0,90)*math.pi/180
        elif self.x == WIDTH and self.y == 0:
            self.asteroid_angle = uniform(90,180)*math.pi/180
        elif self.x == 0 and self.y ==HEIGHT:
            self.asteroid_angle = uniform(-90,0)*math.pi/180
        elif self.x == WIDTH and self.y ==HEIGHT:
            self.asteroid_angle = uniform(-180,-90)*math.pi/180
        self.itself = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'boulder.png')), (100,100))
        
    def moving(self, level_speed):
        self.x += level_speed*math.cos(self.asteroid_angle)
        self.y += level_speed*math.sin(self.asteroid_angle)
        self.rect = pygame.Rect(self.x, self.y, 100, 100  )
        self.rotating_angle += self.rotating_speed

        w, h = self.itself.get_size()
        box = [pygame.math.Vector2(p) for p in [(0, 0), (w, 0), (w, -h), (0, -h)]]
        box_rotate = [p.rotate(self.rotating_angle) for p in box]
        min_box = (min(box_rotate, key=lambda p: p[0])[0], min(box_rotate, key=lambda p: p[1])[1])
        max_box = (max(box_rotate, key=lambda p: p[0])[0], max(box_rotate, key=lambda p: p[1])[1])
        pivot = pygame.math.Vector2(w/2, -h/2)
        pivot_rotate = pivot.rotate(self.rotating_angle)
        pivot_move   = pivot_rotate - pivot
        origin = (self.x + min_box[0] - pivot_move[0], self.y - max_box[1] + pivot_move[1])
        rotated_image = pygame.transform.rotate(self.itself, self.rotating_angle)
        WIN.blit(rotated_image, origin)

class Bullet:
    def __init__(self,angle,x,y):
        self.angle = angle
        self.speed = 5
        self.x = x
        self.y = y
        
    def shoot(self):
        self.bullet = pygame.draw.rect(WIN, WHITE, (self.x,self.y,7,7))
        self.x -=  self.speed*math.sin(math.pi*self.angle/180)
        self.y -= self.speed*math.cos(math.pi*self.angle/180)
        

def main(level_speed, level):
    SPACE_SHIP = pygame.image.load(os.path.join('Assets', 'spaceShip.png'))
    SPACE_SHIP = pygame.transform.scale(SPACE_SHIP, (50,50))
    
    FPS = 60
    run = True
    ship_x = WIDTH//2
    ship_y = HEIGHT//2
    angle = 0
    ship_vel = 0
    asteroid_list = []
    counter = 0
    bullet_list = []
    score = 0
    Text = font.render(str(score), True, WHITE)
    while run:
        clock.tick(FPS)
       
        WIN.fill(BLACK)
      
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and len(bullet_list) < 3:
                    bullet_list.append(Bullet(angle, origin[0]+25, origin[1]+25))
        
        for asteroid in asteroid_list:
                if asteroid.rect.colliderect(space_ship_rect):
                    Text = font.render("Game over Your score is:" + str(score), True, WHITE) 
                    level = 0

        for bullet in bullet_list:
            bullet.shoot()
            if bullet.x < -5 or bullet.x > WIDTH or bullet.y < - 5 or bullet.y > HEIGHT:
                bullet_list.remove(bullet)
            for asteroid in asteroid_list:
                if bullet.bullet.colliderect(asteroid.rect):
                    asteroid_list.remove(asteroid)
                    if bullet in bullet_list: bullet_list.remove(bullet)
                    score += 10
                    Text = font.render(str(score), True, WHITE)
                    if score >= 100*level:
                        level += 1
                        level_speed += level_speed/2
                       
        if level != 0:
            WIN.blit(Text, (WIDTH//2 - 20, 10))
        else:
            WIN.blit(Text,(10,10))
        


        if level != 0 and counter < 120//level:
            counter +=1
        elif level == 0:
            asteroid_list=[]
        else:
            counter = 0
            asteroid_list.append(asteroid_class())
        
        for asteroid in asteroid_list:
            asteroid.moving(level_speed)
            if asteroid.x < -150 or asteroid.x > WIDTH or asteroid.y < - 150 or asteroid.y > HEIGHT:
                asteroid_list.remove(asteroid)
                
        
        # Handling rotation:
        
        w, h = SPACE_SHIP.get_size()
        box = [pygame.math.Vector2(p) for p in [(0, 0), (w, 0), (w, -h), (0, -h)]]
        box_rotate = [p.rotate(angle) for p in box]
        min_box = (min(box_rotate, key=lambda p: p[0])[0], min(box_rotate, key=lambda p: p[1])[1])
        max_box = (max(box_rotate, key=lambda p: p[0])[0], max(box_rotate, key=lambda p: p[1])[1])
        pivot = pygame.math.Vector2(w/2, -h/2)
        pivot_rotate = pivot.rotate(angle)
        pivot_move   = pivot_rotate - pivot
        origin = (ship_x + min_box[0] - pivot_move[0], ship_y - max_box[1] + pivot_move[1])
        rotated_image = pygame.transform.rotate(SPACE_SHIP, angle)
        WIN.blit(rotated_image, origin)
        
        space_ship_rect =pygame.Rect(ship_x,ship_y, 50,50)


        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_LEFT]:
            angle += 2
        if keys_pressed[pygame.K_RIGHT]:
            angle -= 2

        
        if keys_pressed[pygame.K_UP]:
            if ship_vel < 2.5 or ship_vel< 2.5*level/2:
                ship_vel += 0.1*level/2
        else:
            if ship_vel >= 0:
                ship_vel -= 0.05
            elif ship_vel <= 0: 
                ship_vel = 0
        if (ship_x <=WIDTH-50 and ship_x>= 0) or (ship_x >=WIDTH-50 and ship_vel*math.sin(math.pi*angle/180)>0) or (ship_x<= 0 and ship_vel*math.sin(math.pi*angle/180)<0 ):
            ship_x -= ship_vel*math.sin(math.pi*angle/180)
        if (ship_y <= HEIGHT-50 and ship_y >= 0) or (ship_y >= HEIGHT-50 and ship_vel*math.cos(math.pi*angle/180)>0) or (ship_y <= 0 and ship_vel*math.cos(math.pi*angle/180)<0):
            ship_y -= ship_vel*math.cos(math.pi*angle/180) 

        
        pygame.display.flip()
    pygame.quit

if __name__ == "__main__":
    main(level_speed, level)