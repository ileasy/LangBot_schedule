from pkg.plugin.context import register, handler, llm_func, BasePlugin, APIHost, EventContext
from pkg.plugin.events import *  # 导入事件类
from datetime import datetime 

# 注册插件
@register(name="Hello", description="hello world", version="0.1", author="RockChinQ")
class MyPlugin(BasePlugin):

    # 插件加载时触发
    def __init__(self, host: APIHost):
        pass

    # 异步初始化
    async def initialize(self):
        pass

    # 当收到个人消息时触发
    @handler(PersonNormalMessageReceived)
    async def person_normal_message_received(self, ctx: EventContext):
        current_time = datetime.now().strftime("%H:%M")
        msg = ctx.event.text_message  # 这里的 event 即为 PersonNormalMessageReceived 的对象
        #if msg == "hello":  # 如果消息为hello
        if current_time == "07:35":
            self.ap.logger.debug("定时通知触发")
            ctx.add_return("reply", [f"早上好！现在是北京时间 {current_time}，该起床啦！🌞"])
            # 获取当前时间并格式化为字符串
            #current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # 输出调试信息
            self.ap.logger.debug("hello, {}".format(ctx.event.sender_id))

            # 回复消息 "hello, <发送者id>!"
            #ctx.add_return("reply", [f"hello, {ctx.event.sender_id}! The current time is {current_time}."])

            # 阻止该事件默认行为（向接口获取回复）
            ctx.prevent_default()

    # 当收到群消息时触发
    @handler(GroupNormalMessageReceived)
    async def group_normal_message_received(self, ctx: EventContext):
        msg = ctx.event.text_message  # 这里的 event 即为 GroupNormalMessageReceived 的对象
        if msg == "hello":  # 如果消息为hello
            
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            # 输出调试信息
            ctx.add_return("reply", [f"hello, {ctx.event.sender_id}! The current time is {current_time}."])

            # 回复消息 "hello, everyone!"
            ctx.add_return("reply", ["hello, everyone!"])

            # 阻止该事件默认行为（向接口获取回复）
            ctx.prevent_default()

    # 插件卸载时触发
    def __del__(self):
        pass
