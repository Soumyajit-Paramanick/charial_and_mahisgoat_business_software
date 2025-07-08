from django import forms
from .models import CharialBillPartyName, CharialBill, CharialDailyExpensesOtherExpensesName, CharialDailyExpensesWagesName, CharialDailyExpenses, CharialTradeSeller, CharialTrade
from .models import CharialBalanceSheet
from .models import (
    MahisgoatBillPartyName, MahisgoatBill,
    MahisgoatDailyExpensesWagesName, MahisgoatDailyExpensesOtherExpensesName, MahisgoatDailyExpenses,
    MahisgoatTradeSeller, MahisgoatTrade,
    MahisgoatBalanceSheet
)


class PartyNameForm(forms.ModelForm):
    class Meta:
        model = CharialBillPartyName
        fields = ['partyName']
        labels = {'partyName': 'Party Name'}
        widgets = {
            'partyName': forms.TextInput(attrs={
                'placeholder': 'Enter unique party name',
                'class': 'form-control'
            })
        }

class CharialBillForm(forms.ModelForm):
    class Meta:
        model = CharialBill
        fields = ['partyName', 'totalBill', 'commissionPercentage', 'others']
        labels = {
            'partyName': 'Select Party',
            'totalBill': 'Total Bill Amount',
            'commissionPercentage': 'Commission Percentage',
            'others': 'Other Deductions'
        }
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'partyName': forms.Select(attrs={'class': 'form-control'}),
            'totalBill': forms.NumberInput(attrs={'class': 'form-control'}),
            'commissionPercentage': forms.NumberInput(attrs={'class': 'form-control'}),
            'others': forms.NumberInput(attrs={'class': 'form-control'})
        }

class WagesNameForm(forms.ModelForm):
    class Meta:
        model = CharialDailyExpensesWagesName
        fields = ['wagesName']
        labels = {'wagesName': 'Wages Name'}
        widgets = {
            'wagesName': forms.TextInput(attrs={
                'placeholder': 'Enter unique wage name',
                'class': 'form-control'
            })
        }

class OtherExpensesNameForm(forms.ModelForm):
    class Meta:
        model = CharialDailyExpensesOtherExpensesName
        fields = ['otherExpensesName']
        labels = {'otherExpensesName': 'Other Expense Name'}
        widgets = {
            'otherExpensesName': forms.TextInput(attrs={
                'placeholder': 'Enter unique expense name',
                'class': 'form-control'
            })
        }

class DailyExpenseForm(forms.ModelForm):
    class Meta:
        model = CharialDailyExpenses
        fields = ['expenseType', 'wagesName', 'otherExpensesName', 'amount']
        widgets = {
            'expenseType': forms.Select(attrs={
                'onchange': "toggleExpenseType()",
                'class': 'form-control'
            }),
            'wagesName': forms.Select(attrs={'class': 'form-control wages-field'}),
            'otherExpensesName': forms.Select(attrs={'class': 'form-control other-field'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['wagesName'].queryset = CharialDailyExpensesWagesName.objects.all()
        self.fields['otherExpensesName'].queryset = CharialDailyExpensesOtherExpensesName.objects.all()
        self.fields['wagesName'].required = False
        self.fields['otherExpensesName'].required = False

class TradeSellerForm(forms.ModelForm):
    class Meta:
        model = CharialTradeSeller
        fields = ['name', 'pendingAmount']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'pendingAmount': forms.NumberInput(attrs={'class': 'form-control'})
        }

class TradeForm(forms.ModelForm):
    class Meta:
        model = CharialTrade
        fields = ['seller', 'todayPurchase', 'amPayment', 'pmPayment']
        widgets = {
            'seller': forms.Select(attrs={'class': 'form-control'}),
            'todayPurchase': forms.NumberInput(attrs={'class': 'form-control'}),
            'amPayment': forms.NumberInput(attrs={'class': 'form-control'}),
            'pmPayment': forms.NumberInput(attrs={'class': 'form-control'})
        }
# # Add to accounts/forms.py
# class BalanceSheetForm(forms.ModelForm):
#     class Meta:
#         model = CharialBalanceSheet
#         fields = ['date', 'bill', 'commission', 'extra', 'britty', 'expenses']
#         widgets = {
#             'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
#             'bill': forms.NumberInput(attrs={'class': 'form-control'}),
#             'commission': forms.NumberInput(attrs={'class': 'form-control'}),
#             'extra': forms.NumberInput(attrs={'class': 'form-control'}),
#             'britty': forms.NumberInput(attrs={'class': 'form-control'}),
#             'expenses': forms.NumberInput(attrs={'class': 'form-control'}),
#         }






























class BalanceSheetForm(forms.ModelForm):
    class Meta:
        model = CharialBalanceSheet
        fields = ['date', 'bill', 'commission', 'extra', 'britty', 'expenses']
        widgets = {
            'date': forms.HiddenInput(),
            'bill': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'commission': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'extra': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'britty': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'expenses': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }






























# from django import forms
# from .models import CharialBillPartyName, CharialBill, CharialDailyExpensesOtherExpensesName, CharialDailyExpensesWagesName,CharialDailyExpenses

# class PartyNameForm(forms.ModelForm):
#     class Meta:
#         model = CharialBillPartyName
#         fields = ['partyName']
#         labels = {'partyName': 'Party Name'}

# class CharialBillForm(forms.ModelForm):
#     class Meta:
#         model = CharialBill
#         fields = ['partyName', 'totalBill', 'commissionPercentage', 'others']
#         labels = {
#             'partyName': 'Select Party',
#             'totalBill': 'Total Bill Amount',
#             'commissionPercentage': 'Commission Percentage',
#             'others': 'Other Deductions'
#         }
#         widgets = {
#             'date': forms.DateInput(attrs={'type': 'date'})
#         }
# class WagesNameForm(forms.ModelForm):
#     class Meta:
#         model = CharialDailyExpensesWagesName
#         fields = ['wagesName']
#         labels = {'wagesName': 'Wages Name'}

# class OtherExpensesNameForm(forms.ModelForm):
#     class Meta:
#         model = CharialDailyExpensesOtherExpensesName
#         fields = ['otherExpensesName']
#         labels = {'otherExpensesName': 'Other Expense Name'}

# # class DailyExpenseForm(forms.ModelForm):
# #     class Meta:
# #         model = CharialDailyExpenses
# #         fields = ['expenseType', 'wagesName', 'otherExpensesName', 'amount']
# #         widgets = {
# #             'expenseType': forms.Select(attrs={'onchange': "toggleExpenseType()"}),
# #             'wagesName': forms.Select(attrs={'class': 'wages-field'}),
# #             'otherExpensesName': forms.Select(attrs={'class': 'other-field'}),
# #         }

# #     def __init__(self, *args, **kwargs):
# #         super().__init__(*args, **kwargs)
# #         self.fields['wagesName'].queryset = CharialDailyExpensesWagesName.objects.all()
# #         self.fields['otherExpensesName'].queryset = CharialDailyExpensesOtherExpensesName.objects.all()



# # class DailyExpenseForm(forms.ModelForm):
# #     class Meta:
# #         model = CharialDailyExpenses
# #         fields = ['expenseType', 'wagesName', 'otherExpensesName', 'amount']
# #         widgets = {
# #             'expenseType': forms.Select(attrs={
# #                 'onchange': "toggleExpenseType()",
# #                 'class': 'form-control'
# #             }),
# #             'wagesName': forms.Select(attrs={
# #                 'class': 'form-control wages-field',
# #                 'style': 'display: none;'
# #             }),
# #             'otherExpensesName': forms.Select(attrs={
# #                 'class': 'form-control other-field',
# #                 'style': 'display: none;'
# #             }),
# #             'amount': forms.NumberInput(attrs={'class': 'form-control'})
# #         }

# #     def __init__(self, *args, **kwargs):
# #         super().__init__(*args, **kwargs)
# #         self.fields['wagesName'].queryset = CharialDailyExpensesWagesName.objects.all()
# #         self.fields['otherExpensesName'].queryset = CharialDailyExpensesOtherExpensesName.objects.all()
# #         self.fields['wagesName'].required = False
# #         self.fields['otherExpensesName'].required = False




# class DailyExpenseForm(forms.ModelForm):
#     class Meta:
#         model = CharialDailyExpenses
#         fields = ['expenseType', 'wagesName', 'otherExpensesName', 'amount']
#         widgets = {
#             'expenseType': forms.Select(attrs={
#                 'onchange': "toggleExpenseType()",
#                 'class': 'form-control'
#             }),
#             'wagesName': forms.Select(attrs={'class': 'form-control wages-field'}),
#             'otherExpensesName': forms.Select(attrs={'class': 'form-control other-field'}),
#             'amount': forms.NumberInput(attrs={'class': 'form-control'})
#         }

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['wagesName'].queryset = CharialDailyExpensesWagesName.objects.all()
#         self.fields['otherExpensesName'].queryset = CharialDailyExpensesOtherExpensesName.objects.all()
#         self.fields['wagesName'].required = False
#         self.fields['otherExpensesName'].required = False





















































# Add these after the Charial forms
class MahisgoatPartyNameForm(forms.ModelForm):
    class Meta:
        model = MahisgoatBillPartyName
        fields = ['partyName']
        labels = {'partyName': 'Party Name'}
        widgets = {
            'partyName': forms.TextInput(attrs={
                'placeholder': 'Enter unique party name',
                'class': 'form-control'
            })
        }

class MahisgoatBillForm(forms.ModelForm):
    class Meta:
        model = MahisgoatBill
        fields = ['partyName', 'totalBill', 'commissionPercentage', 'others']
        widgets = {
            'partyName': forms.Select(attrs={'class': 'form-control'}),
            'totalBill': forms.NumberInput(attrs={'class': 'form-control'}),
            'commissionPercentage': forms.NumberInput(attrs={'class': 'form-control'}),
            'others': forms.NumberInput(attrs={'class': 'form-control'})
        }

class MahisgoatWagesNameForm(forms.ModelForm):
    class Meta:
        model = MahisgoatDailyExpensesWagesName
        fields = ['wagesName']
        labels = {'wagesName': 'Wages Name'}
        widgets = {
            'wagesName': forms.TextInput(attrs={
                'placeholder': 'Enter unique wage name',
                'class': 'form-control'
            })
        }

class MahisgoatOtherExpensesNameForm(forms.ModelForm):
    class Meta:
        model = MahisgoatDailyExpensesOtherExpensesName
        fields = ['otherExpensesName']
        labels = {'otherExpensesName': 'Other Expense Name'}
        widgets = {
            'otherExpensesName': forms.TextInput(attrs={
                'placeholder': 'Enter unique expense name',
                'class': 'form-control'
            })
        }

class MahisgoatDailyExpenseForm(forms.ModelForm):
    class Meta:
        model = MahisgoatDailyExpenses
        fields = ['expenseType', 'wagesName', 'otherExpensesName', 'amount']
        widgets = {
            'expenseType': forms.Select(attrs={
                'onchange': "toggleExpenseType()",
                'class': 'form-control'
            }),
            'wagesName': forms.Select(attrs={'class': 'form-control wages-field'}),
            'otherExpensesName': forms.Select(attrs={'class': 'form-control other-field'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['wagesName'].queryset = MahisgoatDailyExpensesWagesName.objects.all()
        self.fields['otherExpensesName'].queryset = MahisgoatDailyExpensesOtherExpensesName.objects.all()
        self.fields['wagesName'].required = False
        self.fields['otherExpensesName'].required = False

class MahisgoatTradeSellerForm(forms.ModelForm):
    class Meta:
        model = MahisgoatTradeSeller
        fields = ['name', 'pendingAmount']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'pendingAmount': forms.NumberInput(attrs={'class': 'form-control'})
        }

class MahisgoatTradeForm(forms.ModelForm):
    class Meta:
        model = MahisgoatTrade
        fields = ['seller', 'todayPurchase', 'amPayment', 'pmPayment']
        widgets = {
            'seller': forms.Select(attrs={'class': 'form-control'}),
            'todayPurchase': forms.NumberInput(attrs={'class': 'form-control'}),
            'amPayment': forms.NumberInput(attrs={'class': 'form-control'}),
            'pmPayment': forms.NumberInput(attrs={'class': 'form-control'})
        }

class MahisgoatBalanceSheetForm(forms.ModelForm):
    class Meta:
        model = MahisgoatBalanceSheet
        fields = ['date', 'bill', 'commission', 'extra', 'britty', 'expenses']
        widgets = {
            'date': forms.HiddenInput(),
            'bill': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'commission': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'extra': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'britty': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'expenses': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }