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
    M = []
    
    
    
    
    
    
    psi = []
    L = []
    Ld = []
    x = []
    
    
    def calculatePsi(self):
        for i in self.n:
            psi = float((-self.s[i] + self.c[i]*self.M[i])/(self.e[i] + self.p[i]*self.M[i]))
            self.psi.append(psi)
        
            
        print 'Psi ', self.psi
        
    def calculateLagrangians(self):
        
        Lzero = -self.Q # only by mi 
        
        for i in self.n:
            free = self.s[i] - self.c[i]*self.M[i]
            mi = self.e[i] + self.p[i]*self.M[i]
            mi_upper = self.psi[i]
            
            self.L.append({'free': free, 'mi': mi, 'mi_upper': mi_upper})
        
        
        key = lambda x: x['mi_upper']
        Lsorted = sorted(self.L, key=key)
        
        
        mi_lower = 0
        for i in self.n:
            mi_upper = Lsorted[i]['mi_upper']
#            if i+1 < len(self.L) and mi_upper == self.L[i+1]['mi_upper']:
#                continue
            
            sum_free = 0
            sum_mi = 0
            for j in self.n[i:]:
                sum_free += Lsorted[j]['free']
                sum_mi += Lsorted[j]['mi']
            
            sum_mi += Lzero
            self.Ld.append({'free': sum_free, 'mi': sum_mi, 'mi_lower': mi_lower, 'mi_upper': mi_upper})
            mi_lower = mi_upper
        # self.Ld.append({'free': 0, 'mi': -self.Q, 'mi_lower': mi_upper, 'mi_upper': mi_upper + 0.2*mi_upper})
        self.Ld.append({'free': 0, 'mi': -self.Q, 'mi_lower': mi_upper, 'mi_upper': float('infinity')})
        self.last_mi_upper = mi_upper
            
        print 'Ld ', self.Ld
        
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
    r.calculatePsi()
    r.calculateLagrangians()
    r.findMaximum()
    r.findX()
    
        
    
    