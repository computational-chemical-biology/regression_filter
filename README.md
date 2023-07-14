# regFilter 
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](http://colab.research.google.com/github/computational-chemical-biology/regression_filter/blob/main/notebooks/regression_filter.ipynb)

<p align="center">
  <img src="https://github.com/computational-chemical-biology/blob/main/img/logo.png" alt="logo"/>
</p>

ChemWalker is a python package to propagate spectral library match identities through candidate structures provided by _in silico_ fragmentation, using [random walk](https://github.com/jinhongjung/pyrwr).

## Installation

Install conda

```
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh

```
   
Create a dedicated conda environment and activate

```
conda env create -f environment.yml
conda activate regfilter 
pip install git+https://github.com/computational-chemical-biology/regression_filter.git
```

### License

This project is licensed under the BSD 3-Clause License - see the [LICENSE](LICENSE) file for details

