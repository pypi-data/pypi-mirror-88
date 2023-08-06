import contextlib

from sympy.printing.conventions import split_super_sub
from sympy.printing.latex import translate


@contextlib.contextmanager
def translate_space_latex():
    from sympy.printing.latex import LatexPrinter

    _deal_with_super_sub = LatexPrinter._deal_with_super_sub

    def _deal_with_super_sub_expanded(self, string, style="plain"):
        """
        This function is expansion of _deal_with_super_sub (LatexPrinter's method)

        Copyright (c) 2006-2020 SymPy Development Team
        Copyright (c) 2013-2020 Sergey B Kirpichev
        Copyright (c) 2014 Matthew Rocklin
        Licensed under https://github.com/sympy/sympy/blob/master/LICENSE
        """
        if "{" in string:
            name, supers, subs = string, [], []
        else:
            name, supers, subs = split_super_sub(string)

            names = [translate(name) for name in name.split(" ")]
            supers = [translate(sup) for sup in supers]
            subs = [translate(sub) for sub in subs]

            name = " ".join(names)

        # apply the style only to the name
        if style == "bold":
            name = "\\mathbf{{{}}}".format(name)

        # glue all items together:
        if supers:
            name += "^{%s}" % " ".join(supers)
        if subs:
            name += "_{%s}" % " ".join(subs)

        return name

    LatexPrinter._deal_with_super_sub = _deal_with_super_sub_expanded

    try:
        yield
    finally:
        LatexPrinter._deal_with_super_sub = _deal_with_super_sub
