import importlib
import inspect
from tweetbench.notebook_loader import NotebookLoader
import os
import re
from sklearn.pipeline import Pipeline

exp_dir = 'expirements'
META = 'META'

py_pattern = "^.+\.ipynb$|^.+\.py$"
py = re.compile(py_pattern)

def gather(source_dir=exp_dir):
    """Gather pipelines and metadata from notebooks and python scripts in the 'exp' folder"""

    contents = os.listdir(exp_dir)
    sources = [name for name in contents if py.match(name)]

    expirements = []

    for name in sources:

        module_name, module_type = os.path.splitext(name)

        meta = None
        pipeline = None
        module = importlib.import_module(f'{exp_dir}.{module_name}')

        for (k,v) in module.__dict__.items():

            if k == META:
                meta = getattr(module, k)

            if type(v) == Pipeline:
                pipeline = getattr(module, k)

        # for x in dir(module):
        #     obj = getattr(module, x)
        #     if type(obj) == Pipeline:
        #         pipeline = obj

        if not pipeline is None:
            expirements.append((module_name, meta, pipeline))

    return expirements
