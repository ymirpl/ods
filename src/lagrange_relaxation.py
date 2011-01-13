class Relaxation:
    n = [0, 1, 2]
    M = [2, 1, 3]
    
    s = [2, 0, 2]
    c = [5, 3, 2]
    e = [2, 0, 1]
    p = [1, 1, 1]
    Q = 7
    psi = []
    L = []
    Ld = []
    
    
    def calculatePsi(self):
        for i in self.n:
            psi = float((-self.s[i] + self.c[i]*self.M[i])/(self.e[i] + self.p[i]*self.M[i]))
            self.psi.append(psi)
            
        print self.psi
        
    def calculateLagrangians(self):
        
        Lzero = -self.Q # only by mi 
        
        for i in self.n:
            free = self.s[i] - self.c[i]*self.M[i]
            mi = self.e[i] + self.p[i]*self.M[i]
            mi_upper = self.psi[i]
            
            self.L.append({'free': free, 'mi': mi, 'mi_upper': mi_upper})
        
        
        key = lambda x: x['mi_upper']
        self.L = sorted(self.L, key=key)
        
        
        mi_lower = 0
        for i in self.n:
            mi_upper = self.L[i]['mi_upper']
#            if i+1 < len(self.L) and mi_upper == self.L[i+1]['mi_upper']:
#                continue
            
            sum_free = 0
            sum_mi = 0
            for j in self.n[i:]:
                sum_free += self.L[j]['free']
                sum_mi += self.L[j]['mi']
            
            sum_mi += Lzero
            self.Ld.append({'free': sum_free, 'mi': sum_mi, 'mi_lower': mi_lower, 'mi_upper': mi_upper})
            mi_lower = mi_upper
        self.Ld.append({'free': 0, 'mi': -self.Q, 'mi_lower': mi_upper, 'mi_upper': mi_upper + 0.2*mi_upper})
        self.last_mi_upper = mi_upper
            
        print self.Ld
        
    def plotLagrangian(self):
        import matplotlib.pyplot as plt
        import numpy as np
        for i in xrange(len(self.Ld)):
            t = np.arange(self.Ld[i]['mi_lower'], self.Ld[i]['mi_upper'], 0.01)
            plt.plot(t, self.Ld[i]['free'] + self.Ld[i]['mi']*t)
            
        plt.show()
        plt.savefig('out.png')
    
        
        
        
        
if __name__ == '__main__':
    r = Relaxation()
    r.calculatePsi()
    r.calculateLagrangians()
    r.plotLagrangian()
    
        
    
    