
# System Design: Storyteller-Judge AI

This document outlines the architecture and flow of the bedtime story generation system. The system is designed as a loop of generation and evaluation to ensure the final story meets a high standard of quality and appropriateness for children.

## Components

1.  **User:** The person who provides the initial story idea.
2.  **Orchestrator (`main.py`):** The main Python script that manages the entire process flow. It receives user input, calls the LLMs, and decides the next steps based on the outcomes.
3.  **Storyteller AI (LLM):** An instance of the `gpt-3.5-turbo` model prompted to be a creative children's story author. Its job is to generate or revise a story.
4.  **Judge AI (LLM):** An instance of the `gpt-3.5-turbo` model prompted to be a picky children's book editor. Its job is to evaluate the story against a rubric that includes both appropriateness and creativity.

## Block Diagram of the System Flow


Here is a text-based block diagram illustrating the interaction between the components.
  

```text
               ┌──────────┐
               │   User   │
               └──────────┘
                    │
                    │ 1. Provides a story idea.
                    ▼
          ┌──────────────────────┐
          │ Orchestrator (`main.py`) │
          └──────────────────────┘
                    │
                    │ 2. Creates and sends a "Storyteller Prompt".
                    ▼
     ┌────────────────────────┐
     │  Storyteller AI (LLM)  │
     └────────────────────────┘
                    │
    _               │ 3. Generates and returns the first story draft.
                    ▼
          ┌──────────────────────┐
          │ Orchestrator (`main.py`) │
          └──────────────────────┘
                    │
                    │ 4. Sends the story draft for evaluation.
                    ▼
          ┌───────────────────┐
          │   Judge AI (LLM)  │
        _ └───────────────────┘
                    │
                    │ 5. Returns a verdict ("PASS" or "FAIL") with a reason.
                    ▼
          ┌──────────────────────┐
          │ Orchestrator (`main.py`) │
          │                      │
          │    Makes Decision    │
          └──────────┬───────────┘
                     │
         ┌───────────┴───────────┐
         │                       │
         ▼                       ▼
┌─────────────────┐     ┌──────────────────────────────────┐
│    If "PASS"    │     │             If "FAIL"            │
└─────────────────┘     └──────────────────────────────────┘
         │       _               │
         │ 6a. The final story   │ 6b. The Orchestrator creates a
         │     is displayed      │     "Revision Prompt" using the
         │     to the User.      │     Judge's feedback.
         │                       │
         ▼                       │
       (END)                     └─────► (This loops back to the Storyteller)
```


 

### Flow Explanation

1.  **User Input:** The process starts when the user provides a simple story prompt.
2.  **First Draft:** The Orchestrator takes this input and embeds it into a detailed `STORYTELLER_PROMPT_TEMPLATE`. It calls the LLM, which acts as the **Storyteller** to generate the first draft.
3.  **Evaluation:** The Orchestrator then takes this draft and sends it to the same LLM but with a different prompt, the `JUDGE_PROMPT_TEMPLATE`. In this role, the LLM acts as the **Judge**. The Judge is instructed to be picky and fail stories that are too generic or boring.
4.  **Verdict:** The Judge evaluates the story against the built-in rubric and returns a simple verdict: "PASS" or "FAIL". If it fails, it also provides a reason.
5.  **Decision Point:**
    *   If the verdict is **"PASS"**, the story is considered high-quality and is immediately shown to the user. The process ends successfully.
    *   If the verdict is **"FAIL"**, the Orchestrator captures the reason for failure (e.g., "the story is too generic").
6.  **Revision Loop:** The system uses a `REVISION_PROMPT_TEMPLATE`, which includes the original request, the failed story, and the Judge's feedback. It asks the **Storyteller** to rewrite the story, addressing the specific issues (like adding a magical detail). This new draft is then sent back to the **Judge** for re-evaluation (Step 3).

7.  **Termination:** The loop continues for a set number of attempts. If a story doesn't pass after these attempts, the system informs the user that it could not generate a suitable story and shows the last failed draft.

