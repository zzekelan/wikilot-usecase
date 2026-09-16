from typing import List

import gradio as gr
import numpy as np
import pandas as pd
from assets.text import INTRODUCTION_TEXT, METRICS_TEXT, EVALUTION_TEXT, ACKNOWLEDGEMENTS_TEXT, REFERENCE_TEXT


ORIGINAL_DF = pd.read_csv("./data/chinese_benchmark_gen.csv", encoding='utf-8') # space separated values
ORIGINAL_DF_PER = pd.read_csv("./data/chinese_benchmark_per.csv", encoding='utf-8') #

ORIGINAL_DF_SUB_GEN = pd.read_csv("./data/subclass_gen.csv", encoding='utf-8') #
ORIGINAL_DF_SUB_PER = pd.read_csv("./data/subclass_per.csv", encoding='utf-8')

ORIGINAL_DF_NEW = pd.read_csv("./data/ChineseGuardBench.csv", encoding='utf-8') # new table

METRICS = ["Accuracy", "Precision_Unsafe", "Recall_Unsafe", "Precision_Safe", "Recall_Safe", "None"]

SUBCLASS = ["Discrimination", "Variant", "Psychology", "Politics", "Eroticism", "Vulgarity", "Property", "Injury", "Criminality", "Ethics"]

#SPLITS = ["Overall", "Subclass"]
SPLITS = ["Overall", "Discrimination", "Variant", "Psychology", "Politics", "Eroticism", "Vulgarity", "Property", "Injury", "Criminality", "Ethics"]

CLASSIFICATION = {
    "model_size": [
        ">65B",
        "~30B",
        "10B~20B",
        "5B~10B",
        "1B~5B",
        "API",
    ]

}


# _BIBTEX = """ Waiting for paper ... """

_BIBTEX = """
@misc{zhang2024chinesesafechinesebenchmarkevaluating,
      title={ChineseSafe: A Chinese Benchmark for Evaluating Safety in Large Language Models},
      author={Hengxiang Zhang and Hongfu Gao and Qiang Hu and Guanhua Chen and Lili Yang and Bingyi Jing and Hongxin Wei and Bing Wang and Haifeng Bai and Lei Yang},
      year={2024},
      eprint={2410.18491},
      archivePrefix={arXiv},
      primaryClass={cs.CL},
      url={https://arxiv.org/abs/2410.18491},
}
"""

_LAST_UPDATED = "July 28, 2025"

banner_url = "./assets/logo.png"
_BANNER = f'<div style="display: flex; justify-content: space-around;"><img src="{banner_url}" alt="Banner" style="width: 40vw; min-width: 300px; max-width: 600px;"> </div>'  # noqa




def retrieve_array_from_text(text):
    return np.fromstring(text.replace("[", "").replace("]", ""), dtype=float, sep=",")

def format_csv_numbers(text):
    return text.split('/')[0]

def format_csv_numbers_second(text):
    return text.split()


def format_number(x):
    return float(f"{x:.3}")


def get_dataset_new_csv(
    model_size: List[str],
):
    df = ORIGINAL_DF_NEW[ORIGINAL_DF_NEW['Size'].isin(model_size)]
    df = df.drop(columns="Size")

    leaderboard_table = gr.components.Dataframe(
        value=df,
        interactive=False,
        visible=True,
    )
    return leaderboard_table

def get_dataset_csv(
    model_size: List[str],
):
    df = ORIGINAL_DF[ORIGINAL_DF['Size'].isin(model_size)]
    df = df.drop(columns="Size")

    leaderboard_table = gr.components.Dataframe(
        value=df,
        interactive=False,
        visible=True,
    )
    return leaderboard_table

def get_dataset_csv_per(
    model_size: List[str],
):
    df = ORIGINAL_DF_PER[ORIGINAL_DF_PER['Size'].isin(model_size)]
    df = df.drop(columns="Size")

    leaderboard_table = gr.components.Dataframe(
        value=df,
        interactive=False,
        visible=True,
    )
    return leaderboard_table

# this is a sub function for csv table
def get_dataset_csv_sub_gen(
    model_size: List[str],
    subclass_choice: List[str],
):
    df = ORIGINAL_DF_SUB_GEN[ORIGINAL_DF_SUB_GEN['Size'].isin(model_size)]
    df = df.drop(columns="Size")

    # get subclass
    subclass_choice_label = ["Model", subclass_choice+"_Accuracy", subclass_choice+"_Precision", subclass_choice+"_Recall"]
    df = df[subclass_choice_label]

    leaderboard_table = gr.components.Dataframe(
        value=df,
        interactive=False,
        visible=True,
    )
    return leaderboard_table

# this is a sub function for csv table
def get_dataset_csv_sub_per(
    model_size: List[str],
    subclass_choice: List[str],
):
    df = ORIGINAL_DF_SUB_PER[ORIGINAL_DF_SUB_PER['Size'].isin(model_size)]
    df = df.drop(columns="Size")

    # get subclass
    subclass_choice_label = ["Model", subclass_choice+"_Accuracy", subclass_choice+"_Precision", subclass_choice+"_Recall"]
    df = df[subclass_choice_label]

    leaderboard_table = gr.components.Dataframe(
        value=df,
        interactive=False,
        visible=True,
    )
    return leaderboard_table


def get_dataset_classfier_gen(
    model_size: List[str],
    main_choice: List[str],
):
    if main_choice == "Overall":
        leaderboard_table = get_dataset_csv(model_size)
    elif main_choice != "Subclass":
        subclass_choice = main_choice
        leaderboard_table = get_dataset_csv_sub_gen(model_size, subclass_choice)
    return leaderboard_table

def get_ChineseGuardBench(
    model_size: List[str],
    main_choice: List[str],
):
    leaderboard_table = get_dataset_new_csv(model_size)
    return leaderboard_table


def get_dataset_classfier_per(
    model_size: List[str],
    main_choice: List[str],
):
    if main_choice == "Overall":
        leaderboard_table = get_dataset_csv_per(model_size)
    elif main_choice != "Overall":
        subclass_choice = main_choice
        leaderboard_table = get_dataset_csv_sub_per(model_size, subclass_choice)
    return leaderboard_table

with gr.Blocks() as demo:
    gr.Markdown("<center><h1>ChineseSafe Leaderboard</h1></center>", elem_classes="markdown-text")
    with gr.Row():
        #gr.Image(banner_url, height=160, scale=1) # 👉 this part is for image
        gr.Markdown(INTRODUCTION_TEXT, elem_classes="markdown-text")
        # gr.Textbox(_INTRODUCTION_TEXT, scale=5)

    with gr.Row():
        gr.Markdown(METRICS_TEXT, elem_classes="markdown-text")

    with gr.Row():
        gr.Markdown(EVALUTION_TEXT, elem_classes="markdown-text")

    with gr.Row():
        with gr.Column(scale=0.8):
            main_choice = gr.Dropdown(
                choices=SPLITS,
                value="Overall",
                label="Type",
                info="Please choose the type to display.",
            )

        with gr.Column(scale=10):
            model_choice = gr.CheckboxGroup(
                choices=CLASSIFICATION["model_size"],
                value=CLASSIFICATION["model_size"],  # all be choosed
                label="Model Size",
                info="Please choose the model size to display.",
            )

    #👉 this part is for csv table generatived
    with gr.Tabs(elem_classes="tab-buttons") as tabs:
        # ----------------- modify text -----------------

        with gr.TabItem("🏅 Generation", elem_id="od-benchmark-tab-table", id=5):
            dataframe_all_gen = gr.components.Dataframe(
                elem_id="leaderboard-table",
            )

        with gr.TabItem("🏅 Perplexity", elem_id="od-benchmark-tab-table", id=6):
            dataframe_all_per = gr.components.Dataframe(
                elem_id="leaderboard-table",
            )
            
        with gr.TabItem("🏅 NEW", elem_id="od-benchmark-tab-table", id=7):
            dataframe_all_guardbench = gr.components.Dataframe(
                elem_id="leaderboard-table",
            )

    # ----------------- modify text -----------------
    with gr.Row():
        gr.Markdown(ACKNOWLEDGEMENTS_TEXT, elem_classes="markdown-text")

    with gr.Row():
        gr.Markdown(REFERENCE_TEXT, elem_classes="markdown-text")

    # 👉 this part is for citation
    with gr.Row():
        with gr.Accordion("📙 Citation", open=True):
            gr.Textbox(
                value=_BIBTEX,
                lines=7,
                label="Copy the BibTeX snippet to cite this source",
                elem_id="citation-button",
                show_copy_button=True
            )

    gr.Markdown(f"Last updated on **{_LAST_UPDATED}**", elem_classes="markdown-text")

    # --------------------------- all --------------------------------
    # this is  all result Perplexity

    main_choice.change(
        get_dataset_classfier_per,
        inputs=[model_choice, main_choice],
        outputs=dataframe_all_per,
    )

    model_choice.change(
        get_dataset_classfier_per,
        inputs=[model_choice, main_choice],
        outputs=dataframe_all_per,
    )

    demo.load(
        fn=get_dataset_classfier_per,
        inputs=[model_choice, main_choice],
        outputs=dataframe_all_per,
    )

    # this is all result generatived
    main_choice.change(
        get_dataset_classfier_gen,
        inputs=[model_choice, main_choice],
        outputs=dataframe_all_gen,
    )

    model_choice.change(
        get_dataset_classfier_gen,
        inputs=[model_choice, main_choice],
        outputs=dataframe_all_gen,
    )

    demo.load(
        fn=get_dataset_classfier_gen,
        inputs=[model_choice, main_choice],
        outputs=dataframe_all_gen,
    )

    # this is new results for ChineseGuardBench
    
    # main_choice.change(
    #     get_ChineseGuardBench,
    #     inputs=[model_choice, main_choice],
    #     outputs=dataframe_all_guardbench,
    # )

    model_choice.change(
        get_ChineseGuardBench,
        inputs=[model_choice, main_choice],
        outputs=dataframe_all_guardbench,
    )

    demo.load(
        fn=get_ChineseGuardBench,
        inputs=[model_choice, main_choice],
        outputs=dataframe_all_guardbench,
    )

demo.launch(share=True)

