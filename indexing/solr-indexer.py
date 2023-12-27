import sys
import pysolr
import time

# Solr configuration
SOLR_ADDRESS = 'http://localhost:8983/solr/aequitas_test'
# SOLR_ADDRESS = 'http://107.22.6.9:8983/solr/aequitas_test'
# SOLR_ADDRESS = 'http://34.239.117.195:8983/solr/aequitas_test'


BATCH_SIZE = 100
# Create a client instance
solr = pysolr.Solr(SOLR_ADDRESS, always_commit=True, timeout=610)


def index_documents(id, title, abstract, content, embedding_a, embedding_c, dropbox_link, path):
    solr.ping()
    print("Solr connection successful")
    with open(id, "r", encoding = 'utf-8') as id_file:
        with open(title, "r", encoding = 'utf-8') as title_file:
            with open(abstract, "r", encoding = 'utf-8') as abstract_file:
                with open(content, "r", encoding = 'utf-8') as content_file:
                    with open(embedding_a, "r", encoding = 'utf-8') as embedding_abstract:
                        with open(embedding_c, "r", encoding = 'utf-8') as embedding_constent:
                            with open(dropbox_link, "r", encoding = 'utf-8') as dropbox_link_file:
                                with open(path, "r", encoding = 'utf-8') as dropbox_path_file:
                                    documents = []
                                    # for each document (text and related vector) creates a JSON document
                                    for index, (id, title, abstract, content, vectors_a, vectors_c, dropbox_link, path) in enumerate(zip(id_file, title_file, abstract_file, content_file, embedding_abstract, embedding_constent, dropbox_link_file, dropbox_path_file)):
                                      
                                        vector_a = [float(w)
                                                    for w in vectors_a.split(",")]
                                        vector_c = [float(w)
                                                    for w in vectors_c.split(",")]
                                        doc = {
                                            "id": id.rstrip('\t\n'),
                                            "title": title.rstrip('\t\n'),
                                            "abstract": abstract.rstrip('\t\n'),
                                            "content": content.rstrip('\t\n'),
                                            "vector_abstract": vector_a,
                                            "vector_content": vector_c,
                                            "dropbox_link": dropbox_link.rstrip('\t\n'),
                                            "path": path.rstrip('\t\n'),
                                        }
                                        # append JSON document to a list
                                        documents.append(doc)
                                        # to index batches of documents at a time
                                        # if index % BATCH_SIZE == 0 and index != 0:
                                        if index % BATCH_SIZE == 0 or index == len(documents) - 1:
                                            solr.add(documents)
                                            documents = []
                                            print(
                                                "==== indexed {} documents ======".format(index))
                                    # to index the rest, when 'documents' list < BATCH_SIZE
                                    if documents:
                                        solr.add(documents)
                                    print("Finished")


def main():
    id = "data/aequitas_id.tsv"
    title = "data/aequitas_title.tsv"
    abstract = "data/aequitas_abstract.tsv"
    content = "data/aequitas_content.tsv"
    embedding_a = "data/vector_abstract.tsv"
    embedding_c = "data/vector_content.tsv"
    dropbox_link = "data/aequitas_dropbox.tsv"
    path = "data/aequitas_path.tsv"
    initial_time = time.time()
    index_documents(id, title, abstract, content, embedding_a, embedding_c, dropbox_link, path)
    finish_time = time.time()
    print('Documents indexed in {:f} seconds\n'.format(
        finish_time - initial_time))


if __name__ == "__main__":
    main()
