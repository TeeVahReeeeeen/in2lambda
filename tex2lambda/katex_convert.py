# -*- coding: utf-8 -*-
"""
Created on Wed Jul  5 19:13:28 2023

@author: Matthew Howarth
"""
import re


def latex_to_katex(latex_string: str) -> str:
    # Replace incompatible LaTeX functions with KaTeX compatible equivalents
    katex_string = replace_incompatible_functions(latex_string)
    
    return katex_string


def replace_incompatible_functions(latex_string: str) -> str:
    # dictionary of LaTeX functions to replace
    replacements = {
        
        #delete page formatting functions:
        #these are in-place if a user inserts their entire document into the converter.

        r"\\usepackage\{.*?}": r"", #delete package imports
        r"\\lhead\{.*?}": r"", #adds text to header. in future, text should be passed out
        r"\\pagestyle\{.*?}": r"",
        r"\\setcounter\{.*?}+{.*?}": r"",
        r"\\documentclass\[.*?]+{.*?}": "", #delete document class and arguments   
        
        #delete references:

        r"\\label{.*?}": r"",  # delete label and argument
        r"\\ref": r"",  # delete ref but leave name
        r"\\eqref": r"", # delete ref but leave name
        r"\\caption{.*?}": r"",  # delete caption and argument
        
        #begin functions: either deleted or replaced with alternative: 

        r"\\begin{figure}": r"",  # delete centerline and argument
        r"\\begin{document}": r"", 
        r"\\end{document}": r"",  
        r"\\end{figure}": r"",  # delete centerline and argument
        r"\\begin{center}": r"",  # delete centerline and argument
        r"\\end{center}": r"",  # delete centerline and argument
        r"\\begin{enumerate}": r"",
        r"\\end{enumerate}": r"",
        r"\\item": r"",
        r"\\begin{problem}": r"",  #may need an alternative
        r"\\end{problem}": r"",  #may need an alternative
        r"\\begin{tabular}": r"",
        r"\\end{tabular}": r"",  
        r"\\begin{flushright}+(.*?)": r"",
        r"\\end{flushright}+(.*?)": r"",
        r"\\begin{eqnarray}": r"\\begin{align}",  # KaTeX does not support eqn array: replace with align
        r"\\end{eqnarray}": r"\\end{align}",
        r"\\begin{eqnarray\*}": r"\\begin{align*}",  # KaTeX does not support eqn array: replace with align
        r"\\end{eqnarray\*}": r"\\end{align*}",
        r"\\begin{eqalign}": r"\\begin{align}",
        r"\\end{eqalign}": r"\\end{align}",
        r"\\begin{align\*}": r"\\begin{align*}",
        r"\\end{eqalign\*}": r"\\end{align*}",
        
        #deleting unsupported formatters:
    
        r"\\centerline": r"",  # delete centerline and argument
        r"\\bigskip": r"",
        r"\\medskip": r"",
        r"\\smallskip": r"",  # skipping functions are unsupported
        r"\\noindent": r"",
        r"\\vrulefill": r"",
        r"\\vfill": r"",
        r"\\vfil": r"",
        r"\\hrulefill": r"",
        r"\\hfill": r"",
        r"\\hfil": r"",
        r"\\hline": r"",
        r"\\vline": r"",
        #r"\\vspace\{.*?}": r"",
        #r"\\hspace\{.*?}": r"",
        r"\\setlength{.*?}": r"",
        r"\[h(!)?\]": r"", # remove alignments
        r"\[ht(!)?\]": r"",
        r"\[t(!)?\]": r"",
        r"\[b(!)?\]": r"",
        r"\[p(!)?\]": r"",
        r"\[!\]": r"",  
        r"\[H(!)?\]": r"",
        r"\{l+\}": r"",
        # r"[+-]?(\d*\.)?\d+pt": "",  # Matches ints or decimals followed by pt
        r"\{}": "",  # removes lone {} brackets  

        #delete delims:
        r"\\abovewithdelims": r"",
        r"\\atopwithdelims": r"",
        r"\\overwithdelims": r"",

        #exhaustive dictionary of unsupported functions, either deleted or replaced with an alternative.
        #some functions are followed by arguments; all arguments are deleted.
        #we were not able to identify all functions with associated arguments due to a lack of LaTeX documentation
        #mostly alphabetical !
        r"\\and": r"",
        r"\\ang": r"\\angle",
        r"\\array": r"",
        r"\\Arrowvert": r"\\Vert",
        r"\\arrowvert": r"\\vert",
        r"\\bbox": r"",
        r"\\bfseries": r"\\textbf", #replace bfseries with textbf
        r"\\bigominus": r"", #may be supported in future
        r"\\bigoslash": r"", #may be supported in future
        r"\\bigsqcap": r"", #may be supported in future
        r"\\bracevert": r"",
        r"\\buildrel": r"",
        r"\\C": r"",
        r"\\cancelto": r"",
        r"\\cases": r"",
        r"\\cee": r"",
        r"\\cf": r"",
        r"\\class": r"", #may be supported in future
        r"\\cline": r"", #may be supported in future
        r"\\Coppa": r"",
        r"\\coppa": r"",
        r"\\cssld": r"",
        r"\\dddot": r"",
        r"\\ddddot": r"",
        r"\\DeclareMathOperator(\*)?\{.*?}+{.*?}": r"", #removes 2 associated arguments
        r"\\definecolor(\*)?\{.*?}+{.*?}+{.*?}": r"", #may be supported in future
        r"\\Digamma": r"",
        r"\\else": r"", #may be supported in future
        r"\\emph": r"\\textit",
        r"\\enclose\{.*?}+\[.*?]+{.*?}": r"",
        r"\\euro": r"",
        r"\\euro": r"€",
        r"\\idotint": r"", #may be supported in future
        r"\\iddots": r"", #may be supported in future
        r"\\if": r"", #may be supported in future
        r"\\fi": r"",
        r"\\ifmode": r"",
        r"\\ifx": r"",
        r"\\iiiint": r"", #only integrals up to triple int supported
        r"\\itshape": r"",
        r"\\Koppa": r"",
        r"\\koppa": r"",
        r"\\LeftArrow": r"\\leftarrow",
        r"\\leftroot": r"",
        r"\\leqalignno": r"",
        r"\\lower": r"",
        r"\\mathtip": r"",
        r"\\mit": r"\\mathit",
        r"\\mbox": r"",
        r"\\md": r"",
        r"\\mdseries": r"",
        r"\\mmltoken": r"",
        r"\\moveleft": r"",
        r"\\moveright": r"",
        r"\\mspace": r"",
        r"\\multicolumn(\*)?\{.*?}+{.*?}+{.*?}": r"", #removes all 3 arguments
        r"{multiline}": r"",
        r"\\Newextarrow": r"",
        r"\\newcounter\{.*?}": r"",
        r"\\newenvironment\{.*?}?+\[.*?]+{.*?}+{.*?}": "",
        r"\\addtocounter\{.*?}+{.*?}": r"",
        r"\\normalfont": r"",
        r"\\oldstyle": r"",
        r"\\or": r"",
        r"\\overbracket": r"",
        r"\\pagecolor": r"",
        r"\\part": r"",
        r"\\Q": r"",
        r"\\newtheorem\{.*?}+{.*?}": r"",
        r"\\raise": r"",
        r"\\raisebox": r"",
        r"\\require\{.*?}": r"",
        r"\\root": r"",
        r"\\rule": r"\\Rule",
        r"\\newtheorem\{\}": r"",
        r"\\overparen": r"\\overgroup",
        r"\\Sampi": r"",
        r"\\sampi": r"",
        r"\\sc": r"", #may be supported in the future
        r"\\scalebox\{.*?}": r"",
        r"\\scr": r"\\mathscr",
        r"\\Space": r"\\space",
        r"\\setlength\{.*?}+{.*?}": r"", #may be supported in the future
        r"\\shoveleft": r"",
        r"\\shoveright": r"",
        r"\\sideset\{.*?}+{.*?}": r"",
        r"\\SI": r"",
        r"\\unit": r"",
        r"\\skew": r"",
        r"\\skip": r"",
        r"\\sl": r"",
        r"\\smiley": r"",
        r"\\Stigma": r"",
        r"\\stigma": r"",
        r"\\strut": r"",
        r"\\style": r"",
        r"\{subarray}": r"",
        r"\\textsl": r"",
        r"\\texttip": r"",
        r"\\textvisiblespace": r"",
        r"\\Tiny": r"\\tiny",
        r"\\toggle": r"",
        r"\\unicode": r"",
        r"\\up": r"",
        r"\\uproot": r"",
        r"\\upshape": r"",
        r"\\underparen": r"\\undergroup",
        r"\\overparen": r"\\overgroup",
        r"\\overbracket": r"\\overbrace", #overbracket not supporte, replace with brace
        r"\\underbracket": r"\\underbrace",
        r"\\varcoppa": r"",
        r"\\varstigma": r"",
        r"\\wideparen": r"", #may be supported in the future

    }

    # replace the incompatible functions with their KaTeX equivalents using re.sub
    for old, new in replacements.items():
        latex_string = re.sub(old, new, latex_string)
        

    return latex_string

    


if __name__ == "__main__":
    latex_input = r"""\begin{eqnarray}
$x^2+x+2=0$
\emph{Solve this equation}
\end{align}
"""


    katex_output = latex_to_katex(latex_input)
    print(katex_output)
