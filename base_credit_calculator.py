from abc import ABC, abstractmethod
from typing import Dict

from loguru import logger

from serializers import InputSerializer


class BaseCreditCalculator(ABC):
    """Base class for loan calculations."""
    def __init__(self, user_input: str, payment_type: str = 'annuity') -> None:
        """Parse user input string and save it."""
        parsed_data = InputSerializer(user_input).parse_input()

        self.payment_type = payment_type
        logger.info(f'Payment type is: {self.payment_type}.')
        self.amount = parsed_data['amount']
        self.interest = parsed_data['interest']
        self.downpayment = parsed_data['downpayment']
        self.term = parsed_data['term']
        return None
    
    def calc_amount_of_accrued_interest(self) -> float:
        """Calculate amount of accrued interest.
        
        The difference between the total amount of the payment
        and the body of the loan.
        """
        return round(
            self.clac_total_payout() - (self.amount - self.downpayment), 2
        )
        
    @abstractmethod
    def calc_monthly_payment(self) -> float:
        """Calculate monthly loan payment."""
        pass
    
    @abstractmethod
    def clac_total_payout(self) -> float:
        """Calculate the total payout."""
        pass
    
    def __call__(self) -> Dict:
        """Calculate complete information on the loan.
        
        Returns dict with values: Payment type, monthly loan payment,
        the total payout, amount of accrued interest.
        """
        monthly_payment = self.calc_monthly_payment()
        total_payout = self.clac_total_payout()
        amount_of_accrued_interest = self.calc_amount_of_accrued_interest()
        result = {
            'payment_type': self.payment_type,
            'monthly_payment': monthly_payment,
            'total_payout': total_payout,
            'amount_of_accrued_interest': amount_of_accrued_interest
        }
        logger.success('All calculations result: {}.', result)
        return result
    