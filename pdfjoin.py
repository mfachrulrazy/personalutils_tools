import os
import json
from PyPDF2 import PdfMerger


def merge_pdfs(source_dir, output_dir, output_filename="combined.pdf"):
    pdf_merger = PdfMerger()
    for file in os.listdir(source_dir):
        if file.endswith(".pdf"):
            file_path = os.path.join(source_dir, file)
            try:
                pdf_merger.append(file_path)
            except Exception as e:
                print(f"Error processing {file}: {e}")

    output_path = os.path.join(output_dir, output_filename)
    pdf_merger.write(output_path)
    pdf_merger.close()
    print(f"PDFs combined into: {output_path}")


if __name__ == "__main__":
    with open("config.json") as config_file:
        config = json.load(config_file)
        source_dir = config["mpdf_in_dir"]
        output_dir = config["mpdf_out_dir"]

    merge_pdfs(source_dir, output_dir)
