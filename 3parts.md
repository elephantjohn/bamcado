# start_method_1
### terminal1
python -m fastchat.serve.controller

### terminal2
python -m fastchat.serve.model_worker --model-path /root/work/RAG/resources/chatglm3-6b --num-gpus 1

### terminal3
python -m fastchat.serve.openai_api_server

### curl POST to test
curl -X POST http://localhost:8000/v1/chat/completions \
-H "Content-Type: application/json" \
-d '{
    "model": "chatglm3-6b",
    "messages": [{"role": "user", "content": "Hello! What is your name?"}]
}'

# start_method_2
```python
from multiprocessing import Process

def start_services_in_processes():
    # 创建进程
    controller_process = Process(target=start_controller)
    worker_process = Process(target=start_model_worker)
    api_server_process = Process(target=start_openai_api_server)

    # 启动进程
    controller_process.start()
    worker_process.start()
    api_server_process.start()

    # 等待所有进程完成
    controller_process.join()
    worker_process.join()
    api_server_process.join()
#但无法通信
```

# start_method_3
startup.py
