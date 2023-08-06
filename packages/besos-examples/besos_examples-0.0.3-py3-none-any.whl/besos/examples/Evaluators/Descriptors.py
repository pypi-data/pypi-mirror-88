# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.3.1
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# + [markdown] papermill={"duration": 0.007177, "end_time": "2019-10-28T22:50:11.211540", "exception": false, "start_time": "2019-10-28T22:50:11.204363", "status": "completed"} tags=[]
# # Descriptors
#
# Descriptors specify what kinds of values are valid for a parameter.
# There are currently, three variants: `RangeParameter`, `DependentParameter` and `CategoryParameter`.

# + papermill={"duration": 1.056189, "end_time": "2019-10-28T22:50:12.273175", "exception": false, "start_time": "2019-10-28T22:50:11.216986", "status": "completed"} tags=[]
import pandas as pd

from besos.parameters import (
    RangeParameter,
    DependentParameter,
    CategoryParameter,
    Parameter,
)
from besos.problem import Problem
from besos import sampling
from besos.evaluator import EvaluatorGeneric

# + [markdown] papermill={"duration": 0.004912, "end_time": "2019-10-28T22:50:12.283603", "exception": false, "start_time": "2019-10-28T22:50:12.278691", "status": "completed"} tags=[]
# ### RangeParameters
# $min \leq x \leq max$

# + papermill={"duration": 0.01397, "end_time": "2019-10-28T22:50:12.304946", "exception": false, "start_time": "2019-10-28T22:50:12.290976", "status": "completed"} tags=[]
zero_to_one_exclusive = RangeParameter(min_val=0.01, max_val=0.99)
# -

# ### DependentParameter
#
# The value of dependent parameter depends on a range parameter.
#
# For mode = 'sum', x = factor - target_val
#
# For mode = 'subtract', x = target_val - factor
#
# For mode = 'multiple', x = factor * target_val
#
# For mode = 'power', x = target_val ^ factor
#
# index represents the index of the target range parameter in the parameter list
#
# Check out [this](Evaluators/DependParamAndNonObj.ipynb) notebook for more examples.

dp = DependentParameter(mode="sum", factor=1, index=0)

# + [markdown] papermill={"duration": 0.004436, "end_time": "2019-10-28T22:50:12.314291", "exception": false, "start_time": "2019-10-28T22:50:12.309855", "status": "completed"} tags=[]
# ### CategoryParameters
# A list of options.

# + papermill={"duration": 0.009385, "end_time": "2019-10-28T22:50:12.328129", "exception": false, "start_time": "2019-10-28T22:50:12.318744", "status": "completed"} tags=[]
text_example = CategoryParameter(options=["a", "b", "c", "other"])
single_digit_integers = CategoryParameter(options=range(10))

# + [markdown] papermill={"duration": 0.004336, "end_time": "2019-10-28T22:50:12.337015", "exception": false, "start_time": "2019-10-28T22:50:12.332679", "status": "completed"} tags=[]
# ### Sampling
# These descriptors can be used to make `Parameters`.
# Then we can generate samples.

# + papermill={"duration": 0.021458, "end_time": "2019-10-28T22:50:12.362905", "exception": false, "start_time": "2019-10-28T22:50:12.341447", "status": "completed"} tags=[]
parameters = [
    Parameter(value_descriptor=zero_to_one_exclusive, name="0-1"),
    Parameter(value_descriptor=dp, name="dp"),
    Parameter(value_descriptor=single_digit_integers, name="single digit"),
    Parameter(value_descriptor=text_example, name="text"),
]
problem = Problem(parameters, outputs=["output"])

samples = sampling.dist_sampler(sampling.lhs, problem, num_samples=10)
samples


# + [markdown] papermill={"duration": 0.004504, "end_time": "2019-10-28T22:50:12.372177", "exception": false, "start_time": "2019-10-28T22:50:12.367673", "status": "completed"} tags=[]
# ### Evaluation
# Since we did not specify selectors for the parameters, we cannot evaluate them using an EnergyPlus simulation.
# Instead, we will use a custom evaluation function.

# + papermill={"duration": 0.038359, "end_time": "2019-10-28T22:50:12.415265", "exception": false, "start_time": "2019-10-28T22:50:12.376906", "status": "completed"} tags=[]
def evaluation_function(values):
    v, x, y, z = values
    if z == "other":
        return (v,), ()
    else:
        return (x * y,), ()


evaluator = EvaluatorGeneric(evaluation_function, problem)
# The evaluator will use this objective by default
outputs = evaluator.df_apply(samples, keep_input=True)
# outputs is a pandas dataframe with one column since only one objective was requested

# + papermill={"duration": 0.018132, "end_time": "2019-10-28T22:50:12.440161", "exception": false, "start_time": "2019-10-28T22:50:12.422029", "status": "completed"} tags=[]
outputs

# + papermill={"duration": 0.005969, "end_time": "2019-10-28T22:50:12.452010", "exception": false, "start_time": "2019-10-28T22:50:12.446041", "status": "completed"} tags=[]
