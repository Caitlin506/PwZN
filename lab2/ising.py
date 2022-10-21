import numpy as np
import rich
import tqdm
from PIL import Image,ImageDraw

n=50
m=40
prob=1-0.5
J=1
beta=1
B=1
steps=10
file_name='step'

class Simulation:
    def __init__(self):
        self.current_state=np.ones((n,m),dtype=int)        
    def initialize(self):
        for i in range(n):
            for j in range(m):
                if np.random.rand()<prob:
                    self.current_state[i][j]=-1
    def hamiltonian(self):
        sum1 = 0
        sum2 = 0
        for i in range(n):
            for j in range(m):
                ui=i+1
                uj=j+1
                li=i-1
                lj=j-1
                if ui==n:
                    ui=0
                if uj==m:
                    uj=0
                if li==-1:
                    li=n-1
                if lj==-1:
                    lj=m-1
                sum1+=self.current_state[i][j]*self.current_state[ui][j]+self.current_state[i][j]*self.current_state[li][j]+self.current_state[i][j]*self.current_state[i][uj]+self.current_state[i][j]*self.current_state[i][lj]
                sum2+=self.current_state[i][j]
        ham=-J*sum1-B*sum2  
        return ham;
    def update(self):
        for i in range(n*m):
            E1=self.hamiltonian()
            drawx=np.random.randint(0,m)
            drawy=np.random.randint(0,n)
            self.current_state[drawy][drawx]=-self.current_state[drawy][drawx]
            E2=self.hamiltonian()
            deltaE=E2-E1
            if deltaE>0:
                probability=np.exp(-beta*deltaE)
                if np.random.rand()>probability:
                    self.current_state[drawy][drawx]=-self.current_state[drawy][drawx]
    def draw_state(self):
        img=Image.new('RGB',(m*10,n*10),(96, 61, 145))
        draw=ImageDraw.Draw(img)
        for i in range(m):
            for j in range(n):
                if self.current_state[j][i]==-1:
                    draw.rectangle((i*10,j*10,i*10+10,j*10+10),(204, 255, 168))
                else:
                    draw.rectangle((i*10,j*10,i*10+10,j*10+10),(96, 61, 145))
        return img
    def simulate(self):
        images = []
        self.initialize()
        images.append(self.draw_state())
        for i in tqdm.tqdm(range(steps)):
            self.update()
            images.append(self.draw_state())
        my_name = file_name+'.gif'
        images[0].save(my_name, save_all=True, append_images=images[1:], optimize=False, duration=20*steps, loop=0)
        
s1=Simulation()
s1.simulate()

