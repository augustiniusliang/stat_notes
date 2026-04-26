"""Optional parameter module for tex2md.py.

Edit MACRO_RULES to customize LaTeX command expansion before conversion.
Rules are applied in order.
"""

MACRO_RULES = [
    (r"\\thermfrac\s*\{([^{}]*)\}\s*\{([^{}]*)\}\s*\{([^{}]*)\}", r"\\left( \\frac{\\partial \1}{\\partial \2} \\right)_{\3}"),
    (r"\\jacobian\s*\{([^{}]*)\}\s*\{([^{}]*)\}\s*\{([^{}]*)\}\s*\{([^{}]*)\}", r"\\frac{\\partial \\left(\1, \2\\right)}{\\partial \\left(\3, \4\\right)}"),
    (r"\\ppp\s*\{([^{}]*)\}\s*\{([^{}]*)\}", r"\\frac{\\partial \1}{\\partial \2}"),
    (r"\\tr(?![A-Za-z])", r"\\mathrm{tr}"),
    (r"\\bigzero(?![A-Za-z])", r"\\mbox{\\normalfont\\Large\\bfseries 0}"),
    (r"\\rvline(?![A-Za-z])", r"\\hspace*{-\\arraycolsep}\\vline\\hspace*{-\\arraycolsep}"),
]
