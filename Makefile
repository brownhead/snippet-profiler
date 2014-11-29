.PHONY: serve dev-requirements

dev-requirements:
	virtualenv --prompt "(snip)" venv
	venv/bin/pip install nodeenv

serve:
	~/go_appengine/dev_appserver.py --log_level debug src/
