
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
    
def m1(max_speed, param_a = 0, param_b = 0, param_c = 0):
    """
    return min(max_speed, param_a * param_b / param_c)
    
    Args:
        max_speed (float) : max speed
        param_a (float) : param_a -> water_per_sec of Watering Machine
        param_b (float) : param_b -> watering_coeff 
        param_c (float) : param_c -> total_deficite (sum_{y=-R}^{R} D(X,Y), where D is deficite function -> D(X,Y) = optimal_water_level - current_level)
    """
    return min(max_speed, param_a * param_b / param_c)

def m2(max_speed, param_a = 0, param_b = 0, param_c = 0):
    """
        Args:
            max_speed (float) : max speed
            param_a (float) : param_a -> avg_water_level
            param_b (float) : param_b -> optimal cell water level
            param_c (float) : param_c -> base_speed
    """
    print(param_a, param_b, param_c)
    if param_a < min(0.25, param_b - 1):
        return min(max_speed, max(0.1, param_c * 0.5))
    
    elif min(0.25, param_b - 1)<= param_a <= max(0.65, param_b + 1):
        return param_c

    else: 
        return min(param_c * 1.5, max_speed)
     
         
class SMetrics:
    M1 = m1
    M2 = m2
    
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
    
   
