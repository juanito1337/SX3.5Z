# -*- coding: utf-8 -*-
"""Compile the recipe's normal-thickness formula into unit-consistent text.

Scope: t * sqrt(1 + sx*sx + sy*sy), where grades use numeric millimetres
in the recipe. All length parameters INSIDE sqrt are divided by a native
1-mm length reference. The leading thickness remains a length. This is not
a general dimensional-inference engine and never evaluates Python code.
The Number_mm compatibility mode deliberately omits the length reference.
"""
import ast
import math
import re

VERSION = '07.3'


def _checked(text, known, unitless):
    root = ast.parse(str(text), mode='eval').body
    if not (isinstance(root, ast.BinOp) and isinstance(root.op, ast.Mult)
            and isinstance(root.left, ast.Name)
            and isinstance(root.right, ast.Call)
            and isinstance(root.right.func, ast.Name)
            and root.right.func.id == 'sqrt'
            and len(root.right.args) == 1 and not root.right.keywords):
        raise ValueError('Normaldickenformel muss die Form dicke*sqrt(...) haben.')
    if root.left.id not in known or root.left.id in unitless:
        raise ValueError('Normaldicke muss ein bekannter Laengenparameter sein.')
    names = set()

    def validate(node):
        if isinstance(node, ast.Constant) and type(node.value) in (int, float):
            if not math.isfinite(float(node.value)):
                raise ValueError('Nicht endlicher Zahlenwert in Normaldickenformel.')
        elif isinstance(node, ast.Name):
            if node.id not in known:
                raise ValueError('Unbekannter Variablenname in Normaldickenformel: '+node.id)
            names.add(node.id)
        elif isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.USub, ast.UAdd)):
            validate(node.operand)
        elif isinstance(node, ast.BinOp) and isinstance(node.op, (ast.Add, ast.Sub, ast.Mult, ast.Div)):
            validate(node.left); validate(node.right)
        else:
            raise ValueError('Nicht unterstuetzte Normaldickenformel: '+ast.dump(node))
    validate(root.right.args[0])
    return root, names - set(unitless)


def needs_length_reference(text, known, unitless=()):
    """Validate the full expression before allocating any native helper."""
    _, length_names = _checked(text, known, unitless)
    return bool(length_names)


def normal_thickness_rhs(text, known, unitless=(), length_reference=None):
    """Return NX arithmetic; reference=None means numeric mm compatibility.

    Caller must create and verify length_reference = 1 in a millimetre part,
    using the same typed factory as the actual model parameters. No mm unit
    syntax or new NX API is assumed here.
    """
    root, length_names = _checked(text, known, unitless)
    if length_reference is not None and not re.fullmatch(r'sx_aux_[0-9]+', length_reference):
        raise ValueError('Ungueltiger Name der nativen Millimeterreferenz.')
    operators = {ast.Add: '+', ast.Sub: '-', ast.Mult: '*', ast.Div: '/'}

    def emit(node):
        if isinstance(node, ast.Constant):
            return repr(node.value)
        if isinstance(node, ast.Name):
            name = 'sx_'+node.id
            if length_reference is not None and node.id in length_names:
                return '('+name+'/'+length_reference+')'
            return name
        if isinstance(node, ast.UnaryOp):
            return '('+('-' if isinstance(node.op, ast.USub) else '+')+emit(node.operand)+')'
        if isinstance(node, ast.BinOp):
            return '('+emit(node.left)+operators[type(node.op)]+emit(node.right)+')'
        raise ValueError('Ungepruefter Formelknoten.')
    return 'sx_'+root.left.id+'*sqrt('+emit(root.right.args[0])+')'
