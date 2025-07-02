from abc import ABC, abstractmethod
from decimal import Decimal


class EmailSenderInterface(ABC):

    @abstractmethod
    async def send_activation_email(self, email: str, activation_link: str) -> None:
        pass

    @abstractmethod
    async def send_activation_complete_email(self, email: str, login_link: str) -> None:
        pass

    @abstractmethod
    async def send_password_reset_email(self, email: str, reset_link: str) -> None:
        pass

    @abstractmethod
    async def send_password_reset_complete_email(
        self, email: str, login_link: str
    ) -> None:
        pass

    @abstractmethod
    async def send_password_change(self, email: str) -> None:
        pass

    @abstractmethod
    async def send_remove_movie(
        self, email: str, movie_name: str, cart_id: int
    ) -> None:
        pass

    @abstractmethod
    async def send_comment_answer(self, email: str, answer_text: str) -> None:
        pass

    @abstractmethod
    async def send_payment_email(self, email: str, amount: Decimal) -> None:
        pass

    @abstractmethod
    async def send_refund_email(self, email: str, amount: Decimal) -> None:
        pass

    @abstractmethod
    async def send_cancellation_email(self, email: str, amount: Decimal) -> None:
        pass
