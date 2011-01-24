# -*- encoding: utf-8 -*-
""" Marcin Mincer, IAiIS , ODS Projekt 10"""
class Relaxation:
    import data
    
    n = data.n
    c = data.c
    e = data.e   
    s = data.s
    M = data.M
    p = data.p
    Q = data.Q

    L = []
    peaks = []
    x = [[0 for i in range(2)] for j in range(10)]
    v = [[0 for i in range(2)] for j in range(10)]

    def __init__(self):
        self.Lzero = {'idle': {'ct': 0, 'mi': -1*self.Q, 'l': 0, 'u': float("inf")}}
        self.plotLi(self.Lzero, "L0", "L0")
    
    def intersection(self, lineOne, lineTwo):
        if (lineOne['mi']-lineTwo['mi']) != 0.0:
            return float(lineTwo['ct']-lineOne['ct'])/float(lineOne['mi']-lineTwo['mi'])
        else:
            return float("inf")
            
    def makeLi(self):
        for i in self.n:
            machineOne = {'ct': self.s[i][0]-self.c[i][0]*self.M[i], 'mi': self.e[i][0]+self.p[i][0]*self.M[i], 'l': 0, 'u': float("inf")}
            machineTwo = {'ct': self.s[i][1]-self.c[i][1]*self.M[i], 'mi': self.e[i][1]+self.p[i][1]*self.M[i], 'l': 0, 'u': float("inf")}
            idleOne = {'ct': self.s[i][0], 'mi': self.e[i][0], 'l': 0, 'u': float("inf")}
            idleTwo = {'ct': self.s[i][1], 'mi': self.e[i][1], 'l': 0, 'u': float("inf")}
            
     
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
                    if lineOne['ct'] <= lineTwo['ct']: # line one rules 
                        lineTwo['u'] = 0
                        lineTwo['l'] = 0  
                    else:
                        lineOne['u'] = 0
                        lineOne['l'] = 0
                    
                    
            point = self.intersection(machineOne, machineTwo)
            adjustBorders(point, machineOne, machineTwo)
            point = self.intersection(machineOne, idleOne)
            adjustBorders(point, machineOne, idleOne)
            point = self.intersection(idleOne, machineTwo)
            adjustBorders(point, idleOne, machineTwo)
            point = self.intersection(machineOne, idleTwo)
            adjustBorders(point, machineOne, idleTwo)
            point = self.intersection(idleTwo, machineTwo)
            adjustBorders(point, idleTwo, machineTwo)
            point = self.intersection(idleTwo, idleOne)
            adjustBorders(point, idleTwo, idleOne)
            
            Li = {'mO': machineOne, 'mT': machineTwo, 'idleO': idleOne, 'idleT': idleTwo}
            self.L.append(Li)
            self.plotLi(Li, "L"+str(i+1), "L"+str(i+1))
            
    def maximizeMi(self):
        maxLd = float("-inf")
        LdList = []
        
        # import numpy as np
        # self.peaks = np.arange(0, 30, 0.01) 
        for x in self.peaks:
            localX = [[0 for i in range(2)] for j in range(len(self.n))]
            localV = [[0 for i in range(2)] for j in range(len(self.n))]
            
            ct = 0
            mi = self.Lzero['idle']['mi']
            for i, l in enumerate(self.L):
                for (k,v) in l.items():
                    if v['l'] < x <= v['u']:
                        mi += v['mi']
                        ct += v['ct']
                        print i
                        
                        if k == 'mO':
                            localX[i][0] = self.M[i]
                            localV[i][0] = 1
                        elif k == 'mT':
                            localX[i][1] = self.M[i]
                            localV[i][1] = 1
                        elif k == 'idleO': #idle
                            localV[i][0] = 1
                        else: 
                            localV[i][1] = 1
          
            LdValue = ct + mi*x
            LdList.append(LdValue)
            if LdValue >= maxLd:
                maxLd = LdValue
                maxArg = x
                self.x = localX
                self.v = localV
        
        
        print "Solution found:"
        print "mi: ", maxArg
        print "Ld: ", maxLd

        
        
        
        self.plotDual(LdList)

        while self.quality()[1] > self.Q:
            print "Constraints exceeded, making perturbation step:"
            self.makePerturbation(maxArg)
                    
    def quality(self):
        profit = 0
        usage = 0
        
        for i in self.n:
            for j in range(2):
                if self.v[i][j]:
                    profit += self.s[i][j]
                    usage += self.e[i][j]
                profit -= self.c[i][j]*self.x[i][j]
                usage += self.p[i][j]*self.x[i][j]
        
        print "Solution: "
#        print "x: ", self.x
#        print "v: ", self.v
        print "Profit: ", profit
        print "Usage: ", usage, "Q: ", self.Q
        
        return (profit, usage)  
    
    def makePerturbation(self, mi):
        # we choose element, which gives least gain
        maxL = float("-inf")
        maxArg = tuple()
        for i in self.n:
            for j in range(2):
                if self.x[i][j] > 0:
                    # L = self.s[i][j] - self.c[i][j]*self.x[i][j] + mi*(self.e[i][j] + self.x[i][j]*self.p[i][j]) 
                    L = (self.s[i][j] - self.c[i][j]) + mi*(self.e[i][j] + self.p[i][j])
                    if L > maxL: 
                        maxL = L
                        maxArg = (i, j)
                        
        self.x[maxArg[0]][maxArg[1]] -= 1 # perform permutation
                           
    
                    
    def plotDual(self, LdList):
        try:
            import matplotlib.pyplot as plt
            fig = plt.figure()
            ax = fig.add_subplot(111)
            ax.grid(True)
            ax.set_xlabel('mi')
            
            zipped = zip(self.peaks, LdList)
            zipped = sorted(zipped, key = lambda x: x[0])
            self.peaks, LdList = zip(*zipped)
            
            plt.plot(self.peaks, LdList, 'b-')
            plt.savefig("dual")
        except:
            pass # with no matplotlib fall silently
            
                        
    def plotLi(self, function, name = "L", caption = "L"):
        try:
            import matplotlib.pyplot as plt
            import numpy as np
            
            fig = plt.figure()
            ax = fig.add_subplot(111)
            ax.set_title(caption)
            ax.grid(True)
            
            plots = list()
            legends = list()
            for line in function.values():
                if not line['u'] == line['l']:
                    
                    upperLimit = line['l']+5 if line['u'] == float("inf") else line['u'] 
                        
                    t = np.arange(line['l'], upperLimit, 0.01)
                    plots.append(plt.plot(t, line['ct']+line['mi']*t))
                    legends.append("%.2f + %.2fmi " % (line['ct'], line['mi']) )
                    ax.set_xlabel('mi')
            
            
            plt.legend(plots, legends, loc=4)
            plt.savefig(name)
        except:
            pass # with no matplotlib fall silently
        
        
        
if __name__ == '__main__':
    r = Relaxation()
    r.makeLi()
    r.maximizeMi()
    
        
    
    