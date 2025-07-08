from django.contrib import admin
from .models import (
    CharialBillPartyName,
    CharialBill,
    CharialDailyExpensesWagesName,
    CharialDailyExpensesOtherExpensesName,
    CharialDailyExpenses,
    CharialTradeSeller,  # Add this
    CharialTrade,  # Add this
    CharialBalanceSheet
)

# Existing registrations
admin.site.register(CharialBillPartyName)
admin.site.register(CharialBill)
admin.site.register(CharialDailyExpensesWagesName)
admin.site.register(CharialDailyExpensesOtherExpensesName)
admin.site.register(CharialDailyExpenses)

# Add these new registrations
admin.site.register(CharialTradeSeller)
admin.site.register(CharialTrade)
admin.site.register(CharialBalanceSheet)










from .models import (
    MahisgoatBillPartyName, MahisgoatBill,
    MahisgoatDailyExpensesWagesName, MahisgoatDailyExpensesOtherExpensesName, MahisgoatDailyExpenses,
    MahisgoatTradeSeller, MahisgoatTrade,
    MahisgoatBalanceSheet
)

admin.site.register(MahisgoatBillPartyName)
admin.site.register(MahisgoatBill)
admin.site.register(MahisgoatDailyExpensesWagesName)
admin.site.register(MahisgoatDailyExpensesOtherExpensesName)
admin.site.register(MahisgoatDailyExpenses)
admin.site.register(MahisgoatTradeSeller)
admin.site.register(MahisgoatTrade)
admin.site.register(MahisgoatBalanceSheet)