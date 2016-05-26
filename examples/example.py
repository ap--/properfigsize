"""Example python script showing how to use properfigsize

"""
TEX_FILE = 'document.tex'

import properfigsize
properfigsize.set_tex(TEX_FILE)

import matplotlib
import matplotlib.pyplot as plt
matplotlib.rcParams.update({'font.size': 10})

FigsizeFigure1 = properfigsize.Figsize('figure1.pdf', ratio=4.0/2.0)
plt.figure(figsize=FigsizeFigure1, tight_layout=True)
plt.plot([1,2,3], [3,6,7], 'r-')
plt.savefig('figure1.pdf')

FigsizeFigure2 = properfigsize.Figsize('figure2.pdf', ratio=4.0/3.0)
plt.figure(figsize=FigsizeFigure2, tight_layout=True)
plt.plot([1,2,3], [4,2,1], 'g-')
plt.savefig('figure2.pdf')

FigsizeFigure3 = properfigsize.Figsize('figure3.pdf', ratio=3.0/2.0)
plt.figure(figsize=FigsizeFigure3, tight_layout=True)
plt.plot([1,2,3], [5,2,4], 'b-')
plt.savefig('figure3.pdf')

