import calendar
import datetime as dt
from typing import Union
import os
import sys

from loguru import logger

from base_credit_calculator import BaseCreditCalculator

CURRENT_DIR = os.path.dirname(__file__)

logger.remove()
logger.add(
    CURRENT_DIR + '/logs/input_output.log',
    level='SUCCESS',
    rotation='24h'
)
logger.add(sys.stdout, level='INFO')


class CreditCalculatorAnnuityType(BaseCreditCalculator):
    """Class loan calculator for annuity type payment."""
    def __init__(self, user_input: str) -> None:
        super().__init__(user_input, 'annuity')
        return None
    
    def calc_monthly_payment(self) -> float:
        """Calculate monthly loan payment."""
        credit_amount = self.amount - self.downpayment
        monthly_interest = self.interest / 12 / 100
        term_in_months = self.term * 12
        
        annuity_rate = (
            monthly_interest * (1 + monthly_interest)**term_in_months
            / ((1 + monthly_interest)**term_in_months - 1)
        )
        return round(annuity_rate * credit_amount, 2)
    
    def clac_total_payout(self) -> float:
        """Calculate the total payout."""
        monthly_payment = self.calc_monthly_payment()
        total_payout = monthly_payment * (self.term*12)
        return round(total_payout, 2)
        

class CreditCalculatorDifferentiatedType(BaseCreditCalculator):
    """Class loan calculator for differentiated type payment."""
    def __init__(self, user_input: str) -> None:
        super().__init__(user_input, 'differentiated')
        return None
    
    def calc_monthly_payment(self) -> float:
        """Calculate monthly loan payment."""
        main_debt = self.amount - self.downpayment
        now = dt.datetime.now()
        days_in_current_month = calendar.monthrange(
            now.year, now.month
        )[1]
        return self._differentiated_payment_type(
            days_in_current_month=days_in_current_month,
            main_debt=main_debt
        )

    def clac_total_payout(self) -> float:
        """Calculate the total payout."""
        now = dt.datetime.now().month - 1
        default_months_order = calendar.mdays[:]
        default_months_order.remove(0)
        previous_months = default_months_order[:now]
        future_months = default_months_order[now:]
        current_months_order = future_months + previous_months
        
        self.main_debt = self.amount - self.downpayment
        self.principal_balance = self.main_debt / (self.term*12)
        
        total_payout = sum(
            sum(self._calc_next_differentiated_payment(month) 
                for month in current_months_order)
            for year in range(self.term)
        )
        return round(total_payout, 2)

    def _calc_next_differentiated_payment(self, month: int) -> float:
        """Calculate next differentiated monthly payment.
        
        Based on the main debt paid.
        """
        result = self._differentiated_payment_type(month, self.main_debt)
        self.main_debt -= self.principal_balance
        return result

    def _differentiated_payment_type(
            self,
            days_in_current_month: int,
            main_debt: Union[int, float]
    ) -> float:
        """Calculate a one-time differentiated payment."""
        now = dt.datetime.now()
        days_in_current_year = 366 if calendar.isleap(now.year) else 365
        
        differentiated_interest = (
            main_debt * (self.interest/100)
            * days_in_current_month / days_in_current_year
        )
        
        term_in_months = self.term * 12
        monthly_body_debt = (self.amount-self.downpayment) / term_in_months
        return round(monthly_body_debt + differentiated_interest, 2)

    
if __name__ == '__main__':
    calc1 = CreditCalculatorDifferentiatedType(
        'amount: 100000\ninterest: 5.5%\ndownpayment: 20000\nterm: 30\n'
    )
    print(calc1())
    
    calc2 = CreditCalculatorAnnuityType(
        'amount: 100000\ninterest: 5.5%\ndownpayment: 20000\nterm: 1\n'
    )
    print(calc2())
