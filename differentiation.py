from parsing import parse_to_expt
from symbol_manipulation import *

__author__ = 'Adeel'


op_derivs = {'+': lambda f, g: ('+', derivate_expt(f), derivate_expt(g)),
             '-': lambda f, g: ('-', derivate_expt(f), derivate_expt(g)),
             '/': lambda f, g: (op_derivs['*'])(f, ('^', g, -1)),
             '*': lambda f, g: ('+', ('*', derivate_expt(f), g), ('*', f, derivate_expt(g))),
             '^': lambda f, g: ('+', ('*', ('^', f, g), ('*', derivate_expt(g), ('ln', f))),
                                ('*', ('*', derivate_expt(f), g), ('^', f, ('-', g, 1))))}

func_derivs = {'sin': lambda f: ('cos', f),
               'cos': lambda f: ('*', -1, ('sin', f)),
               'tan': lambda f: ('^', ('/', 1, ('cos', f)), 2),
               'asin': lambda f: ('/', 1, ('^', ('-', 1, ('^', f, 2)), 0.5)),
               'acos': lambda f: ('/', -1, ('^', ('-', 1, ('^', f, 2)), 0.5)),
               'atan': lambda f: ('/', 1, ('+', 1, ('^', f, 2))),
               'sec': lambda f: ('*', ('/', 1, ('cos', f)), ('tan', f)),
               'cosec': lambda f: ('*', ('/', -1, ('sin', f)), ('/', 1, ('tan', f))),
               'cot': lambda f: ('/', -1, ('^', ('sin', f), 2)),
               'ln': lambda f: ('/', 1, f),
               'log10': lambda f: ('/', 1, ('*', f, math.log(10))),
               'log2': lambda f: ('/', 1, ('*', f, math.log(2)))}


def derivate_expt(expt):
    if isinstance(expt, float) or isinstance(expt, int) or expt == 'e' or expt == 'pi':
        return 0
    if expt == 'x':
        return 1
    assert istuple(expt)
    if expt[0] in op_derivs:
        return (op_derivs[expt[0]])(expt[1], expt[2])
    if expt[0] in func_derivs:
        return '*', (func_derivs[expt[0]])(expt[1]), derivate_expt(expt[1])


def main():
    df = (derivate_expt(parse_to_expt(input('f(x) = '))))
    print(df)
    while True:
        tmp = simplify(flatten(df))
        if tmp == df:
            break
        df = tmp
    df = tmp
    print(df)
    print_exp_tree((df))

if __name__ == '__main__':
    main()