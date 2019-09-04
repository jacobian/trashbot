FROM python:3.7

RUN mkdir -p ${HOME}/.config/pypoetry/
RUN touch ${HOME}/.config/pypoetry/config.toml
RUN echo "[virtualenvs]\ncreate = false" > ${HOME}/.config/pypoetry/config.toml

COPY pyproject.toml .
RUN pip install -U pip && pip install poetry --pre
RUN poetry install --no-dev

COPY app.py .
CMD flask run --host 0.0.0.0 --port ${PORT:-5000}

