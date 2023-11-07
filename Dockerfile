FROM python:3.11.6
WORKDIR /app
ENV input_file = ""
ENV output_file = ""
COPY . /app
RUN pip install -r requirements.txt

CMD "python" "whatsapp_chat_logger.py" "$input_file" "${output_file}"  