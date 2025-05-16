import amqp from "amqplib";
import dotenv from "dotenv";
import { addMessageToProcessedList } from "../controllers/processedMessageController.js";

dotenv.config();

const queue = "transcribed-text";
const rabbitmq_url = process.env.RABBITMQ_URL;

function isValidJson(str) {
  try {
    JSON.parse(str);
    return true;
  } catch (e) {
    return false;
  }
}

export async function startConsumer() {
  try {
    //const connection = await amqp.connect(rabbitmq_url);
    const connection = await amqp.connect({
      protocol: 'amqp',
      hostname: process.env.RABBITMQ_HOST,
      port: parseInt(process.env.RABBITMQ_PORT),
      username: process.env.RABBITMQ_USER,
      password: process.env.RABBITMQ_PASS,
      frameMax: 8192, // Must be >= 8192
    });
    
    const channel = await connection.createChannel();

    // Ensure the queue exists and is durable
    await channel.assertQueue(queue, { durable: true });
    console.log(`||🟢 --- @ Worker WAITING FOR MESSAGE --- 🚀`);
    console.log(`\n RabbitMQ url:: ${rabbitmq_url}\n`);

    // Start consuming messages
    channel.consume(
      queue,
      async (msg) => {
        const messageContent = msg.content.toString();

        console.log(`\n[*] Received message: ${messageContent}`);

        let parsedMessage;
        if (isValidJson(messageContent)) {
          parsedMessage = JSON.parse(messageContent);
        } else {
          parsedMessage = { message: messageContent };
        }

        // Add the processed message to in-memory storage
        addMessageToProcessedList(parsedMessage);

        // Acknowledge the message
        channel.ack(msg);
      },
      { noAck: false }
    );
  } catch (error) {
    console.error("Error starting RabbitMQ consumer:", error);
  }
}
