import os
import dropbox
import pysolr
from urllib.parse import urlparse, urlunparse
import csv
import PyPDF2
import requests
from dropbox.exceptions import AuthError
import time
import subprocess

#myapp.py functionality: recursively lists all files in a Dropbox Account
from dropbox import DropboxOAuth2FlowNoRedirect

def download_file(dbx, entry, output_folder):
    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Build the local path where the file will be saved
    local_path = os.path.join(output_folder, entry.name)

    try:
        # Download the file content
        _, file_content = dbx.files_download(entry.path_display)

        # Save the content to the local file
        with open(local_path, 'wb') as local_file:
            local_file.write(file_content.content)

        print(f"Downloaded file: {local_path}")
    except Exception as e:
        print(f"Error downloading file '{entry.name}': {e}")



def list_files_recursive(dbx, folder_path, tsv_file, title_file, path_file, dropbox_file, auth_code, output_folder):

    try:
        with open(tsv_file, 'a', newline='',  encoding="utf-8") as tsvfile:
            with open(title_file, 'a', newline='', encoding="utf-8") as titlefile:
                with open(path_file, 'a', newline='', encoding="utf-8") as pathfile:
                    with open(dropbox_file, 'a', newline='', encoding="utf-8") as dropboxfile:

                        tsv_writer = csv.writer(tsvfile, delimiter = '\t')
                        title_writer = csv.writer(titlefile, delimiter = '\t')
                        path_writer = csv.writer(pathfile, delimiter = '\t')
                        dropbox_writer = csv.writer(dropboxfile, delimiter = '\t')
                        
                        # List files in the current folder
                        result = dbx.files_list_folder(folder_path)
                        
                        for entry in sorted(result.entries, key=lambda entry: entry.name.casefold()):
                            if isinstance(entry, dropbox.files.FileMetadata):
                                shared_link = dbx.sharing_create_shared_link(entry.path_display)
                                file_url = shared_link.url
                                # print(f"File Name: {entry.name}, URL: {file_url}, File ID: {entry.id}, File Path: {entry.path_display}")

                                # #checking if document is a PDF
                                # if '.pdf' in entry.name:
                                #     print("This is a PDF")
                                # Print file content

                                
                                # Download the file
                                download_file(dbx, entry, output_folder)

                                title = entry.name
                                # correcting title; typographic apostrophe
                                title = title.replace('’', "'")

                                # Initialize an empty dictionary to store attributes
                                entry_attributes = {}

                                # Write the ID to the TSV file
                                fixed_entry_id = entry.id[3:]
                                tsv_writer.writerow([fixed_entry_id])
                                # entry_attributes['id'] = fixed_entry_id
                                #Write title to the TSV file
                                title_writer.writerow([title])
                                # entry_attributes['title'] = title
                                #Write path to the TSV file
                                path_writer.writerow([entry.path_display])
                                # entry_attributes['path'] = entry.path_display
                                #Write link to the TSV file
                                dropbox_writer.writerow([file_url])
                                # entry_attributes['link'] = file_url

                                #Write all attributes to a dictionary
                                entries_list = []

                                # Create a dictionary for this entry
                                entry_attributes = {'id': fixed_entry_id, 'title': title, 'path': entry.path_display, 'link': file_url}

                                # Append the dictionary to the list
                                entries_list.append(entry_attributes)

                                print(entries_list)

                            elif isinstance(entry, dropbox.files.FolderMetadata):
                                # If it's a folder, recursively list files in that folder
                                list_files_recursive(dbx, entry.path_display, tsv_file, title_file, path_file, dropbox_file, auth_code, output_folder)

    except dropbox.exceptions.ApiError as e:
        print(f"Error accessing folder '{folder_path}': {e}")


def main():

    APP_KEY = "9jswxpjxifo37tm"
    APP_SECRET = "kb8u7yw57jrhhw8"

    #OAuth2Flow to allow search solr to get access to Dropbox account
    auth_flow = DropboxOAuth2FlowNoRedirect(APP_KEY, APP_SECRET)

    authorize_url = auth_flow.start()
    print("1. Go to: " + authorize_url)
    print("2. Click \"Allow\" (you might have to log in first).")
    print("3. Copy the authorization code.")
    auth_code = input("Enter the authorization code here: ").strip()

    try:
        oauth_result = auth_flow.finish(auth_code)
        print('oauth result: ')
        print(oauth_result)
    except Exception as e:
        print('Error: %s' % (e,))
        exit(1)

    with dropbox.Dropbox(oauth2_access_token=oauth_result.access_token) as dbx:
        dbx.users_get_current_account()
        print("Successfully set up client!")

        output_folder = 'Files'

        BASE_PATH = '/Users/penel/Downloads/dropbox-solr/'

        list_files_recursive(dbx, '', f'{BASE_PATH}/data/aequitas_id.tsv', f'{BASE_PATH}/aequitas_title.tsv', f'{BASE_PATH}/aequitas_path.tsv', f'{BASE_PATH}/aequitas_dropbox.tsv', auth_code, output_folder)

    #code to automate entire indexing process
    # subprocess.run(['python3', 'pdf-extractor.py'])
    # subprocess.run(['python3', 'abstract-extractor.py'])
    # subprocess.run(['python3', 'batch-sentence-transformers.py'])
    # subprocess.run(['python3', 'solr-indexer.py'])
    # subprocess.run(['python3', 'remove-text.py'])

if __name__ == '__main__':
    main()

