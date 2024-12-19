# Lyrics-Audio Alignment

## Project Overview
This project implements a robust pipeline for **lyrics-to-audio alignment** leveraging state-of-the-art self-supervised learning models such as **Wav2Vec 2.0** and **WavLM**. The system incorporates advanced techniques like **vocal separation**, **segmentation**, and **forced alignment**, achieving competitive results on the **Jamendo V1 dataset**. The repository includes modified implementations of popular frameworks and custom preprocessing workflows to simplify the alignment task.

## Key Features
- **Vocal Extraction:** Utilizes the **HTDemucs model** for precise vocal and instrumental separation.
- **Segmentation:** Processes LRC-format lyrics and timestamps them for precise alignment.
- **Forced Alignment:** Employs **Connectionist Temporal Classification (CTC)** and dynamic programming to achieve accurate alignment.
- **Model Fine-Tuning:** Adapts pre-trained models (e.g., `wav2vec2-960h`) for singing voices using custom datasets.
- **Evaluation Metrics:** Includes metrics such as **Average Absolute Error (AAE), Median Absolute Error (MAE), and Percentage of Correct Segments (PCS)**.

## Repository Structure
```plaintext
Lyrics-audio-Alignment/
│
├── code/
│   ├── ARS_base.py                # Base script for alignment system
│   ├── clean_name.py              # Cleans and standardizes file names
│   ├── Evaluation.ipynb           # Script for evaluating alignment accuracy
│   ├── Extract_vocals.ipynb       # Vocal extraction using HTDemucs
│   ├── Finetune.ipynb             # Fine-tuning pipeline
│   ├── get_dataset.py             # Fetches and prepares datasets
│   ├── Lyrics.py                  # Lyrics processing utility
│   ├── MIREXEvaluate.py           # MIREX evaluation metrics implementation
│   ├── MMS_pytorch_base.py        # Base script for MMS model
│   ├── modify.py                  # Utility for dataset modifications
│   ├── Preprocess_en.ipynb        # Preprocessing for English songs
│   ├── Train_en.ipynb             # Training scripts for English datasets
│   ├── Visualization.ipynb        # Visualizes fine-turning loss
│
├── dataset/
│   ├── output-en/                 # Processed files and generated results
│   ├── songs_en/                  # Original songs and lyrics in `.lrc` and `.ogg/.wav`
│
├── model/                         # Checkpoints for fine-tuned models
│   ├── checkpoint-3000/
│   ├── checkpoint-12000/
│
├── newDALICode/                   # Modified DALI dataset scripts
│   ├── README.md
│   ├── download.py
│
├── newTrain/                      # Custom adaptations of lyrics-sync repository
│   ├── train.ipynb
│
├── test/
│   ├── ASR_test.ipynb             # Testing ASR-based models
│   ├── MMS_test.ipynb             # MMS model testing
│
├── README.md                      # This document
├── LICENSE                        # License information
└── Final_Report.pdf               # Detailed project report
```
## Datasets

This project uses the following datasets:
1. **DALI Dataset** ([Zenodo](https://zenodo.org/record/2577915)): A large, annotated dataset of synchronized audio, lyrics, and notes.
2. **Jamendo V1 Dataset** ([GitHub](https://github.com/f90/jamendolyrics)): A benchmark dataset used in MIREX evaluations.
3. **Custom App Dataset**: Audio-lyric pairs collected from popular karaoke and streaming platforms.

Due to size limitations, only sample files are uploaded to the repository. To access the full datasets, refer to the respective links.

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/WF2205/Lyrics-audio-Alignment.git
   cd Lyrics-audio-Alignment
    ```

2. Install dependencies: Recommand to use conda to create a virtual environment and use a Python 3.9+ version.
   ```bash
   conda env update -f environment.yml
   ```

## Usage
### Preprocessing
1. Prepare the dataset using:

```bash
python get_dataset.py
```

2. Fine-Tuning
Run the fine-tuning script

Run the `Preprocessing_en.ipynb` script to preprocess the English dataset.

Run the `Train_en.ipynb` script to train the model.

3. Evaluation
Evaluate the results using:

```bash
jupyter notebook Evaluation.ipynb
```

4. Visualizing Results

Run `Visualization.ipynb` or find the output in `Train_en.ipynb`


## Example Workflow
### To experience the alignment results:

1. Drag a `.lrc` file and its corresponding `.ogg/.wav` file into the [Lyrics Player Tool](https://mikezzb.github.io/lrc-player/).
2. Observe the synchronized lyrics displayed in real time.

## Results
### Jamendo V1 Dataset:

1. FZZ1 (WavLM + Conformer): AAE = 0.547, PCS = 68.6%.
2. NUS Baseline: AAE = 0.217, PCS = 75.1%.
3. Our Model (wav2vec2-960h): AAE = 0.626, PCS = 67.3%.

### Loss Curves:

As shown in `Visualization.ipynb`, the loss curve for fine-tuning the model is visualized.

## References
Baevski et al., 2020. *Wav2Vec 2.0: A Framework for Self-Supervised Learning of Speech Representations. [arXiv:2006.11477](https://arxiv.org/abs/2006.11477)*

Mikezzb, 2023. Lyrics-Sync Repository. [GitHub](https://github.com/mikezzb/lyrics-sync)

[MIREX 2024](https://www.music-ir.org/mirex/wiki/2024:Lyrics-to-Audio_Alignment)

## Acknowledgments
This project is based on the work of Mikezzb, whose repository served as a starting point for our project.