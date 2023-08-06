# scrinet

Modelling

Parts of this package were heavily influenced by the great `rompy` package by Chad R. Galley: https://bitbucket.org/chadgalley/rompy

## Development

```
conda create -n scrinet-dev python=3.7
```

### Tensorflow requirements

```
conda install tensorflow
pip install keras-tqdm
conda install -c conda-forge nodejs
jupyter labextension install @jupyter-widgets/jupyterlab-manager
```

### GPUs

You might need to install cuda. Try `nvcc --version`

```
conda install -c conda-forge cudatoolkit-dev
conda install tensorflow
conda install tensorflow-gpu
```
