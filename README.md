# HEALTH MANAGEMENT SYSTEM


## STEPS TO RUN THE BACKEND
### STEPS 01:- Clone the repositorygit

```bash
git clone git@github.com:SUMITDHAKAD0/docker_ollama_fastapi.git
```

### STEP - For Docker 

```bash
sudo docker-compose up
```

## STEP - For For Backend Test 
### STEP 02- Create a conda environment after opening the repository

```bash
# Using conda
conda create -n envname python=3.10 -y
```

```bash
# Using Python environment
python3.10 -m venv venv
```

### STEP 03- Activate envoronment
```bash
conda activate envname
```
```bash
# Linux
source venv/bin/activate
# Windows
venv/script/activate
```

### STEP 04- install the requirements
```bash
pip install -r backend/requirements.txt
```

### STEP 05- RUN Backend
```bash
uvicorn backend.api_main:app --reload
```

