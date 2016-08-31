import sys

ticket_price = 2.75
bonus = 0.11
min_purchase = 10
initial_balance = float(sys.argv[1])

remaining_balance = initial_balance % ticket_price

to_purchase = 0
print(remaining_balance)
while (remaining_balance > 0.01):
    to_purchase += 1
    remaining_balance = (initial_balance + to_purchase*(1+bonus))  % ticket_price
    print("to_purchase = ", to_purchase, ", remaining_balance = %.2f" %remaining_balance)
