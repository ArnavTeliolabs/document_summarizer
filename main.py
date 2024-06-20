import nltk
nltk.data.path.append("C:\\Users\\Arnav Khairate\\AppData\\Roaming\\nltk_data")

from src.abstractive_summarizer import abstractive_summary
from src.extractive_summarizer import extractive_summary
from src.data_preprocessing import preprocess_text
from src.pdf_handler import extract_text_from_pdf
from src.web_page_handler import extract_text_from_web_page
from src.docx_handler import extract_text_from_docx
from src.model_training import train_model

class DataPreprocessor:
    def __init__(self, summarizer):
        self.summarizer = summarizer

    def preprocess(self, documents):
        summaries = []
        for doc in documents:
            if doc.endswith('.pdf'):
                text = extract_text_from_pdf(doc)
            elif doc.startswith('http'):
                text = extract_text_from_web_page(doc)
            elif doc.endswith('.docx'):
                text = extract_text_from_docx(doc)
            else:
                # Assume it's plain text
                text = doc
            preprocessed_text = preprocess_text(text)
            summaries.append(self.summarizer(preprocessed_text))
        return summaries

def main():
    documents = [
        r"C:\Users\Arnav Khairate\Downloads\Ice-breaking Project.pdf",
        # Add more document paths here
    ]
    preprocessor = DataPreprocessor(abstractive_summary)
    summaries = preprocessor.preprocess(documents)
    for summary in summaries:
        print(summary)

if __name__ == "__main__":
    main()
