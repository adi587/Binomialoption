"""
Usage to find implied volatility given list of strikes and option prices
model=ImpliedVolatility(151.76, 0.04, 0.0465753,0.0061, 250,0.001,
                        {"is_call":True},{"is_eu":True},{'binomial':True})

print(model.get_impliedvol([138], [15.575]))
"""
'''
Usage to calculate option prices and greeks
option=Binomialoption(S_0=65, c=50, r=0.035, t_0=1, N=250,
                      params={"sigma":0.5,
                              "is_eu":True,
                              "is_call":True})

print(option.price())
print(option.greeks())
'''
