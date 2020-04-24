import sys

if len(sys.argv) >= 2:
    old_principal = sys.argv[1]
else:
    print('Enter previous principal in dollars')
    old_principal = input()
old_principal = float(old_principal)

if len(sys.argv) >= 3:
    r = sys.argv[2]
else:
    print('Enter interest rate on the loan per year in percentage (ex:- enter 4 if the interest rate on the loan is 4%)')
    r = input()
r = float(r)

if len(sys.argv) >= 4:
    M = sys.argv[3]
else:
    print('Enter monthly payment (without taxes) in dollars')
    M = input()
M = float(M)

interest_paid = old_principal * (r / 12.0 / 100)
principal_paid = M - interest_paid
new_principal = old_principal - principal_paid
print('{:.2f}'.format(new_principal))
