from datetime import datetime

from fastapi import APIRouter, Depends

from src.constants import ChatRole, HTTPMethod
from src.core.models import (
    ChatRequestDTO, ChatResponseDTO, ChatMessageDTO
)
from src.core.services.llm import LLMService
from src.data.storage.dialogs.base import Storage
from src.dependencies import get_llm_service, get_active_data_storage
from src.utils import report_error


async def chat_message(
        request: ChatRequestDTO,
        llm_service: LLMService = Depends(get_llm_service),
        storage: Storage = Depends(get_active_data_storage),
) -> ChatResponseDTO:
    """
    Processes incoming request,
    use AI model to generate response,
    and returns the response.
    :param request:
    :param storage:
    :return:
    """

    # Create ChatMessageDTO object
    try:
        user_message = ChatMessageDTO(
            session_id=request.session_id,
            role=ChatRole.USER,
            timestamp=datetime.now().timestamp(),
            content=request.content
        )
        await storage.save_message(user_message)
    except Exception as e:
        report_error(str(e))

    # Forward request to LLM
    response_text = await llm_service.generate(
        request.session_id,
        request.content,
    )

    try:
        system_message = ChatMessageDTO(
            session_id=request.session_id,
            role=ChatRole.SYSTEM,
            timestamp=datetime.now().timestamp(),
            content=response_text
        )
        await storage.save_message(system_message)
    except Exception as e:
        report_error(str(e))

    return ChatResponseDTO(
        session_id=request.session_id,
        content=response_text
    )


router = APIRouter()

router.add_api_route(
    "/message",
    endpoint=chat_message,
    methods=[HTTPMethod.POST],
    summary="Processes single chat message"
)
