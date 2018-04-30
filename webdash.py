import web
import dashboard as ds

#ledgerfile = 'myledger'

urls = ('/', 'index',
        '/trax/(.*)', 'trax',
        '/dues/(.*)', 'dues',
        '/balance/(.*)','balance',
        '/mexp/','mexp')
        
render = web.template.render('templates')

class index:
    def GET(self,balsheet = None):
        balsheet = ds.balancesheet(ds.ledgerfile)
        #balsheetacc = ds.getaccounts(ds.ledgerfile,
        income,expenses,profit = ds.incomestat(ds.ledgerfile)
        cm = ds.currentmonth
        nm = ds.getnextmonth()
        currentdues = ds.dues(ds.ledgerfile, cm)
        nextdues = ds.dues(ds.ledgerfile, nm)
        return render.index(balsheet,income,expenses,profit,currentdues,nextdues)

class trax:
    def GET(self, account=''):
        account = web.input( saccount = 'web')
        result, hd = ds.accounttrax(ds.ledgerfile ,web.websafe(account.saccount))
        return render.trax(account = result)

class dues:
    def GET(self, mon='May'):
        cm = ds.currentmonth
        nm = ds.getnextmonth()
        currentdues = ds.dues(ds.ledgerfile, cm)
        nextdues = ds.dues(ds.ledgerfile, nm)
        return render.dues(currentdues, nextdues)

class balance:
    def GET(self, account=''):
        bal = ds.balances(ds.ledgerfile,account)
        return render.balance(bal)

class mexp:
    def GET(self, mexpenses=None, expacc=None,months= None,account = None):
        account = web.input( saccount = 'web')
        expacc = ds.getaccounts(ds.ledgerfile, '{}'.format(web.websafe(account.saccount)))
        mexpenses = ds.monthlyExp(ds.ledgerfile,'{}'.format(web.websafe(account.saccount)))
        months = ds.months
        newdict = dict()
        for ac in expacc:
            accounttotal = 0.00
            for m in mexpenses.keys():
                
                if ac in mexpenses[m].keys():
                    accounttotal = float(mexpenses[m][ac].replace(',','')) + accounttotal
                    #print(accounttotal)
            if len(str(accounttotal)) > 0:
                newdict[ac]= ds.nfm(accounttotal)
                mexpenses['Total']=newdict
                #print(accounttotal)
        return render.mexp(mexpenses,expacc, months)
            
if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
