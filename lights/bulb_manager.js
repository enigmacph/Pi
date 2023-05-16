const TuyAPI = require("tuyapi");

const device = new TuyAPI({
  id: "bf14d5aed474c2ef8bopuj",
  key: "de6f8003feda8bc1",
});

let stateHasChanged = false;

// Find device on network
device.find().then(() => {
  // Connect to device
  device.connect();
});

// Add event listeners
device.on("connected", () => {
  console.log("Connected to device!");
});

device.on("disconnected", () => {
  console.log("Disconnected from device.");
});

device.on("error", (error) => {
  console.log("Error!", error);
});

device.on("data", (data) => {
  console.log("Data from device:", data);

  console.log(`Boolean status of default property: ${data.dps["1"]}.`);

  // Set default property to opposite
  if (!stateHasChanged) {
    device.set({ set: !data.dps["1"] });

    // Otherwise we'll be stuck in an endless
    // loop of toggling the state.
    stateHasChanged = true;
  }
});

// Disconnect after 10 seconds
setTimeout(() => {
  device.disconnect();
}, 10000);
/*
[
    {
      name: 'Gang midt',
      id: 'bf14d5aed474c2ef8bopuj',
      key: 'de6f8003feda8bc1'
    },
    {
      name: 'Gang indgang',
      id: 'bfcfd63b955077f2616mqc',
      key: '4eb0ba087dbfc058'
    },
    {
      name: 'Gang køkken',
      id: 'bf4c1f56e1fadaf09cyoaw',
      key: '710ae8c9c9aa2019'
    }
  ]

  const tuya = new TuyaContext({
  baseUrl: "https://openapi.tuyaeu.com",
  accessKey: "33d9eey4kujyy9w4rs8q",
  secretKey: "faf5dd5be9b446c2aa23753fcdd29e41",
});

*/
