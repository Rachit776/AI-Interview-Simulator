import express from "express";
import mongoose from "mongoose";
import bodyParser from "body-parser";
import cors from "cors";
import dotenv from "dotenv";
import session from "express-session";
import passport from "passport";
import authRouter from "./routes/authRouter.js";
import audioRouter from "./routes/audioRouter.js";
import { route as processedMessageRoute } from "./routes/processedMessageRoute.js";
import { startConsumer } from "./utils/consumer.js";
import "./utils/passport.js";

const app = express();
dotenv.config();

const CLIENT_URL = process.env.CLIENT_URL;

app.use(express.json());
app.use(bodyParser.json());
app.use((req, res, next) => {
	res.setHeader("Cross-Origin-Opener-Policy", "same-origin");
	res.setHeader("Cross-Origin-Embedder-Policy", "require-corp");
	res.setHeader("Access-Control-Allow-Origin", CLIENT_URL);
	res.setHeader("Access-Control-Allow-Methods", "GET, POST");
	res.setHeader("Access-Control-Allow-Headers", "Content-Type, Authorization");
	next();
});

app.use(
	session({
		secret: process.env.SESSION_SECRET,
		resave: false,
		saveUninitialized: true,
	})
);

app.use(
	cors({
		origin: CLIENT_URL,
		methods: ["GET", "POST", "PUT", "DELETE"],
		credentials: true,
	})
);

app.use(passport.initialize());
app.use(passport.session());

app.use("/api/auth", authRouter);
app.use("/api/audio", audioRouter);
app.use("/api/messages", processedMessageRoute);

app.post("/exchange", (req, res) => {
	const { message } = req.body;
	res.json({ status: "Message processed", message });
});

const PORT = process.env.PORT || 8010;
const URL = process.env.MONGOURL;

mongoose
	.connect(URL)
	.then(() => {
		console.log("DB connected successfully.");
		app.listen(PORT, () => {
			console.log(`Listening to Port: ${PORT}`);
			startConsumer();
		});
	})
	.catch((error) => console.log(error));
