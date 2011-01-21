class Relaxation:
#    n = [0, 1, 2]
#    M = [2, 1, 3]
#    
#    s = [2, 0, 2]
#    c = [5, 3, 2]
#    e = [2, 0, 1]
#    p = [1, 1, 1]
#    Q = 7
#    
    
    n = range(10)
    c = [[16,23], [15, 23], [19, 28], [17, 8], [13, 19], [17, 26], [10, 13], [11, 10], [22, 16], [25, 15]]
    e = 1
    s = 1
    M = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    p = [[2, 3], [1, 2], [1, 2], [3, 1], [1, 2], [1, 2], [2, 3], [4, 3], [2, 1], [4, 2]]
    L = []
    Ld = []
    peaks = []
    
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
            self.plotLi(i, "L"+str(i+1), "L"+str(i+1))
    
                    
                    
    def plotLi(self, i = 0, name = "L", caption = "L"):
        import matplotlib.pyplot as plt
        import numpy as np
        
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.set_title(caption)
        
        for line in self.L[i].values():
            if not line['u'] == line['l']:
                
                if line['u'] == float("inf"): 
                    line['u'] = line['l']+5
                    
                t = np.arange(line['l'], line['u'], 0.01)
                plt.plot(t, line['ct']+line['mi']*t)
        
        plt.savefig(name)
        
    def plotLagrangian(self):
        import matplotlib.pyplot as plt
        import numpy as np
        for i in xrange(len(self.Ld)):
            
            if self.Ld[i]['mi_upper'] == float('infinity'):
                upper_bound = self.Ld[i]['mi_lower']*1.2
            else:
                upper_bound = self.Ld[i]['mi_upper']
                
            t = np.arange(self.Ld[i]['mi_lower'], upper_bound, 0.01)
            plt.plot(t, self.Ld[i]['free'] + self.Ld[i]['mi']*t, 'b-')
            
        plt.show()
        plt.savefig('out.png')
        
        
    def findMaximum(self):
        max = float("-infinity")
        arg = 0
        for i in xrange(len(self.Ld)):
            ld = self.Ld[i]['free'] + self.Ld[i]['mi']*self.Ld[i]['mi_lower'] 
            if ld > max:
                max = ld
                arg = self.Ld[i]['mi_lower'] 
            
            ld = self.Ld[i]['free'] + self.Ld[i]['mi']*self.Ld[i]['mi_upper'] 
            if ld > max:
                max = ld
                arg = self.Ld[i]['mi_upper']
                
        print 'Max, arg: ',max, arg
        self.Lmax = (max, arg)
        return(max, arg) 
                
    def findX(self):
        mi = self.Lmax[1]
        
        for i in self.n:
            if mi < self.L[i]['mi_upper']:
                self.x.append(self.M[i])
            else:
                self.x.append(0)
                
        print 'x ',self.x
                
            
    
        
        
        
        
if __name__ == '__main__':
    r = Relaxation()
    r.makeLi()
    
        
    
    