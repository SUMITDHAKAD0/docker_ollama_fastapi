# HEALTH MANAGEMENT SYSTEM


## STEPS TO RUN THE BACKEND
### STEPS 01:- Clone the repository

```bash
git clone git@github.com:VergeImpex/health_backend.git
```

### STEP 02- Create a conda environment after opening the repository

```bash
# Using conda
conda create -n envname python=3.12 -y
```

```bash
# Using Python environment
python3.12 -m venv venv
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
pip install -r requirements.txt
```

### STEP 05- RUN Backend
```bash
uvicorn api_main:app --reload
```

