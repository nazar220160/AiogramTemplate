from src.database.models.user import User
from src.database.models.question import Question
from src.database.models.settings import ComSubChats
from src.common.dto.user import UserDTO
from src.common.dto.question import QuestionDTO
from src.common.dto.settings import ComSubChatsDTO


def convert_user_model_to_dto(model: User) -> UserDTO:
    questions = []
    if 'questions' in model.as_dict():
        questions = [convert_question_model_to_dto(model) for model in model.questions]

    return UserDTO(
        user_id=model.user_id,
        first_name=model.first_name,
        last_name=model.last_name,
        language_code=model.language_code,
        is_premium=model.is_premium,
        admin=model.admin,

        questions=questions,

        created_at=model.created_at,
        updated_at=model.updated_at
    )


def convert_question_model_to_dto(model: Question) -> QuestionDTO:
    user = None
    if 'user' in model.as_dict():
        user = convert_user_model_to_dto(model.user)

    return QuestionDTO(
        id=model.id,
        user_message_id=model.user_message_id,
        admin_message_id=model.admin_message_id,
        status=model.status,
        user_id=model.user_id,

        user=user,

        created_at=model.created_at,
        updated_at=model.updated_at
    )


def convert_com_sub_chats_model_to_dto(model: ComSubChats) -> ComSubChatsDTO:
    return ComSubChatsDTO(
        chat_id=model.chat_id,
        username=model.username,
        turn=model.turn
    )
