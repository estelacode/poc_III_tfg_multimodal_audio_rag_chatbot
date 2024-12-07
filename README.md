# poc_llamaindex_chromadb

### Create Environment 
```bash
conda create --name gen_ai python=3.12
```

### Activate Environment
```bash
conda activate gen_ai
```
### Install Poetry
```bash
conda install -c conda-forge poetry
poetry --version 
```

# Create Project Poetry
```bash
poetry new --src poc_llamaindex_chromadb 
```

# Convert an existing unversioned project to a Git repository
```bash
git init
```

# Configure remote repository 
```bash
git remote add <name> <url>
## git remote add poc_llamaindex_chromadb https://github.com/estelacode/poc_llamaindex_chromadb.git
```

# To push the current branch and set the remote as upstream
```bash
git push --set-upstream poc_llamaindex_chromadb master

```

# ClipEmbedding requires: pip install git+https://github.com/openai/CLIP.git and torch
```bash
pip install git+https://github.com/openai/CLIP.git

```

