# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['datajob', 'datajob.glue', 'datajob.package', 'datajob.stepfunctions']

package_data = \
{'': ['*']}

install_requires = \
['aws-cdk.aws-glue>=1.70.0,<2.0.0',
 'aws-cdk.aws-s3-deployment>=1.70.0,<2.0.0',
 'aws-cdk.cloudformation-include>=1.76.0,<2.0.0',
 'aws-cdk.core>=1.70.0,<2.0.0',
 'aws-empty-bucket>=2.4.0,<3.0.0',
 'contextvars>=2.4,<3.0',
 'dephell>=0.8.3,<0.9.0',
 'stepfunctions>=1.1.2,<2.0.0',
 'typer>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['datajob = datajob.datajob:run']}

setup_kwargs = {
    'name': 'datajob',
    'version': '0.3.0',
    'description': 'Build and deploy a serverless data pipeline with no effort on AWS.',
    'long_description': '# Datajob\n\nBuild and deploy a serverless data pipeline with no effort on AWS.\n\n- Deploy your code to a glue job\n- Package your project and make it available on AWS\n- Orchestrate your pipeline using stepfunctions as simple as `task1 >> [task2,task3] >> task4`\n\n# Installation\n\n datajob can be installed using pip. Beware that we depend on [aws cdk cli](https://github.com/aws/aws-cdk)!\n\n    pip install datajob\n    npm install -g aws-cdk\n\n# Example\n\nA simple data pipeline with 3 Glue python shell tasks that are executed both sequentially and in parallel.\nSee the full example [here](https://github.com/vincentclaes/datajob/tree/main/examples/data_pipeline_simple)\n\n    from datajob.datajob_stack import DataJobStack\n    from datajob.glue.glue_job import GlueJob\n    from datajob.stepfunctions.stepfunctions_workflow import StepfunctionsWorkflow\n\n\n    # the datajob_stack is the instance that will result in a cloudformation stack.\n    # we inject the datajob_stack object through all the resources that we want to add.\n    with DataJobStack(stack_name="data-pipeline-simple") as datajob_stack:\n\n        # here we define 3 glue jobs with the datajob_stack object,\n        # a name and the relative path to the source code.\n        task1 = GlueJob(\n            datajob_stack=datajob_stack,\n            name="task1",\n            path_to_glue_job="data_pipeline_simple/task1.py",\n        )\n        task2 = GlueJob(\n            datajob_stack=datajob_stack,\n            name="task2",\n            path_to_glue_job="data_pipeline_simple/task2.py",\n        )\n        task3 = GlueJob(\n            datajob_stack=datajob_stack,\n            name="task3",\n            path_to_glue_job="data_pipeline_simple/task3.py",\n        )\n\n        # we instantiate a step functions workflow and add the sources\n        # we want to orchestrate. We got the orchestration idea from\n        # airflow where we use a list to run tasks in parallel\n        # and we use bit operator \'>>\' to chain the tasks in our workflow.\n        with StepfunctionsWorkflow(\n            datajob_stack=datajob_stack,\n            name="data-pipeline-simple",\n        ) as sfn:\n            [task1, task2] >> task3\n\n\n## Deploy and destroy\n\nDeploy your pipeline using a unique identifier `--stage` and point to the configuration of the pipeline using `--config`\n\n    export AWS_DEFAULT_ACCOUNT=my-account-number\n    export AWS_PROFILE=my-profile\n    cd examples/data_pipeline_simple\n    datajob deploy --stage dev --config datajob_stack.py\n    datajob destroy --stage dev --config datajob_stack.py\n\n\n> Note: When using datajob cli to deploy a pipeline, we shell out to aws cdk.\n> You can circumvent shelling out to aws cdk by running `cdk` explicitly.\n> datajob cli prints out the commands it uses in the back to build the pipeline.\n> If you want, you can use those.\n\n    cd examples/data_pipeline_simple\n    cdk deploy --app  "python datajob_stack.py"  -c stage=dev\n    cdk destroy --app  "python datajob_stack.py"  -c stage=dev\n\n# Ideas\n\n- trigger a pipeline using the cli; `datajob run --pipeline my-simple-pipeline`\n- implement a data bucket, that\'s used for your pipeline.\n- add a time based trigger to the step functions workflow.\n- add an s3 event trigger to the step functions workflow.\n- add a lambda that copies data from one s3 location to another.\n- version your data pipeline.\n- implement sagemaker services\n    - processing jobs\n    - hyperparameter tuning jobs\n    - training jobs\n    - create sagemaker model\n    - create sagemaker endpoint\n    - expose sagemaker endpoint to the internet by levering lambda + api gateway\n\nAny suggestions can be shared by starting a [discussion](https://github.com/vincentclaes/datajob/discussions)\n',
    'author': 'Vincent Claes',
    'author_email': 'vincent.v.claes@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/vincentclaes/datajob',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
