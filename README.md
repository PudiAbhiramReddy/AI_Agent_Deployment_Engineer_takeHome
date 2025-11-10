# Hippocratic AI Coding Assignment: An Intelligent Story Generation System

## Project Overview

This project implements an intelligent bedtime story generation system that goes beyond a simple prompt-to-story script. The solution uses a multi-agent AI architecture to ensure every story is high-quality, creative, and perfectly appropriate for its target audience of children aged 5-10.

The core of the system is a **Storyteller-Judge loop**, which iteratively generates, evaluates, and refines a story until it meets a high standard of quality, creativity, and engagement.

---

## My Approach: The Storyteller-Judge System

The system is designed to mimic a professional creative and editorial workflow, ensuring a robust and reliable output.

### Core Components

1.  **Orchestrator (`main.py`):** The main script that manages the entire process, from taking user input to coordinating between the AI agents.
2.  **Storyteller AI:** A `gpt-3.5-turbo` instance prompted to act as a creative children's author. Its primary job is to generate an initial story draft based on the user's request.
3.  **Judge AI:** The same `gpt-3.5-turbo` model but prompted with a different persona: a **picky, hard-to-please children's book editor**. The Judge's job is not just to check for basic appropriateness but to ensure the story is also engaging and creative, failing any story that is too generic or boring.

### The Self-Correction Loop

The system's real strength lies in its ability to self-correct and improve its own output:

1.  **Generate:** The Storyteller creates a first draft of the story.
2.  **Evaluate:** The draft is passed to the picky Judge, who evaluates it against a specific rubric that includes appropriateness, clarity, and engagement.
3.  **Decide:**
    *   If the story **PASSES**, it is presented to the user.
    *   If the story **FAILS**, the Judge provides a clear, actionable reason for the rejection (e.g., "The story is too generic and lacks a magical element.").
4.  **Revise:** The system enters a revision loop. It provides the Storyteller with the original failed draft and the Judge's specific feedback, instructing it to write a new, improved version that directly addresses the editor's concerns, for example, by adding a unique or magical detail.

This cycle continues for a set number of attempts, ensuring the final product is the result of iterative refinement.

---

## How to Run This Project

### Prerequisites
- Python 3.7+
- An OpenAI API Key

### 1. Clone the Repository
Clone the project to your local machine and navigate into the directory.

### 2. Install Dependencies
Install the required Python libraries using pip.

pip install openai python-dotenv


### 3. Set Up Your API Key
1.  In the root of the project directory, create a new file named '.env'.
2.  Open the '.env' file and add your OpenAI API key.


### 4. Run the Script
Execute the main script from your terminal:
