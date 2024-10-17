import gradio as gr


def show_warning(selection: gr.SelectData):
    print(selection.value['image'],selection,sep="\n")
    gr.Warning(
        f"Your choice is #{selection.index}, with image: {selection.value['image']['path']}!"
    )


with gr.Blocks() as demo:
    image_gallery = gr.Gallery(
        [
            "inputs/faces/thumbnils/men1.png",
            "inputs/faces/thumbnils/men2.png",
            "inputs/faces/thumbnils/men3.png",
        ],
        allow_preview=False,
        preview=False,
        columns=[7],
        rows=[10],
    )

    image_gallery.select(fn=show_warning, inputs=None)

demo.launch()
