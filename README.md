# regFilter 
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](http://colab.research.google.com/github/computational-chemical-biology/regression_filter/blob/main/notebooks/regression_filter.ipynb)

<p align="center">
  <img src="https://github.com/gsarini/regression_filter/blob/main/logo/regfilter_logo.png" alt="logo" height="230" width="230"/>
</p>

## Installation

Install conda

```
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh

```
   
Create a dedicated conda environment and activate

```
conda env create -f regfilter_env.yml
conda activate regfilter 
pip install git+https://github.com/computational-chemical-biology/regression_filter.git
```

## Using the filter itself

Once installed, access the Python notebook building_spl_and_assessing_XIC_for_all_ions.ipynb to access the filtering algorithm. Enter the path where your .csv file is located and execute the cells as indicated in the notebook itself. After selecting the number of points to filter (npts=) and performing the feature filtering, a new .csv file with the features that meet the desired criteria will be exported to the notebooks directory of the package installed on your machine.

```
   

### License

This project is licensed under the BSD 3-Clause License - see the [LICENSE](LICENSE) file for details

