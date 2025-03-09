from ..build.Funcs import (call_basic_function as raw_call_basic_function, exp_step as raw_exp_step, poly_step as raw_poly_step, base as raw_base, Gk as raw_Gk, dGkdw as raw_dGkdw, dGkdv as raw_dGkdv)
#==========================================================
# BASE MODULE TEMPLATE
#==========================================================

from ..build.Funcs import (
    call_basic_function as raw_basic_function
)


# TODO:  dGkdw, dGkdv, plot_Gk
class FuncsModule:
    
    def __init__(self):
        pass
    
    @staticmethod
    def dGkdw(*params):
        """
        G_k derivative by w function.

        Args:
            field (double*): Field.
            rows (int): Number of rows.
            cols (int): Number of columns.
            x_cur (int): Current x.
            w (double): W.
            v (double): V.
            t_k (double): T_k.
            eta (double): Eta.
            Wm (double): Water mass.
            Deltat (double): Delta t.
            delta (double): Delta.
            rx (double): Rx.
            ry (double): Ry.
            rx_cells (int): Rx cells.
            ry_cells (int): Ry cells.
            line (int): Line.
            a (double): A.
            b (double): B.
            c (double): C.
            alpha (double): Alpha.
            beta (double): Beta.
            gamma (double): Gamma.
            lmbda (double): Lambda.
        """
        return raw_dGkdw(*params)

    @staticmethod
    def dGkdv(*params):
        """
        G_k derivative by v function.

        Args:
            field (double*): Field.
            rows (int): Number of rows.
            cols (int): Number of columns.
            x_cur (int): Current x.
            w (double): W.
            v (double): V.
            t_k (double): T_k.
            eta (double): Eta.
            Wm (double): Water mass.
            Deltat (double): Delta t.
            delta (double): Delta.
            rx (double): Rx.
            ry (double): Ry.
            rx_cells (int): Rx cells.
            ry_cells (int): Ry cells.
            line (int): Line.
            a (double): A.
            b (double): B.
            c (double): C.
            alpha (double): Alpha.
            beta (double): Beta.
            gamma (double): Gamma.
            lmbda (double): Lambda.
        """
        return raw_dGkdv(*params)
    
    @staticmethod
    def Gk(*params):
        """
        G_k function.

        Args:
            field (double*): Field.
            rows (int): Number of rows.
            cols (int): Number of columns.
            x_cur (int): Current x.
            w (double): W.
            v (double): V.
            t_k (double): T_k.
            eta (double): Eta.
            Wm (double): Water mass.
            Deltat (double): Delta t.
            delta (double): Delta.
            rx (double): Rx.
            ry (double): Ry.
            rx_cells (int): Rx cells.
            ry_cells (int): Ry cells.
            line (int): Line.
            a (double): A.
            b (double): B.
            c (double): C.
            alpha (double): Alpha.
            beta (double): Beta.
            gamma (double): Gamma.
            lmbda (double): Lambda.
        """
        return raw_Gk(*params)

    @staticmethod
    def poly_step(*params):
        """
        Polynomial step.

        Args:
            l_0 (float): Initial value.
            step (int): Step.
            alpha (float, optional): Alpha. Defaults to 0.5.
            beta (float, optional): Beta. Defaults to 1.
            
        Returns:
            float: Result of the polynomial step.
        """
        return raw_poly_step(*params)

    @staticmethod
    def base(*params):
        """
        Base function.
        
        FUNCTION
        ===
        F(i,j) = -a*(field[i][j] - b)**2 + c
        
        Args:
            field(matrix): Field.
            a (float): a.
            b (float): b.
            c (float): c.    
        """
        return raw_base(*params)

    @staticmethod
    def exp_step(*params):
        """
        Exponential step.

        Args:
            l_0 (float): Initial value.
            step (int): Step.
            lmbda (float, optional): Lambda. Defaults to 0.05.

        Returns:
            float: Result of the exponential step.
        """ 
        return raw_exp_step(*params)
    
    def call_basic_function(self):
        return raw_basic_function()

def sample_function():
    instance = FuncsModule()
    FuncsModule.c_exp_step()
