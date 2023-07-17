import gradio as gr
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def talk_to_chatgpt(messages):
    history_turn=5
    dt = {
        "model": "gpt-3.5-turbo",
        "messages": ([messages[0]] + messages[-history_turn:]) if len(messages) > history_turn else messages,
        "temperature": 1,
        "max_tokens": 512
    }
    API_URL = 'http://127.0.0.1:8000/v1/chat/completions'
    message = {'role': 'assistant', 'content': ''}
    try:
        x = requests.post(API_URL, json=dt, stream=True, verify=False)
        message = x.json()['choices'][0]['message']
    except Exception as e:
        message['content'] = str(e)
    finally:
        return message


def add_text(log, messages, text):
    messages.append({'role': 'user', 'content': text})
    message = talk_to_chatgpt(messages)
    messages.append(message)
    log.append((text, message['content']))
    return log, messages, log


# def add_image(state, image):
#     state = state + [(f"![](/file={image.name})", "Cool pic!")]
#     return state, state


with gr.Blocks(css="#chatbot .overflow-y-auto{height:500px}") as demo:
    gr.HTML('<h1 align="center">基于ChatGPT封装接口的聊天机器人</h1>')
    chatbot = gr.Chatbot(elem_id="chatbot")
    messages = gr.State(
        [{'role': 'system', 'content': '你的名字叫小之，是一个就职于之江实验室的智能机器人，属于智能机器人中心。'}])
    log = gr.State([])

    txt = gr.Textbox(show_label=False, placeholder="输入内容……").style(container=False)

    txt.submit(add_text, [log, messages, txt], [log, messages, chatbot])
    txt.submit(lambda: "", None, txt)
#     btn.upload(add_image, [state, btn], [state, chatbot])
demo.queue(100).launch(server_name='0.0.0.0', share=False)
