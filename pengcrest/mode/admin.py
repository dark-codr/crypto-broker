from django.contrib import admin
from .models import Mode, Currency, FAQ, Privacy, Agreement, Return, TradeOpen
# Register your models here.
admin.site.register(TradeOpen)
admin.site.register(Mode)
admin.site.register(Currency)
admin.site.register(FAQ)
admin.site.register(Privacy)
admin.site.register(Agreement)
admin.site.register(Return)

