
# A simple paper makefile
# 2008 (c) Sergio Fernandez

DESTDIR =
NAME = vapour
COMPILER = rubber --pdf
SALT = /usr/local/salt/salt.sh
PDFVIEWER = evince

all:	compile

compile:	
	$(COMPILER) $(NAME).tex

salt:
	$(SALT) -input $(NAME).tex  -dirty -nocompile $(NAME).pdf -style lncs

view:	compile
	$(PDFVIEWER) $(NAME).pdf &

clean:
	rm -f $(NAME).log $(NAME).blg $(NAME).pdf $(NAME).pdf.rdf $(NAME).aux $(NAME).bbl $(NAME).text.backup
	rm -f `find . -name "*~"`




