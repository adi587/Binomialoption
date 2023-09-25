from Stockoptions import Stockoption
import math
import numpy as np
from Binomialoption import Binomialoption
from scipy.stats import norm

class ImpliedVolatility:
    '''
    Stock option class has all the parameters defined for underlying asset
    Attributes:
        S_0=Current price of underlying
        c=Strike price
        r=Risk free rate (annually)
        t_0=Time to expiration (yrs)
        div=Dividends of underlying (annualised)
        N=no.steps in binomial tree

        is_call=Whether it is a call (True,False)
        is_eu=Whether it is european or american option (True, False respectively)
        binomial=Whether to value using binomial tree or BS equation (True,False)
        
        Usage eg: model=ImpliedVolatility(151.76, 0.04, 0.0465753,0.0061, 250,0.001,
                        {"is_call":True},{"is_eu":True},{'binomial':True})

        
    Methods:
        optionval=Calculates the option value using binomial tree
        black=Calculates option value using BS equation
        get_implied=Given list of strikes and option prices calculated implied volatility through binomial tree or BS

    '''
    def __init__(self,S_0,r,t_0,div,N,res,call,eu,binomial):
        self.S_0=S_0 #stock price now
        self.r=r     #riskfree rate
        self.t_0=t_0 #time to expiry
        self.N=N     #no. steps in the tree
        self.div=div #divedends of underlying
        self.is_call = call.get("is_call", True)  
        self.is_eu=eu.get("is_eu",True)
        self.res=res #The resolution that volatility will be correct to
        self.binomial=binomial.get("binomial",False) # To choose via binomial or not
    
    #Binomial tree model
    def optionval(self,c,sigma):
        opt=Binomialoption(self.S_0, c, self.r, self.t_0, self.N,{
                    "div":self.div,
                    "sigma":sigma,
                    "is_call":self.is_call,
                    "is_eu":self.is_eu})        
         
        return opt.price()   
    
    
    #BS model 
    def black(self,c,sigma):
        d=(math.log(self.S_0/c)+(self.r+(sigma**2)/2)*self.t_0)/(sigma*math.sqrt(self.t_0))
        ans=self.S_0*norm.cdf(d)-c*math.exp(-self.r*self.t_0)*norm.cdf(d-sigma*math.sqrt(self.t_0))
        return ans

    def get_impliedvol(self,strikes,opt_values):
        impvol=[]
        for i in range(len(strikes)):
            #Bisection calc:
            a=0.1 #lower bound estimate
            b=1 #upper bound estimate
            
            #Making sure bounds contain the solution
            if self.binomial:
                while not self.optionval(strikes[i], a)<opt_values[i]:
                    a=a/2
                while not self.optionval(strikes[i], b)>opt_values[i]:
                    b=b*2
            else:
                while not self.black(strikes[i],a)<opt_values[i]:
                    a=a/2
                while not self.black(strikes[i],b)>opt_values[i]:
                    b=b*2     
            d=(a+b)/2
            impv=self.optionval(strikes[i], d)
            
            #Iteratively finding solution until correct to resolution previously set
            while abs(impv-opt_values[i])>self.res:
                if impv>opt_values[i]:
                    b=d
                else: a=d
                d=(a+b)/2
                if self.binomial:
                    impv=self.optionval(strikes[i], d)
                else:
                    impv=self.black(strikes[i], d)
            
                
            impvol=np.append(impvol,d)    
                                                      
        return impvol
