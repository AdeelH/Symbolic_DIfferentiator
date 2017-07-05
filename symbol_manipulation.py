from collections import deque
from functools import reduce
import operator
import math


precedence_levels = [['+', '-'], ['/', '*'], ['^']]
commutative_ops = ['+', '*']
arith_ops = ['+', '-', '*', '/']

operations = {
	'+': operator.add,
	'-': operator.sub,
	'/': operator.truediv,
	'*': operator.mul,
	'^': operator.pow
}

funcs = {
	'sin': math.sin,
	'cos': math.cos,
	'tan': math.tan,
	'asin': math.asin,
	'acos': math.acos,
	'atan': math.atan,
	'sec': lambda x: 1.0 / math.sin(x),
	'cosec': lambda x: 1.0 / math.cos(x),
	'cot': lambda x: 1.0 / math.tan(x),
	'ln': math.log,
	'log10': math.log10,
	'log2': math.log2
}


def istuple(arg):
	return isinstance(arg, tuple)


def flatten(expt):
	def flattener(expt, parent_op):
		if istuple(expt):
			if expt[0] in operations:
				if expt[0] in commutative_ops:
					arg_ls = deque()
					for arg in expt[1:]:
						tmp = flattener(arg, expt[0])
						if isinstance(tmp, deque):
							arg_ls.extend(tmp)
						else:
							arg_ls.append(tmp)
					if expt[0] == parent_op:
						return arg_ls
					arg_ls.appendleft(expt[0])
					return tuple(arg_ls)
				if len(expt) > 3:
					if expt[0] == '-':
						return flattener(tuple(list(expt[:2]) + [tuple(['+'] + list(expt[2:]))]))
					if expt[0] == '/':
						return flattener(tuple(list(expt[:2]) + [tuple(['*'] + list(expt[2:]))]))
				if expt[0] in funcs:
					return expt[0], flattener(expt[1], None)
		return expt

	return flattener(expt, None)


def simplify_completely(expt, max_tries=100):
	for i in range(max_tries):
		tmp = simplify(flatten(expt))
		if tmp == expt:
			break
		expt = tmp
	return expt, i


def simplify(expt):
	if expt in ['x', 'e', 'pi']:
		return expt
	if istuple(expt):
		if expt[0] in arith_ops:
			consts = []
			vars = []
			for arg in expt[1:]:
				tmp = simplify(arg)
				if isinstance(tmp, float) or isinstance(tmp, int):
					if tmp == 0:
						if expt[0] == '*':
							return 0.0
						if expt[0] == '+':
							continue
					if tmp == 1:
						if expt[0] == '*':
							continue
						if expt[0] == '/' and arg == expt[2]:
							continue
					consts.append(tmp)
				else:
					vars.append(tmp)
			if not consts:
				if len(vars) > 1:
					return tuple([expt[0]] + vars)
				if not vars:
					if expt[0] == '*':
						return 1.0
					if expt[0] == '+':
						return 0.0
				return vars[0]
			if not vars:
				return reduce(lambda x, y: (operations[expt[0]])(x, y), consts[1:], consts[0])
			return tuple([expt[0]] + [reduce(lambda x, y: (operations[expt[0]])(x, y), consts[1:], consts[0])] + vars)
		if expt[0] in funcs:
			return expt[0], simplify(expt[1])
		if expt[0] == '^':
			b = simplify(expt[1])
			e = simplify(expt[2])
			if isinstance(b, float) and isinstance(e, float):
				return float(b**e)
			if b == 0:
				return 0
			if b == 1:
				return 1
			if e == 0:
				return 1
			if e == 1:
				return b
			return expt[0], b, e
		raise Exception
	return float(expt)


# def simplify_vars(expt):
#     if not (istuple(expt) or expt[0] == '+' or '*'):
#         return expt
#     seen = []
#     for term in expt[1:]:
#         if not istuple(term):
#             comm = term
#         else:
#             comm =


def equiv(expt1, expt2):
	def list_equiv(ls1, ls2):
		return set(ls1) == set(ls2)

	if not (istuple(expt1) and istuple(expt2)):
		return expt1 == expt2
	if expt1[0] == expt2[0] and len(expt1) == len(expt2):
		ls1 = list(expt1[1:])
		ls2 = list(expt2[1:])
		return list_equiv(ls1, ls2)


def expt_to_string(expt):
	if istuple(expt):
		if expt[0] in operations:
			exp = ""
			for arg in expt[1:-1]:
				if istuple(arg):
					exp += "({0}){1}".format(expt_to_string(arg), expt[0])
				else:
					exp += "{0}{1}".format(arg, expt[0])
			arg = expt[len(expt) - 1]
			if istuple(arg):
				exp += "({0})".format(expt_to_string(arg), expt[0])
			else:
				exp += "{0}".format(arg, expt[0])
			return exp
		if expt[0] in funcs:
			return '{0}({1})'.format(expt[0], expt_to_string(expt[1]))
	else:
		return str(expt)


def test():
	assert equiv('x', 'x')
	assert not equiv('x', ('*', 'x', 2))
	assert equiv(('+', 'x', 1), ('+', 1, 'x'))
	assert equiv(('+', 'x', 1, ('*', 2, 2)), ('+', 1, 'x', ('*', 2, 2)))
	print('All tests passed')


if __name__ == '__main__':
	test()
