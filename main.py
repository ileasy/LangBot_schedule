from pkg.plugin.context import register, handler, llm_func, BasePlugin, APIHost, EventContext
from pkg.plugin.events import *
import asyncio
import schedule
import time

# 注册插件
@register(name="DailyReminder", description="每日工作提醒插件", version="0.1", author="RockChinQ")
class MyPlugin(BasePlugin):

    # 插件加载时触发
    def __init__(self, host: APIHost):
        self.host = host
        # 启动定时任务
        asyncio.ensure_future(self.start_scheduler())

    # 异步初始化
    async def initialize(self):
        pass

    # 定时任务调度器
    async def start_scheduler(self):
        def job():
            # 输出调试信息
            self.host.logger.debug("发送每日工作提醒")

            # 发送提醒消息到所有群和个人（这里假设你有方法获取目标用户或群列表）
            for user_id in self.get_target_users():
                self.send_message_to_user(user_id, "请检查每日工作内容是否完成")
            for group_id in self.get_target_groups():
                self.send_message_to_group(group_id, "请检查每日工作内容是否完成")

        # 设置每天下午16点执行job函数
        schedule.every().day.at("14:35").do(job)

        while True:
            schedule.run_pending()
            await asyncio.sleep(1)

    # 获取目标用户列表（需要根据实际情况实现）
    def get_target_users(self):
        # 示例：返回用户ID列表
        return [kif00pjoz5gw22]

    # 获取目标群列表（需要根据实际情况实现）
    def get_target_groups(self):
        # 示例：返回群ID列表
        return [26700423460]

    # 向用户发送消息（需要根据实际情况实现）
    def send_message_to_user(self, user_id, message):
        # 示例：调用API发送消息给用户
        self.host.logger.info(f"向用户 {user_id} 发送消息: {message}")
        # 实际发送逻辑（假设有一个API可以发送消息）
        # self.host.api.send_message_to_user(user_id, message)

    # 向群发送消息（需要根据实际情况实现）
    def send_message_to_group(self, group_id, message):
        # 示例：调用API发送消息给群
        self.host.logger.info(f"向群 {group_id} 发送消息: {message}")
        # 实际发送逻辑（假设有一个API可以发送消息）
        # self.host.api.send_message_to_group(group_id, message)

    # 当收到个人消息时触发
    @handler(PersonNormalMessageReceived)
    async def person_normal_message_received(self, ctx: EventContext):
        msg = ctx.event.text_message
        if msg == "hello":
            # 输出调试信息
            self.host.logger.debug("hello, {}".format(ctx.event.sender_id))

            # 回复消息 "hello, <发送者id>!"
            ctx.add_return("reply", ["hello, {}!".format(ctx.event.sender_id)])

            # 阻止该事件默认行为（向接口获取回复）
            ctx.prevent_default()

    # 当收到群消息时触发
    @handler(GroupNormalMessageReceived)
    async def group_normal_message_received(self, ctx: EventContext):
        msg = ctx.event.text_message
        if msg == "hello":
            # 输出调试信息
            self.host.logger.debug("hello, {}".format(ctx.event.sender_id))

            # 回复消息 "hello, everyone!"
            ctx.add_return("reply", ["hello, everyone!"])

            # 阻止该事件默认行为（向接口获取回复）
            ctx.prevent_default()

    # 插件卸载时触发
    def __del__(self):
        pass
