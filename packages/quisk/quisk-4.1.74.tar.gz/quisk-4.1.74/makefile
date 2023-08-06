.PHONY: quisk

quisk:
	@echo 'Please specify either quisk2 or quisk3 for Python 2 or 3'

quisk2:
	python2 setup.py build_ext --force --inplace
	@echo
	@echo 'Use "make soapy2" to make the Python2 soapy module'
	@echo 'Use "make perseus2" to make the Python2 perseus package'
	@echo 'Use "make afedrinet2" to make the Python2 afedrinet package'

quisk3:
	python3 setup.py build_ext --force --inplace
	@echo
	@echo 'Use "make soapy3" to make the Python3 soapy module'
	@echo 'Use "make perseus3" to make the Python3 perseus package'
	@echo 'Use "make afedrinet3" to make the Python3 afedrinet package'

soapy2:
	(cd soapypkg; make soapy2)

soapy3:
	(cd soapypkg; make soapy3)

afedrinet2:
	(cd afedrinet; make afedrinet2)

afedrinet3:
	(cd afedrinet; make afedrinet3)

perseus2:
	(cd perseuspkg; make perseus2)

perseus3:
	(cd perseuspkg; make perseus3)
