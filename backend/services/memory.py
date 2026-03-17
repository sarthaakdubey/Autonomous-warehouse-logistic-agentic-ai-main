history = []

def add_memory(q, a):
    history.append((q, a))
    if len(history) > 5:
        history.pop(0)

def get_memory():
    text = ""
    for q, a in history:
        text += f"Previous Question: {q}\nPrevious Answer: {a}\n\n"
    return text