from pathlib import Path

from aws_cdk import aws_glue as glue, core, aws_s3_deployment
from aws_cdk import aws_iam as iam

from datajob import logger
from datajob.datajob_base import DataJobBase
from datajob.datajob_context import DatajobContext
from datajob.stepfunctions import stepfunctions_workflow


@stepfunctions_workflow.task
class GlueJob(DataJobBase):
    """
    Configure a glue job to run some business logic.
    """

    def __init__(
        self,
        datajob_stack: core.Construct,
        name: str,
        path_to_glue_job: str,
        job_type: str = "pythonshell",
        glue_version: str = "1.0",
        max_capacity: int = None,
        arguments: dict = None,
        python_version: str = "3",
        role: iam.Role = None,
        *args,
        **kwargs,
    ):
        """
        :param datajob_stack: aws cdk core construct object.
        :param name: a name for this glue job (will appear on the glue console).
        :param path_to_glue_job: the path to the glue job relative to the project root.
        :param job_type: choose pythonshell for plain python / glueetl for a spark cluster.
        :param glue_version: at the time of writing choose 1.0 for pythonshell / 2.0 for spark.
        :param max_capacity: max nodes we want to run.
        :param arguments: the arguments as a dict for this glue job.
        :param python_version: 3 is the default
        :param args: any extra args for the glue.CfnJob
        :param kwargs: any extra kwargs for the glue.CfnJob
        """
        logger.info(f"creating glue job {name}")
        super().__init__(datajob_stack, name, **kwargs)
        self.path_to_glue_job = (
            str(Path(self.project_root, path_to_glue_job))
            if self.project_root is not None
            else path_to_glue_job
        )
        self.arguments = arguments if arguments else {}
        self.job_type = job_type
        self.python_version = python_version
        self.glue_version = glue_version
        self.max_capacity = max_capacity
        self.args = args
        self.kwargs = kwargs
        self.role = (
            self.get_role(
                unique_name=self.unique_name, service_principal="glue.amazonaws.com"
            )
            if role is None
            else role
        )
        logger.info(f"glue job {name} created.")

    def create(self):
        s3_url_glue_job = self._deploy_glue_job_code(
            datajob_context=self.datajob_context,
            glue_job_name=self.unique_name,
            path_to_glue_job=self.path_to_glue_job,
        )
        self._create_glue_job(
            datajob_context=self.datajob_context,
            glue_job_name=self.unique_name,
            s3_url_glue_job=s3_url_glue_job,
            arguments=self.arguments,
            job_type=self.job_type,
            python_version=self.python_version,
            glue_version=self.glue_version,
            max_capacity=self.max_capacity,
            *self.args,
            **self.kwargs,
        )

    @staticmethod
    def _create_s3_url_for_job(
        glue_job_context: DatajobContext, glue_job_id: str, glue_job_file_name: str
    ):
        """path to the script on s3 for this job."""
        s3_url_glue_job = f"s3://{glue_job_context.deployment_bucket_name}/{glue_job_id}/{glue_job_file_name}"
        logger.debug(f"s3 url for glue job {glue_job_id}: {s3_url_glue_job}")
        return s3_url_glue_job

    @staticmethod
    def _get_glue_job_dir_and_file_name(path_to_glue_job: str):
        """Split the full path in a dir and filename."""
        logger.debug(f"splitting path {path_to_glue_job}")
        pathlib_path_to_glue_job = Path(path_to_glue_job)
        glue_job_dir = str(pathlib_path_to_glue_job.parent)
        glue_job_file_name = pathlib_path_to_glue_job.name
        logger.debug(f"splitted into {glue_job_dir} and {glue_job_file_name}")
        return glue_job_dir, glue_job_file_name

    def _deploy_glue_job_code(
        self, datajob_context: DatajobContext, glue_job_name: str, path_to_glue_job: str
    ):
        """deploy the code of this glue job to the deployment bucket
        (can be found in the glue context object)"""
        glue_job_dir, glue_job_file_name = GlueJob._get_glue_job_dir_and_file_name(
            path_to_glue_job=path_to_glue_job
        )
        logger.debug(f"deploying glue job folder {glue_job_dir}")
        aws_s3_deployment.BucketDeployment(
            self,
            f"{glue_job_name}-CodeDeploy",
            sources=[
                # we can either sync dirs or zip files.
                # To keep it easy for now we agreed to sync the full dir.
                # todo - sync only the glue job itself.
                aws_s3_deployment.Source.asset(glue_job_dir)
            ],
            destination_bucket=datajob_context.deployment_bucket,
            destination_key_prefix=glue_job_name,
        )

        s3_url_glue_job = GlueJob._create_s3_url_for_job(
            glue_job_context=datajob_context,
            glue_job_id=glue_job_name,
            glue_job_file_name=glue_job_file_name,
        )
        return s3_url_glue_job

    def _create_glue_job(
        self,
        datajob_context: DatajobContext,
        glue_job_name: str,
        s3_url_glue_job: str = None,
        arguments: dict = None,
        job_type: str = "pythonshell",
        python_version: str = "3",
        glue_version: str = None,
        max_capacity: int = None,
        *args,
        **kwargs,
    ):
        """Create a glue job with the necessary configuration like,
        paths to wheel and business logic and arguments"""
        logger.debug(f"creating Glue Job {glue_job_name}")
        default_arguments = None
        if datajob_context.s3_url_wheel:
            extra_py_files = {
                # path to the wheel of this project
                "--extra-py-files": datajob_context.s3_url_wheel
            }
            default_arguments = {**extra_py_files, **arguments}
        glue.CfnJob(
            self,
            id=glue_job_name,
            name=glue_job_name,
            role=self.role.role_arn,
            command=glue.CfnJob.JobCommandProperty(
                name=job_type,
                python_version=python_version,
                script_location=s3_url_glue_job,
            ),
            glue_version=glue_version,
            max_capacity=max_capacity,
            default_arguments=default_arguments,
            *args,
            **kwargs,
        )
