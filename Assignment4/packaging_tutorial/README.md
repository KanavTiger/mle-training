# Python Package Installation

Just go through this tutorial : "https://packaging.python.org/en/latest/tutorials/packaging-projects/" quite handy and usefull.

This repository contains a Python package that can be installed and used easily. Below are the steps to install and test the package.

## Installation Instructions
### Using Wheel (.whl) File
1. Download the .whl file from the distribution archive.
2. Install the package with:

  ```bash
   pip install /path/to/package_name.whl
   ```

### Using Source Distribution (.tar.gz) File
1. Download the .tar.gz file from the distribution archive.
2. Extract the file:
    ```bash
    tar -xvzf package_name.tar.gz
    ```

3. Navigate to the extracted folder:
    ```bash
    cd package_name/
    ```

4. Install the package:
    ```bash
        pip install .
    ```

Testing the Installation
Create a file test_installation.py with the following content

## Testing the Installation
Create a file 'test_installation.py' with the following content:
    ```bash
    import package_name
    print(package_name.__version__)
    ```

Run the script:
    ```bash
        python test_installation.py
    ```

If installed correctly, it will print the version of the package.

## Running the Application
To run the application, use the command:
    ```bash
        command
    ```

## Dependencies
Dependencies are listed in the env.yml file. To install them, run:
    ```bash
        conda env create -f env.yml
    ```

Activate the environment:
    ```bash
        conda activate your_environment_name
    ```

## Configuration & Logging
Configuration and logs are stored in the specified directories. Refer to the documentation for detailed instructions on how to modify settings or view logs.



