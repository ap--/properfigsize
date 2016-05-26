# properfigsize

Use the proper figure size for your matplotlib plots that you embed in a PDF with pdflatex.
Finally no more stupid font size scaling after you created all your plots and compile you PDF.

## Usage

Look at the example in the examples folder. Let's say you want to create a PDF with 2 plots.
One of them is going to be one column wide in your two column document, the other plot will
be two columns wide. You know the aspect ratios your plots should have, but not the final
sizes in your document. With **properfigsize** you can use a placeholder figsize which will
be set to the correct size, after running your plotting script twice. It's important that
you use `tight_layout=True` when creating your matplotlib figure.

## Installation

```
pip install git+https://github.com/ap--/properfigsize.git
```

## Run the example

You need pdflatex and matplotlib. To see the resulting document.pdf file, run:
```
python example.py  # first pass
python example.py  # second pass, figures now have the correct size
pdflatex document.tex
```
