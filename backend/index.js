require('dotenv').config();
const express = require('express');
const { Storage } = require('@google-cloud/storage');
const multer = require('multer');

const app = express();
const PORT = process.env.PORT || 8080;

// Set up Google Cloud Storage
const storage = new Storage({
  keyFilename: process.env.GOOGLE_APPLICATION_CREDENTIALS,
});
const bucketName = process.env.GCS_BUCKET_NAME;

// Set up multer for handling file uploads
const upload = multer({
  storage: multer.memoryStorage(), // Store files in memory before uploading
  limits: { fileSize: 10 * 1024 * 1024 }, // 10 MB limit
});

// Endpoint to upload files
app.post('/upload', upload.single('file'), async (req, res) => {
  try {
    if (!req.file) {
      return res.status(400).send('No file uploaded.');
    }

    const blob = storage.bucket(bucketName).file(req.file.originalname);
    const blobStream = blob.createWriteStream({
      resumable: false,
    });

    blobStream.on('error', (err) => {
      console.error(err);
      res.status(500).send('Error uploading file.');
    });

    blobStream.on('finish', () => {
      res.status(200).send('File uploaded successfully.');
    });

    blobStream.end(req.file.buffer);
  } catch (error) {
    console.error(error);
    res.status(500).send('An error occurred while uploading the file.');
  }
});

// Root endpoint
app.get('/', (req, res) => {
  res.send('Backend v1.0 running on Google Cloud Run!');
});

app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});
