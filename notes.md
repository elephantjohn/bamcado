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


###### 前端逻辑
 ```javascript
async function h(b) {
  // 检查用户输入的消息内容是否为空，如果是空白字符串，则直接返回，不进行后续操作
  if (!b.trim()) return;

  // 创建一个新的消息对象 d，包含以下属性：
  const d = {
    id: "",                  // 消息的唯一标识符，初始为空字符串，等待后续从后端获取
    conversation_id: s,      // 当前会话的 ID，变量 s 在组件中保存了当前会话的标识
    chat_type: "",           // 聊天类型，初始为空字符串，可以根据实际需求填写
    query: b,                // 用户输入的消息内容，即函数参数 b
    response: "",            // 系统的回复内容，初始为空字符串，等待后续接收系统回复
    create_time: ""          // 消息创建时间，初始为空字符串，后续可从后端获取
  };

  // 将新创建的消息对象添加到消息列表 i.value 中
  i.value.push(d);

  // 调用 u() 函数，通常用于界面更新，例如将聊天窗口滚动到底部，确保最新消息可见
  u();

  // 创建一个请求对象 g，包含以下属性：
  const g = {
    query: b,                // 用户输入的消息内容
    conversation_id: s,      // 当前会话的 ID，与之前相同
    conversation_name: n,    // 当前会话的名称，变量 n 保存了会话名称
    history: []              // 历史记录，初始为空数组，可根据需要添加之前的对话内容
  };

  // 调用 e.chat 函数，将请求对象 g 发送到后端，并设置消息接收的回调函数
  e.chat(g, {
    onmessage: async m => {
      // 从后端接收到的数据 m.data 中解析出消息内容
      const y = JSON.parse(m.data);

      // 遍历消息列表 i.value，找到与当前消息对应的消息对象 v
      i.value.map(async v => {
        // 如果消息的 id 与后端返回的消息 id 匹配，或者初始的 id 为空字符串
        if (y && (v.id === y.message_id || v.id === "") && y.text) {
          // 将后端返回的文本 y.text 累加到消息对象 v 的 response 属性中，形成完整的回复
          v.response += y.text;
          // 更新消息对象的 id，为后端返回的唯一消息标识符
          v.id = y.message_id;
        }
      });

      // 再次调用 u() 函数，更新界面显示，确保最新的回复内容可见
      u();
    }
  });
}
```
