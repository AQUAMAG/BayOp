FROM jupyter/base-notebook:latest

# Install additional dependencies
USER root
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /home/jovyan/work 



# Install JupyterLab extensions and commonly used libraries
RUN pip install --no-cache-dir \
    jupyterlab \
    jupyterlab-git \
    jupyterlab-lsp \
    'python-lsp-server[all]' \
    numpy \
    pandas \
    matplotlib \
    seaborn \
    scipy \
    scikit-learn \
    transformers \
    requests \
    beautifulsoup4 \
    tqdm \
    bayesian-optimization==2.0.0

# Set user back to Jupyter default user
USER jovyan

# Clone a Git repository into a persistent volume
RUN git clone https://github.com/AQUAMAG/BayOp.git

# Expose the default JupyterLab port
EXPOSE 8888

# Print Jupyter Notebook access URL on startup and open in cloned repository
CMD jupyter lab --ip=0.0.0.0 --port=8888 --allow-root --NotebookApp.root_dir='/home/jovyan/work'