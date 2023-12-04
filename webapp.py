
import argparse
import io
import os
from PIL import Image
import datetime



#Firebase
import firebase_admin
from google.cloud import firestore
from firebase_admin import credentials, firestore

cred = credentials.Certificate('credentials.json')
firebase_admin.initialize_app(cred)

# Initialize Firestore client
db = firestore.client()





import torch
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__, template_folder='templates')  # Specify the templates folder


DATETIME_FORMAT = "%Y-%m-%d_%H-%M-%S-%f"

@app.route("/", methods=["GET", "POST"])
def predict():
    if request.method == "POST":
        if "file" not in request.files:
            return redirect(request.url)
        file = request.files["file"]
        if not file:
            return

        img_bytes = file.read()
        img = Image.open(io.BytesIO(img_bytes))
        results = model([img])

        results.render()  # updates results.imgs with boxes and labels
        now_time = datetime.datetime.now().strftime(DATETIME_FORMAT)
        img_savename = f"static/{now_time}.png"
        Image.fromarray(results.ims[0]).save(img_savename)
        
        
        collection_ref = db.collection("foods")

        # Query all documents in the collection
        docs = collection_ref.stream()

        # Create a dictionary to store document IDs and data
        documents_dict = {}

        # Store document data in the dictionary
        for doc in docs:
            doc_id = doc.id
            doc_data = doc.get('calories')
            documents_dict[doc_id] = doc_data
            
        document_new_list=[]
        for names in results.pandas().xyxy[0].name:
            det_doc_id=names
            if(names in documents_dict.keys()):
                det_doc_data=documents_dict[names]
            document_new_list.append((det_doc_id,det_doc_data))
            

        # Pass the image URL to the result template
        img_url = url_for('static', filename=f"{now_time}.png")
        return render_template("another.html", img_url=img_url, results=document_new_list)

    return render_template("index.html")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Flask app exposing yolov5 models")
    parser.add_argument("--port", default=5000, type=int, help="port number")
    args = parser.parse_args()

    model = torch.hub.load('ultralytics/yolov5', 'custom', path='yolov5/runs/train/exp/weights/best_best.pt', force_reload=True)  # force_reload = recache latest code
    model.eval()
    app.run(host="0.0.0.0", port=args.port)  # debug=True causes Restarting with stat
