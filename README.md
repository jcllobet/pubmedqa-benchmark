# Medical Question Answering via RAG

This repo contains code for Medical Question Answering using RAG and state-of-the-art LLMs.

## Data

The data was retrieved from official source of [PubMedQA](https://pubmedqa.github.io/).

To download the data, you can follow the steps in the main [PubMedQA repository](https://github.com/pubmedqa/pubmedqa/tree/master).
Here are the required steps:

### Download

Download [PubMedQA repository](https://github.com/pubmedqa/pubmedqa/tree/master).
PQA-L is in `./data/`

To download the unlabeled data, use this link - [PQA-U](https://drive.google.com/open?id=1RsGLINVce-0GsDkCLDuLZmoLuzfmoCuQ)

To download the answers data, use this link - [PQA-A](https://drive.google.com/open?id=15v1x6aQDlZymaHGP7cZJZZYFfeJt2NdS)

### Split the dataset

After downloading PQA-A and PQA-U as `ori_pqaa.json` and `ori_pqau.json` in the `./data/`, enter the `./preprocess/` directory and split the dataset:

```bash
cd preprocess
python split_dataset.py pqaa
python split_dataset.py pqal
```

If all the steps were performed correctly, you will be able to find the files needed to run this repo in:
`pubmedqa-master/data/test_set.json` and `pubmedqa-master/data/test_ground_truth.json`.

## Experiments

### Dataset Analysis

Data Analysis was conducted in notebook - ``Data/```
We uploaded the dataset to Nomic embeddings, the resulting embedding space is visualized and publicly stored via
this [map link](https://atlas.nomic.ai/data/md927/pubmedqaunlabeled/map).

### 1. RAG: Unlabeled Data & Prompt: context and question

In this experiment the setup is the following:

- Embeddings in RAG: All unlabeled data from PubMedQA train set
- Input prompt:

```
Answer question: {QUESTION} given context: {CONTEXT}.
Answer can only be one word and it should be either 'yes', 'no', or 'maybe'
```

Results when context is included in the question:

| Model                                                | Accuracy | F1     |
| ---------------------------------------------------- | -------- | ------ |
| GPT3.5                                               | 0.686    | 0.5468 |
| GPT4 (gpt-4-0613)                                    | 0.552    | 0.2371 |
| GPT4 (gpt-4-0125-preview)                            | 0.748    | 0.5837 |
| GPT4 (gpt-4-turbo-2024-04-09)                        | 0.766    | 0.6212 |
| Meditron                                             | 0.364    | 0.2209 |
| RAG (Unlabeled Data) + GPT4 (gpt-4-0125-preview)     | 0.552    | 0.237  |
| RAG (Unlabeled Data) + GPT4 (gpt-4-turbo-2024-04-09) | 0.676    | 0.540  |

To evaluate baseline models run:

- [GPT3.5-GPT4-Prediction.ipynb](baselines%2FGPT3.5-GPT4-Prediction.ipynb)

To evaluate RAG run:

- [llamarun.ipynb](https://github.com/jcllobet/pubmedqa-benchmark/blob/main/llamarun.ipynb)
- with the relevant packages in requirements.txt and OPENAI and NOMIC keys:
  `cp .env.example .env`

````pip install -r requirements.txt
    # or
    conda install --file requirements.txt```
You can run all the cells directly. The only parameter you need to change is the `model_name` in the `llamarun.ipynb` notebook with one of the relevant models from OpenAI API [here](https://platform.openai.com/docs/models). Given the amount of time that it takes to upload the RAG vector DB, it is better to not re-run the entire notebook and just run the cells beneath the model name.

_Note: due to the stochastic nature of such models, the results may vary slightly between runs. You can set a seed and freeze it if you want the same results across different runs._
_Note: If you want to run it from the exact same data we originally ran the results, it can be downloaded from [here](https://drive.google.com/file/d/1pD4ua1HbPJLyjaSpa3fY68UKhTMf10AM/view?usp=sharing) and brought into the `./data/` folder._
### 2. RAG: Unlabeled Data & Prompt: Only Question

* Embeddings in RAG: All unlabeled data from PubMedQA train set
* Input prompt:
````

Answer question {QUESTION}. Answer can only be one word and it should be either 'yes', 'no', or 'maybe'

```

Results when context is excluded from the question:

| Model                                                | Accuracy | F1     |
|------------------------------------------------------|----------|--------|
| GPT3.5                                               | 0.348    | 0.2898 |
| GPT4 (gpt-4-0125-preview)                            | 0.552    | 0.3875 |
| GPT4 (gpt-4-turbo-2024-04-09)                        | 0.478    | 0.3725 |
| RAG (Unlabeled Data) + GPT4 (gpt-4-0125-preview)     | 0.462    | 0.3062 |
| RAG (Unlabeled Data) + GPT4 (gpt-4-turbo-2024-04-09) | 0.548    | 0.2435 |

To evaluate baseline models run:
* [GPT3.5-GPT4-Prediction-NoContext.ipynb](baselines%2FGPT3.5-GPT4-Prediction-NoContext.ipynb)

To evaluate RAG run:
- [llamarun.ipynb](https://github.com/jcllobet/pubmedqa-benchmark/blob/main/llamarun.ipynb)


### 3. RAG: Only Context & Prompt: Only Question

* Embeddings in RAG: Only Context from Test PubMedQA
* Input prompt:
```

Answer question {QUESTION}. Answer can only be one word and it should be either 'yes', 'no', or 'maybe'

````

Results when context is excluded from the question:

| Model                                         | Accuracy | F1     |
|-----------------------------------------------|----------|--------|
| GPT3.5                                        | 0.348    | 0.2898 |
| GPT4 (gpt-4-0125-preview)                     | 0.552    | 0.3875 |
| GPT4 (gpt-4-turbo-2024-04-09)                 | 0.478    | 0.3725 |
| RAG (Context) + GPT4 (gpt-4-0125-preview)     | 0.696    | 0.5137 |
| RAG (Context) + GPT4 (gpt-4-turbo-2024-04-09) | 0.69     | 0.5075 |

The baseline results are the same as for the previous experiment, and we only changed the RAG component.

To evaluate RAG run:
* [RAG_Context_GPT4.ipynb](rag%2FRAG_Context_GPT4.ipynb)


## Requirements
We used Google Colab to run the experiments but performed the data processing and selection on a local computer.
The dependencies required to run the code are thus included within the file since it is needed in Google Colab.
Libraries include:
```angular2html
pandas
transformers
torch
openai
sklearn
numpy
llama-index
matplotlib
nest_asyncio
````

## References & Resources

1. “PubMedQA: A Dataset for Biomedical Research Question Answering”, Jin et al., https://aclanthology.org/D19-1259/

2. “MEDITRON-70B: Scaling Medical Pretraining for Large Language Models”, Chen et al., https://arxiv.org/pdf/2311.16079.pdf

3. Evaluating Multimodal Models, “Nomic Blog” https://blog.nomic.ai/posts/improving-multimodal-models-with-atlas

4. Retrieval-Augmented Generation for Large Language Models: A Survey by Yunfan Gao et al. https://arxiv.org/abs/2312.10997
