from pkg.plugin.context import register, handler, llm_func, BasePlugin, APIHost, EventContext
from pkg.plugin.events import *
from datetime import datetime, timedelta
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import pytz

# 配置项（TEST_MODE=True时会立即发送测试消息）
TARGET_USER = "wxid_kif00pjoz5gw22"
TARGET_GROUP = "26700423460@chatroom"
NOTIFY_TIME = "08:02"
TIME_ZONE = "Asia/Shanghai"
TEST_MODE = True  # 测试模式开关

@register(name="DailyNotifier", 
         description="优化版定时通知插件", 
         version="2.1",
         author="iLeasy")
class DailyNotifierPlugin(BasePlugin):

    def __init__(self, host: APIHost):
        self.scheduler = AsyncIOScheduler(timezone=TIME_ZONE)
        self.host = host  # 关键修复：保存host引用

    async def initialize(self):
        try:
            if TEST_MODE:
                # 添加60秒后执行的测试任务
                self.scheduler.add_job(
                    self.send_daily_notice,
                    'date',
                    run_date=datetime.now(pytz.timezone(TIME_ZONE)) + timedelta(seconds=60)
                )
            else:
                self.scheduler.add_job(
                    self.send_daily_notice,
                    'cron',
                    hour=int(NOTIFY_TIME.split(':')[0]),
                    minute=int(NOTIFY_TIME.split(':')[1]),
                    misfire_grace_time=300
                )

            self.scheduler.start()
            self.ap.logger.info("调度器已启动，下次触发时间: {}".format(
                self.scheduler.get_jobs()[0].next_run_time)
            )
        except Exception as e:
            self.ap.logger.error("调度器初始化失败: {}".format(str(e)), exc_info=True)

    async def send_daily_notice(self):
        try:
            self.ap.logger.debug("== 开始执行通知任务 ==")
            
            # 验证基础发送功能
            test_res = await self.host.send_active_message(
                target_id=TARGET_USER,  # 改为 target_id
                message="🏓 服务活跃性检查（收到本条说明定时器正常）"
            )
            self.ap.logger.info("基础消息发送状态: {}".format(test_res))

            # 正式消息
            current_time = datetime.now(pytz.timezone(TIME_ZONE)).strftime("%Y-%m-%d %H:%M:%S")
            success_count = 0
            
            # 发送个人消息
            person_res = await self.host.send_active_message(
                target_id=TARGET_USER,  # 改为 target_id
                message=f"⏰ 每日提醒（{current_time}）"
            )
            if person_res['status'] == 'success':
                success_count += 1
            
            # 发送群消息
            group_res = await self.host.send_group_active_message(
                room_id=TARGET_GROUP,
                message=f"🗓 群通知（{current_time}）"
            )
            if group_res['status'] == 'success':
                success_count += 1
                
            self.ap.logger.info("通知完成，成功发送{}条".format(success_count))
            
        except Exception as e:
            self.ap.logger.error("!! 严重错误 !!", exc_info=True)

    def __del__(self):
        if self.scheduler.running:
            self.scheduler.shutdown(wait=False)
