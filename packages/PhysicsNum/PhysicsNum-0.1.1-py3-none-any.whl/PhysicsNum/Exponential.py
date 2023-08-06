import numpy as np

def ExpRegression(xval, yval):
    """Takes an array of x-values, and y-values and perform a origin exponential regression, with least square method. Returns the function with corresponding constants, and the constants.
        One notes that f(x) = a* e^(-x/b) and thus returns the constants on the form (a,b)."""
    if not isinstance((xval, yval), (np.generic, np.ndarray)):
        if isinstance((xval, yval), (list, tuple)):
            xval, yval = np.array(xval), np.array(yval)
        else:
            raise TypeError("[ExpRegression]: Need a iterable as input.")
    if len(xval) != len(yval):
        raise KeyError("[ExpRegression]: Input xval and yval are not of the same size")
    try:
        A_Matrix = np.array([xval, -np.ones(len(xval))]).T
        A_Matrix_Transposed = A_Matrix.T
        A_AT_Inverse = np.linalg.inv(A_Matrix_Transposed.dot(A_Matrix))
        #Computation to find constants.
        Corrected_yval = np.log(yval)
        ylist = A_Matrix_Transposed.dot(Corrected_yval)
        Constants = A_AT_Inverse.dot(ylist)
        a = np.exp(Constants[1])
        b = Constants[0]
        Expfunc = lambda x: b[0] * np.exp(x/a[0])
        if np.isnan(Constants[0]) or np.isnan(Constants[1]):
            raise TypeError("[ExpRegression]: Performing edited version")
        return Expfunc, (b[0], a[0])
    except Exception as e:
        try:
            print("[ExpRegression]: Performing edited version")
            A_Matrix = np.array([xval, -np.ones(len(xval))]).T
            A_Matrix_Transposed = A_Matrix.T
            A_AT_Inverse = np.linalg.inv(A_Matrix_Transposed.dot(A_Matrix))
            #Computation to find constants.
            ylist1 = np.array([[arg + 1] for arg in yval])
            Corrected_yval = np.log(ylist1)
            ylist = A_Matrix_Transposed.dot(Corrected_yval)
            Constants = A_AT_Inverse.dot(ylist)
            a = np.exp(Constants[1])
            b = Constants[0]
            Expfunc = lambda x: b[0] * np.exp(x/a[0])
            return Expfunc, (b[0],a[0])
        except Exception as e:
            raise e
"""
xlist = (1,2,3,4,5,6,7,8,9)
ylist = (0,0,0,0,1,2,4,8,16)
print(ExpRegression(xlist, ylist))
"""
