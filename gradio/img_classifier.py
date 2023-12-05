import gradio as gr

def image_classifier(inp):
    # 这里可以写一写实际实现的逻辑
    return {'cat': 0.3, 'dog': 0.7}

demo = gr.Interface(fn=image_classifier, inputs="image", outputs="label")
demo.launch()