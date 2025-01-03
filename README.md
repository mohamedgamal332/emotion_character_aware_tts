# Emotion-Character-Aware TTS

## Overview
Emotion-Character-Aware TTS is a novel processing pipeline designed to transform written novels into emotionally rich and character-aware audiobooks. The system extracts characters from the text, identifies their gender, and analyzes the emotional tone of their dialogue. This information is then passed to a Text-to-Speech (TTS) engine, which generates spoken audio with appropriate emotional and character-specific inflections.

The project leverages state-of-the-art NLP models for sentiment analysis and a powerful TTS engine to create a seamless and immersive audiobook experience. It is particularly useful for authors, publishers, and audiobook producers who want to automate the process of converting novels into high-quality, emotionally expressive audio content.

## Key Features

1. **Character Extraction**:
   - Identifies characters in the novel and clusters them based on semantic and string similarity.
   - Determines the gender of each character using contextual analysis.

2. **Sentiment Analysis**:
   - Uses the [j-hartmann/emotion-english-distilroberta-base model](https://huggingface.co/j-hartmann/emotion-english-distilroberta-base) to analyze the emotional tone of each character's dialogue.

3. **Text-to-Speech (TTS)**:
   - Integrates with [EmotiVoice](https://github.com/netease-youdao/EmotiVoice), a multi-voice and prompt-controlled TTS engine, to generate emotionally expressive audio.
   - Uses a Dockerized API for seamless TTS processing.

4. **Automated Pipeline**:
   - Processes novels from raw text to final audiobook output with minimal manual intervention.

## Workflow

1. **Input**: A novel in PDF or text format.
2. **Character Extraction**:
   - Extracts characters and their dialogue.
   - Determines character gender based on contextual clues.
3. **Sentiment Analysis**:
   - Analyzes the emotional tone of each character's dialogue using a pre-trained sentiment analysis model.
4. **TTS Generation**:
   - Passes the dialogue and emotional tone to the EmotiVoice TTS engine.
   - Generates audio files for each character's dialogue.
5. **Output**: A merged audiobook file with emotionally expressive and character-specific narration.

## Installation

### Prerequisites
- Python 3.11
- Docker (for running the EmotiVoice TTS API)
- GPU (recommended for faster processing)

### Steps

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/emotion_character_aware_tts.git
   cd emotion_character_aware_tts
   ```

2. **Set Up the Environment**:
   - Install Python dependencies:
     ```bash
     pip install -r requirements.txt
     ```

3. **Run the EmotiVoice TTS API**:
   - Start the Docker container for EmotiVoice:
     ```bash
     docker run -d -p 5000:5000 --gpus=all r8.im/bramhooimeijer/emotivoice@sha256:261b541053a0a30d922fd61bb47fbbc669941cb84f96a8f0042f14e8ad34f494
     ```

## Usage

1. **Prepare the Input**:
   - Place your novel in PDF or text format in the `input` directory.

2. **Run the Pipeline**:
   - Execute the main script to process the novel:
     ```bash
     python main.py
     ```

3. **Output**:
   - The final audiobook will be saved as `Audiobook.mp3` in the `output` directory.

## API Request Format

The EmotiVoice TTS API is used to generate audio. Here is the request format:

```bash
curl -s -X POST \
  -H "Content-Type: application/json" \
  -d $'{
    "input": {
      "prompt": "Happy",
      "content": "Emoti-Voice - a Multi-Voice and Prompt-Controlled T-T-S Engine",
      "speaker": "8051",
      "language": "English"
    }
  }' \
  http://localhost:5000/predictions
```

## Example

### Input:
A novel in PDF format (e.g., `Moby_Dick.pdf`).

### Output:
An audiobook file (`Audiobook.mp3`) with character-specific and emotionally expressive narration.

## Contributing

Contributions are welcome! If you'd like to contribute, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Submit a pull request with a detailed description of your changes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgments

- [EmotiVoice](https://github.com/netease-youdao/EmotiVoice) for the TTS engine.
- [j-hartmann/emotion-english-distilroberta-base](https://huggingface.co/j-hartmann/emotion-english-distilroberta-base) for sentiment analysis.
- [PyPDF2](https://pypi.org/project/PyPDF2/) for PDF text extraction.

## Contact

For questions or feedback, please open an issue on GitHub or contact the maintainer at mohamednafel006@gmail.com.

Enjoy creating emotionally rich audiobooks with Emotion-Character-Aware TTS! 🎧📚
