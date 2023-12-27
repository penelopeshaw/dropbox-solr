#!/usr/bin/python

from sentence_transformers import SentenceTransformer
import torch
import sys
from itertools import islice
import time

BATCH_SIZE = 100
INFO_UPDATE_FACTOR = 1
MODEL_NAME = 'all-MiniLM-L6-v2'

# load or create a SentenceTransformer model
model = SentenceTransformer(MODEL_NAME)
# get device like 'cuda'/'cpu' that should be used for computation
if torch.cuda.is_available():
    model = model.to(torch.device("cuda"))
print(model.device)


def main():
    input_filename = 'data/aequitas_content.tsv'
    input_file_abstract = 'data/aequitas_abstract.tsv'
    output_filename = 'data/vector_content.tsv'
    output_file_abstract = 'data/vector_abstract.tsv'
    initial_time = time.time()
    batch_encode_to_vectors(input_filename, output_filename)
    batch_encode_to_vectors_abstract(input_file_abstract, output_file_abstract)
    finish_time = time.time()
    print('Vectors created in {:f} seconds\n'.format(
        finish_time - initial_time))


def batch_encode_to_vectors(input_filename, output_filename):
    # open the file containing text
    with open(input_filename, 'r', encoding = "utf-8") as documents_file:
        # documents_file.seek(1016)
        # prob_byte = documents_file.read(1)
        # print(f"Problematic byte: {prob_byte}")
        # open the file in which the vectors will be saved
        with open(output_filename, 'w+', encoding="utf-8") as out:
            processed = 0
            # processing 100 documents at a time
            for n_lines in iter(lambda: tuple(islice(documents_file, BATCH_SIZE)), ()):
                processed += 1
                if processed % INFO_UPDATE_FACTOR == 0:
                    print("processed {} batch of documents".format(processed))
                # create sentence embedding
                vectors = encode(n_lines)
                # write each vector into the output file
                for v in vectors:
                    out.write(','.join([str(i) for i in v]))
                    out.write('\n')

def batch_encode_to_vectors_abstract(input_filename, output_filename):
    # open the file containing text
    with open(input_filename, 'r', encoding = "utf-8") as documents_file:
        # documents_file.seek(1016)
        # prob_byte = documents_file.read(1)
        # print(f"Problematic byte: {prob_byte}")
        # open the file in which the vectors will be saved
        with open(output_filename, 'w+', encoding = "utf-8") as out:
            processed = 0
            # processing 100 documents at a time
            for n_lines in iter(lambda: tuple(islice(documents_file, BATCH_SIZE)), ()):
                processed += 1
                if processed % INFO_UPDATE_FACTOR == 0:
                    print("processed {} batch of documents".format(processed))
                # create sentence embedding
                vectors = encode(n_lines)
                # write each vector into the output file
                for v in vectors:
                    out.write(','.join([str(i) for i in v]))
                    out.write('\n') 


def encode(documents):
    embeddings = model.encode(documents, show_progress_bar=True)
    print('vector dimension: ' + str(len(embeddings[0])))
    return embeddings


if __name__ == "__main__":
    main()
