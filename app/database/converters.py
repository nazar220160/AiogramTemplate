from app.database.models.user import User
from app.database.models.question import Question
from app.database.dto.user import UserDTO
from app.database.dto.question import QuestionDTO


def convert_user_model_to_dto(user: User) -> UserDTO:
    return UserDTO(
        user_id=user.user_id,
        is_bot=user.is_bot,
        first_name=user.first_name,
        last_name=user.last_name,
        language_code=user.language_code,
        is_premium=user.is_premium,
        added_to_attachment_menu=user.added_to_attachment_menu,
        can_join_groups=user.can_join_groups,
        can_read_all_group_messages=user.can_read_all_group_messages,
        supports_inline_queries=user.supports_inline_queries
    )


def convert_question_model_to_dto(question: Question) -> QuestionDTO:
    return QuestionDTO(
        user_message_id=question.user_message_id,
        admin_message_id=question.admin_message_id,
        answered=question.answered
    )
