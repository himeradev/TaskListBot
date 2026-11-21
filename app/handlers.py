import asyncio
from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

import app.keyboards as kb
from db.executors import *

rt = Router()

class Edit(StatesGroup):
    add = State()
    remove = State()

@rt.message(CommandStart())
async def start(message: Message):
    txt = (
        "💠 Добро пожаловать в бот!\n"
        "– Данный бот создан для сохранения планов/задач.\n"
        "\n"
        "🔽 Используй меню ниже, чтобы управлять списком планов."
    )
    
    await message.answer(
        txt,
        parse_mode="HTML",
        reply_markup=kb.start
    )
    
@rt.callback_query(F.data == "create")
async def create(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    
    txt = (
        "⌨️ Введите <b>название/суть</b> плана или задачи:"
    )
    
    await callback.message.answer(
        text=txt,
        parse_mode="HTML"
    )
    
    await state.set_state(Edit.add)
    
@rt.message(Edit.add)
async def create_text(message: Message, state: FSMContext):
    title = message.text
    
    result = await add_task(title)
    
    if result == True:
        await message.answer(
            "✅ Задача успешно добавлена!"
        )
    else:
        await message.answer(
            "🚫 Произошла ошибка при создании задачи."
        )
    
    await state.clear()
    
@rt.callback_query(F.data == "tasks")
async def tasks(callback: CallbackQuery):
    await callback.answer()

    task_list = await get_tasks()

    if not task_list:
        txt = "🚫 У вас нет ни одного плана.\n\n⚡️ Для удаления или добавления плана используйте кнопки ниже."
    else:
        txt = (
            "💠 Текущие планы:\n\n"
            "<i>Формат: АЙДИ | ПЛАН</i>\n\n"
        )

        for task in task_list:
            t_id = task["id"]
            title = task["task"]
            txt += f"<b>{t_id} | {title}</b>\n"

        txt += "\n⚡️ Для удаления или добавления плана используйте кнопки ниже."

    await callback.message.answer(
        txt,
        parse_mode="HTML",
        reply_markup=kb.edit
    )

@rt.callback_query(F.data == "remove")
async def remove(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    
    await callback.message.answer("⌨️ Введите айди плана (число) для удаления:")
    
    await state.set_state(Edit.remove)
    
@rt.message(Edit.remove)
async def remove_id(message: Message, state: FSMContext):
    id = int(message.text)
    
    result = await remove_task(id)
    
    if result == True:
        await message.answer(
            "✅ Задача успешно удалена!"
        )
    else:
        await message.answer(
            "🚫 Произошла ошибка при удалении задачи."
        )
    
    await state.clear()