# Example DAGs

## DAG dependency scheduling options

To make workflows more readable and modular, you may choose to separate groups of tasks into separate DAGs. There are a couple of ways to make one DAG run after another:

### Using TriggerDagRunOperator

TriggerDagRunOperator is a good option if you're writing a parent DAG and already know which child DAG you need to trigger next (this can depend on a condition and supports branching). The operator is placed in the parent DAG and triggers the child DAG directly.

#### [Example Parent](/dags/parent_TriggerDagRunOperator.py)

#### [Example Child](/dags/child_TriggerDagRunOperator.py)

### Using ExternalTaskSensor

ExternalTaskSensor is a good option if you're writing a child DAG that should only run after an already existing parent DAG completes. The sensor is placed in the child DAG and monitors the parent DAG for completion.

#### [Example Parent](/dags/parent_ExternalTaskSensor.py)

#### [Example Child](/dags/child_ExternalTaskSensor.py)

## Dataset dependency

In addition to scheduling DAGs based on time, you can also schedule DAGs to run based on when a task updates a dataset. This is known as data-aware scheduling.

Use the following example DAGs to get started. Update DB connection parameters and dataset definition to match actual credentials.

[dataset1](/dags/dataset1.py): Creates dataset "my_dataset" if does not already exist.

> Manually trigger [dataset0](/dags/dataset0.py) to test the database connection with an example query.

[dataset2](/dags/dataset2.py): Generates a random string and inserts it into the dataset.

[dataset3](/dags/dataset3.py): Automatically scheduled when dataset is updated (by dataset2, in this case). Prints most recent string in dataset.
