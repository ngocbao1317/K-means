import pygame
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import cv2

pygame.init()
screen=pygame.display.set_mode((1200,700))
pygame.display.set_caption('Xu Ly Anh')
running=True
clock = pygame.time.Clock()
BACKGROUND=(214,214,214)
BLACK=(0,0,0)
WHITE=(255,255,255)
BACKGROUND_PANEL=(249,255,230)
font=pygame.font.SysFont('sans',40)
fontsmall=pygame.font.SysFont('sans',20)
text_plus=font.render('+', True, WHITE)
text_min=font.render('-', True, WHITE)
text_run=font.render('Run co dinh', True, WHITE)
text_run2=font.render('Run chuyen dong', True, WHITE)
text_reset=font.render('Reset', True, WHITE)
text_save=font.render('Save Image', True, WHITE)
input_box =pygame.Rect(445,555,100,40)
input_box2 =pygame.Rect(1000,350,100,40)
text=''
tenanh=''
K=0
img_loaded = False
loaded_img = None

while running:
    clock.tick(60)
    screen.fill(BACKGROUND)
    mouse_x, mouse_y=pygame.mouse.get_pos()
    text_k=font.render('K='+str(K),True,BLACK)
    screen.blit(text_k,(1050,50))
    pygame.draw.rect(screen,BLACK,(850,50,50,50))
    screen.blit(text_plus,(860,50))
    pygame.draw.rect(screen,BLACK, (950,50,50,50))
    screen.blit(text_min,(960,50))
    pygame.draw.rect(screen,BLACK,(850,150,300,50))
    screen.blit(text_run,(880,150))
    pygame.draw.rect(screen,BLACK,(850,250,300,50))
    screen.blit(text_run2,(880,250))
    pygame.draw.rect(screen,BLACK,(850,550,150,50))
    screen.blit(text_reset,(850,550))
    pygame.draw.rect(screen,BLACK,(50,50,700,500))
    pygame.draw.rect(screen,BACKGROUND_PANEL,(55,55,690,490))
    pygame.draw.rect(screen,WHITE,input_box,2)
    pygame.draw.rect(screen,WHITE,input_box2,2)
    pygame.draw.rect(screen,BLACK,(850,450,300,50))
    screen.blit(text_save,(850,450))
    text_hinhanh=font.render('Nhap hinh anh:',True,BLACK)
    screen.blit(text_hinhanh,(200,550))
    text_input=font.render(text,True,BLACK)
    screen.blit(text_input,(450,550))
    width=max(200, text_input.get_width()+10)
    input_box.w =width
    
    text_tenanhsave=font.render('Ten anh:',True,BLACK)
    screen.blit(text_tenanhsave,(850,350))
    text_inputten=font.render(tenanh,True,BLACK)
    screen.blit(text_inputten,(1000,350))
    width=max(200, text_inputten.get_width()+10)
    input_box.w =width
    if 50<mouse_x<750 and 50<mouse_y<550:
        text_mouse=fontsmall.render('('+str(mouse_x-50)+','+str(mouse_y-50)+')',True,BLACK)
        screen.blit(text_mouse,(mouse_x+10,mouse_y+10))
    if img_loaded and loaded_img:
        screen.blit(loaded_img,(175,100))
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
        if event.type==pygame.MOUSEBUTTONDOWN:
            if 850<mouse_x<900 and 50<mouse_y<100:
                if K<8:
                    K+=1
            if 950<mouse_x<1000 and 50<mouse_y<100:
                if K>0:
                    K-=1
            if 850<mouse_x<1000 and 150<mouse_y<200:
                img = plt.imread(text)
                width = img.shape[0]
                height = img.shape[1]
                img_flat = img.reshape(width*height,3)
                kmeans = KMeans(n_clusters=K).fit(img_flat)
                labels = kmeans.predict(img_flat)
                clusters = kmeans.cluster_centers_
                img_clustered=clusters[labels].reshape(width,height,3).astype(np.uint8)
                plt.imshow(img_clustered)
                plt.axis('off')
                plt.show()
            if 850<mouse_x<1000 and 450<mouse_y<500: 
                    print("da click luu anh")
                    anh = img_clustered
                    anh = cv2.cvtColor(anh, cv2.COLOR_BGR2RGB)
                    cv2.imwrite(tenanh+'.jpg', anh)
            if 850<mouse_x<1000 and 250<mouse_y<300:
                img = plt.imread(text)
                width = img.shape[0]
                height = img.shape[1]
                img_flat = img.reshape(width*height,3)
                K_max=K
                for K in range(1,K_max+1):
                    kmeans = KMeans(n_clusters=K).fit(img_flat)
                    labels = kmeans.predict(img_flat)
                    clusters = kmeans.cluster_centers_
                    img_clustered = clusters[labels].reshape(width,height,3).astype(np.uint8)
                    plt.imshow(img_clustered)
                    plt.title(f"K = {K}")
                    plt.axis('off')
                    plt.pause(3)
            if 850<mouse_x<1000 and 550<mouse_y<600:
                K = 0
                text= ''
                img_loaded = False
            if 1000<mouse_x<1100 and 350<mouse_y<400:
                    active2 = True
            else:
                    active2 = False
        if event.type == pygame.KEYDOWN:
                    if active2:
                        if event.key == pygame.K_BACKSPACE:
                            tenanh = tenanh[:-1]
                        else:
                            tenanh += event.unicode
        if 450<mouse_x<540 and 560<mouse_y<590:
                active = True
        else:
                active = False
        if event.type == pygame.KEYDOWN:
                if active:
                    if  event.key == pygame.K_RETURN:
                        try:
                            img = pygame.image.load(text).convert()
                            loaded_img = pygame.transform.scale(img,(450,400))
                            img_loaded = True
                        except pygame.error as e:
                            print(f"Error loading img:{e}")
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode
    pygame.display.flip()
pygame.quit()
