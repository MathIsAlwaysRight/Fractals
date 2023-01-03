import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import hsv_to_rgb 
import os 
import glob
import shutil
import imageio

#Class for generating
class Fractal:
    def __init__(self, function, maxIter=100, borderRad=10):
        #function is a function of the fractal example: lambda z,c = z**2 + c
        self.function = function
        #maxIter maximum iterations of the function
        self.maxIter = maxIter
        #borderRad If number crosses the border, it's considered as diverging
        self.borderRad = borderRad
    
    def ConvergenceCheck(self, num):
        #Returns "C" if num converges, else returns 0-1 based on how quickly it diverged, where 0 is fastest
        val = num
        for i in range(self.maxIter):
            val = self.function(val,num)
            if abs(val) > self.borderRad:
                return i/(self.maxIter-1)
        return "C"
    
    def drawImage(self, size=[600,600], xRange=[-3,3], yRange=[-3,3], figSize=[7,7], hsvMap=[0,1,lambda iter: iter], hsvCvg=[0,0,0], axes=False):
        #Draws image of fractal
        
        #Size is 2 digit array that indicates X and Y resolution of the picture
        #xRange and yRange are 2 digit arrays, they are borders of the picture. Eg: xRange and yRange [-3,3] means, that the fractal will be plotted from -3 to 3 and from -3i to 3i
        #figSize 2 digit array that determines size of printed image
        #hsvMap is 3 digit array that colors the whole picture. In the first element of array is a color hue, in range 0,1, other element stays for saturation, and the last one stays for brightness
        #   inserting lambda function instead of number, takes iterations converted to value between 0 and 1 where 0 diverges fastest and 1 slowest 
        #hsvCvg hsv (all in range 0,1) of converging points
        #axes shows axes in the image, with real and imaginary axis. Useful for generating julia sets
        for idx in range(len(hsvMap)):
            if not callable(hsvMap[idx]):
                hsvMap[idx]=(lambda int: (lambda x: int))(hsvMap[idx])
        func=np.vectorize(lambda it: np.array([i(it) for i in hsvMap]) if it !=-1 else hsvCvg, otypes=[object])
        z=np.linspace(xRange[0],xRange[1],size[0]).reshape((1,size[0])) + 1j*np.linspace(yRange[1],yRange[0],size[1]).reshape((size[1],1))
        c=z.copy()
        iter=np.full(z.shape,-1, dtype=object)
        d=np.full(c.shape,True,dtype=bool)
        for i in range(self.maxIter):
            z[d]=self.function(z[d], c[d])
            diverged=np.greater(np.abs(z),self.borderRad,out=np.full(c.shape, False), where=d)
            iter[diverged]=i/self.maxIter
            d[np.abs(z)>self.borderRad]=False
        iter=np.concatenate(np.concatenate(func(iter))).reshape(size[0],size[1],3)
        fig,ax=plt.subplots(figsize=tuple(figSize))
        ax.axis("on" if axes else "off")
        plt.imshow(hsv_to_rgb(iter), extent=xRange+yRange, aspect="auto")

    def saveImage(self, size=[600,600], xRange=[-3,3], yRange=[-3,3], savePath="fractal.png", hsvMap=[0,1,lambda iter: iter], hsvCvg=[0,0,0], axes=False):
        #Saves image of fractal
        
        #Size is 2 digit array that indicates X and Y resolution of the picture
        #xRange and yRange are 2 digit arrays, they are borders of the picture. Eg: xRange and yRange [-3,3] means, that the fractal will be plotted from -3 to 3 and from -3i to 3i
        #savePath is path to directory, into where is image saved and file name
        #hsvMap is 3 digit array that colors the whole picture. In the first element of array is a color hue, in range 0,1, other element stays for saturation, and the last one stays for brightness
        #   inserting lambda function instead of number, takes iterations converted to value between 0 and 1 where 0 diverges fastest and 1 slowest 
        #hsvCvg hsv (all in range 0,1) of converging points
        #axes shows axes in the image, with real and imaginary axis. Useful for generating julia sets
        for idx in range(len(hsvMap)):
            if not callable(hsvMap[idx]):
                hsvMap[idx]=(lambda int: (lambda x: int))(hsvMap[idx])
        func=np.vectorize(lambda it: np.array([i(it) for i in hsvMap]) if it !=-1 else hsvCvg, otypes=[object])
        z=np.linspace(xRange[0],xRange[1],size[0]).reshape((1,size[0])) + 1j*np.linspace(yRange[0],yRange[1],size[1]).reshape((size[1],1))
        c=z.copy()
        iter=np.full(z.shape,-1, dtype=object)
        d=np.full(c.shape,True,dtype=bool)
        for i in range(self.maxIter):
            z[d]=self.function(z[d], c[d])
            diverged=np.greater(np.abs(z),self.borderRad,out=np.full(c.shape, False), where=d)
            iter[diverged]=i/self.maxIter
            d[np.abs(z)>self.borderRad]=False
        iter=np.concatenate(np.concatenate(func(iter))).reshape(size[0],size[1],3)
        plt.axis("on" if axes else "off")
        plt.imsave(savePath, np.clip(hsv_to_rgb(iter),0,1))
    
    def saveGif(function, fBounds, frames, FPS=30, maxIter=100, borderRad=10, size=[600,600], xRange=[-3,3], yRange=[-3,3], savePath="fractal.gif", hsvMap=[0,1,lambda iter: iter], hsvCvg=[0,0,0]):
        #Saves Gif of fractal
        
        #function is function with 3 arguments where first argument 
        #fBounds are bounds of the iterating parameter
        #frames is number of frames in gif
        #maxIter maximum iterations of the function
        #borderRad If number crosses the border, it's considered as diverging
        #Size is 2 digit array that indicates X and Y resolution of the picture
        #xRange and yRange are 2 digit arrays, they are borders of the picture. Eg: xRange and yRange [-3,3] means, that the fractal will be plotted from -3 to 3 and from -3i to 3i
        #savePath is path to directory, into where is image saved and file name
        #hsvMap is 3 digit array that colors the whole picture. In the first element of array is a color hue, in range 0,1, other element stays for saturation, and the last one stays for brightness
        #   inserting lambda function instead of number, takes iterations converted to value between 0 and 1 where 0 diverges fastest and 1 slowest 
        #hsvCvg hsv (all in range 0,1) of converging points
        os.makedirs(os.getcwd() + r'/animate')
        for idx,i in enumerate(np.arange(fBounds[0],fBounds[1],(fBounds[1]-fBounds[0])/frames)):
            fractal=Fractal(lambda a,b: function(a,b,i), maxIter=maxIter, borderRad=borderRad)
            fractal.saveImage(size=size, xRange=xRange, yRange=yRange, savePath="animate/frac"+str(idx).zfill(5)+".png", hsvMap=hsvMap, hsvCvg=hsvCvg)
        imgs = sorted(glob.glob("animate/*.png"))
        framesImg=[]
        for i in imgs:
            new_frame = imageio.imread(i)
            framesImg.append(new_frame)
        imageio.mimsave(savePath, framesImg, fps=FPS)
        shutil.rmtree("animate")

    def ConvergencePic(self,num,steps=15, border=10):
        #Shows picture of how the number iterates through complex plane
        
        #num is the complex number
        #steps is number determining number of shown iterations
        #border if number reaches border, it stops
        points=[num]
        for i in range(steps):
            points.append(self.function(points[-1], points[0]))
            if abs(points[-1])>border:
                break
        fig,ax=plt.subplots(figsize=(10,10))
        for i in range(len(points)-1):
            ax.plot([points[i].real, points[i+1].real], [points[i].imag, points[i+1].imag], color="black")
        plt.show()

    def ASCII(self, empty=" ", size=[40,20], xRange=[-3,3], yRange=[-3,3]):
        #Creates ASCII art of the fractal
        #empty is the character used for empty space. When your image appears broken change the empty character
        #size is number of characters on x-axis and number of characters on y-axis. For realistic ratio it's recommended to have y axis half the x
        map=[empty, '░', '▒', '▓', '█']
        c=np.linspace(xRange[0],xRange[1],size[0]).reshape((1,size[0])) + 1j*np.linspace(yRange[0],yRange[1],size[1]).reshape((size[1],1))
        z=c.copy()
        d=np.full(c.shape, True, dtype=bool)
        it=np.full(c.shape, "█", dtype=object)
        for i in range(self.maxIter):
            z[d]=self.function(z[d], c[d])
            div=np.greater(abs(z), self.borderRad, out=np.full(c.shape, False), where=d)
            it[div]=map[int((4*(i+1)/self.maxIter)//1)]
            d[abs(z)>self.borderRad]=False 
        return("\n".join("".join(l).rstrip(empty) for l in it)) #Strip is for character count optimization! If causing troubles remove
