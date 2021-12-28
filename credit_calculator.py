import calendar
import datetime as dt
from typing import Tuple, Union

from serializers import InputSerializer, InputSerializerError
            

class CreditCalculator:
    
    PAYMENT_TYPES = {
        'ann': 'annuity',
        'dif': 'differentiated'
    }
    def __init__(self, user_input: str, payment_type: str = 'ann') -> None:
        """Parse user input string and save it."""
        parsed_data = InputSerializer(user_input).parse_input()

        self.payment_type = self.PAYMENT_TYPES[payment_type]
        self.amount = parsed_data['amount']
        self.interest = parsed_data['interest']
        self.downpayment = parsed_data['downpayment']
        self.term = parsed_data['term']
        return None
    
    def calc_monthly_payment(self) -> float:
        """Calculate monthly loan payment.
        
        Depending on the type of loan payment.
        """
        if self.payment_type == self.PAYMENT_TYPES['ann']:
            result = self.annuity_payment_type()
            
        elif self.payment_type == self.PAYMENT_TYPES['dif']:
            main_debt = self.amount - self.downpayment
            now = dt.datetime.now()
            days_in_current_month = calendar.monthrange(now.year, now.month)[1]
            
            result = self.differentiated_payment_type(
                days_in_current_month=days_in_current_month,
                main_debt=main_debt
            )
        else:
            raise InputSerializerError(
                'Input "ann" for annuity payment type,\n'
                'or "dif" for differentiated payment type.'
            )
        return result
    
    def calc_amount_of_accrued_interest(self) -> float:
        """Calculate amount of accrued interest.
        
        The difference between the total amount of the payment
        and the body of the loan.
        """
        return round(
            self.clac_total_payout() - (self.amount - self.downpayment), 2
        )
    
    def clac_total_payout(self) -> float:
        """Calculate the total payout.
        
        Depending on the type of loan payment.
        """
        print(f'{self.payment_type=}')
        
        if self.payment_type == 'annuity':
            monthly_payment = self.annuity_payment_type()
            total_payout = monthly_payment * (self.term * 12)
        
        now = dt.datetime.now().month - 1
        default_months_order = calendar.mdays[:]
        default_months_order.remove(0)
        previous_months = default_months_order[:now]
        future_months = default_months_order[now:]
        current_months_order = future_months + previous_months
        
        main_debt = self.amount - self.downpayment
        principal_balance = main_debt / (self.term * 12)
        total_payout = 0
        for _ in range(self.term):
            for month in current_months_order:
                total_payout += self.differentiated_payment_type(
                    month, main_debt
                )
                main_debt -= principal_balance
                
        return round(total_payout, 2)

    def annuity_payment_type(self) -> float:
        """Calculate a one-time annuity payment."""
        credit_amount = self.amount - self.downpayment
        monthly_interest = self.interest / 12 / 100
        term_in_months = self.term * 12
        
        annuity_rate = (
            monthly_interest * (1 + monthly_interest)**term_in_months /
            ((1 + monthly_interest)**term_in_months - 1)
        )
        return round(annuity_rate * credit_amount, 2)
    
    def differentiated_payment_type(
        self,
        days_in_current_month: int,
        main_debt: Union[int, float]
    ) -> float:
        """Calculate a one-time differentiated payment."""
        now = dt.datetime.now()
        days_in_current_year = 365
        if calendar.isleap(now.year):
            days_in_current_year = 366
        
        differentiated_interest = (
            main_debt * (self.interest / 100) * 
            days_in_current_month / days_in_current_year
        )
        
        term_in_months = self.term * 12
        monthly_body_debt = (self.amount - self.downpayment) / term_in_months
        return round(monthly_body_debt + differentiated_interest, 2)
        
    def __call__(self) -> Tuple:
        """Calculate complete information on the loan.
        
        Returns tuple with: Monthly loan payment,
        the total payout, amount of accrued interest.
        """
        monthly_payment = self.calc_monthly_payment()
        total_payout = self.clac_total_payout()
        amount_of_accrued_interest = self.calc_amount_of_accrued_interest()
        return (
            monthly_payment,
            total_payout,
            amount_of_accrued_interest
        )
    
    
if __name__ == '__main__':
    calc1 = CreditCalculator(
        'amount: 100000\ninterest: 5.5%\ndownpayment: 20000\nterm: 30\n',
        'dif'
    )
    print(calc1())
    
    
    calc2 = CreditCalculator(
        'amount: 100000\ninterest: 5.5%\ndownpayment: 20000\nterm: 1\n',
        payment_type='ann'
    )
    print(calc2())
