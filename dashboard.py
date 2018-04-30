import os.path
import subprocess
from datetime import date, datetime

# variables
months = 'Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec'.split()
currentmonth = months[int(date.today().month)-1]

def getnextmonth():
    ''' return will the next month name '''
    nextmonth = int(date.today().month) + 1
    if nextmonth == 13:
        nextmonth = 1
    nextmonth = months[nextmonth -1]
    return nextmonth

ledgerfile= 'mygl.ledger'
 # Balance sheet report
if os.path.isfile(ledgerfile):
    ''' checking the file '''
    print('Using ledger file : {}'.format(ledgerfile))
else:
    ledgerfile = input('Enter the Ledger file name: ')

def getaccounts(ledgerfile, acc='',depth='5'):
    ''' list all accounts if account is not define '''
    qry = 'ledger -f {} accounts {} --depth {}'.format(ledgerfile, acc, depth).split()
    result = subprocess.Popen(qry, stdout=subprocess.PIPE)
    result = result.communicate()[0].decode("utf-8")
    return result.split('\n')

def nfm(number):
    n = '{:14,.2f}'.format(float(number))
    return n
    

    
def result_to_dic(qry):
    ''' converting query result to dict '''
    level1 = '-->'
    level2 = '---->'
    result = subprocess.Popen(qry, stdout=subprocess.PIPE)
    result = result.communicate()[0].decode("utf-8")
    #print(result)
    result= result.split(',,')
    outdata = dict()
    for data in result :
        if data != '':
            try :
                k,v = data.split('|')
            except:
                return result
            outdata[k] = nfm(float(v))
    return outdata

def balances(ledgerfile, account = '', depth ='5'):
    ''' getting the balances in dict format'''
    qry1 = ['ledger','-f','{}'.format(ledgerfile),'bal']
    qry2 = ['{}'.format(account),'--depth',depth]
    qry3 = '--no-total -F %A|%T,, -E'.split()
    abal = dict()
    if account == '':
        qry = qry1 + qry3
    else:
        qry = qry1 + qry2 + qry3
    #print(qry)
    abal = result_to_dic(qry)
    return abal
    
def balancesheet(ledgerfile,level='1'):
    bs_accounts = ['Assets','Liabilities','Equity']
    btotal=0.00
    bsheet = dict()
    for acc in bs_accounts:
        result = balances(ledgerfile,account = ('^'+acc),depth=level)
        btotal = btotal + float(result[acc].replace(',',''))
        bsheet[acc]=result
    bsheet['Total']=nfm(float(btotal))
    return bsheet

def incomestat(ledgerfile,level='1'):
    is_accounts = ['Income','Expenses']
    totalinc=0.00
    totalexp=0.00
    profit = dict()
    inc_result = balances(ledgerfile,account ='^Income',depth=level)
    exp_result = balances(ledgerfile,account ='^Expenses',depth=level)
    for acc,amt in inc_result.items():
        totalinc = totalinc + float(amt.replace(',',''))
    for acc,amt in exp_result.items():
        totalexp = totalexp + float(amt.replace(',',''))
    profit['totalincome']=nfm(float(totalinc))
    profit['totalexpenses']=nfm(float(totalexp))
    profit['netprofit']=nfm(float(totalinc + totalexp))
    return inc_result,exp_result,profit
        

def dues(ledgerfile,m=''):
    ''' getting the dues for the required month default will be next month'''
    qry1= ['ledger','-f', '{}'.format(ledgerfile)]
    qry2 = 'reg CreditCard PDC  -F %d|%A|%N|%t,, --no-total --pending'.split()
    qry = qry1 + qry2
    result = result_to_dic(qry)
    maincat = []
    subcat = dict()
    for line in result:
        if line != '':
            dt,acc,note,amt =line.split('|')
            #subcat[dt]=float(amt)
            month = dt.split('-')[1]
            if month == m:
                maincat.append([month,dt,acc,note,nfm(float(amt))])
    if not maincat:
        return None
    else: 
        return maincat

def monthlyExp(ledgerfile, account=None):
    ''' return monthly expenses '''
    if account is None : account = '^Expenses'
    qry1 = ['ledger','-f','{}'.format(ledgerfile),'bal','{}'.format(account)] 
    qry2 = '-F %A|%t,, --no-total --period-sort (date) --period'.split()
    qry = qry1 + qry2
    monthly = dict()
    for mon in months:
        qrymon = qry + ['{}'.format(mon)]
        #print(qrymon)
        result = result_to_dic(qrymon)
        monthly[mon]=result
    return monthly
        

def accounttrax(ledgerfile, account='Assets'):
    ''' getting account details by default will get asset register'''
    qry1= ['ledger','-f', '{}'.format(ledgerfile)]
    qry2 = ['reg','{}'.format(account)] 
    qry3 = '-F %d|%A|%N|%t,, --sort (date) --no-total'.split()
    qry = qry1 + qry2 + qry3
    result = result_to_dic(qry)
    maincat = []
    subcat = dict()
    balance =0.00
    dr = 0.00
    cr = 0.00
    for line in result:
        if line != '':
            #print(line.split('|'))
            dt,acc,note,amt =line.split('|')
            #subcat[dt]=float(amt)
            month = dt.split('-')[1]
            if float(amt) > 0:
                dr=amt
                cr=0.00
            else:
                dr=0.00
                cr=amt
            balance = balance + float(amt)
            maincat.append([month,dt,acc,note,nfm(dr),nfm(cr),nfm(balance)])
    header = ['Month','Date','group','Note','Debit','Credit','Balance']
    return maincat, header

if __name__ == '__main__':
    #print(tabulate(balances(ledgerfile)))
    #print('Dues for the month of {} :'.format('May'))
    #print(tabulate(dues(ledgerfile,'May')))
    #acc,header = accounttrax(ledgerfile,'Hassan')
    print(monthlyExp(ledgerfile))
