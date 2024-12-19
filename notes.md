### 1. test_langchainRag
pip install --upgrade langchain langchain-community langchainhub httpx httpx-sse PyJWT langchain-chroma bs4 python-dotenv

### 2. Chat-GPT WebUI
- 开始启动控制器
>processes["controller"] = process ；             func: run_controller 
> 创建了controller的app实体，确定了dispatch_method为shortest_queue的负载均衡策略，处理来自客户端的请求，分配给后端的服务器实例；app的startevent事件启动；uvicorn.run(app, host, port)

- 开始启动openaiapi
> processes["openai_api"] = process ;              func: run_openai_api, 
> 创建了openai_api的app实体，创建时传入了controller的地址，在app创建时，向app中添加了中间件处理请求和响应；                    app的startevent事件启动；uvicorn.run(app, host, port)

- 开始启动模型引擎
>processes["model_worker"][model_name] = process  func: run_model_worker
>创建了model_worker的app实体，创建时，按照在线模型或本地模型，分别用 继承了fastchat源码里的类例如集成ApiModelWorker的ChatGLMWorker 或者 fastchat提供的ModelWorker
> ，传入模型名字，controller地址，模型地址（离线），最大gpu数量（离线），最大gpu显存（离线）等；

- 启动在线api模型
processes["online_api"][model_name] = process    func: run_model_worker
>  同上

- 启动api
>processes["api"] = process                       func: run_api_server
> 创建app实体，在app创建时，向app中添加了中间件处理请求和响应；挂载 Vue 构建的前端静态文件夹； 挂载了路由，即不同路由触发不同函数，例如/api/chat
> 触发chat函数，/api/conversations触发create_conversation函数，       

--------
--------
###### 运行核心过程：
在/api/chat挂载的chat函数中，用新的messageid和conversationid，userid写入了新的数据，创建了conversation的回调，构建memory对象，在用langchain
流程化，即chain = LLMChain(prompt=chat_prompt, llm=model, memory=memory)，在通过asyncio创建任务creat_task,在task中，用一个包装器，wrap_done
，即先等待fn函数（chain.acall({"input": query}）执行完毕，再执行event的set方法，这一过程在chatiterator中，作为EventSourceResponse的参数，能够把chatinterator
返回的值返回给前端，即/api/chat处，由前端处理；



