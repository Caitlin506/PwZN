import numpy as np
from rich.progress import track
from PIL import Image,ImageDraw
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("n",type=int,help="Creates a nxn size lattice")
parser.add_argument("J",type=float,help="Interaction: J>0 ferromagnetic, J<0 antiferromagnetic, J=0 noninteracting")
parser.add_argument("beta",type=float,help="Parameter")
parser.add_argument("B",type=float,help="External magnetic field")
parser.add_argument("steps",type=int,help="Number of steps in the simulation")
parser.add_argument('-p','--positive', type=float, default=0.5, help='Percentage of positive spins, default=0.5')
args = parser.parse_args()
n=args.n
J=args.J
beta=args.beta
B=args.B
steps=args.steps
prob=1-args.positive

file_name='step'

class Simulation:
    def __init__(self):
        self.current_state=np.ones((n,n),dtype=int)        
    def initialize(self):
        for i in range(n):
            for j in range(n):
                if np.random.rand()<prob:
                    self.current_state[i][j]=-1
    def magnetization(self,iter):
        spinsum = 0
        for i in range(n):
            for j in range(n):
                spinsum+=self.current_state[i][j]
        magn = 1/(n*n)*spinsum
        print(magn,iter)
        return magn
    def hamiltonian(self):
        sum1 = 0
        sum2 = 0
        for i in range(n):
            for j in range(n):
                ui=i+1
                uj=j+1
                li=i-1
                lj=j-1
                if ui==n:
                    ui=0
                if uj==n:
                    uj=0
                if li==-1:
                    li=n-1
                if lj==-1:
                    lj=n-1
                sum1+=self.current_state[i][j]*self.current_state[ui][j] + self.current_state[i][j]*self.current_state[li][j] + self.current_state[i][j]*self.current_state[i][uj] + self.current_state[i][j]*self.current_state[i][lj]
                sum2+=self.current_state[i][j]
        ham=-J*sum1-B*sum2  
        return ham;
    def update(self):
        for i in range(n*n):
            E1=self.hamiltonian()
            drawx=np.random.randint(0,n)
            drawy=np.random.randint(0,n)
            self.current_state[drawy][drawx]=-self.current_state[drawy][drawx]
            E2=self.hamiltonian()
            deltaE=E2-E1
            if deltaE>0:
                probability=np.exp(-beta*deltaE)
                if np.random.rand()>probability:
                    self.current_state[drawy][drawx]=-self.current_state[drawy][drawx]
    def draw_state(self,iter):
        img=Image.new('RGB',(n*10,n*10),(96, 61, 145))
        draw=ImageDraw.Draw(img)
        for i in range(n):
            for j in range(n):
                if self.current_state[j][i]==-1:
                    draw.rectangle((i*10,j*10,i*10+10,j*10+10),(204, 255, 168))
                else:
                    draw.rectangle((i*10,j*10,i*10+10,j*10+10),(96, 61, 145))
        my_name = file_name+str(iter)+'.png'
        img.save(my_name)
        return img
    def simulate(self):
        images = []
        self.initialize()
        images.append(self.draw_state(0))
        self.magnetization(0)
        for i in track(range(steps),description="Processing..."):
            self.update()
            images.append(self.draw_state(i+1))
            self.magnetization(i+1)
        my_name = file_name+'.gif'
        images[0].save(my_name, save_all=True, append_images=images[1:], optimize=False, duration=20*steps, loop=0)
        
s1=Simulation()
s1.simulate()