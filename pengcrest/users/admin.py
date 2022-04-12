from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from pengcrest.users.forms import UserAdminChangeForm, UserAdminCreationForm

User = get_user_model()

from .models import (
    Wallet,
    QuickFund,
    KYCVerify,
    Withdraw,
    Deposit,
    TransactionHistory
)

admin.site.register(Wallet)
admin.site.register(QuickFund)
admin.site.register(KYCVerify)
admin.site.register(Withdraw)
admin.site.register(Deposit)
admin.site.register(TransactionHistory)

@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):

    form = UserAdminChangeForm
    add_form = UserAdminCreationForm
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("name", "email", "phone")}),
        (_("Private info"), {"fields": ("unique_id", "recommended_by")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "has_invested", "has_toped", "can_topup", "can_withdraw_roi",
                    "can_withdraw",
                    "newsletter",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    list_display = ["username", "name", "can_withdraw", "has_invested", "has_toped", "can_topup", "can_withdraw_roi", "newsletter", "is_active", "is_superuser"]
    search_fields = ["name", "username", "email"]
