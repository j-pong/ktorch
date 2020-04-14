# If a Python interpreter is specified, then creates a virtualenv from it
# PYTHON := /usr/bin/python3.7
PYTHON :=
# The python version installed in the conda setup
PYTHON_VERSION := 3.7.3
CUPY_VERSION := 6.0.0
CUDA_VERSION := 10.0
TH_VERSION := 1.0.0
ifeq ($(shell expr $(strip $(subst .,,$(TH_VERSION))) \< 120), 1)
INSTALL_WARPCTC := 1
else
INSTALL_WARPCTC :=
endif
# Use a prebuild Kaldi to omit the installation
KALDI :=
WGET := wget --tries=3

# Both Miniconda2/3 can install any Python versions
CONDA_URL := https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh
# PyTorch>=1.0.0 requires gcc>=4.9 when buliding the extensions
GCC_VERSION := $(shell gcc -dumpversion)


ifneq ($(shell which nvidia-smi),) # 'nvcc' found
CONDA_PYTORCH := pytorch=$(TH_VERSION) cudatoolkit=$(CUDA_VERSION)
else
CONDA_PYTORCH := pytorch-cpu=$(TH_VERSION)
endif


.PHONY: all clean

all: kaldi.done python

python: venv warp-ctc.done

ifneq ($(strip $(KALDI)),)
kaldi.done:
	test -d $(KALDI)
	ln -s $(abspath $(KALDI)) kaldi
	touch kaldi.done
else
kaldi.done:
	test -d kaldi || git clone https://github.com/kaldi-asr/kaldi.git
	cd kaldi/tools; $(MAKE) all
	cd kaldi/src; ./configure --shared --use-cuda=no; $(MAKE) depend; $(MAKE) all
	touch kaldi.done
endif


ifneq ($(strip $(PYTHON)),)
venv:
	test -d venv || virtualenv -p $(PYTHON) venv
ktorch.done: venv
	. venv/bin/activate; pip install pip --upgrade
	. venv/bin/activate; pip install -e ..
	. venv/bin/activate; pip install torch==$(TH_VERSION)
	touch ktorch.done
else
miniconda.sh:
	test -f miniconda.sh || $(WGET) $(CONDA_URL) -O miniconda.sh
venv: miniconda.sh
	test -d $(PWD)/venv || bash miniconda.sh -b -p $(PWD)/venv
	. venv/bin/activate && conda install -y setuptools -c anaconda
	. venv/bin/activate && conda install -y pip -c anaconda
	. venv/bin/activate && conda update -y conda
	. venv/bin/activate && conda install -y python=$(PYTHON_VERSION)
	. venv/bin/activate && conda info -a
ktorch.done: venv
	. venv/bin/activate && conda install -y $(CONDA_PYTORCH) -c pytorch
	. venv/bin/activate && pip install -e ..
	touch ktorch.done
endif

warp-ctc.done: ktorch.done
ifneq ($(strip $(INSTALL_WARPCTC)),)
	if . venv/bin/activate && python -c 'import torch as t;major=t.__version__.split(".")[0];assert major == "1"' &> /dev/null; then \
		if [ ! -z "$(strip $(CUPY_VERSION))" ]; then \
			. venv/bin/activate && pip install warpctc-pytorch10-cuda$(strip $(subst .,,$(CUDA_VERSION))); \
		else \
			. venv/bin/activate && pip install warpctc-pytorch10-cpu; \
		fi \
	else \
		rm -rf warp-ctc; \
		git clone https://github.com/espnet/warp-ctc.git; \
		cd warp-ctc; git checkout -b pytorch-0.4 remotes/origin/pytorch-0.4; \
		mkdir build && cd build && cmake .. && $(MAKE) && cd ..; \
		. ../venv/bin/activate; pip install cffi; cd pytorch_binding && python setup.py install; \
	fi
	touch warp-ctc.done
endif