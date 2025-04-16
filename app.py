from flask import Flask, render_template, request, jsonify
from collections import deque

app = Flask(__name__)


def fifo_page_replacement(pages, frames):
    memory = deque(maxlen=frames)
    page_faults = 0
    history = []

    for page in pages:
        if page not in memory:
            memory.append(page)
            page_faults += 1
        history.append(list(memory))

    return history, page_faults


def lru_page_replacement(pages, frames):
    memory = []
    page_faults = 0
    history = []

    for page in pages:
        if page not in memory:
            if len(memory) == frames:
                memory.pop(0)  # Remove least recently used
            memory.append(page)
            page_faults += 1
        else:
            memory.remove(page)  # Move page to most recently used
            memory.append(page)

        history.append(list(memory))

    return history, page_faults


def mru_page_replacement(pages, frames):
    memory = []
    page_faults = 0
    history = []

    for page in pages:
        if page not in memory:
            if len(memory) == frames:
                memory.pop()  # Remove most recently used
            memory.append(page)
            page_faults += 1
        else:
            memory.remove(page)  # Move page to most recently used
            memory.append(page)

        history.append(list(memory))

    return history, page_faults


def optimal_page_replacement(pages, frames):
    memory = []
    page_faults = 0
    history = []

    for i, page in enumerate(pages):
        if page not in memory:
            if len(memory) < frames:
                memory.append(page)
            else:
                # Predict which page will be used farthest in the future
                future_use = {p: (pages[i + 1:].index(p) if p in pages[i + 1:] else float('inf')) for p in memory}
                page_to_remove = max(future_use, key=future_use.get)
                memory.remove(page_to_remove)
                memory.append(page)

            page_faults += 1

        history.append(list(memory))

    return history, page_faults


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/simulate', methods=['POST'])
def simulate():
    try:
        data = request.json
        pages = list(map(int, data.get('pages', '').split(',')))
        frames = int(data.get('frames', 0))
        algo = data.get('algorithm', 'FIFO').upper()

        if frames <= 0:
            return jsonify({'error': 'Number of frames must be greater than zero'}), 400
        if not pages:
            return jsonify({'error': 'Pages input cannot be empty'}), 400

        algorithms = {
            'FIFO': fifo_page_replacement,
            'LRU': lru_page_replacement,
            'MRU': mru_page_replacement,
            'OPTIMAL': optimal_page_replacement
        }

        if algo not in algorithms:
            return jsonify({'error': 'Invalid algorithm selected'}), 400

        history, faults = algorithms[algo](pages, frames)

        return jsonify({'history': history, 'faults': faults})

    except ValueError:
        return jsonify({'error': 'Invalid input format. Pages should be comma-separated numbers.'}), 400


if __name__ == '__main__':
    app.run(debug=True)
