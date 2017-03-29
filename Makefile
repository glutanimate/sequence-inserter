# builds zip file for AnkiWeb (among other things)

VERSION = `git describe HEAD --tags --abbrev=0`
ADDON = "sequence-inserter"
ADDONDIR = "sequence_inserter"

all: zip

clean:
	rm -rf dist
	rm $(ADDON)-*.zip

zip:
	rm -rf dist
	mkdir -p dist
	find . -name '*.pyc' -delete
	cp *.py dist/
	cp -r $(ADDONDIR) dist/
	cd dist && zip -r ../$(ADDON)-current.zip *
	rm -rf dist

release:
	rm -rf dist
	mkdir -p dist
	find . -name '*.pyc' -delete
	git archive --format tar $(VERSION) | tar -x -C dist/
	cd dist &&  \
		zip -r ../$(ADDON)-release-$(VERSION).zip $(ADDONDIR) *.py
	rm -rf dist