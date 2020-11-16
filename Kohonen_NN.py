import itertools as it
import numpy as np
import matplotlib.pyplot as plt
import pygame
import matplotlib.backends.backend_agg as agg
import pylab


class Kohonen_SOM(object):

    def __init__(self, x, y, num_dim):

        self.SOM_shape = (x, y, num_dim)
        self.som = np.zeros((x, y, num_dim))

        self.Lr_0 = float(0)
        self.lambda_const = float(0)
        self.radius_0 = float(0)

        self.data = []

        self.hit_score = np.zeros((x, y))

    def fit(self, data, Lr_0, lambda_const, radius_0, initialize_SOM = np.random.rand, frames=None):

        self.Lr_0 = Lr_0
        self.lambda_const = lambda_const
        self.radius_0 = radius_0

        self.som = initialize_SOM(*self.SOM_shape)
        self.data = data

        for t in it.count(start=0, step=1):

            if frames != None:
                frames.append(self.som.copy())

            if self.radius_define(t) < 0.5:
                print("Training Time:", t)
                break

            i_data = np.random.choice(range(len(data)))

            winner_n = self.find_winner(data[i_data])
            self.hit_score[winner_n] += 1

            self.actualize_nn(winner_n, data[i_data], t)

    def find_winner(self, inp):

        list_winner_n = []
        for y in range(self.SOM_shape[0]):
            for x in range(self.SOM_shape[1]):
                distance = np.linalg.norm((inp - self.som[y, x]))
                list_winner_n.append(((y, x), distance))
        list_winner_n.sort(key=lambda x: x[1])
        return list_winner_n[0][0]

    def neighbor_fun(self, distance_to_winner_n, time):

        radius_factor = self.radius_0 * np.exp(-time / self.lambda_const)
        return np.exp(-(distance_to_winner_n ** 2) / (2 * radius_factor ** 2))

    def cluster_update(self, cluster, distance_to_winner_n, inp, time):

        self.som[cluster] += self.neighbor_fun(distance_to_winner_n, time) * self.update_lr(time) * (
                    inp - self.som[cluster])

    def actualize_nn(self, winner_n, inp, time):

        for y in range(self.SOM_shape[0]):
            for x in range(self.SOM_shape[1]):
                distance_to_winner_n = np.linalg.norm((np.array(winner_n) - np.array((y, x))))
                self.cluster_update((y, x), distance_to_winner_n, inp, time)

    def diff_winner(self, winner_n, inp, time):

        self.som[winner_n] = self.som[winner_n] + self.update_lr(time) * (inp - self.som[winner_n])

    def update_lr(self, time):

        return self.Lr_0 * np.exp(-time / self.lambda_const)

    def radius_define(self, time):

        return self.radius_0 * np.exp(-time / self.lambda_const)


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((500, 800))
    done = True
    buton = [0, 0, 0, 0, 0, 0, 0, 0]
    color_data = []
    end = 0

    while done:
            for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                            done = False
            myFont = pygame.font.SysFont("Arial", 40)
            pygame.display.set_caption("Kohonen")
            screen.fill((50, 80, 80))
            bg = pygame.image.load("back.jpg")
            screen.blit(bg, (0, 0))
            # pygame.draw.rect(screen, (250,255,255),(0,600,500,3))

            if buton[0]==1:
                pygame.draw.rect(screen, (250,255,255),(98,48,104,104))
            if buton[1]==1:
                pygame.draw.rect(screen, (255,255,255),(298,48,104,104))
            if buton[2]==1:
                pygame.draw.rect(screen, (255,255,255),(98,198,104,104))
            if buton[3]==1:
                pygame.draw.rect(screen, (255,255,255),(298,198,104,104))
            if buton[4]==1:
                pygame.draw.rect(screen, (255,255,255),(98,348,104,104))
            if buton[5]==1:
                pygame.draw.rect(screen, (255,255,255),(298,348,104,104))
            if buton[6]==1:
                pygame.draw.rect(screen, (255,255,255),(98,498,104,104))
            if buton[7]==1:
                pygame.draw.rect(screen, (255,255,255),(298,498,104,104))
            pygame.draw.rect(screen, (250,0,0),(100,50,100,100))
            pygame.draw.rect(screen, (250,150,0),(300,50,100,100))
            pygame.draw.rect(screen, (250,250,0),(100,200,100,100))
            pygame.draw.rect(screen, (0,200,0),(300,200,100,100))
            pygame.draw.rect(screen, (0,200,250),(100,350,100,100))
            pygame.draw.rect(screen, (0,0,200),(300,350,100,100))
            pygame.draw.rect(screen, (150,30,200),(100,500,100,100))
            pygame.draw.rect(screen, (0,0,0),(300,500,100,100))
            # pygame.draw.rect(screen, (250,250,250),(150,690,300,70))
            # pygame.draw.rect(screen, (250,250,250),(275,650,150,100))
            # textsurface = myFont.render('Submit', False, (0, 0, 0))
            # screen.blit(textsurface,(285,675))
            mouse = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()
            # textsurface = myFont.render('Vyber max. 3 farby', False, (250, 250, 250))
            # screen.blit(textsurface,(100,5))
            if 95 > mouse[0] > 25 and 760 > mouse[1] > 690:
                        if click[0]==1:
                            buton = [0,0,0,0,0,0,0,0]
                            color_data=[]
            if 450 > mouse[0] > 150 and 760 > mouse[1] > 690:
                        if click[0]==1:
                            bg = pygame.image.load("sprac.jpg")
                            screen.blit(bg, (0, 0))
                            # sprite_image = pygame.image.load("g.gif").convert_alpha()
                            done = False
            if buton.count(1) !=3:
                if buton[0] == 0:
                    if 200 > mouse[0] > 100 and 150 > mouse[1] > 50:
                        if click[0]==1:
                            pygame.draw.rect(screen, (250,255,255),(98,48,104,104))
                            pygame.draw.rect(screen, (255,0,0),(100,50,100,100))
                            buton[0] = 1
                            color_data.append([0.99899629 ,0.10718603, 0.00290041])
                if buton[1] == 0:
                    if 400 > mouse[0] > 300 and 150 > mouse[1] > 50:
                        if click[0]==1:
                            pygame.draw.rect(screen, (255,255,255),(298,48,104,104))
                            pygame.draw.rect(screen, (250,150,0),(300,50,100,100))
                            buton[1] = 1
                            color_data.append([0.92283725, 0.40987178, 0.05836382])
                if buton[2] == 0:
                    if 200 > mouse[0] > 100 and 300 > mouse[1] > 200:
                        if click[0]==1:
                            pygame.draw.rect(screen, (255,255,255),(98,198,104,104))
                            pygame.draw.rect(screen, (250,250,0),(100,200,100,100))
                            buton[2] = 1
                            color_data.append([0.92417364 ,0.93291849, 0.34483919])

                if buton[3] == 0:
                    if 400 > mouse[0] > 300 and 300 > mouse[1] > 200:
                        if click[0]==1:
                            pygame.draw.rect(screen, (255,255,255),(298,198,104,104))
                            pygame.draw.rect(screen, (0,200,0),(300,200,100,100))
                            buton[3] = 1
                            color_data.append([0.02984492 ,0.78458051, 0.21597978])
                if buton[4] == 0:
                    if 200 > mouse[0] > 100 and 450 > mouse[1] > 350:
                        if click[0]==1:
                            pygame.draw.rect(screen, (255,255,255),(98,348,104,104))
                            pygame.draw.rect(screen, (0,200,250),(100,350,100,100))
                            buton[4] = 1
                            color_data.append([0.41085355, 0.61391669, 0.97319804])
                if buton[5] == 0:
                    if 400 > mouse[0] > 300 and 450 > mouse[1] > 350:
                        if click[0]==1:
                            pygame.draw.rect(screen, (255,255,255),(298,348,104,104))
                            pygame.draw.rect(screen, (0,0,200),(300,350,100,100))
                            buton[5] = 1
                            color_data.append([0.06323093 ,0.02068764 ,0.472268  ])
                if buton[6] == 0:
                    if 200 > mouse[0] > 100 and 600 > mouse[1] > 500:
                        if click[0]==1:
                            pygame.draw.rect(screen, (255,255,255),(98,498,104,104))
                            pygame.draw.rect(screen, (150,30,200),(100,500,100,100))
                            buton[6] = 1
                            color_data.append([0.27294468, 0.12497859, 0.27580946])
                if buton[7] == 0:
                    if 400 > mouse[0] > 300 and 600 > mouse[1] > 500:
                        if click[0]==1:
                            pygame.draw.rect(screen, (255,255,255),(298,498,104,104))
                            pygame.draw.rect(screen, (0,0,0),(300,500,100,100))
                            buton[7] = 1
                            color_data.append([0.0102025566,0.02256625,0.01658860])

            pygame.display.flip()


    # if buton.count(1) !=0:
    #     som_color = SOM(40,40,3)
    #     frames_color = []
    #     som_color.train(color_data,L0=0.8,lam=1e2,sigma0=20,frames=frames_color)
    #     plt.figure(figsize=(5,5))
    #     plt.imshow(frames_color[-1])
    #     plt.show()
    #     pass
    # color_data = np.random.rand(3,3)
    # print(color_data)
    # plt.figure(figsize=(10,8))
    # for (i,d) in enumerate(color_data):
    #     plt.subplot(1,3,i+1)
    #     plt.imshow([[d]])
    # plt.show()

    pygame.init()
    myFont = pygame.font.SysFont("Arial", 50)

    som_color = Kohonen_SOM(40, 40, 3)
    frames_color = []
    som_color.fit(color_data, Lr_0=0.8, lambda_const=1e2, radius_0=20, frames=frames_color)
    plt.figure(figsize=(10, 10))
    plt.imshow(frames_color[-1])
    fig = pylab.figure(figsize=[5, 5], dpi=100,        )
    ax = fig.gca()
    ax.imshow(frames_color[-1])

    canvas = agg.FigureCanvasAgg(fig)
    canvas.draw()
    renderer = canvas.get_renderer()
    raw_data = renderer.tostring_rgb()

    screen = pygame.display.set_mode((500, 600))

    size = canvas.get_width_height()

    surf = pygame.image.fromstring(raw_data, size, "RGB")
    screen.blit(surf, (0, 100))
    pygame.draw.rect(screen, (255, 255, 255), (0, 0, 500, 100))
    textsurface = myFont.render('Kohonen Clustering', False, (0, 0, 0))
    screen.blit(textsurface, (64, 25))

    pygame.display.flip()

    crashed = False
    while not crashed:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                crashed = True
