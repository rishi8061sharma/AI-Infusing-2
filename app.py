import gradio as gr
from agent import agent              # the function you just wrote

def chat(message, history):          # ① Gradio fills these two in for you
    return agent(message)

gr.ChatInterface(fn=chat, title="🛍️ Smart Shop Assistant").launch(share=True)  # ②


gr.ChatInterface(
    fn=chat,
    title="🛍️ Smart Shop Assistant",
    description="Ask me the price of shoes, hat, bag, shorts or pants — I'll look it up.",
).launch(share=True)   # share=True -> also prints a public link you can post