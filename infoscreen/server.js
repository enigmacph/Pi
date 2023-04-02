const http = require('http');
const fs = require('fs');
const path = require('path');
const socketIO = require('socket.io');

// Create an HTTP server
const server = http.createServer((req, res) => {
  if (req.url === '/') {
    fs.readFile(path.join(__dirname, 'welcome.html'), (err, data) => {
      if (err) {
        res.writeHead(500);
        res.end('Error loading welcome.html');
      } else {
        res.writeHead(200, { 'Content-Type': 'text/html' });
        res.end(data);
      }
    });
  } else {
    res.writeHead(404);
    res.end('Not found');
  }
});

const io = socketIO(server);

function getHtmlFilesFromFolder(folderPath) {
  return new Promise((resolve, reject) => {
    fs.readdir(folderPath, (err, files) => {
      if (err) {
        reject(err);
      } else {
        const htmlFiles = files.filter(file => path.extname(file) === '.html');
        resolve(htmlFiles);
      }
    });
  });
}

let currentFileIndex = 0;

async function getNextHtmlFile(folderPath) {
  const files = await getHtmlFilesFromFolder(folderPath);
  
  // Check if there are any files in the folder
  if (files.length === 0) {
    throw new Error('No HTML files found in the folder');
  }

  const nextFile = path.join(folderPath, files[currentFileIndex]);
  currentFileIndex = (currentFileIndex + 1) % files.length;
  return nextFile;
}

io.on('connection', (socket) => {
  console.log('A user connected');

  setInterval(async () => {
    try {
      const nextHtmlFile = await getNextHtmlFile(path.join(__dirname, 'HTML'));
  
      fs.readFile(nextHtmlFile, (err, data) => {
        if (err) {
          console.error('Error reading next HTML file:', err);
        } else {
          socket.emit('updateContent', data.toString());
        }
      });
    } catch (err) {
      console.error('Error getting next HTML file:', err);
    }
  }, 5 * 60 * 1000); // Update every 5 minutes

const PORT = process.env.PORT || 3000;
server.listen(PORT, () => console.log(`Server running on port ${PORT}`));
