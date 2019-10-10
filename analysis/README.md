## Environment and dependencies

Install conda and get all the dependencies:
```
curl -O -L https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh -b 

# adds conda to the end of ~/.bashrc, so relogin after executing this line
~/miniconda3/bin/conda init

# stops conda from activating the base environment on login
conda config --set auto_activate_base false
conda config --add channels conda-forge

conda create --name analysisenv uproot matplotlib pandas jupyter numba -y
```

Start analysis jupyter notebook:
```bash
conda activate analysisenv 
jupyter notebook --no-browser

# then execute on your local computer to forward the port, and visit the url
ssh -N -f -L localhost:1234:localhost:1234 uaf-10.t2.ucsd.edu
```
