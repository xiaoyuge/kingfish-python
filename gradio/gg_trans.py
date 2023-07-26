import gradio as gr
import requests
import json

def translate(text, target_language):
    url = "<https://translation.googleapis.com/language/translate/v2>"
    params = {
        "q": text,
        "target": target_language,
        "key": "YOUR_API_KEY"
    }
    response = requests.post(url, params=params)
    return response.json()["data"]["translations"][0]["translatedText"]

iface = gr.Interface(
    fn=translate,
    inputs=[
        gr.inputs.Textbox(label="输入文本"),
        gr.inputs.Dropdown(
            ["英语", "西班牙语", "法语", "德语", "日语"],
            label="目标语言"
        )
    ],
    outputs=gr.outputs.Textbox(label="翻译结果")
)

iface.launch()