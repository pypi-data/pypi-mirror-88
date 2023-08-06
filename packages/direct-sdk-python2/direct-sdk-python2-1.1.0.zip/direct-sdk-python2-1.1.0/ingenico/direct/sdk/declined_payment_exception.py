from declined_transaction_exception import DeclinedTransactionException


class DeclinedPaymentException(DeclinedTransactionException):
    """
    Represents an error response from a create payment call.
    """

    def __init__(self, status_code, response_body, error_response):
        if error_response is not None:
            super(DeclinedPaymentException, self).__init__(status_code,
                                                           response_body,
                                                           error_response.error_id,
                                                           error_response.errors,
                                                           DeclinedPaymentException.__create_message(error_response))
        else:
            super(DeclinedPaymentException, self).__init__(status_code,
                                                           response_body,
                                                           None, None,
                                                           DeclinedPaymentException.__create_message())
        self.__error_response = error_response

    @staticmethod
    def __create_message(error_response=None):
        if error_response is not None and error_response.payment_result is not None:
            payment = error_response.payment_result.payment
        else:
            payment = None
        if payment is not None:
            return "declined payment '" + payment.id + "' with status '" + payment.status + "'"
        else:
            return "the Ingenico ePayments platform returned a declined payment response"

    @property
    def create_payment_result(self):
        """
        :return: The result of creating a payment if available, otherwise None.
        """
        if self.__error_response is None:
            return None
        else:
            return self.__error_response.payment_result
