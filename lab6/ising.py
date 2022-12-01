import numpy as np
from rich.progress import track
from PIL import Image,ImageDraw
import argparse
import numba
import time

parser = argparse.ArgumentParser()
parser.add_argument("n",type=int,help="Creates a nxn size lattice")
parser.add_argument("J",type=float,help="Interaction: J>0 ferromagnetic, J<0 antiferromagnetic, J=0 noninteracting")
parser.add_argument("beta",type=float,help="Parameter")
parser.add_argument("B",type=float,help="External magnetic field")
parser.add_argument("steps",type=int,help="Number of steps in the simulation")
parser.add_argument('-p','--positive', type=float, default=0.5, help='Percentage of positive spins, default=0.5')
parser.add_argument('-a', '--animation', help="Creates a gif and saves it under the provided name")
parser.add_argument('-s', '--save_pictures', help="Creates a picture for every step and saves them under the provided name")
parser.add_argument('-m', '--magnetization', help="Creates file with magnetization valued and saves it under the provided name")
args = parser.parse_args()
n=args.n
J=args.J
beta=args.beta
B=args.B
steps=args.steps
prob=1-args.positive

file_name='step'

@numba.njit(numba.int64[:,:](numba.int64[:,:]))
def initialize(current_state):
    for i in range(n):
        for j in range(n):
            if np.random.rand()<prob:
                current_state[i][j]=-1
    return current_state
@numba.njit               
def magnetization(iter,current_state):
    spinsum = 0
    for i in range(n):
        for j in range(n):
            spinsum+=current_state[i][j]
    magn = 1/(n*n)*spinsum
    return magn,iter

@numba.njit
def hamiltonian(current_state):
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
            sum1+=current_state[i][j]*current_state[ui][j]+current_state[i][j]*current_state[li][j]+current_state[i][j]*current_state[i][uj]+current_state[i][j]*current_state[i][lj]
            sum2+=current_state[i][j]
    ham=-J*sum1-B*sum2  
    return ham;

@numba.njit
def update(current_state):
    for i in range(n*n):
        E1=hamiltonian(current_state)
        drawx=np.random.randint(0,n)
        drawy=np.random.randint(0,n)
        current_state[drawy][drawx]=-current_state[drawy][drawx]
        E2=hamiltonian(current_state)
        deltaE=E2-E1
        if deltaE>0:
            probability=np.exp(-beta*deltaE)
            if np.random.rand()>probability:
                current_state[drawy][drawx]=-current_state[drawy][drawx]
    return current_state
                
def draw_state(iter,current_state):
    img=Image.new('RGB',(n*10,n*10),(96, 61, 145))
    draw=ImageDraw.Draw(img)
    for i in range(n):
        for j in range(n):
            if current_state[j][i]==-1:
                draw.rectangle((i*10,j*10,i*10+10,j*10+10),(204, 255, 168))
            else:
                draw.rectangle((i*10,j*10,i*10+10,j*10+10),(96, 61, 145))
    if(args.save_pictures):
        my_name = args.save_pictures+str(iter)+'.png'
        img.save(my_name)
    return img

def simulate():
    zero_state = np.ones((n,n),dtype=int)
    images = []
    magnet = []
    current_state = initialize(zero_state)
    images.append(draw_state(0,current_state))
    magnet.append(magnetization(0,current_state))
    for i in track(range(steps),description="Processing..."):
        current_state=update(current_state)
        images.append(draw_state(i+1,current_state))
        magnet.append(magnetization(i+1,current_state))
    if(args.animation):
        images[0].save(args.animation+'.gif', save_all=True, append_images=images[1:], optimize=False, duration=20*steps, loop=0)
    if (args.magnetization):
        with open(args.magnetization+'.txt', 'w') as f:
            f.write('n \t magnetization \n')
            for m in magnet:
                f.write(str(m[1])+'\t'+str(m[0])+'\n')
start = time.time()     
simulate()
stop = time.time()
print("Time = ",stop-start)