# SQUAD Reformatter

The [SQuAD dataset](https://rajpurkar.github.io/SQuAD-explorer/) was designed for the task of machine reading comprehension. The task consists in answering a question related to a specific passage by selecting which part of the passage answers the question.

In this repo you will find a simple tool which reformats the SQuAD dataset into a more useful way in which it breaks apart the passages into sentences, and adds to the answers the sentence in which it is found.

## Usage

```
python SquadProcessing.py <squad_file> <save_file>
```

## Data Description

### Original format
The dataset was given in 2 different JSON files that have the following structure:

  - title : str
  - paragraphs : []
      - context : str
      - qas : []
          - question : str
          - id : int
          - answers : []
              - text : str
              - answer_start : int

 The index described in *answer_start* is 0 based.

### Output format
Processed QA JSON Structure:

- root : []
    - topic : str
    - paragraphs : []
        - pid : int
        - sentences: []
            - text : str
            - pos : int
            - start_idx : int
        - qas: []
            - qid : int
            - question : str
            - answers:
                - sent_pos : int
                - text : str
                - answer_start : int

The passage id embeds the id for the topic and its corresponding passages in the following way:

- the 10k's describe the topic
- the units describe the passage