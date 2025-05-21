import pygame
from random import randint
from sklearn.cluster import KMeans
import math
import numpy as np 
import matplotlib.pyplot as plt

def distance(p1,p2): 
    return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)
pygame.init()
screen=pygame.display.set_mode((1250,700))
pygame.display.set_caption('KMean Visualition')
running=True
clock =pygame.time.Clock()
BACKGROUND=(214,214,214)
BLACK=(0,0,0)
WHITE=(255,255,255)
BACKGROUND_PANEL=(249,255,230)
RED=(255,0,0)
GREEN=(0,255,0)
BLUE=(0,0,255)
YELLOW=(147,153,35)
SKY=(0,255,255)
ORGANCE=(255,125,25)
GRAPE=(100,155,65)
GRASS=(55,155,65)
COLORS=[RED,GREEN, BLUE, YELLOW, SKY, ORGANCE, GRAPE, GRASS]
font=pygame.font.SysFont('sans',40)
fontsmall=pygame.font.SysFont('sans',20)
text_plus=font.render('+', True, WHITE)
text_minus=font.render('-', True, WHITE)
text_run=font.render('Run', True, WHITE)
text_random=font.render('Random', True, WHITE)
text_algorithm=font.render('Algorithm', True, WHITE)
text_reset=font.render('Reset', True, WHITE)
text_elbow = font.render("Elbow", True, WHITE)
K=0
error=0
points=[]
clusters=[]
labels=[]

while running:
    clock.tick(60)
    screen.fill(BACKGROUND)
    mouse_x, mouse_y=pygame.mouse.get_pos()
    pygame.draw.rect(screen, BLACK, (50,50,700,500))
    pygame.draw.rect(screen, BACKGROUND_PANEL, (55,55,690,490))
    pygame.draw.rect(screen, BLACK, (850,50,50,50))
    screen.blit(text_plus, (860,50))
    pygame.draw.rect(screen, BLACK, (950,50,50,50))
    screen.blit(text_minus, (960,50))
    text_k= font.render('K=' +str(K), True, BLACK)
    screen.blit(text_k, (1050,50))
    pygame.draw.rect(screen, BLACK, (850,150,150,50))
    screen.blit(text_run, (900,150))
    pygame.draw.rect(screen, BLACK, (850,250,150,50))
    screen.blit(text_random, (850,250))
    pygame.draw.rect(screen, BLACK, (850,350,150,50))
    screen.blit(text_algorithm, (850,350))
    pygame.draw.rect(screen, BLACK, (850, 450, 150, 50))
    screen.blit(text_elbow, (850, 450))
    pygame.draw.rect(screen, BLACK, (850,550,150,50))
    screen.blit(text_reset, (850,550))

    if 50<mouse_x <750 and 50<mouse_y<550:
        text_mouse=fontsmall.render('(' +str(mouse_x-50)+','+ str(mouse_y-50)+ ')',True, BLACK)
        screen.blit(text_mouse, (mouse_x+10,mouse_y))
    mouse_x, mouse_y=pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
        if event.type==pygame.MOUSEBUTTONDOWN:
            
            if 50<mouse_x<750 and 50<mouse_y<550:
                labels=[]
                point=[mouse_x-50, mouse_y-50]
                points.append(point)
            if 850<mouse_x< 900 and 50<mouse_y<100:
                if K<8:             
                    K+=1
            if 950<mouse_x<1000 and 50<mouse_y<100:
                if K>0:
                    K-=1
            if 850<mouse_x< 1000 and 150<mouse_y<200:
                labels=[]
                if clusters==[]:
                    continue
                for p in points:
                    distances_to_cluster=[]
                    for c in clusters:
                        dis=distance(p,c)
                        distances_to_cluster.append(dis)
                    min_distance=min(distances_to_cluster)
                    label=distances_to_cluster.index(min_distance)
                    labels.append(label)
                for i in range(K):
                    sum_x=0
                    sum_y=0
                    count=0
                    for j in range(len(points)):
                        if labels[j]==i:
                            sum_x+=points[j][0]
                            sum_y+=points[j][1]
                            count+=1
                    if count!=0:
                        new_cluster_x=sum_x/count
                        new_cluster_y=sum_y/count
                        clusters[i]=(new_cluster_x,new_cluster_y)
            if 850<mouse_x< 1000 and 250<mouse_y<300:
                labels=[]
                clusters=[]
                for i in range(K):
                    random_point=[randint(0,700), randint(0,500)]
                    clusters.append(random_point)                                  
            if 850<mouse_x< 1000 and 350<mouse_y<400:
                kmeans=KMeans(n_clusters=K).fit(points)
                labels=kmeans.predict(points).tolist()
                clusters=kmeans.cluster_centers_.tolist()
            if 850 < mouse_x < 1000 and 450 < mouse_y < 500:
                Min,Pos = 10**18,0
                X = np.array(points)
                inertias = []
                for k in range(1,9):
                    kmeanModel = KMeans(n_clusters=k).fit(X)
                    kmeanModel.fit(X)
                    inertias.append(kmeanModel.inertia_)
                    if k*kmeanModel.inertia_ < Min:
                        Min = k*kmeanModel.inertia_
                        Pos = k
                K = Pos
                plt.plot(range(1,9), inertias, 'bx-')
                plt.xlabel('Values of K')
                plt.ylabel('Inertias')
                plt.title('Elbow Method')
                plt.show()  
            if 850<mouse_x< 1000 and 550<mouse_y<600:
                K=0
                points=[]
                labels=[]
                clusters=[]
                error=0  
    for i in range(len(clusters)):
        pygame.draw.circle(screen, COLORS[i], (int(clusters[i][0])+50, int(clusters[i][1])+50),10)
    for i in range(len(points)):
        pygame.draw.circle(screen, BLACK, (points[i][0]+50, points[i][1]+50), 6)
        if labels==[]:
            pygame.draw.circle(screen, WHITE, (points[i][0]+50, points[i][1]+50), 5)
        else: 
            pygame.draw.circle(screen, COLORS[labels[i]], (points[i][0]+50, points[i][1]+50), 5)       
    error=0
    if clusters!=[] and labels!=[]:
        for i in range(len(points)):
            error+=distance(points[i], clusters[labels[i]])
    text_error=font.render('Error =' +str(int(error)), True, BLACK)
    screen.blit(text_error,(1050, 150))
    pygame.display.flip()
pygame.quit()


                           
                        
                           
