LIBDIR := lib
include $(LIBDIR)/main.mk

# Apply the otpauth.dev look to the HTML editor's copy (see theme/apply.py).
# This rule has the same target and prerequisites as the one in main.mk, so its recipe replaces that one.
# The recipe is main.mk's, plus the final apply.py line.  If apply.py fails, the plain page is kept.
%.html: %.xml $(XML2RFC_CSS) $(DEPS_FILES)
	$(at)$(trace) $@ -s xml2rfc-html $(xml2rfc) $(XML2RFC_HTML) $< -o $@
	@-sed -i.rfc-local -e 's,<link[^>]*href=["'"'"]rfc-local.css["'"'"][^>]*>,,' $@; rm -f $@.rfc-local
ifneq (,$(FAVICON))
	@-sed -i.favicon -e '/<link[^>]*rel="license">/{p;c \'$$'\n''$(FAVICON)'$$'\n'';}' $@; rm -f $@.favicon
endif
	@python3 theme/apply.py $@ || echo "warning: theme/apply.py failed; keeping the unthemed $@" 1>&2

$(drafts_html): $(wildcard theme/*)

$(LIBDIR)/main.mk:
ifneq (,$(shell grep "path *= *$(LIBDIR)" .gitmodules 2>/dev/null))
	git submodule sync
	git submodule update --init
else
ifneq (,$(wildcard $(ID_TEMPLATE_HOME)))
	ln -s "$(ID_TEMPLATE_HOME)" $(LIBDIR)
else
	git clone -q --depth 10 -b main \
	    https://github.com/martinthomson/i-d-template $(LIBDIR)
endif
endif
