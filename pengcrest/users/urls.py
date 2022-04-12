from django.urls import path

from pengcrest.users.views import (
    check_username,
    user_detail_view,
    user_redirect_view,
    user_update_view,

    user_dashboard,
    kycverify,

    deposit,
    topup,

    withdraw,
    withdraw_bonus,
    withdraw_roi,

    get_referrals,
    get_transactions,
)

app_name = "users"
urlpatterns = [
    path("~redirect/", view=user_redirect_view, name="redirect"),
    path("~update/", view=user_update_view, name="update"),

    path("<str:username>/", view=user_detail_view, name="detail"),

    path("<str:username>/~deposit/", view=deposit, name="deposit"),
    path("<str:username>/~get-referrals/", view=get_referrals, name="refs"),
    path("<str:username>/~get-transactions/", view=get_transactions, name="trans"),
    path("<str:username>/~topup/", view=topup, name="topup"),

    path("<str:username>/~withdraw/", view=withdraw, name="withdraw"),
    path("<str:username>/~withdraw-bonus/", view=withdraw_bonus, name="withdraw_bonus"),
    path("<str:username>/~withdraw-roi/", view=withdraw_roi, name="withdraw_roi"),

    path("<str:username>/dashboard/", view=user_dashboard, name="dashboard"),
    path("<str:username>/kycverify/", view=kycverify, name="kyc"),

]
