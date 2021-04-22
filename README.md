# How to run 

## Classical way: ##

### 1. Clone the repository
>IMPORTANT: Before cloning the repository, navigate to the folder where the project will be stored.
```
git clone https://github.com/TvylorMvde/pytest-macmillan-ui-testing.git
```
### 3. Set up the virtual environment
* Create virtual environment:

    ```
    python -m venv venv
    ```
* Activate venv:
    - bash/zsh:

    ```
    source venv/bin/activate
    ```
    - Windows (cmd):

    ```
    venv\Scripts\activate.bat
    ```
    - Windows (PowerShell):

    ```
    venv\Scripts\Activate.ps1
    ```
### 4. Install all required packages
```
pip3 install -r requirements.txt
```
### 5. Download chromedriver
Navigate to https://chromedriver.chromium.org and download the latest stable release of chromedriver for your system.
>IMPORTANT: Extract the downloaded chromedriver file inside the cloned repository.

### 6. Run the tests
```
pytest test_module.py
```

## Using Docker 🐳

### 1. Install docker
* Navigate to [Get Started with Docker](https://www.docker.com/get-started) and download **Docker Desktop** compatible with your system.
* Install **Docker Desktop** following the on-screen instructions.
* Check in your terminal if Docker has been successfully installed:

    ```
    docker --version
    OR
    docker -v

    ## Docker version 20.10.5, build 55c4c88
    ```
### 2. Run the image's container from Docker Hub
```
docker run tvylormvde/test_macmillan:test_macmillan
```














