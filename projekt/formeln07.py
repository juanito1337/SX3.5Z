"""Safe arithmetic, extended only by sqrt for normal sheet thickness.
Never eval, attributes, arbitrary function calls or imports. Parse tree cache
contains syntax only; values are resolved afresh on every call.
"""
import ast
import math
from functools import lru_cache

@lru_cache(maxsize=32768)
def _parse(text):
    return ast.parse(text,mode='eval')

def evaluate(text,values):
    def rec(n):
        if isinstance(n,ast.Expression):return rec(n.body)
        if isinstance(n,ast.Constant) and type(n.value) in (int,float):return float(n.value)
        if isinstance(n,ast.Name) and n.id in values:
            v=values[n.id]
            if isinstance(v,bool):raise ValueError('Boolean ist kein Mass')
            return float(v)
        if isinstance(n,ast.UnaryOp) and isinstance(n.op,(ast.UAdd,ast.USub)):
            return rec(n.operand)*(-1 if isinstance(n.op,ast.USub) else 1)
        if isinstance(n,ast.BinOp):
            a,b=rec(n.left),rec(n.right)
            if isinstance(n.op,ast.Add):return a+b
            if isinstance(n.op,ast.Sub):return a-b
            if isinstance(n.op,ast.Mult):return a*b
            if isinstance(n.op,ast.Div):return a/b
        if (isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='sqrt'
            and len(n.args)==1 and not n.keywords):return math.sqrt(rec(n.args[0]))
        raise ValueError('Nicht unterstuetzter Ausdruck: '+str(text))
    if isinstance(text,bool):raise ValueError('Boolean ist kein Mass')
    result=float(text) if type(text) in (int,float) else rec(_parse(str(text)))
    if not math.isfinite(result):raise ValueError('Nicht endlicher Zahlenwert: '+str(text))
    return result
