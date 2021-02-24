# проверка количества дней в месяце. возвращает - (1. корректность запроса, 2. кол-во дней в этом месяце)
def Check_Day(a=[2000,1,1]):
    v = a[0] % 4
    e = 31
    i = 0
    j = True
    if v==0:
        i=1
    if a[1] in (4,6,9,11):
        e = 30
    if a[1] == 2:
        e = 28 + i
    if (a[1] < 1 or a[1] > 12 or a[2] < 0 or a[2] > e):
        j = False
    return (j,e)


class Client_Bank():
    def __init__(self, id = 1, First_Name = "Ivan", Last_Name = "Ivanov", Bank_Name = "Sber", Loan_amount = 100000.0,Loan_Date=[2020, 1, 1], Duration = 12, Interest = 10, Date=[2020, 8, 1]):
        self.id = id
        self.First_Name = First_Name
        self.Last_Name = Last_Name
        self.Bank_Name = Bank_Name
        self.Loan_amount = Loan_amount
        self.Loan_Date = Loan_Date
        self.Duration = Duration
        self.Interest = Interest
        self.Date = Date

        # данные из словаря
    def Get_Data(self, Dict={}):
        self.First_Name = Dict['First_Name']
        self.Last_Name = Dict['Last_Name']
        self.id = Dict['id']
        self.Loan_Date = Dict['Loan_Date']
        self.Bank_Name = Dict['Bank_Name']
        self.Duration = Dict['Duration']
        self.Interest = Dict['Interest']
        self.Loan_amount = Dict['Loan_amount']
        self.Date = Dict['Date']

        # аннуитентный платеж (annuity payment):
    def Calculate(self):
        # дата окончания кредита
        self.Finish_Date = [self.Loan_Date[0]+int(self.Duration/12),self.Loan_Date[1] + self.Duration%12,self.Loan_Date[2]]

        # месячный процент
        self.Mounthly_interest = self.Interest/(12*100)

        # месячный платеж
        self.Mounthly_loan = self.Loan_amount * (self.Mounthly_interest + (self.Mounthly_interest / ((1 + self.Mounthly_interest) ** self.Duration - 1)))

        # остаток
        self.Loan_Balance = {}
        self.Loan_Balance[0] = self.Loan_amount

        # сумма процентов выплачиваемых в месяц
        self.Mounthly_loan_percent = {}

        # сумма погашения основного долга в месяц
        self.Mounthly_repayment = {}

        # сумма всех выплаченных процентов на период
        self.Interest_amount = {}

        # даты периодов
        self.Period_Date = {}

        # расчеты
        for i in range(self.Duration):
            self.Mounthly_loan_percent[i] = self.Mounthly_interest * self.Loan_Balance[i]
            self.Mounthly_repayment[i] = self.Mounthly_loan - self.Mounthly_loan_percent[i]
            self.Loan_Balance[i + 1] = self.Loan_Balance[i] - self.Mounthly_repayment[i]
            self.Interest_amount[i] = sum(self.Mounthly_loan_percent.values())
            year = self.Loan_Date[0] + (self.Loan_Date[1] + i)  // 12
            month = self.Loan_Date[1] + 1 + i  - (year - self.Loan_Date[0]) * 12
            day = min(self.Loan_Date[2], Check_Day([year, month, 1])[1])
            self.Period_Date[i] = [year,month,day]

        self.Full_amount = self.Loan_amount + self.Interest_amount[self.Duration - 1]

        # длительность (кол-во периодов) запрашиваемой даты от даты кредита
        if self.Check_Date():
            m = 0
            if self.Loan_Date[2] - self.Date[2] > 0 :
                m = 1
            self.Request_Duration = (self.Date[0] - self.Loan_Date[0]) * 12 + (self.Date[1] - self.Loan_Date[1])
            # баланс на дату запроса
            self.Current_balance = self.Loan_Balance[self.Request_Duration - m]
            # дата следующего платежа
            self.Next_Date = self.Period_Date[self.Request_Duration - m]
        else:
            self.Request_Duration = 0
            self.Current_balance = self.Loan_Balance[0]
            self.Next_Date = self.Period_Date[0]

        # проверка корректности даты запроса
    def Check_Date(self):
        if (self.Date[1] or self.Loan_Date[1] > 12) and Check_Day(self.Loan_Date):
            if (self.Date[0] > self.Finish_Date[0] or self.Date[0] < self.Loan_Date[0]):
                #('incorrect year')
                return False
            elif ((self.Date[0] == self.Loan_Date[0] and self.Date[1] < self.Loan_Date[1]) or (self.Date[0] == self.Finish_Date[0] and self.Date[1] > self.Finish_Date[1])):
                #('incorrect month')
                return False
            elif ((self.Date[1] == self.Loan_Date[1] and self.Date[2] <= self.Loan_Date[2]) or (self.Date[1] == self.Finish_Date[1] and self.Date[2] > self.Finish_Date[2])):
                #('incorrect day')
                return False
            return True
        else:
            return False

    #инфа по кредиту
    def Credit_Info(self):
        print('Date of request:',self.Date,'correct date:',self.Check_Date())
        print('Client Name:\t',self.First_Name,self.Last_Name,',\tID =',self.id,',\tBank - ',self.Bank_Name)
        print('Credit amount = ',self.Loan_amount,'\tLoan Date - ',self.Loan_Date,'\tInterest : ',self.Interest,'\tDuration - ',self.Duration,'\tFinish Date - ',self.Finish_Date)
        print('Mounthly_interest',self.Mounthly_interest,'\tMounthly_loan :',self.Mounthly_loan,'Full amount : ',self.Full_amount)
        print('Current Balance:',self.Current_balance,'\tNext payment date:',self.Next_Date)

    #график платежей
    def Payment_schedule(self):
        print('#\t\tdate:\t\t\tLoan balance(in):\t\tLoan:\t\t\tMounthly_loan_percent:\tMounthly_repayment:\tLoan balance(out):')
        for i in range(self.Duration):
            print(i,'\t',self.Period_Date[i],':',self.Loan_Balance[i],'\t',self.Mounthly_loan,'\t',self.Mounthly_loan_percent[i],'\t',self.Mounthly_repayment[i],'\t',self.Loan_Balance[i+1])


#example:
a = Client_Bank(Loan_Date = [2019,1,31],Date = [2019,2,1],Duration = 6,Loan_amount = 100000.0)
a.Calculate()
a.Credit_Info()
a.Payment_schedule()

b = {'First_Name': "Boris",
     'Last_Name':  "Petrov",
     'id': 2,
     'Loan_Date':[2010,10,10],
     'Bank_Name': "VTB",
     'Duration': 12,
     'Interest': 26,
     'Loan_amount': 50000.0,
     'Date': [2011,9,11]}
c = Client_Bank()
c.Get_Data(b)
c.Calculate()
c.Credit_Info()
c.Payment_schedule()
