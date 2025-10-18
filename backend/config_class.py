class Config():
    def __init__(self):
        self.create_new_embedings = True
        self.document_directiory = "docs/"
        self.chunk_size = 256
        self.chunk_overlap = 64
        self.ebmedings_model_name = "sentence-transformers/all-MiniLM-L6-v2"
        self.vector_store_path = "./vector_store/"
        self.model_name = "google/flan-t5-base"
        self.default_message = 'No relevant context found for this question.'
        self.clasification_model = "facebook/bart-large-mnli"
        self.search = 5
        self.error = "This question could not be processed!"

config = Config()