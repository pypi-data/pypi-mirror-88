from typing import List, Optional
from pathlib import Path
import zipfile
from pycaprio import Pycaprio
from pycaprio.mappings import InceptionFormat
from annotated_dataset.annotated_resource_uima_cas_xmi import AnnotatedResourceUimaCasXmi
from annotated_dataset.annotated_resource_base import AnnotatedResourceBase
import logging


class ProjectNotFound(Exception):
    def __init__(self, project_name: str, inception_client: Pycaprio):
        super().__init__(f'Project `{project_name}` in {inception_client} ')


class InceptionProject:
    def __init__(self, path, use_curated_data: bool = False,  allowed_resources: Optional[str] = None):
        self.path = Path(path)
        self.use_curated_data = use_curated_data
        self.allowed_resources = allowed_resources
        if not self.path.is_dir():
            raise ValueError(f'Dir `{path}` not found')

    def extract_resources(self, restore_segmentation_by_newline=False) -> List[AnnotatedResourceBase]:
        resources = []
        directory = 'annotation'
        if self.use_curated_data:
            directory = 'curation'
        for path in sorted(self.path.glob(f'{directory}/*/*.zip')):
            project_name = self.path.name
            resource = AnnotatedResourceUimaCasXmi(
                str(path),
                project_name=project_name,
                restore_segmentation_by_newline=restore_segmentation_by_newline,
                is_curated_data=self.use_curated_data)
            if self.allowed_resources is None \
                    or (self.allowed_resources is not None and resource.resource_id in self.allowed_resources):
                resources.append(resource)
        return resources

    @staticmethod
    def create_from_remote(
            project_name: str,
            inception_client:
            Pycaprio, location: str,
            use_curated_data: bool = False,
            allowed_resources: Optional[str] = None):
        # Get project id
        project_id = None
        projects = inception_client.api.projects()
        for project in projects:
            if project.project_name == project_name:
                project_id = project.project_id
                break

        if project_id is None:
            raise ProjectNotFound(project_name, inception_client)

        # Download project zip
        logging.info(f'Download project `{project_name}`')
        zip_file = Path(location).joinpath(f"{project_name}.zip")
        with open(zip_file, 'wb') as z:
            zip_content = inception_client.api.export_project(
                project_id,
                project_format=InceptionFormat.XMI)
            z.write(zip_content)

        # Unzip project
        project_dir = Path(location).joinpath(project_name)
        with zipfile.ZipFile(zip_file, 'r') as z:
            z.extractall(project_dir)

        # Create the project
        project = InceptionProject(
            str(Path(location).joinpath(project_name)),
            use_curated_data=use_curated_data,
            allowed_resources=allowed_resources
        )
        logging.info(f' ---> Done')

        return project

