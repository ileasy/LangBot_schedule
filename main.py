from pkg.plugin.context import register, handler, BasePlugin, APIHost, EventContext
from pkg.plugin.events import *  # 导入事件类
from datetime import datetime  # 导入datetime模块以获取当前时间


# 注册插件
@register(name="Hello", description="hello world", version="0.1", author="RockChinQ")
class MyPlugin(BasePlugin):

    # 插件加载时触发
    def __init__(self, host: APIHost):
        self.host = host  # 保存APIHost实例以便后续使用

    # 异步初始化
    async def initialize(self):
        pass

    # 当收到个人消息时触发
    @handler(PersonNormalMessageReceived)
    async def person_normal_message_received(self, ctx: EventContext):
        msg = ctx.event.text_message  # 获取消息内容
        if msg == "hello":  # 如果消息为 "hello"

            # 获取当前时间并格式化为字符串
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # 输出调试信息
            self.host.logger.debug(f"User {ctx.event.sender_id} said hello at {current_time}")

            # 回复消息，包含当前时间
            reply_message = f"Hello, {ctx.event.sender_id}! The current time is {current_time}."
            ctx.add_return("reply", [reply_message])

            # 阻止该事件默认行为（向接口获取回复）
            ctx.prevent_default()

    # 当收到群消息时触发
    @handler(GroupNormalMessageReceived)
    async def group_normal_message_received(self, ctx: EventContext):
        msg = ctx.event.text_message  # 获取消息内容
        if msg == "hello":  # 如果消息为 "hello"

            # 获取当前时间并格式化为字符串
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # 输出调试信息
            self.host.logger.debug(f"Group user {ctx.event.sender_id} said hello at {current_time}")

            # 回复消息，包含当前时间
            reply_message = f"Hello, everyone! The current time is {current_time}."
            ctx.add_return("reply", [reply_message])

            # 阻止该事件默认行为（向接口获取回复）
            ctx.prevent_default()

    # 插件卸载时触发
    def __del__(self):
        pass
