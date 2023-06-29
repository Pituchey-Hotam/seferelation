# Welcome
This project is a tool to recommend what you should learn.  
Online beta version is available [here (bit.ly/seferelation)](https://bit.ly/seferelation)

# Developers Installation
First, clone this repository and go to the cloned directory.

Install dependencies:

python3 is required.
To install the requirements, run: 
```bash
sudo pip install -r src/requirements.txt
sudo pip install -e src/
```

You can generate the graph-model from the sefaria source sheets by running:
```bash
cd src/seferelation
python main.py
```
Or download it and put it in the `src/seferelation` directory. Contact me if you want to download. 

Now you can run the api server with the graph in it by running: 
```bash
cd src
uvicorn apiserver:app
```
