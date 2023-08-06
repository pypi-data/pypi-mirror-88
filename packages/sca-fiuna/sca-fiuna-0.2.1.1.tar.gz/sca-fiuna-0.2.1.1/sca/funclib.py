import cmath
from control.matlab import TransferFunction
from control.xferfcn import tf

def phase(V):
    """
    function phase:

    receive one or vector of complex numbers and return the vector of phase
    angle respect the origin on radian

    num: complex single or vector of complex

    def: single number or vector of phases
    """
    if not type(V) == type([]): V = [V]
    fases = [cmath.phase(Poriginal) for Poriginal in V]
    if len(fases) == 1: return fases[0]
    return fases

def phased(V):
    """
    function phased:

    receive one or vector of complex numbers and return the vector of phase
    angle respect the origin on deg

    num: complex single or vector of complex

    def: single number or vector of phases
    """
    fases = phase(V)
    if not type(fases) == type([]): fases = [fases]
    fases = [fase*180/cmath.pi for fase in fases]
    if len(fases) == 1: return fases[0]
    return fases

def evals(G, Pole):
    """
    function evals:

    Receive a TransferFunction and one complex number s and evaluate in

    G: TransferFunction
    Pole: complex number

    return the complex number of result

    """
    return G.horner(Pole)[0][0]

def zpk(zeros, poles, gain):
    """
    zero pole gain function

    Create a Transfer Function with the zero, pole and gain


    Inputs:

    zeros: zero list of the system
    poles: pole list of the system
    gain: gain of the system


    Output:

    G: the transfer function


    Example:

    G = zpk([0],[3,2],10)

            10*s
    G =  -----------
          s^2-5*s+6

    """

    s = tf("s")
    G = 1
    for i in zeros:
        z = s-i
        G = G*z
    for i in poles:
        p = s-i
        G = G/p
    return G*gain


def canon_controllable(sys):
  """
  Función canon_controllable(sys):

  input:
        sys: state space system 

  output:
        zsys: state space system
        T: matrix of transformation
  
  Recibe un sistema de tipo state space y devuelve otro sistema del mismo tipo 
  en su forma canónica controlable usando la matriz de transformación T
  
  A' = inv(T)*A*T
  B' = inv(T)*B
  C' = C*T
  D' = D

  Donde:
  T = M*W

  M = [B | A*B | A^2*B | ... | A^(n-1)*B | A^n*B]
  W = [[a_(n-1), a_(n-2), ... a_1, 1]
       [a_(n-2), a_(n-3), ...   1, 0]
       [a_(n-3), ... ,      1 , 0, 0]
            .
            .
            .
       [1, 0, 0,         ... 0, 0, 0]]
  """
  A = sys.A
  B = sys.B
  n = len(A)
  #Calcular la Matriz Mister
  M = eye(n)
  M[:,0] = B.T[0]

  #Calcular la matriz Wilson
  pol_car = poly(A).tolist()
  W = flip(eye(n),-1)
  aux = eye(n)
  pol_car.pop(0)
  pol_car = flip(pol_car, -1).tolist()
  for i in range(n-1):
    aux = aux*A
    aux2 = aux*B
    M[:,i+1] = aux2.T[0]
    pol_car.pop(0)
    m = len(pol_car)
    W[i,0:m] = pol_car
  
  T = matrix(M)*matrix(W)
  A = inv(T)*A*T
  B = inv(T)*B
  C = sys.C*T
  D = sys.D
  return ss(A,B,C,D), T
