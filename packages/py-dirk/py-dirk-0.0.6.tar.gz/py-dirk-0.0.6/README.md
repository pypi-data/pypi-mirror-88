# py-dirk

dirk is a tool for Kubernetes administrators who manage a large number of clusters. 
dirk makes sure that you always communicate with the right kubernetes cluster, even though you switch between many project folders.

py-dirk is the Python implementation of dirk.

# Install py-dirk

Install py-dirk like this:

```bash
pip install py-dirk
```

# Use dirk

Init dirk for a certain project folder like this:

```bash
dirk init <directory>
```

This command creates a kubeconfig file which will be used by kubectl as long your current working directory is in the project folder.
Leaving the project folder will lead to the kubeconfig file to be unloaded.

# Example of use

How to use dirk is shown in [https://github.com/deepshore/how-to-use-dirk](https://github.com/deepshore/how-to-use-dirk).
