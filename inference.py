from google.cloud import documentai 

def process_document(
    project_id: str,
    location: str,
    processor_id: str,
    file_path: str,
    mime_type: str,
) -> documentai.Document:
    """
    A function to process a document online using Google Document AI.
    """

    opts = {"api_endpoint": f"{location}-documentai.googleapis.com"}

    documentai_client = documentai.DocumentProcessorServiceClient(client_options=opts)
    resource_name = documentai_client.processor_path(project_id, location, processor_id)

    with open(file_path, "rb") as image:
        image_content = image.read()

        raw_document = documentai.RawDocument(
            content=image_content, mime_type=mime_type
        )
        request = documentai.ProcessRequest(
            name=resource_name, raw_document=raw_document
        )
        result = documentai_client.process_document(request=request)

        return result.document