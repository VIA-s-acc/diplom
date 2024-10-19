
def base_func(x, a, b, c):
    return a * (x-b)**2 + c

def wheat_m(x, a = -10, b = 0.35, c = 2):
    return base_func(x, a, b, c)

def corn_m(x, a = -8, b = 0.4, c = 3.5):
    return base_func(x, a, b, c)

def soybean_m(x, a = -12, b = 0.45, c = 1.5):
    return base_func(x, a, b, c)

def potato_m(x, a = -15, b = 0.5, c = 4):
    return base_func(x, a, b, c)
    
class Metrics:
    WHEAT = wheat_m
    CORN = corn_m
    SOYBEAN = soybean_m
    POTATO = potato_m
    
    WHEAT_MAX_AT = 0.35
    CORN_MAX_AT = 0.4
    SOYBEAN_MAX_AT = 0.45
    POTATO_MAX_AT = 0.5

    @property
    def WHEAT_MAX():
        return Metrics.WHEAT_MAX_AT
    
    @property
    def CORN_MAX():
        return Metrics.CORN_MAX_AT

    @property
    def SOYBEAN_MAX():
        return Metrics.SOYBEAN_MAX_AT
    
    @property
    def POTATO_MAX():
        return Metrics.POTATO_MAX_AT
    
   
