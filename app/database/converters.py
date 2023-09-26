from app.database.models.user import User
from app.database.models.question import Question
from app.database.models.settings import ComSubChats
from app.database.dto.user import UserDTO
from app.database.dto.question import QuestionDTO
from app.database.dto.settings import ComSubChatsDTO


def convert_user_model_to_dto(user: User) -> UserDTO:
    return UserDTO(
        user_id=user.user_id,
        first_name=user.first_name,
        last_name=user.last_name,
        language_code=user.language_code,
        is_premium=user.is_premium,
        admin=user.admin
    )


def convert_question_model_to_dto(question: Question) -> QuestionDTO:
    return QuestionDTO(
        user_message_id=question.user_message_id,
        admin_message_id=question.admin_message_id,
        answered=question.answered
    )


def convert_com_sub_chats_model_to_dto(com_sub_chats: ComSubChats) -> ComSubChatsDTO:
    return ComSubChatsDTO(
        chat_id=com_sub_chats.chat_id,
        username=com_sub_chats.username,
        turn=com_sub_chats.turn
    )
