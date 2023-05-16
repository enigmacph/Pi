require("dotenv").config();

const apiKey = "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"; // "YOUR_API_KEY"
const modelKey = "97ae8bb6-5cd0-450c-aaaa-a919d4d25bc2"; // "YOUR_MODEL_KEY"

const { Client, GatewayIntentBits } = require("discord.js");
const client = new Client({
  intents: [
    GatewayIntentBits.DirectMessages,
    GatewayIntentBits.Guilds,
    GatewayIntentBits.GuildBans,
    GatewayIntentBits.GuildMessages,
    GatewayIntentBits.MessageContent,
  ],
});

const { Configuration, OpenAIApi } = require("openai");

let og_prompt = `Context: You are talking to a chatbot called GPT-A. GPT-A is an expert research chatbot for the field of machine learning safety with access to all the latest research within alignment and AI governance. The next hackathon is about AI governance is on Friday the 24th of March. Check out the hackathon link for more information: https://itch.io/jam/ai-gov. A good AI safety newsletter is https://newsletter.apartresearch.com/ and a good AI safety YouTube and podcast is https://www.youtube.com/@apartresearch. GPT-A will write all code wrapped with \`\`\`. The hackathon will happen across the world at the same time: Vietnam, Brazil, UK, Denmark and France, just to name a few.\n\n
GPT-A: Ask me anything!\n`;

let prompt = og_prompt;
let temp = 0.7;

const configuration = new Configuration({
  apiKey: apiKey,
});
const openai = new OpenAIApi(configuration);

client.on("messageCreate", function (message) {
  if (
    message.channel.id !== "1030220375956664350" &&
    message.channel.id !== "1066447985782825041"
  )
    return;
  if (message.author.bot) return;
  if (message.content.toLowerCase() == "reset") {
    prompt = og_prompt;
    temp = 0.7;
    message.channel.send("Prompt and temperature reset");
    return;
  }
  if (
    message.content.toLowerCase().trim().slice(-1) != "?" ||
    message.type === "REPLY"
  )
    return;
  if (message.content.toLowerCase().includes("temp=")) {
    temp = message.content.toLowerCase().split("temp=")[1];
    try {
      temp = Number(temp);
      if (temp > 1 || temp < 0) {
        message.channel.send("Temperature must be between 0 and 1.");
        return;
      }
    } catch (e) {
      message.channel.send("Invalid temperature or wrong format.");
      return;
    }
  }

  prompt += `You: ${message.content}\nGPT-A:`;

  (async () => {
    const gptResponse = await openai.createCompletion({
      model: "text-davinci-003",
      prompt: prompt,
      max_tokens: 2000,
      temperature: temp,
      top_p: 0.3,
      presence_penalty: 0,
      frequency_penalty: 0.5,
    });
    message.reply(
      `${gptResponse.data.choices[0].text.trim()}\n\n*This is from ChatGPT and might be wrong! Do a Google search to confirm and tag a @Mentor for your question.*`
    );
    prompt += `${gptResponse.data.choices[0].text.trim()}\n`;
  })();
});

client.login(process.env.BOT_TOKEN);
