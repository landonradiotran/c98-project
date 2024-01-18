from flask import Flask, render_template, request, redirect
import os
from time import time
from wallet import Account, Wallet

STATIC_DIR = os.path.abspath('static')

app = Flask(__name__, static_folder=STATIC_DIR)
app.use_static_for_root = True

account = Account()
myWallet =  Wallet()

@app.route("/", methods= ["GET", "POST"])
def index():
    global account, myWallet
      
    isConnected = myWallet.checkConnection()
    balance = "No Balance"
    if(account):
        balance = myWallet.getBalance(account.address)

    return render_template('index.html', isConnected=isConnected,  account= account, balance = balance)

   
@app.route('/transactions')
def transactions():
    global account, myWallet    

    transactions = None

    # Call getTransactions() method and pass it account.address and store the result in transactions variable
    transactions=myWallet.getTransactions(account.address)

    # Pass transaction as transaction attribute
    return render_template('transactions.html', account=account, transactions= {})

@app.route("/makeTransaction", methods = ["GET", "POST"])
def makeTransaction():
    global myWallet, account

    sender = request.form.get("senderAddress")
    receiver = request.form.get("receiverAddress")
    amount = request.form.get("amount")

    senderType = 'ganache'
    if(sender == account.address):
        senderType = 'newAccountAddress'

    tnxHash= myWallet.makeTransactions(sender, receiver, amount, senderType, account.privateKey)
    myWallet.addTransactionHash(tnxHash, sender, receiver, amount)
    return redirect("/")

if __name__ == '__main__':
    app.run(debug = True, port=4000)
