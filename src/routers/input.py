from fastapi import APIRouter, Depends

from src.controllers.input import InputController
from src.core.database import DBManager, get_db
from src.depends import get_current_user_from_db
from src.schema.input import InputIn, InputOut
from src.schema.user import UserOut

router = APIRouter(
    prefix="/input",
    tags=[
        "input",
    ],
)


@router.post("/", description="create user inputs", response_model=InputOut)
async def create_user_input(
        data: InputIn,
        db_session: DBManager = Depends(get_db),
        current_user: UserOut = Depends(get_current_user_from_db),
) -> InputOut:
    return await InputController(db_session=db_session, current_user=current_user).create_user_input(**data.dict())


@router.get("/", description="get user inputs")
async def get_user_inputs(
        db_session: DBManager = Depends(get_db),
        current_user: UserOut = Depends(get_current_user_from_db),
) -> list[InputOut]:
    return await InputController(db_session=db_session, current_user=current_user).get_user_inputs()


@router.get("/{input_id}", description="get user input by id", response_model=InputOut)
async def get_user_input(
        input_id: int,
        db_session: DBManager = Depends(get_db),
        current_user: UserOut = Depends(get_current_user_from_db),
) -> InputOut:
    return await InputController(db_session=db_session, current_user=current_user).get_user_input(input_id=input_id)
