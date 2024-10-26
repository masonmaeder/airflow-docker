# Example DAGs

## Dependency scheduling options

To make workflows more readable and modular, you may choose to separate groups of tasks into separate DAGs. There are a couple of ways to make one DAG run after another:

### Using TriggerDagRunOperator

TriggerDagRunOperator is a good option if you're writing a parent DAG and already know which child DAG you need to trigger next (this can depend on a condition and supports branching). The operator is placed in the parent DAG and triggers the child DAG directly.

#### [Example Parent](/parent_TriggerDagRunOperator.py)

#### [Example Child](/child_TriggerDagRunOperator.py)

### Using ExternalTaskSensor

ExternalTaskSensor is a good option if you're writing a child DAG that should only run after an already existing parent DAG completes. The sensor is placed in the child DAG and monitors the parent DAG for completion.

#### [Example Parent](/parent_ExternalTaskSensor.py)

#### [Example Child](/child_ExternalTaskSensor.py)