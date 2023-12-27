# dropbox-solr
Application to download files from any Dropbox account and upload them to a Solr Search Engine


indexing folder:
- 'dropbox-connect.py' establishes a connection to the Dropbox account using the Dropbox API. The owner of the Dropbox account must sign in to their account and grant permission for this application to access their files. This is done by receiving and inputting an access code into the program.

- 'pdf-extractor.py' extracts all the content from each document. 'abstract_extractor.py' extracts the first few hundred characters of each document.

- 'batch-sentence-transformers.py' transforms the content of each document into vectors for semantic processing.

- 'solr-indexer' indexes each file into the Apache Solr Search engine.

- 'remove-text.py' removes all the text from the .tsv files in the data folder

data folder:
- contains .tsv files to store abstract, content, dropbox link, id, path, title, and vectors of each document
