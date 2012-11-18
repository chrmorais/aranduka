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
