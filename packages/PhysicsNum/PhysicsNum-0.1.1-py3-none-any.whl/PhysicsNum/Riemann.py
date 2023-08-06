
def RiemanSum(f, a, b, Increment = 0.0001):
    """One dimensional function that returns the riemansum between two points; This implies that the function has the property of Rieman integrability."""
    if not callable(f):
        raise TypeError("[Rieman.py]: Function RiemanSum needs the input function f to be callabe")
    h = Increment #Just a small number
    rie = []
    if not a < b:
        raise ValueError("[Rieman.py] Input a has to be smaller than input b.")
    while a < b:
        rie.append(f(a)*h)
        a += h
    return sum(rie)
