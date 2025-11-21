import pygame
import math
import sys
import random

pygame.init()
WIDTH, HEIGHT = 1000, 900
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gravity Simulator")


clock = pygame.time.Clock()
G = 6.674

class Body:
    list_bodies=[]
    def __init__(self, pos, vel, mass, color, radius):
        self.pos = [pos[0], pos[1]]
        self.vel = [vel[0], vel[1]]
        self.acc = [0, 0]
        self.mass = mass
        self.color = color
        self.radius = radius
        
        Body.list_bodies.append(self)
    
    def get_total_force(self):
        list_forces=[]
        sum_of_forces = 0
        av_angle = 0
        av_magnitude = 0

        for object in Body.list_bodies:
            if self is object:
                continue
            
            dy = (self.pos[1] - object.pos[1])
            dx = (self.pos[0] - object.pos[0])
            d = math.hypot(dx, dy)
            gravity_force = (G*(self.mass*object.mass)/d**2)


            #horrible angle calc

            if dx==0: #division with zero
                if dy>0:
                    angle = 3*math.pi/2
                elif dy<0:
                    angle = math.pi/2
            elif dy==0:
                if dx>0:
                   angle = math.pi 
                elif dx<0:
                    angle = 0
            else:                   
                if dx<0 and dy>0:  #quadrant II
                    angle = math.atan(abs(dx/dy))+3*math.pi/2
                elif dx<0 and dy<0: #quadrant III
                    angle = math.atan(abs(dy/dx))
                elif dx>0 and dy<0: #quadrant IV
                    angle = math.atan(abs(dx/dy))+math.pi/2
                else:
                    angle = math.atan(abs(dy/dx))+math.pi  #quadrant I

            list_forces.append([gravity_force, angle])

            av_angle += gravity_force*angle
            sum_of_forces+=gravity_force
        
        if sum_of_forces != 0: av_angle /= sum_of_forces 
        else: av_angle = 0
        
        for sett in list_forces:
            av_magnitude += sett[0]*math.cos(av_angle-sett[1]) # F*cos(av_angle - force_angle)
        
        return (av_magnitude, av_angle)

    def check_collision(self):
        damp = 0.8
        for object in Body.list_bodies:
            if self is object:
                continue
            dy = -(self.pos[1] - object.pos[1])
            dx = (self.pos[0] - object.pos[0])
            distance = math.hypot(dx, dy)

            if distance<object.radius+self.radius:
                if object.mass == self.mass:
                    Body.list_bodies.remove(self)
                    Body.list_bodies.remove(object)
                elif object.mass > self.mass: 
                    Body.list_bodies.remove(self)
                    object.vel[0] = object.vel[0] * damp
                    object.vel[1] = object.vel[1] * damp
                elif object.mass < self.mass: 
                    Body.list_bodies.remove(object)
                    self.vel[0] = self.vel[0] * damp
                    self.vel[1] = self.vel[1] * damp
    
    def check_edges(self):
        damp = 0.6
        if self.pos[0]>=WIDTH: self.vel[0] = -self.vel[0]*damp
        if self.pos[0]<=0: self.vel[0] = -self.vel[0]*damp
        if self.pos[1]>=HEIGHT: self.vel[1] = -self.vel[1]*damp
        if self.pos[1]<=0: self.vel[1] = -self.vel[1]*damp
    
    def change_positions():
        for object in Body.list_bodies:

            g_force = object.get_total_force()
            object.acc[0] = g_force[0]*math.cos(g_force[1])/object.mass
            object.acc[1] = g_force[0]*math.sin(g_force[1])/object.mass
                
            object.vel[0] += object.acc[0]
            object.vel[1] += object.acc[1]

            object.pos[0] += object.vel[0]
            object.pos[1] += object.vel[1]

            object.check_collision()
            #object.check_edges()
    
    def draw_bodies():
        for object in Body.list_bodies:
            pygame.draw.circle(window, object.color, object.pos, object.radius)
    
    def draw_vectors():
        offset = 75
        
        for object in Body.list_bodies:
            fx = object.acc[0]
            fy = object.acc[1]

            #changing scale
            mag = math.hypot(fx, fy)
            compressed_mag = math.sqrt(mag)*offset

            unit_x = fx/mag if mag!=0 else 0
            unit_y = fy/mag if mag!=0 else 0

            scaled_fx = unit_x*compressed_mag
            scaled_fy = unit_y*compressed_mag
            pygame.draw.line(window, (250, 10, 10), object.pos, 
                            (object.pos[0]+scaled_fx, object.pos[1]+scaled_fy), width=2)
    
    def draw_center_mass():
        centerx = 0
        centery = 0
        mass_sum = 0
        for object in Body.list_bodies:
            mass_sum += object.mass
            centerx += object.pos[0] * object.mass
            centery += object.pos[1] * object.mass
        
        if mass_sum != 0:
            centerx /= mass_sum
            centery /= mass_sum
        else:
            centerx, centery = WIDTH/2, HEIGHT/2

        pygame.draw.circle(window, (200, 200, 50), (centerx, centery), radius=3)
    
    def draw_orbit_line():
        for object in Body.list_bodies:
            pygame.draw.circle(orbit_lines, (250, 10, 250), object.pos, radius=1)
        window.blit(orbit_lines, (0, 0))
    
    
black = (0, 0, 0)
white = (255, 255, 255)
blue = (20, 100, 250)
light_blue = (150, 150, 200)
green = (30, 255, 30)
yellow = (250, 200, 10)

gray = (100, 100, 100)
red = (200, 80, 80)



preset = 0 #choose preset (0-2)

if preset==0:
    mass = 500
    distances = [80, 130, 190, 320, 400]
    orbit_vel = []
    for d in distances:
        orbit_vel.append(math.sqrt(G*mass/d))

    sun = Body((500, 450), (0, 0), mass, white, radius=10)
    mercury = Body((500-distances[0], 450), (0, -orbit_vel[0]), 0.01, gray, radius=8)
    earth = Body((500-distances[1], 450), (0, -orbit_vel[1]), 0.01, green, radius=10)
    mars = Body((500-distances[2], 450), (0, -orbit_vel[2]), 0.01, red, radius=6)
    uranus = Body((500-distances[3], 450), (0, -orbit_vel[3]), 0.01, light_blue, radius=12)
    neptune = Body((500-distances[4], 450), (0, -orbit_vel[4]), 0.01, blue, radius=18)
    comet = Body((800, 800), (-1, 0), 0.001, light_blue, radius=6)

if preset==1:
    rigel_kentaurus = Body((400, 450), (0, -1.2), 100, white, radius=8)
    toliman = Body((600, 450), (0, +1.2), 100, yellow, radius=8)
    proxima = Body((250, 450), (0, -2.0), 0.01, red, radius=5)
    proxima2 = Body((750, 450), (+1, +2.1), 0.01, red, radius=5)

if preset==2:
    black_hole = Body((500, 450), (0, 0), 100, black, radius=25)
    for i in range(100):
        photon = Body((i*WIDTH/95, 0), (0, 1), 0.001, white, radius=1)


orbit_lines = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
orbit_lines.fill((0, 0, 0, 0))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    window.fill((10, 10, 10))
    Body.draw_orbit_line()
    Body.change_positions()
    Body.draw_bodies()
    Body.draw_vectors()
    Body.draw_center_mass()


    pygame.display.flip()
    

    clock.tick(60)