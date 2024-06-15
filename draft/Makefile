all: pdf

# Define auxiliary and output directory
AUXDIR=.tmp
OUTDIR=.pdf

pdf:
	latexmk -pdf $(FILE).tex -auxdir="$(AUXDIR)" -outdir="$(OUTDIR)"

# cd draft
# make FILE=IA_L/probability.anki