from Funcs import *
from ConfigLoader import ConfigLoader
from Field import Field
from multiprocessing import Pool
from multiprocessing import cpu_count
from multiprocessing import Manager
import numpy as np
import time
import os
import sys
import pickle
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
from matplotlib.ticker import MaxNLocator, FormatStrFormatter
from matplotlib import rcParams
import matplotlib.patches as patches
import matplotlib.gridspec as gridspec
import matplotlib.lines as mlines
from matplotlib.animation import FuncAnimation, writers
import matplotlib.ticker as ticker
import time
from copy import deepcopy



class GradientOptimizer:
    def __init__(self, l_r, eps, max_iter, save=False, **params):
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
                
    
    def Gradient_Max_step(self, Field, x_cur, w, v, t_k, Ms, Mr, eta, delta,a,b, gamma, lmbda):
        if self.save:
            Steps_WV = [(w,v,0,0)]
        start_v = v
        Water1, Water2 = 0, 0
        for i in range(self.max_iter):
            # print(f"Iteration {i}: w = {w}, v = {v}")
            
            dgkdw, Water1 = dGkdw(Field, x_cur, w, v, t_k, eta, Field.Wm, Field.Deltat, delta, Field.rx, Field.ry, Field.ry_cells, Field.line, a, b, Field.alpha, Field.beta, Water1)
            dgkdv, Water2 = dGkdv(Field, x_cur, w, v, t_k, eta, Field.Wm, Field.Deltat, delta, Field.rx, Field.ry, Field.ry_cells, Field.line, a, b, Field.alpha, Field.beta, gamma, lmbda, Water2)
            
            w_new = w + dgkdw * self.l_r 
            v_new = v + dgkdv * self.l_r 
            
            
            if w_new > 1:
                w_new = 1
            if v_new > Ms:
                v_new = Ms
            if w_new < 0:   
                w_new = 0
            if v_new < 0:
                v_new = 0
                
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
                
        return 1


if __name__ == "__main__":

    Loader = ConfigLoader('../config.ini')   
    Loader.print_config() 
    a,b,c,wp,v,ms,mr,wm,alpha,beta,lmbda,eta,gamma,delta = Loader.getfloat("Model", "a"), Loader.getfloat("Model", "b"), Loader.getfloat("Model", "c"), Loader.getfloat("Model", "wp"), Loader.getfloat("Model", "v"), Loader.getfloat("Model", "ms"), Loader.getfloat("Model", "mr"), Loader.getfloat("Model", "wm"), Loader.getfloat("Model", "alpha"), Loader.getfloat("Model", "beta"), Loader.getfloat("Model", "lmbda"), Loader.getfloat("Model", "eta"), Loader.getfloat("Model", "gamma"), Loader.getfloat("Model", "delta"), 
    
    length_m, width_m, rows, cols, rx, ry = Loader.getfloat("Field", "length_m"), Loader.getfloat("Field", "width_m"), Loader.getint("Field", "rows"), Loader.getint("Field", "cols"), Loader.getfloat("Field", "rx"), Loader.getfloat("Field", "ry")

    Deltat = Loader.getfloat("Model", "deltat")
    

    field = Field(length_m=length_m, width_m=width_m, rows = rows, cols = cols, rx = rx, ry = ry, alpha = alpha, beta = beta, Wm = wm, Deltat = Deltat)
    
    field.randomize_field(0, 0.531)
    
    print(field.avg_field())
    
    l_r, eps, max_iter = Loader.getfloat("Optimization", "l_r"), Loader.getfloat("Optimization", "eps"), Loader.getint("Optimization", "max_iter")
    
    gd = GradientOptimizer(l_r, eps, max_iter, save=True)
    
    gd.Gradien_max_Field(field, 0, 0, 0, 0, mr, ms, eta, delta,a,b, gamma, lmbda)
    
    print(field.avg_field())
    print(gd.info["Optimization"][list(gd.info["Optimization"].keys())[0]]['result'])
    plot_Gk(gd.info["Optimization"][list(gd.info["Optimization"].keys())[0]]['field'], gd.info["Optimization"][list(gd.info["Optimization"].keys())[0]]['result']['x (cell)'], list(gd.info["Optimization"].keys())[0], eta, wm, Deltat, delta, rx, ry, field.ry_cells, field.line, a, b, c, alpha, beta, gamma, lmbda, points=[(gd.info["Optimization"][list(gd.info["Optimization"].keys())[0]]['result']['w'], gd.info["Optimization"][list(gd.info["Optimization"].keys())[0]]['result']['v'])])
    
    print(gd.info["Optimization"][list(gd.info["Optimization"].keys())[1]]['result'])
    plot_Gk(gd.info["Optimization"][list(gd.info["Optimization"].keys())[1]]['field'], gd.info["Optimization"][list(gd.info["Optimization"].keys())[1]]['result']['x (cell)'], list(gd.info["Optimization"].keys())[1], eta, wm, Deltat, delta, rx, ry, field.ry_cells, field.line, a, b, c, alpha, beta, gamma, lmbda, points=[(gd.info["Optimization"][list(gd.info["Optimization"].keys())[1]]['result']['w'], gd.info["Optimization"][list(gd.info["Optimization"].keys())[1]]['result']['v'])])
    
    print(gd.info["Optimization"][list(gd.info["Optimization"].keys())[5]]['result'])
    plot_Gk(gd.info["Optimization"][list(gd.info["Optimization"].keys())[5]]['field'], gd.info["Optimization"][list(gd.info["Optimization"].keys())[5]]['result']['x (cell)'], list(gd.info["Optimization"].keys())[5], eta, wm, Deltat, delta, rx, ry, field.ry_cells, field.line, a, b, c, alpha, beta, gamma, lmbda, points=[(gd.info["Optimization"][list(gd.info["Optimization"].keys())[5]]['result']['w'], gd.info["Optimization"][list(gd.info["Optimization"].keys())[5]]['result']['v'])])
    
    print(gd.info["Optimization"][list(gd.info["Optimization"].keys())[15]]['result'])
    plot_Gk(gd.info["Optimization"][list(gd.info["Optimization"].keys())[15]]['field'], gd.info["Optimization"][list(gd.info["Optimization"].keys())[15]]['result']['x (cell)'], list(gd.info["Optimization"].keys())[15], eta, wm, Deltat, delta, rx, ry, field.ry_cells, field.line, a, b, c, alpha, beta, gamma, lmbda, points=[(gd.info["Optimization"][list(gd.info["Optimization"].keys())[15]]['result']['w'], gd.info["Optimization"][list(gd.info["Optimization"].keys())[15]]['result']['v'])])
    
    print(gd.info["Optimization"][list(gd.info["Optimization"].keys())[-1]]['result'])
    plot_Gk(gd.info["Optimization"][list(gd.info["Optimization"].keys())[-1]]['field'], gd.info["Optimization"][list(gd.info["Optimization"].keys())[-1]]['result']['x (cell)'], list(gd.info["Optimization"].keys())[-1], eta, wm, Deltat, delta, rx, ry, field.ry_cells, field.line, a, b, c, alpha, beta, gamma, lmbda, points=[(gd.info["Optimization"][list(gd.info["Optimization"].keys())[-1]]['result']['w'], gd.info["Optimization"][list(gd.info["Optimization"].keys())[-1]]['result']['v'])])
    