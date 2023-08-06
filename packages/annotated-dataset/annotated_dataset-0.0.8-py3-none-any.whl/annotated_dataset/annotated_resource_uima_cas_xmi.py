from typing import List
from annotated_dataset.annotated_text import AnnotatedText, AnnotatedTextToken
from annotated_dataset.annotation import Annotation
from annotated_dataset.annotated_resource_base import AnnotatedResourceBase
from dkpro_cassis_tools import load_cas_from_zip_file, \
    restore_cas_segmentation_by_newline, \
    SENTENCE_NS, \
    NAMED_ENTITY_NS, \
    TOKEN_NS
from dkpro_cassis_tools.get_document_meta_data import get_document_meta_data


class AnnotatedResourceUimaCasXmi(AnnotatedResourceBase):
    def __init__(self, path, restore_segmentation_by_newline=False, project_name='', is_curated_data=False):
        self.path = path
        self.restore_segmentation_by_newline = restore_segmentation_by_newline

        # Open Resource
        with open(self.path, 'rb') as f:
            self.cas, self.type_system = load_cas_from_zip_file(f, return_type_system=True)

        # Document Meta Data
        document_meta_data = get_document_meta_data(self.cas)
        if not document_meta_data:
            raise ValueError(f'Unable to load meta data for {self.path}')
        self.document_meta_data_title = document_meta_data.documentTitle
        self.document_meta_data_id = document_meta_data.documentId

        # Resource id
        type_ = "annotation" if not is_curated_data else 'curation'
        resource_id = f'{project_name}/{type_}/{self.document_meta_data_title}/{self.document_meta_data_id}'
        super().__init__(resource_id)

        # Extract annotated texts
        self.annotated_texts = []
        if self.restore_segmentation_by_newline:
            self.cas = restore_cas_segmentation_by_newline(self.cas)
        for i, sentence in enumerate(self.cas.select(SENTENCE_NS)):
            # Text
            text = sentence.get_covered_text()

            # Annotations
            annotations = []
            for a in self.cas.select_covered(NAMED_ENTITY_NS, sentence):
                annotations.append(Annotation(
                    label=a.value,
                    start=a.begin - sentence.begin,
                    stop=a.end - sentence.begin

                ))

            # Tokens
            tokens = []
            for token in self.cas.select_covered(TOKEN_NS, sentence):
                tokens.append(AnnotatedTextToken(
                    start=token.begin-sentence.begin,
                    stop=token.end-sentence.begin
                ))
            not_spaces = set()
            for token in tokens:
                for j in range(token.start, token.stop):
                    not_spaces.add(j)
            for j, char in enumerate(text):
                if j not in not_spaces:
                    if not text[j].isspace():
                        # TODO
                        print("Tokenizing Error")

            self.annotated_texts.append(AnnotatedText(
                text=text,
                annotations=annotations,
                resource_id=self.resource_id,
                resource_index=i + 1,
                tokens=tokens
            ))

    def get_annotated_texts(self) -> List[AnnotatedText]:
        return self.annotated_texts

