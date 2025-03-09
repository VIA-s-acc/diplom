import model as md
import time
import time
from copy import deepcopy
  

##  
#   @mainpage 
#    
#  @section toc Table of Contents  
#  - @ref ConfigLoader  
#  - @ref Funcs
#  - @ref Field
#  - @ref Optimizer
#   @author Georgii
#   @version v1a
#  


##
# @package Optimizer
# @brief Class for gradient optimization
# @author Georgii
# @file     Optimizer.py
# @author   Georgii 
# @brief    Class for gradient optimization
# @version v1a
# @date 15.02.2025
#

# === CLASSES ===
class GradientOptimizer:
    """!
    GradientOptimizer class.
    
    @brief Class for gradient optimization.
    """
    def __init__(self, l_r, eps, max_iter, save=False, **params):
        """!
        Constructor.

        @param l_r Learning rate.
        @param eps Epsilon.
        @param max_iter Maximum number of iterations.
        @param save Save optimization info.
        @param params Parameters for optimization. - Field, a, b, c, base
        @Field Field
        @a a
        @b b
        @c c
        @base base function
        """
        
        
        
        # === ATTRIBUTES ===
        self.l_r = l_r
        self.eps = eps
        self.max_iter = max_iter
        self.info = {}
        self.save = save
        if save:
            self.info["Optimization"] = {}
        else: 
            self.info["Optimization"] = "OFF"
        self.info['l_r'] = self.l_r
        self.info['eps'] = self.eps
        self.info['max_iter'] = self.max_iter
        self.info['start_time'] = time.time()
        self.info['end_time'] = None
        self.info["duration"] = None
        self.params = params
        if "field" in list(params.keys()) and "a" in list(params.keys()) and "b" in list(params.keys()) and "c" in list(params.keys()) and "base" in list(params.keys()):
            self.info["start_base"] = params["field"].calc_base(params["base"], params["a"], params["b"], params["c"])
            self.info['start_avg'] = params["field"].avg_field()
        else:
            self.info["start_base"] = None
            self.info['start_avg'] = None
        self.info['end_base'] = None
        self.info['end_avg'] = None
        
                
    # === METHODS ===
    def Gradient_Max_step(self, Field, x_cur, w, v, t_k, Ms, Mr, eta, delta,a,b, gamma, lmbda):
        """!
        Gradient Max step.

        @param Field Field.
        @param x_cur Current x.
        @param w Current w.
        @param v Current v.
        @param t_k Current t_k.
        @param Ms Maximum value for v.
        @param Mr Maximum relative change for v.
        @param eta Eta.
        @param delta Delta.
        @param a A.
        @param b B.
        @param gamma Gamma.
        @param lmbda Lambda.
        @return New w and v.
        
        """
        if self.save:
            Steps_WV = [(w,v,0,0)]
        start_v = v
        Water1, Water2 = 0, 0
        for i in range(self.max_iter):
            # print(f"Iteration {i}: w = {w}, v = {v}")
            
            # dgkdw, dgkdv
            dgkdw = md.FuncsModule.dGkdw(Field.field, x_cur, w, v, t_k, eta, Field.Wm, Field.Deltat, delta, Field.rx, Field.ry, Field.rx_cells, Field.ry_cells, Field.line, a, b, self.params['c'], Field.alpha, Field.beta, gamma, lmbda)
            dgkdv = md.FuncsModule.dGkdv(Field.field, x_cur, w, v, t_k, eta, Field.Wm, Field.Deltat, delta, Field.rx, Field.ry, Field.rx_cells, Field.ry_cells, Field.line, a, b, self.params['c'], Field.alpha, Field.beta, gamma, lmbda)
            #def dGkdw(field, x_cur, w, v, t_k, eta, Wm, Deltat, delta, rx, ry, rx_cells, ry_cells, line, a, b, c, alpha, beta, gamma, lmbda):

            # w_new = w + dgkdw * poly_step(self.l_r, i)
            # v_new = v + dgkdv * poly_step(self.l_r, i)
            
            step = md.FuncsModule.exp_step(self.l_r, i)
            w_new = w + dgkdw * step
            v_new = v + dgkdv * step
            
            # w_new = w + dgkdw * self.l_r
            # v_new = v + dgkdv * self.l_r
            
            
            w_new = max(0, min(1, w_new))
            v_new = max(0, min(Ms, v_new))
                
            if abs(v_new - start_v) > Mr:
                if v_new > start_v:
                    v_new = start_v + Mr
                else:
                    v_new = start_v - Mr
                    
            if abs (w_new - w) < self.eps and abs(v_new - v) < self.eps and i != 0: 
                w = w_new
                v = v_new
                if self.save:
                    Steps_WV.append((w,v,Water1,Water2))
                if self.save:
                    if t_k in self.info["Optimization"]:
                        self.info["Optimization"][t_k]['steps'] = Steps_WV
                    else:
                        self.info["Optimization"][t_k] = {
                            'steps': Steps_WV
                        }
                return w, v
            else:
                w = w_new
                v = v_new
                if self.save:
                    Steps_WV.append((w,v, Water1, Water2))
                    
        if self.save:
            if t_k in self.info["Optimization"]:
                self.info["Optimization"][t_k]['steps'] = Steps_WV
            else:
                self.info["Optimization"][t_k] = {
                    'steps': Steps_WV
                }
        return w, v

    def Gradien_max_Field(self, Field, x, w, v, t_k, Mr, Ms, eta, delta,a,b, gamma, lmbda, Water=0):
        """!
        Gradient max field.

        @param Field Field.
        @param x Current x.
        @param w Current w.
        @param v Current v.
        @param t_k Current t_k.
        @param Mr Maximum relative change for v.
        @param Ms Maximum value for v.
        @param eta Eta.
        @param delta Delta.
        @param a A.
        @param b B.
        @param gamma Gamma.
        @param lmbda Lambda.
        @param Water Water.
        @return Water
        """
        x_met = 0
        counter = 0
        while x <= cols+Field.rx_cells:
            w, v = self.Gradient_Max_step(Field, x, w, v, t_k, Ms, Mr, eta, delta,a,b, gamma, lmbda)
            start_col = max(0, x - Field.rx_cells) #+1
            end_col = min(cols, x + 1)
            if start_col == end_col:
                start_col -= Field.rx_cells

            res = Field.parallel_update_field(x, w, v)
            
            Water+=sum(res)
            if self.save:
                if t_k not in self.info["Optimization"]:
                    self.info["Optimization"][t_k] = {
                        'result': {
                            "w": round(w, 5),
                            "v": round(v, 5),
                            "x (cell)": x,
                            "x (m)": round(x_met,5)
                            },
                        'field':deepcopy(Field)
                    }
                else:
                    self.info["Optimization"][t_k]['result'] = {
                        "w": round(w, 5),
                        "v": round(v, 5),
                        "x (cell)": x,
                        "x (m)": round(x_met,5)
                    }
                    self.info["Optimization"][t_k]['field'] = deepcopy(Field)
        
            # print(f"t_k = {t_k:.2f}, w = {w:.4f}, v = {v:.4f}, x = {x}")
            
            change = v * Deltat
            if change <= 0.001:
                counter += 1
                if counter == 3:
                    # print("Error | x_met + change <= x_met | break")
                    v+=Mr
            else:
                counter = 0
            x_met += change
            if int(t_k)%25==0 or field.length_m - x_met < 10:
            
                print(f"t_k = {t_k:.2f}, w = {w:.4f}, v = {v:.4f}, x = {x}, x_met = {x_met}")
            x = int(round(x_met / Field.cell_length_m))
            t_k += Deltat
        self.info["end_time"] = time.time()
        self.info["Water"] = Water
        self.info["duration"] = self.info["end_time"] - self.info["start_time"]
        self.info["end_avg"] = Field.avg_field()
        if 'base' in list(self.params.keys()) and 'a' in list(self.params.keys()) and 'b' in list(self.params.keys()) and 'c' in list(self.params.keys()):
            self.info['end_base'] = self.params["field"].calc_base(self.params["base"], self.params["a"], self.params["b"], self.params["c"])
        return 1


if __name__ == "__main__":
    Loader = md.ConfigloaderModule('config.ini')   
    Loader.print_config() 
    a,b,c,wp,v,ms,mr,wm,alpha,beta,lmbda,eta,gamma,delta = Loader.getfloat("Model", "a"), Loader.getfloat("Model", "b"), Loader.getfloat("Model", "c"), Loader.getfloat("Model", "wp"), Loader.getfloat("Model", "v"), Loader.getfloat("Model", "ms"), Loader.getfloat("Model", "mr"), Loader.getfloat("Model", "wm"), Loader.getfloat("Model", "alpha"), Loader.getfloat("Model", "beta"), Loader.getfloat("Model", "lmbda"), Loader.getfloat("Model", "eta"), Loader.getfloat("Model", "gamma"), Loader.getfloat("Model", "delta"), 
    
    length_m, width_m, rows, cols, rx, ry = Loader.getfloat("Field", "length_m"), Loader.getfloat("Field", "width_m"), Loader.getint("Field", "rows"), Loader.getint("Field", "cols"), Loader.getfloat("Field", "rx"), Loader.getfloat("Field", "ry")

    Deltat = Loader.getfloat("Model", "deltat")
    

    field = md.FieldModule(length_m=length_m, width_m=width_m, rows = rows, cols = cols, rx = rx, ry = ry, alpha = alpha, beta = beta, Wm = wm, Deltat = Deltat)

    field.randomize_field(MAX_V=0.412, MIN_V=0.07694)


    
    l_r, eps, max_iter = Loader.getfloat("Optimization", "l_r"), Loader.getfloat("Optimization", "eps"), Loader.getint("Optimization", "max_iter")
    
    gd = GradientOptimizer(l_r, eps, max_iter, save=False, field = field, a = a, b = b, c = c, base = md.FuncsModule.base)
    st = time.time()  
    # print(field.calc_base(base))
    gd.Gradien_max_Field(field, 0, 0, 0, 0, mr, ms, eta, delta,a,b, gamma, lmbda)
    
    print(time.time() - st)

    # opt_key = list(gd.info["Optimization"].keys())[0]
    # start_field = gd.info["Optimization"][opt_key]["field"]

    # print(f"start_base: {gd.info['start_base']}\nend_base: {gd.info['end_base']}")
    # print(f"start_avg: {start_field.avg_field()}\nend_avg: {field.avg_field()}")
    from pprint import pprint
    pprint(gd.info)
    # print(start_field[0])
    # print(field[0])
    # print(gd.info["Optimization"][list(gd.info["Optimization"].keys())[0]]['result'])
    # plot_Gk(gd.info["Optimization"][list(gd.info["Optimization"].keys())[0]]['field'], gd.info["Optimization"][list(gd.info["Optimization"].keys())[0]]['result']['x (cell)'], list(gd.info["Optimization"].keys())[0], eta, wm, Deltat, delta, rx, ry, field.ry_cells, field.line, a, b, c, alpha, beta, gamma, lmbda, points=[(gd.info["Optimization"][list(gd.info["Optimization"].keys())[0]]['result']['w'], gd.info["Optimization"][list(gd.info["Optimization"].keys())[0]]['result']['v'])])
    
    # print(gd.info["Optimization"][list(gd.info["Optimization"].keys())[1]]['result'])
    # plot_Gk(gd.info["Optimization"][list(gd.info["Optimization"].keys())[1]]['field'], gd.info["Optimization"][list(gd.info["Optimization"].keys())[1]]['result']['x (cell)'], list(gd.info["Optimization"].keys())[1], eta, wm, Deltat, delta, rx, ry, field.ry_cells, field.line, a, b, c, alpha, beta, gamma, lmbda, points=[(gd.info["Optimization"][list(gd.info["Optimization"].keys())[1]]['result']['w'], gd.info["Optimization"][list(gd.info["Optimization"].keys())[1]]['result']['v'])])
    
    # print(gd.info["Optimization"][list(gd.info["Optimization"].keys())[5]]['result'])
    # plot_Gk(gd.info["Optimization"][list(gd.info["Optimization"].keys())[5]]['field'], gd.info["Optimization"][list(gd.info["Optimization"].keys())[5]]['result']['x (cell)'], list(gd.info["Optimization"].keys())[5], eta, wm, Deltat, delta, rx, ry, field.ry_cells, field.line, a, b, c, alpha, beta, gamma, lmbda, points=[(gd.info["Optimization"][list(gd.info["Optimization"].keys())[5]]['result']['w'], gd.info["Optimization"][list(gd.info["Optimization"].keys())[5]]['result']['v'])])
    
    # print(gd.info["Optimization"][list(gd.info["Optimization"].keys())[15]]['result'])
    # plot_Gk(gd.info["Optimization"][list(gd.info["Optimization"].keys())[15]]['field'], gd.info["Optimization"][list(gd.info["Optimization"].keys())[15]]['result']['x (cell)'], list(gd.info["Optimization"].keys())[15], eta, wm, Deltat, delta, rx, ry, field.ry_cells, field.line, a, b, c, alpha, beta, gamma, lmbda, points=[(gd.info["Optimization"][list(gd.info["Optimization"].keys())[15]]['result']['w'], gd.info["Optimization"][list(gd.info["Optimization"].keys())[15]]['result']['v'])])
    
    # print(gd.info["Optimization"][list(gd.info["Optimization"].keys())[-1]]['result'])
    # plot_Gk(gd.info["Optimization"][list(gd.info["Optimization"].keys())[-1]]['field'], gd.info["Optimization"][list(gd.info["Optimization"].keys())[-1]]['result']['x (cell)'], list(gd.info["Optimization"].keys())[-1], eta, wm, Deltat, delta, rx, ry, field.ry_cells, field.line, a, b, c, alpha, beta, gamma, lmbda, points=[(gd.info["Optimization"][list(gd.info["Optimization"].keys())[-1]]['result']['w'], gd.info["Optimization"][list(gd.info["Optimization"].keys())[-1]]['result']['v'])])
    
    
    



