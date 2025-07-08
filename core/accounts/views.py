from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import HttpResponse
from .models import CharialBillPartyName, CharialBill, CharialDailyExpenses, CharialTradeSeller, CharialTrade, CharialBalanceSheet
from .forms import PartyNameForm, CharialBillForm, WagesNameForm, DailyExpenseForm, OtherExpensesNameForm, TradeSellerForm, TradeForm, BalanceSheetForm
import pandas as pd
from django.db.models import Sum
import calendar
from datetime import datetime, date
from django.http import JsonResponse
# Mahisgoat models and forms
from .models import (
    MahisgoatBillPartyName, MahisgoatBill,
    MahisgoatDailyExpensesWagesName, MahisgoatDailyExpensesOtherExpensesName,
    MahisgoatDailyExpenses, MahisgoatTradeSeller, 
    MahisgoatTrade, MahisgoatBalanceSheet
)
from .forms import (
    MahisgoatPartyNameForm, MahisgoatBillForm,
    MahisgoatWagesNameForm, MahisgoatOtherExpensesNameForm,
    MahisgoatDailyExpenseForm, MahisgoatTradeSellerForm,
    MahisgoatTradeForm, MahisgoatBalanceSheetForm
)

# Context processor for current date (add this to settings.py later)
def get_current_date(request):
    return {'current_date': timezone.now().date()}

def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return redirect('login')

@login_required
def dashboard(request):
    context = {
        'current_date': timezone.now().date()
    }
    return render(request, 'dashboard.html', context)

# Charial Views
@login_required
def charial_main(request):
    context = {
        'heading': 'CHARIAL Dashboard',
        'current_date': timezone.now().date()
    }
    return render(request, 'charial/main.html', context)

@login_required
def charial_bill(request):
    party_form = PartyNameForm(request.POST or None)
    if request.method == 'POST' and 'party_submit' in request.POST:
        if party_form.is_valid():
            party_form.save()
            return redirect('charial_bill')

    bill_form = CharialBillForm(request.POST or None)
    if request.method == 'POST' and 'bill_submit' in request.POST:
        if bill_form.is_valid():
            bill_form.save()
            return redirect('charial_bill')

    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if not start_date and not end_date:
        today = timezone.now().date()
        bills = CharialBill.objects.filter(date=today)
    else:
        bills = CharialBill.objects.all()
        if start_date and end_date:
            bills = bills.filter(date__range=[start_date, end_date])
        elif start_date:
            bills = bills.filter(date__gte=start_date)
        elif end_date:
            bills = bills.filter(date__lte=end_date)

    total_bill = sum(bill.totalBill for bill in bills)
    total_commission = sum(bill.commissionAmount for bill in bills)
    total_others = sum(bill.others for bill in bills)
    total_net = sum(bill.netBill for bill in bills)

    context = {
        'heading': 'CHARIAL BILL Management',
        'party_form': party_form,
        'bill_form': bill_form,
        'bills': bills,
        'total_bill': total_bill,
        'total_commission': total_commission,
        'total_others': total_others,
        'total_net': total_net,
        'current_date': timezone.now().date()
    }
    return render(request, 'charial/bill.html', context)

def export_charial_bills(request):
    # Get filter parameters
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    
    bills = CharialBill.objects.all()
    if start_date and end_date:
        bills = bills.filter(date__range=[start_date, end_date])
    
    # Create DataFrame
    data = []
    total_bill = 0
    total_commission = 0
    total_others = 0
    total_net = 0
    
    for bill in bills:
        data.append([
            bill.date.strftime("%Y-%m-%d"),
            bill.partyName.partyName,
            float(bill.totalBill),
            float(bill.commissionPercentage),
            float(bill.commissionAmount),
            float(bill.others),
            float(bill.netBill)
        ])
        
        # Accumulate totals
        total_bill += float(bill.totalBill)
        total_commission += float(bill.commissionAmount)
        total_others += float(bill.others)
        total_net += float(bill.netBill)
    
    # Add totals row
    data.append([
        "Total",
        "",
        total_bill,
        "",
        total_commission,
        total_others,
        total_net
    ])
    
    df = pd.DataFrame(data, columns=[
        'Date', 'Party Name', 'Total Bill', 'Commission %', 
        'Commission Amount', 'Others', 'Net Bill'
    ])
    
    # Create response
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="charial_bills.xlsx"'
    df.to_excel(response, index=False)
    return response
@login_required
def charial_daily_expenses(request):
    wages_form = WagesNameForm(request.POST or None)
    if request.method == 'POST' and 'wages_submit' in request.POST:
        if wages_form.is_valid():
            wages_form.save()
            return redirect('charial_daily')

    other_form = OtherExpensesNameForm(request.POST or None)
    if request.method == 'POST' and 'other_submit' in request.POST:
        if other_form.is_valid():
            other_form.save()
            return redirect('charial_daily')

    expense_form = DailyExpenseForm(request.POST or None)
    if request.method == 'POST' and 'expense_submit' in request.POST:
        if expense_form.is_valid():
            expense_type = expense_form.cleaned_data.get('expenseType')
            wages_name = expense_form.cleaned_data.get('wagesName')
            other_name = expense_form.cleaned_data.get('otherExpensesName')

            if expense_type == 'wages' and not wages_name:
                expense_form.add_error('wagesName', 'This field is required for wages')
            elif expense_type == 'other' and not other_name:
                expense_form.add_error('otherExpensesName', 'This field is required for other expenses')
            else:
                expense = expense_form.save(commit=False)
                expense.date = timezone.now().date()
                expense.save()
                return redirect('charial_daily')

    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    expense_type = request.GET.get('expense_type')

    if not start_date and not end_date and not expense_type:
        today = timezone.now().date()
        expenses = CharialDailyExpenses.objects.filter(date=today)
    else:
        expenses = CharialDailyExpenses.objects.all()
        if start_date and end_date:
            expenses = expenses.filter(date__range=[start_date, end_date])
        elif start_date:
            expenses = expenses.filter(date__gte=start_date)
        elif end_date:
            expenses = expenses.filter(date__lte=end_date)

        if expense_type:
            expenses = expenses.filter(expenseType=expense_type)

    total_amount = sum(expense.amount for expense in expenses)

    context = {
        'heading': 'CHARIAL Daily Expenses',
        'current_date': timezone.now().date(),
        'wages_form': wages_form,
        'other_form': other_form,
        'expense_form': expense_form,
        'expenses': expenses,
        'total_amount': total_amount
    }
    return render(request, 'charial/daily_expenses.html', context)


def export_charial_daily_expenses(request):
    # Get filter parameters
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    expense_type = request.GET.get('expense_type')
    
    expenses = CharialDailyExpenses.objects.all()
    
    if start_date and end_date:
        expenses = expenses.filter(date__range=[start_date, end_date])
    if expense_type:
        expenses = expenses.filter(expenseType=expense_type)
    
    # Create DataFrame
    data = []
    total_amount = 0
    
    for expense in expenses:
        data.append([
            expense.date.strftime("%Y-%m-%d"),
            expense.get_expenseType_display(),
            expense.get_name(),
            float(expense.amount)
        ])
        
        # Accumulate total
        total_amount += float(expense.amount)
    
    # Add totals row
    data.append([
        "Total",
        "",
        "",
        total_amount
    ])
    
    df = pd.DataFrame(data, columns=[
        'Date', 'Expense Type', 'Name', 'Amount'
    ])
    
    # Create response
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="charial_daily_expenses.xlsx"'
    df.to_excel(response, index=False)
    return response








def export_charial_trade(request):
    # Get all filter parameters
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    unique_names = request.GET.get('unique_names', False)
    
    # Replicate the same filtering logic as main view
    trades = CharialTrade.objects.all()
    
    # Date filtering
    if start_date and end_date:
        trades = trades.filter(date__range=[start_date, end_date])
    elif start_date:
        trades = trades.filter(date__gte=start_date)
    elif end_date:
        trades = trades.filter(date__lte=end_date)
    
    # Unique names filter
    if unique_names:
        latest_trades = CharialTrade.objects.filter(
            seller=OuterRef('seller')
        ).order_by('-date', '-tradeId')
        trades = trades.filter(pk__in=Subquery(latest_trades.values('pk')[:1]))

    # Create DataFrame with identical data to web view
    data = []
    total_purchase = 0
    total_am = 0
    total_pm = 0
    total_new_pending = 0
    
    for trade in trades:
        data.append([
            trade.date.strftime("%Y-%m-%d"),
            trade.seller.name,
            float(trade.todayPurchase),
            float(trade.amPayment),
            float(trade.pmPayment),
            float(trade.new_pending)
        ])
        
        # Accumulate totals
        total_purchase += float(trade.todayPurchase)
        total_am += float(trade.amPayment)
        total_pm += float(trade.pmPayment)
        total_new_pending += float(trade.new_pending)
    
    # Add totals row
    data.append([
        "Total",
        "",
        total_purchase,
        total_am,
        total_pm,
        total_new_pending
    ])
    
    df = pd.DataFrame(data, columns=[
        'Date', 'Seller', 'Today Purchase', 
        'AM Payment', 'PM Payment', 'New Pending'
    ])
    
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="charial_trade.xlsx"'
    df.to_excel(response, index=False)
    return response



from django.db.models import Subquery, OuterRef
@login_required
def charial_trade(request):
    seller_form = TradeSellerForm(request.POST or None)
    if request.method == 'POST' and 'seller_submit' in request.POST:
        if seller_form.is_valid():
            seller_form.save()
            return redirect('charial_trade')

    trade_form = TradeForm(request.POST or None)
    if request.method == 'POST' and 'trade_submit' in request.POST:
        if trade_form.is_valid():
            trade_form.save()
            return redirect('charial_trade')

    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    unique_names = request.GET.get('unique_names', False)

    if not start_date and not end_date and not unique_names:
        today = timezone.now().date()
        trades = CharialTrade.objects.filter(date=today)
    else:
        trades = CharialTrade.objects.all()
        if start_date and end_date:
            trades = trades.filter(date__range=[start_date, end_date])
        elif start_date:
            trades = trades.filter(date__gte=start_date)
        elif end_date:
            trades = trades.filter(date__lte=end_date)

        if unique_names:
            latest_trades = CharialTrade.objects.filter(
                seller=OuterRef('seller')
            ).order_by('-date', '-tradeId')
            trades = trades.filter(pk__in=Subquery(latest_trades.values('pk')[:1]))

    total_purchase = sum(t.todayPurchase for t in trades)
    total_am = sum(t.amPayment for t in trades)
    total_pm = sum(t.pmPayment for t in trades)
    total_new_pending = sum(t.new_pending for t in trades)

    context = {
        'heading': 'CHARIAL Trade',
        'current_date': timezone.now().date(),
        'seller_form': seller_form,
        'trade_form': trade_form,
        'trades': trades,
        'total_purchase': total_purchase,
        'total_am': total_am,
        'total_pm': total_pm,
        'total_new_pending': total_new_pending,
        'unique_names': unique_names
    }
    return render(request, 'charial/trade.html', context)

@login_required
def charial_balance_sheet(request):
    context = {
        'heading': 'CHARIAL Balance Sheet',
        'current_date': timezone.now().date()
    }
    return render(request, 'charial/balance_sheet.html', context)

# Mahisgoat Views
@login_required
def mahisgoat_main(request):
    context = {
        'heading': 'MAHISGOAT Dashboard',
        'current_date': timezone.now().date()
    }
    return render(request, 'mahisgoat/main.html', context)

from django.http import JsonResponse
from django.db.models import F, ExpressionWrapper, DecimalField
from django.db import transaction
import pandas as pd
import calendar
from datetime import datetime, date
import xlsxwriter
from io import BytesIO

# Add these imports at the top
from .models import CharialBalanceSheet
from .forms import BalanceSheetForm

@login_required
def charial_balance_sheet(request):
    # Get current year and month
    current_year = datetime.now().year
    current_month = datetime.now().month
    
    # Get selected year and month from request
    selected_year = int(request.GET.get('year', current_year))
    selected_month = int(request.GET.get('month', current_month))
    
    # Get all days in selected month
    num_days = calendar.monthrange(selected_year, selected_month)[1]
    days_in_month = [date(selected_year, selected_month, day) for day in range(1, num_days + 1)]
    
    # Get existing records
    records = {}
    for record in CharialBalanceSheet.objects.filter(date__year=selected_year, date__month=selected_month):
        records[record.date] = record
    
    # Create forms for each day
    forms = []
    for day in days_in_month:
        if day in records:
            form = BalanceSheetForm(instance=records[day])
        else:
            form = BalanceSheetForm(initial={'date': day})
        forms.append(form)
    
    # Calculate totals
    totals = {
        'bill': 0,
        'commission': 0,
        'extra': 0,
        'britty': 0,
        'income': 0,
        'expenses': 0,
        'profit_loss': 0
    }
    
    for record in records.values():
        totals['bill'] += record.bill
        totals['commission'] += record.commission
        totals['extra'] += record.extra
        totals['britty'] += record.britty
        totals['income'] += record.income
        totals['expenses'] += record.expenses
        totals['profit_loss'] += record.profit_loss
    
    # Handle form submission
    if request.method == 'POST':
        date_value = request.POST.get('date')
        try:
            # Convert string to date object
            date_obj = datetime.strptime(date_value, '%Y-%m-%d').date()
            
            # Get or create record
            record, created = CharialBalanceSheet.objects.get_or_create(
                date=date_obj,
                defaults={
                    'bill': 0,
                    'commission': 0,
                    'extra': 0,
                    'britty': 0,
                    'expenses': 0
                }
            )
            
            # Update record
            record.bill = float(request.POST.get('bill', 0))
            record.commission = float(request.POST.get('commission', 0))
            record.extra = float(request.POST.get('extra', 0))
            record.britty = float(request.POST.get('britty', 0))
            record.expenses = float(request.POST.get('expenses', 0))
            record.save()
            
            return JsonResponse({'status': 'success', 'date': date_value})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e), 'date': date_value})
    
    # Years range for dropdown
    years = range(current_year - 5, current_year + 1)
    
    context = {
        'heading': 'CHARIAL Balance Sheet',
        'current_date': timezone.now().date(),
        'forms': forms,
        'days_in_month': days_in_month,
        'totals': totals,
        'years': years,
        'selected_year': selected_year,
        'selected_month': selected_month,
        'months': [
            (1, 'January'), (2, 'February'), (3, 'March'), (4, 'April'),
            (5, 'May'), (6, 'June'), (7, 'July'), (8, 'August'),
            (9, 'September'), (10, 'October'), (11, 'November'), (12, 'December')
        ]
    }
    return render(request, 'charial/balance_sheet.html', context)








def export_balance_sheet(request):
    # Get filter parameters
    year = request.GET.get('year')
    month = request.GET.get('month')
    
    # Get records
    records = CharialBalanceSheet.objects.filter(
        date__year=year,
        date__month=month
    ).order_by('date')
    
    # Create DataFrame
    data = []
    total_bill = 0
    total_commission = 0
    total_extra = 0
    total_britty = 0
    total_income = 0
    total_expenses = 0
    total_profit_loss = 0
    
    for record in records:
        data.append([
            record.date.strftime("%d-%b-%Y"),
            float(record.bill),
            float(record.commission),
            float(record.extra),
            float(record.britty),
            float(record.income),
            float(record.expenses),
            float(record.profit_loss)
        ])
        
        # Accumulate totals
        total_bill += float(record.bill)
        total_commission += float(record.commission)
        total_extra += float(record.extra)
        total_britty += float(record.britty)
        total_income += float(record.income)
        total_expenses += float(record.expenses)
        total_profit_loss += float(record.profit_loss)
    
    # Add totals row
    data.append([
        "Total",
        total_bill,
        total_commission,
        total_extra,
        total_britty,
        total_income,
        total_expenses,
        total_profit_loss
    ])
    
    df = pd.DataFrame(data, columns=[
        'Date', 'Bill', 'Commission', 'Extra', 
        'Britty', 'Income', 'Expenses', 'Profit/Loss'
    ])
    
    # Create response
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = f'attachment; filename="charial_balance_{year}_{month}.xlsx"'
    df.to_excel(response, index=False)
    return response


@login_required
def mahisgoat_bill(request):
    party_form = MahisgoatPartyNameForm(request.POST or None)
    if request.method == 'POST' and 'party_submit' in request.POST and party_form.is_valid():
        party_form.save()
        return redirect('mahisgoat_bill')

    bill_form = MahisgoatBillForm(request.POST or None)
    if request.method == 'POST' and 'bill_submit' in request.POST and bill_form.is_valid():
        bill_form.save()
        return redirect('mahisgoat_bill')

    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    # Apply today's filter by default
    if not start_date and not end_date:
        today = timezone.now().date()
        start_date = end_date = today

    bills = MahisgoatBill.objects.all()
    if start_date and end_date:
        bills = bills.filter(date__range=[start_date, end_date])
    elif start_date:
        bills = bills.filter(date__gte=start_date)
    elif end_date:
        bills = bills.filter(date__lte=end_date)

    total_bill = sum(bill.totalBill for bill in bills)
    total_commission = sum(bill.commissionAmount for bill in bills)
    total_others = sum(bill.others for bill in bills)
    total_net = sum(bill.netBill for bill in bills)

    context = {
        'heading': 'MAHISGOAT BILL Management',
        'party_form': party_form,
        'bill_form': bill_form,
        'bills': bills,
        'total_bill': total_bill,
        'total_commission': total_commission,
        'total_others': total_others,
        'total_net': total_net,
        'current_date': timezone.now().date()
    }
    return render(request, 'mahisgoat/bill.html', context)
@login_required
def mahisgoat_daily_expenses(request):
    wages_form = MahisgoatWagesNameForm(request.POST or None)
    if request.method == 'POST' and 'wages_submit' in request.POST and wages_form.is_valid():
        wages_form.save()
        return redirect('mahisgoat_daily')

    other_form = MahisgoatOtherExpensesNameForm(request.POST or None)
    if request.method == 'POST' and 'other_submit' in request.POST and other_form.is_valid():
        other_form.save()
        return redirect('mahisgoat_daily')

    expense_form = MahisgoatDailyExpenseForm(request.POST or None)
    if request.method == 'POST' and 'expense_submit' in request.POST:
        if expense_form.is_valid():
            expense_type = expense_form.cleaned_data.get('expenseType')
            wages_name = expense_form.cleaned_data.get('wagesName')
            other_name = expense_form.cleaned_data.get('otherExpensesName')
            
            if expense_type == 'wages' and not wages_name:
                expense_form.add_error('wagesName', 'This field is required for wages')
            elif expense_type == 'other' and not other_name:
                expense_form.add_error('otherExpensesName', 'This field is required for other expenses')
            else:
                expense = expense_form.save(commit=False)
                expense.date = timezone.now().date()
                expense.save()
                return redirect('mahisgoat_daily')

    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    expense_type = request.GET.get('expense_type')

    # Default filter to today
    if not start_date and not end_date:
        today = timezone.now().date()
        start_date = end_date = today

    expenses = MahisgoatDailyExpenses.objects.all()

    if start_date and end_date:
        expenses = expenses.filter(date__range=[start_date, end_date])
    elif start_date:
        expenses = expenses.filter(date__gte=start_date)
    elif end_date:
        expenses = expenses.filter(date__lte=end_date)

    if expense_type:
        expenses = expenses.filter(expenseType=expense_type)

    total_amount = sum(expense.amount for expense in expenses)

    context = {
        'heading': 'MAHISGOAT Daily Expenses',
        'current_date': timezone.now().date(),
        'wages_form': wages_form,
        'other_form': other_form,
        'expense_form': expense_form,
        'expenses': expenses,
        'total_amount': total_amount
    }
    return render(request, 'mahisgoat/daily_expenses.html', context)

@login_required
def mahisgoat_trade(request):
    seller_form = MahisgoatTradeSellerForm(request.POST or None)
    if request.method == 'POST' and 'seller_submit' in request.POST and seller_form.is_valid():
        seller_form.save()
        return redirect('mahisgoat_trade')

    trade_form = MahisgoatTradeForm(request.POST or None)
    if request.method == 'POST' and 'trade_submit' in request.POST and trade_form.is_valid():
        trade_form.save()
        return redirect('mahisgoat_trade')

    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    unique_names = request.GET.get('unique_names', False)

    # Default filter to today
    if not start_date and not end_date:
        today = timezone.now().date()
        start_date = end_date = today

    trades = MahisgoatTrade.objects.all()

    if start_date and end_date:
        trades = trades.filter(date__range=[start_date, end_date])
    elif start_date:
        trades = trades.filter(date__gte=start_date)
    elif end_date:
        trades = trades.filter(date__lte=end_date)

    if unique_names:
        latest_trades = MahisgoatTrade.objects.filter(
            seller=OuterRef('seller')
        ).order_by('-date', '-tradeId')
        trades = trades.filter(
            pk__in=Subquery(latest_trades.values('pk')[:1])
        )

    total_purchase = sum(t.todayPurchase for t in trades)
    total_am = sum(t.amPayment for t in trades)
    total_pm = sum(t.pmPayment for t in trades)
    total_new_pending = sum(t.new_pending for t in trades)

    context = {
        'heading': 'MAHISGOAT Trade',
        'current_date': timezone.now().date(),
        'seller_form': seller_form,
        'trade_form': trade_form,
        'trades': trades,
        'total_purchase': total_purchase,
        'total_am': total_am,
        'total_pm': total_pm,
        'total_new_pending': total_new_pending,
        'unique_names': unique_names
    }
    return render(request, 'mahisgoat/trade.html', context)

@login_required
def mahisgoat_balance_sheet(request):
    current_year = datetime.now().year
    current_month = datetime.now().month
    
    selected_year = int(request.GET.get('year', current_year))
    selected_month = int(request.GET.get('month', current_month))
    
    num_days = calendar.monthrange(selected_year, selected_month)[1]
    days_in_month = [date(selected_year, selected_month, day) for day in range(1, num_days + 1)]
    
    records = {}
    for record in MahisgoatBalanceSheet.objects.filter(date__year=selected_year, date__month=selected_month):
        records[record.date] = record
    
    forms = []
    for day in days_in_month:
        if day in records:
            form = MahisgoatBalanceSheetForm(instance=records[day])
        else:
            form = MahisgoatBalanceSheetForm(initial={'date': day})
        forms.append(form)
    
    totals = {
        'bill': 0,
        'commission': 0,
        'extra': 0,
        'britty': 0,
        'income': 0,
        'expenses': 0,
        'profit_loss': 0
    }
    
    for record in records.values():
        totals['bill'] += record.bill
        totals['commission'] += record.commission
        totals['extra'] += record.extra
        totals['britty'] += record.britty
        totals['income'] += record.income
        totals['expenses'] += record.expenses
        totals['profit_loss'] += record.profit_loss
    
    if request.method == 'POST':
        date_value = request.POST.get('date')
        try:
            date_obj = datetime.strptime(date_value, '%Y-%m-%d').date()
            record, created = MahisgoatBalanceSheet.objects.get_or_create(
                date=date_obj,
                defaults={
                    'bill': 0,
                    'commission': 0,
                    'extra': 0,
                    'britty': 0,
                    'expenses': 0
                }
            )
            record.bill = float(request.POST.get('bill', 0))
            record.commission = float(request.POST.get('commission', 0))
            record.extra = float(request.POST.get('extra', 0))
            record.britty = float(request.POST.get('britty', 0))
            record.expenses = float(request.POST.get('expenses', 0))
            record.save()
            return JsonResponse({'status': 'success', 'date': date_value})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e), 'date': date_value})
    
    years = range(current_year - 5, current_year + 1)
    
    context = {
        'heading': 'MAHISGOAT Balance Sheet',
        'current_date': timezone.now().date(),
        'forms': forms,
        'days_in_month': days_in_month,
        'totals': totals,
        'years': years,
        'selected_year': selected_year,
        'selected_month': selected_month,
        'months': [
            (1, 'January'), (2, 'February'), (3, 'March'), (4, 'April'),
            (5, 'May'), (6, 'June'), (7, 'July'), (8, 'August'),
            (9, 'September'), (10, 'October'), (11, 'November'), (12, 'December')
        ]
    }
    return render(request, 'mahisgoat/balance_sheet.html', context)

# Export functions
def export_mahisgoat_bills(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    
    bills = MahisgoatBill.objects.all()
    if start_date and end_date:
        bills = bills.filter(date__range=[start_date, end_date])
    
    data = []
    total_bill = 0
    total_commission = 0
    total_others = 0
    total_net = 0
    
    for bill in bills:
        data.append([
            bill.date.strftime("%Y-%m-%d"),
            bill.partyName.partyName,
            float(bill.totalBill),
            float(bill.commissionPercentage),
            float(bill.commissionAmount),
            float(bill.others),
            float(bill.netBill)
        ])
        total_bill += float(bill.totalBill)
        total_commission += float(bill.commissionAmount)
        total_others += float(bill.others)
        total_net += float(bill.netBill)
    
    data.append([
        "Total",
        "",
        total_bill,
        "",
        total_commission,
        total_others,
        total_net
    ])
    
    df = pd.DataFrame(data, columns=[
        'Date', 'Party Name', 'Total Bill', 'Commission %', 
        'Commission Amount', 'Others', 'Net Bill'
    ])
    
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="mahisgoat_bills.xlsx"'
    df.to_excel(response, index=False)
    return response

def export_mahisgoat_daily_expenses(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    expense_type = request.GET.get('expense_type')
    
    expenses = MahisgoatDailyExpenses.objects.all()
    
    if start_date and end_date:
        expenses = expenses.filter(date__range=[start_date, end_date])
    if expense_type:
        expenses = expenses.filter(expenseType=expense_type)
    
    data = []
    total_amount = 0
    
    for expense in expenses:
        data.append([
            expense.date.strftime("%Y-%m-%d"),
            expense.get_expenseType_display(),
            expense.get_name(),
            float(expense.amount)
        ])
        total_amount += float(expense.amount)
    
    data.append([
        "Total",
        "",
        "",
        total_amount
    ])
    
    df = pd.DataFrame(data, columns=[
        'Date', 'Expense Type', 'Name', 'Amount'
    ])
    
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="mahisgoat_daily_expenses.xlsx"'
    df.to_excel(response, index=False)
    return response

def export_mahisgoat_trade(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    unique_names = request.GET.get('unique_names', False)
    
    trades = MahisgoatTrade.objects.all()
    
    if start_date and end_date:
        trades = trades.filter(date__range=[start_date, end_date])
    elif start_date:
        trades = trades.filter(date__gte=start_date)
    elif end_date:
        trades = trades.filter(date__lte=end_date)
    
    if unique_names:
        latest_trades = MahisgoatTrade.objects.filter(
            seller=OuterRef('seller')
        ).order_by('-date', '-tradeId')
        trades = trades.filter(pk__in=Subquery(latest_trades.values('pk')[:1]))

    data = []
    total_purchase = 0
    total_am = 0
    total_pm = 0
    total_new_pending = 0
    
    for trade in trades:
        data.append([
            trade.date.strftime("%Y-%m-%d"),
            trade.seller.name,
            float(trade.todayPurchase),
            float(trade.amPayment),
            float(trade.pmPayment),
            float(trade.new_pending)
        ])
        total_purchase += float(trade.todayPurchase)
        total_am += float(trade.amPayment)
        total_pm += float(trade.pmPayment)
        total_new_pending += float(trade.new_pending)
    
    data.append([
        "Total",
        "",
        total_purchase,
        total_am,
        total_pm,
        total_new_pending
    ])
    
    df = pd.DataFrame(data, columns=[
        'Date', 'Seller', 'Today Purchase', 
        'AM Payment', 'PM Payment', 'New Pending'
    ])
    
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="mahisgoat_trade.xlsx"'
    df.to_excel(response, index=False)
    return response

def export_mahisgoat_balance_sheet(request):
    year = request.GET.get('year')
    month = request.GET.get('month')
    
    records = MahisgoatBalanceSheet.objects.filter(
        date__year=year,
        date__month=month
    ).order_by('date')
    
    data = []
    total_bill = 0
    total_commission = 0
    total_extra = 0
    total_britty = 0
    total_income = 0
    total_expenses = 0
    total_profit_loss = 0
    
    for record in records:
        data.append([
            record.date.strftime("%d-%b-%Y"),
            float(record.bill),
            float(record.commission),
            float(record.extra),
            float(record.britty),
            float(record.income),
            float(record.expenses),
            float(record.profit_loss)
        ])
        total_bill += float(record.bill)
        total_commission += float(record.commission)
        total_extra += float(record.extra)
        total_britty += float(record.britty)
        total_income += float(record.income)
        total_expenses += float(record.expenses)
        total_profit_loss += float(record.profit_loss)
    
    data.append([
        "Total",
        total_bill,
        total_commission,
        total_extra,
        total_britty,
        total_income,
        total_expenses,
        total_profit_loss
    ])
    
    df = pd.DataFrame(data, columns=[
        'Date', 'Bill', 'Commission', 'Extra', 
        'Britty', 'Income', 'Expenses', 'Profit/Loss'
    ])
    
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = f'attachment; filename="mahisgoat_balance_{year}_{month}.xlsx"'
    df.to_excel(response, index=False)
    return response