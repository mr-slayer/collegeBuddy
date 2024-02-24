from django.http import HttpResponse
from django.template import loader
from firebase_admin import credentials
from google.cloud import firestore
from google.oauth2 import service_account
from django.shortcuts import render
from pathlib import Path
import requests
from google.cloud import storage



# Firebase credentials 
credentials = service_account.Credentials.from_service_account_file(Path.cwd() / 'firebase_cred.json')
db = firestore.Client(project=credentials.project_id, credentials=credentials)
storage_client = storage.Client(project=credentials.project_id, credentials=credentials)
def jobs(request):

  collection_name = 'jobs'
  # Fetch all data from Firestore collection
  docs = db.collection(collection_name).stream()
  jobs = []
  for doc in docs:
    jobs.append(doc.to_dict())
  print(jobs)
  return render(request, 'jobs.html', {'my_data': jobs})


def createJob(request):
  return render(request, 'job_form.html')

def saved(request):
  # Define your data
  photo_file = request.FILES['photo']

  if(request.method=="POST"):
    data = {
      'companyName': request.POST['companyName'],
      'lastDate': request.POST['lastDate'],
      'salary': request.POST['salary'],
      'link': request.POST['link'],
    }
  
# Specify the collection and document to store the data
  collection_name = 'jobs'
# ------------------
# Upload the photo to Firebase Storage
  bucket_name = 'collegebuddy-7d37f.appspot.com'
  bucket = storage_client.bucket(bucket_name)
  blob = bucket.blob(photo_file.name)
# Set content type for the image
  blob.upload_from_file(photo_file, content_type=photo_file.content_type)
# ---------------
  #get image url 
  blob_url = 'https://firebasestorage.googleapis.com/v0/b/collegebuddy-7d37f.appspot.com/o/' + blob.name
  print("here is blob_url")
  print(blob_url)
  response = requests.get(blob_url).json()
  print('Here is response')
  print(response)
  photo_url = blob_url + '?alt=media&token=' + response.get('downloadTokens')

# Get the URL of the uploaded photo
  # photo_url = blob.public_url
  print("here is photo url:\n")
  print(photo_url)
# Add the photo URL to the data
  data['photo'] = photo_url
# Push data to Firestore
  db.collection(collection_name).add(data)
  return render(request, 'saved.html')