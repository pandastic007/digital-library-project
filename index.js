const express = require('express');
const app = express();
const port = process.env.PORT || 8080;

// Basic route that sends a response
app.get('/', (req, res) => {
  res.send('Backend is running on Google Cloud Run!');
});

// Start the server
app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});
