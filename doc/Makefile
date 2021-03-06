# makefile for rendering documents from ReStructured Text

BIB4TXT=bib4txt.py
IMGMATHHACK=formatting/imgmathhack.py
ODTRESPACE=odt-respace
RST2ODT=rst2odt.py
UNOCONV=unoconv

STYLESODT=styles.odt
STYLESODTPATH=formatting/$(STYLESODT)

PAPER=subsample_interpolation
RESPONSE1=reviewer_1_response
RESPONSE2=reviewer_2_response

all: $(PAPER).doc $(RESPONSE1).doc $(RESPONSE2).doc

$(PAPER)_w_math.rst: $(PAPER).rst
	$(IMGMATHHACK) $(PAPER).rst $(PAPER)_w_math.rst

$(RESPONSE1)_w_math.rst: $(RESPONSE1).rst
	$(IMGMATHHACK) $(RESPONSE1).rst $(RESPONSE1)_w_math.rst

$(RESPONSE2)_w_math.rst: $(RESPONSE2).rst
	$(IMGMATHHACK) $(RESPONSE2).rst $(RESPONSE2)_w_math.rst

# add '-s example_numbered' for numbered references instead of last names
$(PAPER)_w_cite.rst: $(PAPER)_w_math.rst $(PAPER).bib
	PYTHONPATH='./formatting' $(BIB4TXT) -s my_numbered --all -i $(PAPER)_w_math.rst -no $(PAPER)_w_cite.rst $(PAPER).bib

$(PAPER).odt: $(PAPER)_w_cite.rst $(STYLESODTPATH)
	$(RST2ODT) --stylesheet=$(STYLESODTPATH) $(PAPER)_w_cite.rst $(PAPER).odt

$(RESPONSE1).odt: $(RESPONSE1)_w_math.rst $(STYLESODTPATH)
	$(RST2ODT) --stylesheet=$(STYLESODTPATH) $(RESPONSE1)_w_math.rst $(RESPONSE1).odt

$(RESPONSE2).odt: $(RESPONSE2)_w_math.rst $(STYLESODTPATH)
	$(RST2ODT) --stylesheet=$(STYLESODTPATH) $(RESPONSE2)_w_math.rst $(RESPONSE2).odt

$(PAPER)_double_spaced.odt: $(PAPER).odt
	$(ODTRESPACE) $(PAPER).odt $(PAPER)_double_spaced.odt

$(RESPONSE1)_double_spaced.odt: $(RESPONSE1).odt
	$(ODTRESPACE) $(RESPONSE1).odt $(RESPONSE1)_double_spaced.odt

$(RESPONSE2)_double_spaced.odt: $(RESPONSE2).odt
	$(ODTRESPACE) $(RESPONSE2).odt $(RESPONSE2)_double_spaced.odt

$(PAPER).doc: $(PAPER)_double_spaced.odt
	$(UNOCONV) -f doc $(PAPER)_double_spaced.odt
	mv $(PAPER)_double_spaced.doc $(PAPER).doc

$(RESPONSE1).doc: $(RESPONSE1)_double_spaced.odt
	$(UNOCONV) -f doc $(RESPONSE1)_double_spaced.odt
	mv $(RESPONSE1)_double_spaced.doc $(RESPONSE1).doc

$(RESPONSE2).doc: $(RESPONSE2)_double_spaced.odt
	$(UNOCONV) -f doc $(RESPONSE2)_double_spaced.odt
	mv $(RESPONSE2)_double_spaced.doc $(RESPONSE2).doc

clean:
	rm -f $(shell find . -name '*.doc' -or -name '*.odt' -not -name $(STYLESODT) -or -name '*_w_cite.rst' -or -name '*_w_math.rst') mti* imgmath/*
