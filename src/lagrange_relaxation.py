class Relaxation:

    n = range(10)
    c = [[16,23], [15, 23], [19, 28], [17, 8], [13, 19], [17, 26], [10, 13], [11, 10], [22, 16], [25, 15]]
    e = 1
    s = 1
    M = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    p = [[2, 3], [1, 2], [1, 2], [3, 1], [1, 2], [1, 2], [2, 3], [4, 3], [2, 1], [4, 2]]
    L = []
    peaks = []
    Q = 15
    x = [[0 for i in range(2)] for j in range(10)]
    v = [[0 for i in range(2)] for j in range(10)]

    def __init__(self):
        self.Lzero = {'idle': {'ct': 0, 'mi': -1*self.Q, 'l': 0, 'u': float("inf")}}
        self.plotLi(self.Lzero, "L0", "L0")
    
    def intersection(self, lineOne, lineTwo):
        if (lineOne['mi']-lineTwo['mi']) != 0.0:
            return float(lineTwo['ct']-lineOne['ct'])/float(lineOne['mi']-lineTwo['mi'])
        else:
            float("inf")
            
    def makeLi(self):
        for i in self.n:
            machineOne = {'ct': self.s-self.c[i][0]*self.M[i], 'mi': self.e+self.p[i][0]*self.M[i], 'l': 0, 'u': float("inf")}
            machineTwo = {'ct': self.s-self.c[i][1]*self.M[i], 'mi': self.e+self.p[i][1]*self.M[i], 'l': 0, 'u': float("inf")}
            idle = {'ct': self.s, 'mi': self.e, 'l': 0, 'u': float("inf")}
            
     
            def adjustBorders(point, lineOne, lineTwo):
                self.peaks.append(point) # for later use
                if point != float('inf'):
                    if lineOne['mi'] > lineTwo['mi']:
                        if point < lineOne['u']: lineOne['u'] = point 
                        if point > lineTwo['l']: lineTwo['l'] = point
                    else: 
                        if point > lineOne['l']: lineOne['l'] = point
                        if point < lineTwo['u']: lineTwo['u'] = point
                else: # paralell
                    if lineOne['ct'] < lineTwo['ct']: # line one rules 
                        lineTwo['u'] = 0
                        lineTwo['l'] = 0  
                    else:
                        lineOne['u'] = 0
                        lineOne['l'] = 0
                    
                    
            point = self.intersection(machineOne, machineTwo)
            adjustBorders(point, machineOne, machineTwo)
            point = self.intersection(machineOne, idle)
            adjustBorders(point, machineOne, idle)
            point = self.intersection(idle, machineTwo)
            adjustBorders(point, idle, machineTwo)
            
            Li = {'mO': machineOne, 'mT': machineTwo, 'idle': idle}
            self.L.append(Li)
            self.plotLi(Li, "L"+str(i+1), "L"+str(i+1))
            
    def maximizeMi(self):
        maxMi = float("-inf")
        miList = []
        
        for x in self.peaks:
            localX = [[0 for i in range(2)] for j in range(10)]
            localV = [[0 for i in range(2)] for j in range(10)]
            
            ct = 0
            mi = self.Lzero['idle']['mi']
            for i, l in enumerate(self.L):
                for (k,v) in l.items():
                    if v['l'] <= x < v['u']:
                        mi += v['mi']
                        ct += v['ct']
                        
                        if k == 'mO':
                            localX[i][0] = self.M[i]
                            localV[i][0] = 1
                        elif k == 'mT':
                            localX[i][1] = self.M[i]
                            localV[i][1] = 1
                        else: #idle
                            localV[i][0] = 1
            miValue = ct + mi*x
            miList.append(miValue)
            print "mi ", miValue
            if miValue >= maxMi:
                maxMi = miValue
                self.x = localX
                self.v = localV
        
        print "x ", self.x
        print "v ", self.v
        self.plotDual(miList)
                    
                    
    
                    
    def plotDual(self, miList):
        import matplotlib.pyplot as plt
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.grid(True)
        
        plt.plot(self.peaks, miList, 'r*')
        plt.savefig("dual")
        
                        
    def plotLi(self, function, name = "L", caption = "L"):
        import matplotlib.pyplot as plt
        import numpy as np
        
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.set_title(caption)
        ax.grid(True)
        
        for line in function.values():
            if not line['u'] == line['l']:
                
                if line['u'] == float("inf"): 
                    line['u'] = line['l']+5
                    
                t = np.arange(line['l'], line['u'], 0.01)
                plt.plot(t, line['ct']+line['mi']*t)
        
        plt.savefig(name)
        
        
        
        
if __name__ == '__main__':
    r = Relaxation()
    r.makeLi()
    r.maximizeMi()
    
        
    
    