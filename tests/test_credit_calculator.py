from credit_calculators import (CreditCalculatorAnnuityType,
                               CreditCalculatorDifferentiatedType)


def test_success_create_calc():
    """Check all expected attributes."""
    input_string = (
        'amount: 232000\ninterest: 3.7%\ndownpayment: 5000\nterm: 15\n'
    )
    calc = CreditCalculatorDifferentiatedType(user_input=input_string)
    assert calc.amount == 232000
    assert calc.interest == 3.7
    assert calc.downpayment == 5000
    assert calc.term == 15
    assert calc.payment_type == 'differentiated'


def test_annuity_monthly_payment():
    input_string = (
        'amount: 150000\ninterest: 2.9%\ndownpayment: 0\nterm: 4\n'
    )
    calc = CreditCalculatorAnnuityType(user_input=input_string)
    assert calc.calc_monthly_payment() == 3313.52
    

def test_differentiated_monthly_payment():
    input_string = (
        'amount: 111000\ninterest: 9.9%\ndownpayment: 11000\nterm: 12\n'
    )
    calc = CreditCalculatorDifferentiatedType(user_input=input_string)
    assert calc.calc_monthly_payment() == 1535.27
    
    
def test_annuity_total_payout():
    input_string = (
        'amount: 150000\ninterest: 2.9%\ndownpayment: 0\nterm: 4\n'
    )
    calc = CreditCalculatorAnnuityType(user_input=input_string)
    assert calc.clac_total_payout() == 159048.96
    
    
def test_differentiated_total_payout():
    input_string = (
        'amount: 111000\ninterest: 9.9%\ndownpayment: 11000\nterm: 12\n'
    )
    calc = CreditCalculatorDifferentiatedType(user_input=input_string)
    assert calc.clac_total_payout() == 159806.84
    
    
def test_amount_of_accrued_interest():
    input_string = (
        'amount: 100000\ninterest: 5.5%\ndownpayment: 20000\nterm: 30\n'
    )
    calc = CreditCalculatorDifferentiatedType(user_input=input_string)
    assert calc.calc_amount_of_accrued_interest() == 66180.76
    

def test_call_all_calculations():
    input_string = (
        'amount: 100000\ninterest: 5.5%\ndownpayment: 20000\nterm: 1\n'
    )
    calc = CreditCalculatorAnnuityType(user_input=input_string)
    result_dict = calc()
    assert result_dict['monthly_payment'] == 6866.94
    assert result_dict['total_payout'] == 82403.28
    assert result_dict['amount_of_accrued_interest'] == 2403.28
