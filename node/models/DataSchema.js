import mongoose from "mongoose";

const dataSchema = new mongoose.Schema({
  id: { type: String, required: true },
  question: { type: String, required: true },
  transcribed_text: { type: String, required: true },
  loggedInEmail: { type: String, required: true },
  session_id: { type: Number },  // optional, add required: true if needed
  report: {
    CosineSimilarity: { type: Number },
    TechnicalWordConcurrency: { type: Number },
    RepeatedWords: { type: Number },
    Precision: { type: Number },
    PredefinedTechnicalWordsCount: { type: Number },
    InputTechnicalWordsCount: { type: Number },
    Accuracy: { type: Number },
    tfidf_matrix: { type: [String] },
  },
}, { timestamps: true });

const Data = mongoose.model("Data", dataSchema);
export default Data;
