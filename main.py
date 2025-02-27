from pkg.plugin.context import register, handler, llm_func, BasePlugin, APIHost, EventContext
from pkg.plugin.events import *
from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import pytz

# 配置项（需要根据实际情况修改）
TARGET_USER = "kif00pjoz5gw22"    # 要通知的个人账号
TARGET_GROUP = "52326925588@chatroom"       # 要通知的群聊
NOTIFY_TIME = "07:46"             # 每天通知时间（24小时制）
TIME_ZONE = "Asia/Shanghai"       # 时区

# 注册插件
@register(name="DailyNotifier", 
         description="每日定时通知插件", 
         version="1.1",
         author="iLeasy")
class DailyNotifierPlugin(BasePlugin):

    def __init__(self, host: APIHost):
        # 初始化调度器
        self.scheduler = AsyncIOScheduler(timezone=TIME_ZONE)
        
    async def initialize(self):
        """异步初始化"""
        try:
            # 添加每日定时任务
            self.scheduler.add_job(
                self.send_daily_notice,
                'cron',
                hour=int(NOTIFY_TIME.split(':')[0]),
                minute=int(NOTIFY_TIME.split(':')[1]),
                misfire_grace_time=60*5,  # 允许5分钟内的延迟触发
                max_instances=1
            )
            
            self.scheduler.start()
            self.ap.logger.info(f"已启动每日{NOTIFY_TIME}定时通知服务")
        except Exception as e:
            self.ap.logger.error(f"定时任务启动失败: {str(e)}")

    async def send_daily_notice(self):
        """执行通知操作"""
        try:
            current_time = datetime.now(pytz.timezone(TIME_ZONE)).strftime("%Y-%m-%d %H:%M:%S")
            message = f"⏰ 每日提醒（{current_time}）\n该起床工作啦！💼\n今日也要元气满满哦！✨"
            
            # 发送个人消息
            await self.host.send_person_message(
                user_id=TARGET_USER,
                message=message
            )
            
            # 发送群消息
            await self.host.send_group_message(
                room_id=TARGET_GROUP,
                message=message
            )
            
            self.ap.logger.info(f"已发送每日通知到用户[{TARGET_USER}]和群组[{TARGET_GROUP}]")
            
        except Exception as e:
            self.ap.logger.error(f"通知发送失败: {str(e)}")
            # 可以添加重试逻辑...

    def __del__(self):
        """插件卸载时清理"""
        if self.scheduler.running:
            self.scheduler.shutdown()
            self.ap.logger.info("定时通知服务已关闭")
