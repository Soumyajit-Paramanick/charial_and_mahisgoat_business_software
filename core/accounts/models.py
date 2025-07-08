from django.db import models
from django.utils import timezone

class CharialBillPartyName(models.Model):
    partyNameId = models.AutoField(primary_key=True)
    partyName = models.CharField(max_length=100, unique=True, error_messages={'unique': 'This party name already exists!'})
    dateAdded = models.DateField(default=timezone.now)

    def __str__(self):
        return self.partyName

class CharialBill(models.Model):
    partyName = models.ForeignKey(CharialBillPartyName, on_delete=models.CASCADE)
    totalBill = models.DecimalField(max_digits=10, decimal_places=2)
    commissionPercentage = models.DecimalField(max_digits=5, decimal_places=2)
    others = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(default=timezone.now)
    
    @property
    def commissionAmount(self):
        return self.totalBill * (self.commissionPercentage / 100)
    
    @property
    def netBill(self):
        return self.totalBill - (self.commissionAmount + self.others)

class CharialDailyExpensesWagesName(models.Model):
    wagesNameId = models.AutoField(primary_key=True)
    wagesName = models.CharField(max_length=100, unique=True, error_messages={'unique': 'This wage name already exists!'})
    dateAdded = models.DateField(default=timezone.now)

    def __str__(self):
        return self.wagesName

class CharialDailyExpensesOtherExpensesName(models.Model):
    otherExpensesId = models.AutoField(primary_key=True)
    otherExpensesName = models.CharField(max_length=100, unique=True, error_messages={'unique': 'This expense name already exists!'})
    dateAdded = models.DateField(default=timezone.now)

    def __str__(self):
        return self.otherExpensesName

class CharialDailyExpenses(models.Model):
    EXPENSE_TYPES = [
        ('wages', 'Wages'),
        ('other', 'Other'),
    ]
    
    expenseId = models.AutoField(primary_key=True)
    date = models.DateField(default=timezone.now)
    expenseType = models.CharField(max_length=10, choices=EXPENSE_TYPES)
    wagesName = models.ForeignKey(CharialDailyExpensesWagesName, on_delete=models.CASCADE, null=True, blank=True)
    otherExpensesName = models.ForeignKey(CharialDailyExpensesOtherExpensesName, on_delete=models.CASCADE, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def get_name(self):
        return self.wagesName if self.expenseType == 'wages' else self.otherExpensesName

class CharialTradeSeller(models.Model):
    sellerId = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True, error_messages={'unique': 'This seller name already exists!'})
    pendingAmount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    dateAdded = models.DateField(default=timezone.now)

    def __str__(self):
        return self.name
class CharialTrade(models.Model):
    tradeId = models.AutoField(primary_key=True)
    date = models.DateField(default=timezone.now)
    seller = models.ForeignKey(CharialTradeSeller, on_delete=models.CASCADE)
    todayPurchase = models.DecimalField(max_digits=10, decimal_places=2)
    amPayment = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    pmPayment = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    # Add these new fields
    pprevious_pending = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0.00,
        editable=False
    )
    new_pending = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0.00,
        editable=False
    )

    def save(self, *args, **kwargs):
        # Store the pending amount before this transaction
        self.previous_pending = self.seller.pendingAmount
        
        # Calculate new pending
        self.new_pending = self.previous_pending + self.todayPurchase - (self.amPayment + self.pmPayment)
        
        # Update seller's record
        self.seller.pendingAmount = self.new_pending
        self.seller.save()
        
        super().save(*args, **kwargs)

# # Add to accounts/models.py
# class CharialBalanceSheet(models.Model):
#     date = models.DateField(unique=True)
#     bill = models.DecimalField(max_digits=10, decimal_places=2, default=0)
#     commission = models.DecimalField(max_digits=10, decimal_places=2, default=0)
#     extra = models.DecimalField(max_digits=10, decimal_places=2, default=0)
#     britty = models.DecimalField(max_digits=10, decimal_places=2, default=0)
#     expenses = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
#     @property
#     def income(self):
#         return self.commission + self.extra + self.britty
    
#     @property
#     def profit_loss(self):
#         return self.income - self.expenses
    
#     def __str__(self):
#         return f"Balance Sheet - {self.date.strftime('%d %b %Y')}"












class CharialBalanceSheet(models.Model):
    date = models.DateField(unique=True)
    bill = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    commission = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    extra = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    britty = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    expenses = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    @property
    def income(self):
        return self.commission + self.extra + self.britty
    
    @property
    def profit_loss(self):
        return self.income - self.expenses
    
    def __str__(self):
        return f"Balance - {self.date}"
    










































# Add these after the Charial models
class MahisgoatBillPartyName(models.Model):
    partyNameId = models.AutoField(primary_key=True)
    partyName = models.CharField(max_length=100, unique=True, error_messages={'unique': 'This party name already exists!'})
    dateAdded = models.DateField(default=timezone.now)

    def __str__(self):
        return self.partyName

class MahisgoatBill(models.Model):
    partyName = models.ForeignKey(MahisgoatBillPartyName, on_delete=models.CASCADE)
    totalBill = models.DecimalField(max_digits=10, decimal_places=2)
    commissionPercentage = models.DecimalField(max_digits=5, decimal_places=2)
    others = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(default=timezone.now)
    
    @property
    def commissionAmount(self):
        return self.totalBill * (self.commissionPercentage / 100)
    
    @property
    def netBill(self):
        return self.totalBill - (self.commissionAmount + self.others)

class MahisgoatDailyExpensesWagesName(models.Model):
    wagesNameId = models.AutoField(primary_key=True)
    wagesName = models.CharField(max_length=100, unique=True, error_messages={'unique': 'This wage name already exists!'})
    dateAdded = models.DateField(default=timezone.now)

    def __str__(self):
        return self.wagesName

class MahisgoatDailyExpensesOtherExpensesName(models.Model):
    otherExpensesId = models.AutoField(primary_key=True)
    otherExpensesName = models.CharField(max_length=100, unique=True, error_messages={'unique': 'This expense name already exists!'})
    dateAdded = models.DateField(default=timezone.now)

    def __str__(self):
        return self.otherExpensesName

class MahisgoatDailyExpenses(models.Model):
    EXPENSE_TYPES = [
        ('wages', 'Wages'),
        ('other', 'Other'),
    ]
    
    expenseId = models.AutoField(primary_key=True)
    date = models.DateField(default=timezone.now)
    expenseType = models.CharField(max_length=10, choices=EXPENSE_TYPES)
    wagesName = models.ForeignKey(MahisgoatDailyExpensesWagesName, on_delete=models.CASCADE, null=True, blank=True)
    otherExpensesName = models.ForeignKey(MahisgoatDailyExpensesOtherExpensesName, on_delete=models.CASCADE, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def get_name(self):
        return self.wagesName if self.expenseType == 'wages' else self.otherExpensesName

class MahisgoatTradeSeller(models.Model):
    sellerId = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True, error_messages={'unique': 'This seller name already exists!'})
    pendingAmount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    dateAdded = models.DateField(default=timezone.now)

    def __str__(self):
        return self.name

class MahisgoatTrade(models.Model):
    tradeId = models.AutoField(primary_key=True)
    date = models.DateField(default=timezone.now)
    seller = models.ForeignKey(MahisgoatTradeSeller, on_delete=models.CASCADE)
    todayPurchase = models.DecimalField(max_digits=10, decimal_places=2)
    amPayment = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    pmPayment = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    previous_pending = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0.00,
        editable=False
    )
    new_pending = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0.00,
        editable=False
    )

    def save(self, *args, **kwargs):
        self.previous_pending = self.seller.pendingAmount
        self.new_pending = self.previous_pending + self.todayPurchase - (self.amPayment + self.pmPayment)
        self.seller.pendingAmount = self.new_pending
        self.seller.save()
        super().save(*args, **kwargs)

class MahisgoatBalanceSheet(models.Model):
    date = models.DateField(unique=True)
    bill = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    commission = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    extra = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    britty = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    expenses = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    @property
    def income(self):
        return self.commission + self.extra + self.britty
    
    @property
    def profit_loss(self):
        return self.income - self.expenses
    
    def __str__(self):
        return f"Mahisgoat Balance - {self.date}"