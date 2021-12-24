from serializers import InputSerializer
            

class CreditCalculator:
    
    PAYMENT_TYPES = {
        'ann': 'annuity',
        'dif': 'differentiated'
    }
    def __init__(self, user_input, payment_type='ann'):
        parsed_data = InputSerializer(user_input).parse_input()

        self.payment_type = self.PAYMENT_TYPES[payment_type]
        self.amount = parsed_data['amount']
        self.interest = parsed_data['interest']
        self.downpayment = parsed_data['downpayment']
        self.term = parsed_data['term']
        return None
    
    def calc_monthly_payment(self):
        """Месячная выплата по кредиту."""
        self.payment_type
        
        pass
    
    def calc_amount_of_accrued_interest(self):
        """Общий объём начисленных процентов."""
        pass
    
    def clac_total_payout(self):
        """Общая сумма выплаты."""
        pass

    def annuity_payment_type(self):
        pass
    
    def differentiated_payment_type(self):
        pass
    
    def __call__(self, *args, **kwargs):
        # Call three methods
        pass
    
    
if __name__ == '__main__':
    pass
