clean_translations:
	rm -f translations/*_en_US.ts translations/*_en_US.qm

translations:	translations/aranduka_en_US.qm translations/aranduka_es_AR.qm 

translations/aranduka_en_US.qm:	translations/aranduka_en_US.ts
	lrelease translations/aranduka_en_US.ts -compress -qm translations/aranduka_en_US.qm

translations/aranduka_en_US.ts:	*.py ui/*.ui
	pylupdate4 -verbose *.py */*.py ui/*.ui -ts translations/aranduka_en_US.ts

translations/aranduka_es_AR.qm:	translations/aranduka_es_AR.ts
	lrelease translations/aranduka_es_AR.ts -compress -qm translations/aranduka_es_AR.qm

translations/aranduka_es_AR.ts:	*.py ui/*.ui
	pylupdate4 -verbose *.py */*.py ui/*.ui -ts translations/aranduka_es_AR.ts

plugins_translations: plugins_qm

plugins_qm: plugins_ts
	for f in `ls plugins/`; do \
		if [ -d $$f ]; then \
			lrelease $$f/translations/en_US.ts -compress -qm $$f/translations/en_US.qm; \
			lrelease $$f/translations/es_AR.ts -compress -qm $$f/translations/es_AR.qm; \
		fi; \
	done

plugins_ts: 
	for f in `ls plugins/`; do \
		if [ -d $$f ]; then \
			mkdir -p $$f/translations && \
			pylupdate4 -verbose $$f/*.py $$f/*.ui -ts $$f/translations/en_US.ts && \
			pylupdate4 -verbose $$f/*.py $$f/*.ui -ts $$f/translations/es_AR.ts; \
		fi; \
	done
