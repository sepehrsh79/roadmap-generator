from fastapi import BackgroundTasks

from src.core.database import DBManager
from src.crud.input import InputCRUD
from src.repository.chatGPT import create_roadmap_in_background
from src.schema.input import InputOut

from src.schema.user import UserOut


class InputController:
    input_crud = InputCRUD()

    def __init__(
        self,
        db_session: DBManager,
        current_user: UserOut,
        background_tasks: BackgroundTasks | None = None,
        input_crud: InputCRUD | None = None,
    ):
        self.input_crud = input_crud or self.input_crud
        self.db_session = db_session
        self.current_user = current_user
        self.background_tasks = background_tasks

    async def create_user_input(self, **kwargs) -> InputOut:
        input = await self.input_crud.create(**kwargs, db_session=self.db_session, user_id=self.current_user.id)
        assert input is not None
        self.background_tasks.add_task(create_roadmap_in_background, input=input,
                                       user_id=self.current_user.id,
                                       db_session=self.db_session
                                       )
        # await create_roadmap_in_background(
        #     input = input,
        #     user_id = self.current_user.id,
        #     db_session = self.db_session
        # )
        return InputOut.from_orm(input)

    async def get_user_input(self, input_id: int) -> InputOut:
        input = await self.input_crud.get_by_id(self.db_session, input_id=input_id, user_id=self.current_user.id)
        assert input is not None
        return InputOut.from_orm(input)

    async def get_user_inputs(self) -> list[InputOut]:
        inputs = await self.input_crud.get_query(self.db_session, user_id=self.current_user.id)
        input_out_list = [InputOut.from_orm(input_instance) for input_instance in inputs]
        return input_out_list
