# Installation

## Locally 

1. Install Anaconda or Miniconda Package Manager from here
2. Create a new virtual environment and install the required packages.

```sh
conda create -n transformers python==3.8 pandas tqdm
conda activate transformers
```

If using cuda:
`conda install pytorch cudatoolkit=10.0 -c pytorch`

else:  

```sh
conda install pytorch -y
conda install -c anaconda scipy -y
conda install -c anaconda scikit-learn -y 
pip install transformers
pip install tensorboardx
```

3. Install simpletransformers.  

`pip install simpletransformers`  

4. Extract `train.csv` and `test.csv` and place them in a directory `data/`

```sh
# Untar the dataset
tar -xvzf ag_news_csv.tgz
# Create the data directory
mkdir data
# move the extracted data into it
mv ag_* data  
``` 

# Resource
https://medium.com/swlh/simple-transformers-multi-class-text-classification-with-bert-roberta-xlnet-xlm-and-8b585000ce3a



