import sys

ticket_price = 2.75
bonus = 0.11
min_purchase = 10
remaining_balance_threshold = 0.01

# ticket_price = 1.75
# bonus = 0
# remaining_balance_threshold = 0.05

initial_balance = float(sys.argv[1])

remaining_balance = initial_balance % ticket_price

to_purchase = 0
print(remaining_balance)
while (remaining_balance > remaining_balance_threshold):
    to_purchase += 1
    remaining_balance = (initial_balance + to_purchase * (1 + bonus)) % ticket_price
    print("to_purchase = ", to_purchase,
          ", remaining_balance = %.2f" % remaining_balance)
