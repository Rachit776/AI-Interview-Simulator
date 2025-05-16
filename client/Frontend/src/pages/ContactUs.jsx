import React from "react";
import { FaLinkedin, FaGithub } from "react-icons/fa"; // Import the icons
import "./ContactUs.css";

const ContactUs = () => {
  const developerPhoto = "https://avatars.githubusercontent.com/u/98811013?v=4"; // Developer's photo

  return (
    <div className="contact-container">
        <img src={developerPhoto} alt="Developer" className="profile-pic" />
        <h2 className="created-by">Created by</h2>
        <h1 className="name">Rachit Kumar Choudhary</h1>
        <h2>About This Project</h2>
        <div className="summary">
        <p>
        The AI Interview Simulator is a full-stack platform that replicates technical interview scenarios using AI for real-time feedback. Built with React (frontend), Node.js (backend), and Flask (AI service), it offers users practice in Frontend, Backend, or Machine Learning interviews. The platform features audio recording, speech-to-text transcription via OpenAI’s Whisper, and performance grading based on custom NLP algorithms. User sessions are secured with Google OAuth and JWT authentication, while RabbitMQ handles communication between services. MongoDB stores interview data for tracking progress. Designed for low-latency, actionable insights, it helps candidates refine their interview skills effectively.
        </p>
        </div>

      

      <div className="links">
        <a href="https://www.linkedin.com/in/rachit-kumar-593a5b24a" target="_blank" rel="noopener noreferrer">
          <FaLinkedin size={30} /> 
        </a>
        <a href="https://github.com/rachit776" target="_blank" rel="noopener noreferrer">
          <FaGithub size={30} /> 
        </a>
      </div>
    </div>
  );
};

export default ContactUs;
