# Image Classification

This project is a deep learning image classification task using TensorFlow and Keras. It includes training a CNN on a custom image dataset.


## Run Project Locally

### 1. Clone the project and change the directory:

```bash
git clone https://github.com/ashuguptahere/parspec-assignment.git
cd parspec-assignment
```


### 2. Install [uv](https://docs.astral.sh/uv/getting-started/installation/) for Linux:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```


### 3. To install all the requirements:
```bash
uv sync
```

### 4. Download and extract `dataset.zip` file:
```bash
gdown "https://drive.google.com/uc?id=1KQebmd59f_PT1taK0EsJF5DCSMcqxNYX"
unzip dataset.zip
```


### 5. Starting the `frontend` and `backend` servers and innstall all the dependencies:

```bash
uv run main.py
```


## Demo

Wait for few seconds to let the above script start both the frontend and backend services and then go to the link: ```http://localhost:5173/```