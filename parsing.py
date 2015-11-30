from symbol_manipulation import *

__author__ = 'Adeel'


def skip_parens(exp, ind, depth=1):
    if depth == 0:
        ind = exp.find(')')
        if ind != -1:
            depth = 1
    while depth > 0:
        ind -= 1
        if exp[ind] == ')':
            depth += 1
        if exp[ind] == '(':
            depth -= 1
    return ind - 1


def parse(exp):
    assert isinstance(exp, str)
    if not exp:
        return lambda x: 0

    if exp == 'x':
        return lambda x: float(x)

    if exp == 'e':
        return lambda x: math.e

    for level in precedence_levels:
        i = 0
        while i < len(exp):
            if exp[i] == '(':
                i = skip_parens(exp, i)
                continue
            if exp[i] in level:
                return lambda x: (operations[exp[i]])(parse(exp[: i])(x), parse(exp[i + 1:])(x))
            i += 1

    if len(exp) > 2:
        if exp[0] == '(' and exp[-1] == ')':
            return parse(exp[1: -1])
        open_paren = exp.find('(')
        if exp[: open_paren] in funcs:
            return lambda x: (funcs[exp[: open_paren]])(parse(exp[open_paren + 1: exp.find(')')])(x))
        if exp[: open_paren] == 'log':
            return lambda x: math.log(parse(exp[open_paren + 1: exp.find(',')])(x)) / math.log(
                parse(exp[exp.find(',') + 1: exp.find(')')])(x))

    return lambda x: float(exp)


def parse_to_expt(exp):
    assert isinstance(exp, str)
    if not exp:
        return 0

    if exp == 'x':
        return exp

    for level in precedence_levels:
        i = len(exp) - 1
        while i >= 0:
            if exp[i] == ')':
                i = skip_parens(exp, i)
                continue
            if exp[i] in level:
                # if exp[i] == '/':
                #     return '*', parse_to_expt(exp[: i]), ('^', parse_to_expt(exp[i + 1:]), -1)
                return exp[i], parse_to_expt(exp[: i]), parse_to_expt(exp[i + 1:])
            i -= 1

    if len(exp) > 2:
        if exp[0] == '(' and exp[-1] == ')':
            return parse_to_expt(exp[1: -1])
        open_paren = exp.find('(')
        if exp[: open_paren] in funcs:
            return exp[: open_paren], parse_to_expt(exp[open_paren + 1: exp.find(')')])
        if exp[: open_paren] == 'log':
            return '/', ('ln', parse_to_expt(exp[open_paren + 1: exp.find(',')])), parse_to_expt(
                exp[exp.find(',') + 1: exp.find(')')])
    return float(exp)


def exp_to_func(exp):
    if exp == 'x':
        return lambda x: float(x)

    if exp == 'e':
        return lambda x: math.e

    if exp == 'pi':
        return lambda x: math.pi

    open_paren = exp.find('(')

    comma = exp.find(',', skip_parens(exp[open_paren + 1:], 0, 0)) if exp.find('(', open_paren + 1) < exp.find(
        ',') else exp.find(',')

    if exp[: open_paren] in operations:
        return lambda x: (operations[exp[: open_paren]])(exp_to_func(exp[open_paren + 1: comma])(x),
                                                         exp_to_func(exp[comma + 1: -1])(x))

    if exp[: exp.find('(')] in funcs:
        return lambda x: (funcs[exp[: open_paren]])(exp_to_func(exp[open_paren + 1: -1])(x))

    return lambda x: float(exp)


def expt_to_func(expt):
    if expt == 'x':
        return lambda x: float(x)

    if expt == 'e':
        return lambda x: math.e

    if expt == 'pi':
        return lambda x: math.pi

    if istuple(expt):
        if expt[0] in operations:
            return lambda x: (operations[expt[0]])(expt_to_func(expt[1])(x), expt_to_func(expt[2])(x))
        if expt[0] in funcs:
            return lambda x: (funcs[expt[0]])(expt_to_func(expt[1])(x))

    return lambda x: float(expt)
