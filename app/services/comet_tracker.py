import os
from comet_ml import Experiment
_exp=None

def exp():
    global _exp
    if _exp: return _exp
    api_key=os.getenv("COMET_API_KEY")
    workspace=os.getenv("COMET_WORKSPACE")
    project=os.getenv("COMET_PROJECT","ai-knowledge-sprint")
    if not api_key: 
        class _Null: 
            def log_metric(*a,**k): pass
            def log_parameters(*a,**k): pass
            def log_asset(*a,**k): pass
        _exp=_Null()
        return _exp
    _exp=Experiment(api_key=api_key, workspace=workspace, project_name=project, auto_param_logging=False, auto_metric_logging=False)
    return _exp
