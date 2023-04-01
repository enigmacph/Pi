const fs = require('fs');
const path = require('path');
const electron = require('electron');
const { app, BrowserWindow } = electron;

let mainWindow;
let htmlFiles = [];

function createWindow() {
  mainWindow = new BrowserWindow({
    kiosk: true,
    fullscreen: true,
    frame: false
  });

  // Load the first file in the list
  mainWindow.loadFile(htmlFiles[0]);

  // Set up an interval to cycle through the files
  let index = 1;
  setInterval(() => {
    mainWindow.loadFile(htmlFiles[index]);
    index = (index + 1) % htmlFiles.length;
  }, 10000);
}

// Read the contents of the HTML folder and store the filenames in an array
fs.readdirSync(path.join(__dirname, 'HTML')).forEach(file => {
  if (path.extname(file) === '.html') {
    htmlFiles.push(path.join(__dirname, 'HTML', file));
  }
});

app.on('ready', createWindow);
