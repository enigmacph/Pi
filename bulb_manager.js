// import { TuyaContext } from "@tuya/tuya-connector-nodejs";
// Write the above as require
const TuyaContext = require("@tuya/tuya-connector-nodejs").TuyaContext;

const tuya = new TuyaContext({
  baseUrl: "https://openapi.tuyaeu.com",
  accessKey: "33d9eey4kujyy9w4rs8q",
  secretKey: "faf5dd5be9b446c2aa23753fcdd29e41",
});

const controlLight = async (deviceId, newState) => {
  try {
    const device = await tuya.device.detail({
      device_id: "bf14d5aed474c2ef8bopuj",
    });
    await tuyaDevice.initDevice(deviceId);

    const status = await tuyaDevice.getDeviceState();
    console.log(`Current status of light ${deviceId}:`, status);

    await tuyaDevice.setDeviceState({ dps: 1, set: newState });

    const newStatus = await tuyaDevice.getDeviceState();
    console.log(`New status of light ${deviceId}:`, newStatus);
  } catch (error) {
    console.error(`Error controlling light ${deviceId}:`, error);
  }
};

(async () => {
  // Replace with the deviceId of the light you want to control
  const deviceId = "bf14d5aed474c2ef8bopuj";

  // Set the desired state for the light (true for on, false for off)
  const newState = false;

  // Control the light
  await controlLight(deviceId, newState);
})();
