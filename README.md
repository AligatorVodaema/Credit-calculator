# Credit calculator for loan calculations.
## Сan calculate monthly payment, amount of accrued interest and the total payout.
Requirements: Python 3.9

Without user interface.
## Usage:

1. Create venv and install 3th party packages. There is support Poetry.
2. Run python<code>$ python(your_version)</code> in directory with project.
3. Import this <code>from credit_calculators import CreditCalculatorAnnuityType, CreditCalculatorDifferentiatedType</code>.
4. Depending on your loan payment type choose <code>CreditCalculatorAnnuityType</code> or <code>CreditCalculatorDifferentiatedType</code>.
5. Put your loan details in this format <code>'amount: 100000\ninterest: 5.5%\ndownpayment: 20000\nterm: 30\n'</code> to <br>
<code>calculate = CreditCalculator"PaymentType"(your_loan_dertails)</code>.<br>
6. Call received instance <code>result = calculate()</code>. All calculations are in the resulting Dict.

## Tests:

You can use tests <code>$ python pytest</code>, in working directory.
