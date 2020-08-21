from django.db import models
# Create your models here.


class WaitList(models.Model):

    objects = models.Manager()                  # for reminder purpose

    id = models.AutoField('ID', primary_key=True)
    order_id = models.IntegerField('队列ID', unique=True, auto_created=True)
    account_email = models.EmailField('账户邮箱', )
    sender_address = models.CharField('请求者地址', max_length=64)
    exec_app = models.CharField('执行主流程', max_length=128)
    mission_name = models.CharField('任务名称', max_length=64)
    mission_data = models.TextField('任务详情', )
    register_time = models.DateTimeField('注册时间', auto_now_add=True)
    start_time = models.CharField('开始时间', blank=True, default='', max_length=64)
    used_time = models.CharField('用时', max_length=64, blank=True, default='')

    def __str__(self):
        tip = """[Order: %s, Mission: %s, Account: %s] """ % (str(self.order_id), self.mission_name, self.account_email)
        return tip

    def get_data_dict(self):
        data_dict = {
            'id': self.id,
            'order_id': self.order_id,
            'account_email': self.account_email,
            'sender_address': self.sender_address,
            'mission_name': self.mission_name,
            'mission_data': self.mission_data,
            'register_time': self.register_time,
        }
        return data_dict

    class Meta:
        ordering = ["order_id"]
        verbose_name = "等待队列"
        verbose_name_plural = "等待队列"


class RunningList(models.Model):

    objects = models.Manager()

    id = models.AutoField('ID', primary_key=True)
    order_id = models.CharField('队列ID', blank=True, default='', max_length=16)
    account_email = models.EmailField('账户邮箱', )
    sender_address = models.CharField('请求者地址', max_length=64)
    exec_app = models.CharField('执行主流程', max_length=128)
    mission_name = models.CharField('任务名称', max_length=64)
    mission_data = models.TextField('任务详情', )
    register_time = models.DateTimeField('注册时间')
    start_time = models.DateTimeField('开始时间', auto_now_add=True)
    used_time = models.CharField('用时', max_length=64, blank=True, default='')

    def __str__(self):
        tip = """[ID: %s, Mission: %s, Account: %s] """ % (str(self.id), self.mission_name, self.account_email)
        return tip

    class Meta:
        ordering = ["start_time"]
        verbose_name = "正在计算队列"
        verbose_name_plural = "正在计算队列"


class HistoryList(models.Model):

    objects = models.Manager()

    id = models.AutoField('ID', primary_key=True)
    order_id = models.CharField('队列ID', blank=True, default='', max_length=16)
    account_email = models.EmailField('账户邮箱', )
    sender_address = models.CharField('请求者地址', max_length=64)
    exec_app = models.CharField('执行主流程', max_length=128)
    mission_name = models.CharField('任务名称', max_length=64)
    mission_data = models.TextField('任务详情', )
    register_time = models.DateTimeField('注册时间')
    start_time = models.DateTimeField('开始时间')
    used_time = models.CharField('用时', max_length=64)

    def __str__(self):
        tip = """[ID: %s, Mission: %s, Account: %s] """ % (str(self.id), self.mission_name, self.account_email)
        return tip

    class Meta:
        ordering = ["id"]
        verbose_name = "历史记录队列"
        verbose_name_plural = "历史记录队列"
