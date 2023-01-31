import os
from azure.storage.blob import BlobServiceClient
from flask import Flask, request, render_template

app = Flask(__name__)

connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING') # retrieve the connection string from the environment variable
container_name = "pdf" # container name in which images will be store in the storage account

blob_service_client = BlobServiceClient.from_connection_string(conn_str=connect_str) # create a blob service client to interact with the storage account


try:
    container_client = blob_service_client.get_container_client(container=container_name) # get container client to interact with the container in which PDFs will be stored
    container_client.get_container_properties() # get properties of the container to force exception to be thrown if container does not exist
except Exception as e:
    print(e)
    print("Creating container...")
    container_client = blob_service_client.create_container(container_name) # create a container in the storage account if it does not exist

@app.route("/", methods=["GET"])
def index():


    return render_template("index.html")

@app.route("/upload-pdf", methods=["POST"])
def upload_pdf():
    filenames = ""

    for file in request.files.getlist("pdf"):
        try:
            container_client.upload_blob(file.filename, file) # upload the file to the container using the filename as the blob name
            filenames += file.filename
        except Exception as e:
            print(e)
            print("Ignoring duplicate filenames") # ignore duplicate filenames
        
    return render_template('output.html', filenames=filenames)


if __name__ == "__main__":
    app.run(debug=True, port=1212)