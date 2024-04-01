# Spectral library storage app

This app enables the storage of fragmentation spectra acquired by fragmentations lists.

After installing the `regfilter` environment, to use it, first, create the folders to store the fragmentation list (`spls`), the MSMS spectra generated from the list (`mzmls`) and a folder to store the databases (`dbs`).


```
mkdir static
mkdir static/spls static/mzmls static/dbs
```

After the creation of these folders, run the application with

```
conda activate regfilter 
python app.py
```

