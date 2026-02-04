import tkinter as tk
from tkinter import filedialog, messagebox
import os
import json
from kafka import KafkaProducer
from common import config

from validator.validator import validate
from producer.producer import load_json_file, make_message

def run_validator(path):
    try:
        validate(path)
        messagebox.showinfo("Проверка JSON", "JSON корректный!")
        return True
    except Exception as e:
        messagebox.showerror("Ошибка", str(e))
        return False

def send_json_via_producer(path):
    try:
        table, schema, rows = load_json_file(path)
        msg = make_message(table, schema, rows)

        producer = KafkaProducer(bootstrap_servers=config.KAFKA_LOCAL)
        future = producer.send(table, msg)
        future.get(timeout=10)  # ждем подтверждения отправки
        producer.flush() # отправляет все сообщения с буфера KafkaProducer на Kafka
        producer.close() # закрывает соединение с кафкой

        messagebox.showinfo("Kafka", f"JSON успешно отправлен в топик: {table}")

    except Exception as e:
        messagebox.showerror("Ошибка Kafka", str(e))

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("ETL JSON GUI")
        self.root.geometry("450x250")

        self.json_path = None

        tk.Button(root, text="Выбрать JSON файл", width=40, command=self.select_json).pack(pady=10)
        tk.Button(root, text="Проверить JSON (validator.py)", width=40, command=self.check_json).pack(pady=10)
        tk.Button(root, text="Отправить в Kafka (producer.py)", width=40, command=self.produce_kafka).pack(pady=10)

        self.label = tk.Label(root, text="Файл не выбран")
        self.label.pack(pady=10)

    def select_json(self):
        path = filedialog.askopenfilename(
            title="выберите JSON файл",
            filetypes=[("JSON files", "*.json")]
        )
        if path:
            self.json_path = path
            self.label.config(text=f"выбран файл:\n{os.path.basename(path)}")

    def check_json(self):
        if not self.json_path:
            messagebox.showwarning("нет файла", " выберите JSON")
            return
        run_validator(self.json_path)

    def produce_kafka(self):
        if not self.json_path:
            messagebox.showwarning("нет файла", " выберите JSON")
            return

        # сначала проверяем JSON
        if run_validator(self.json_path):
            send_json_via_producer(self.json_path)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()

# docker exec -it etl_json_project-kafka-1 \
#    kafka-topics --bootstrap-server localhost:9092 \
#    --create --topic json_topic --partitions 1 --replication-factor 1

#PYTHONPATH=. python3 -m loader.loader \
#   --bootstrap localhost:9092 \
#   --group etl_loader_group_13 \
#   --topics users \
#   --pg postgresql://etl_user:etl_pass@localhost:5432/etl_db

# docker exec -it etl_json_project-postgres-1 psql -U etl_user -d etl_db