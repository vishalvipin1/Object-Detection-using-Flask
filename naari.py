import firebase_admin
from google.cloud import firestore
from firebase_admin import credentials, firestore

cred = credentials.Certificate('credentials.json')
firebase_admin.initialize_app(cred)

# Initialize Firestore client
db = firestore.client()

def fetch_and_store_documents(collection_name):
    # Reference to the Firestore collection
    collection_ref = db.collection(collection_name)

    # Query all documents in the collection
    docs = collection_ref.stream()

    # Create a dictionary to store document IDs and data
    documents_dict = []

    # Store document data in the dictionary
    for doc in docs:
        doc_id = doc.id
        doc_data = doc.get('calories')
        documents_dict.append((doc_id,doc_data))

    return documents_dict

# Replace 'your_collection_name' with the actual name of your Firestore collection
collection_name = 'foods'

# Fetch documents and store in a dictionary
documents_dict = fetch_and_store_documents(collection_name)

print(documents_dict)
    
