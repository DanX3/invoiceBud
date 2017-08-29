all: run

run: main.py
	python3 $<

.PHONY: invoice
invoice:
	@cd invoice && rm -f codes/* counts/*
	@echo "previous files removed"
	@cd invoice && convert -density 200 invoice.pdf -quality 100 codes/out.png
	@cp invoice/codes/* invoice/counts/
	@echo "Pages extracted"
	@echo "Now cut the correct areas"

.PHONY: parse
parse:
	cd invoice && bash parse.sh

compare: main.py
	python3 $< --compare
	sort booksExported > booksSorted
	sort invoiceExported > invoiceSorted
	rm booksExported invoiceExported
	vimdiff booksSorted invoiceSorted
