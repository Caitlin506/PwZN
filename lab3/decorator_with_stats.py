import time
import functools
import numpy as np

def my_decorator(stats = False):
    times = []
    def decorator(func):
        def wrapper(*args, **kwargs):
            start = time.time()
            value = func(*args,**kwargs)
            stop = time.time()
            times.append(stop-start)
            if stats == True:
                suma = 0
                for t in times:
                    suma+=t
                mean = suma/len(times)
                print("Mean: ",mean)
                print("Minumum: ",min(times))
                print("Maximum: ",max(times))
                print("Standard deviation: ",np.std(times))
            return value
        
        return wrapper

    return decorator


@my_decorator(True)
def useless(n):
    for i in range(1000000):
        if i%3==2:
            n=n*-0.5**9
        if i%5==0:
            n=n+n/100**3
        for i in range(5):
            n+=1
    return n
        

print(useless(1))
print(useless(-20))
print(useless(35))
print(useless(-2000))
print(useless(350))


