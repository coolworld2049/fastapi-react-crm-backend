from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession


from backend.app import crud, schemas
from backend.app.api import deps
from backend.app.db import models
from backend.app.schemas.request_params import RequestParams

router = APIRouter()


# noinspection PyUnusedLocal
@router.get("/", response_model=List[schemas.TaskStudent])
async def read_task_students(
        response: Response,
        db: AsyncSession = Depends(deps.get_db),
        current_user: models.TaskStudent = Depends(deps.get_current_active_user),
        request_params: RequestParams = Depends(deps.parse_react_admin_params(models.TaskStudent))
) -> Any:
    """
    Retrieve Tasks.
    """
    items, total = await crud.task_student.get_multi(db, request_params=request_params)
    response.headers["Content-Range"] = f"{request_params.skip}-{request_params.skip + len(items)}/{total}"
    return items


# noinspection PyUnusedLocal
@router.post("/", response_model=schemas.TaskStudent)
async def create_task_student(
        *,
        db: AsyncSession = Depends(deps.get_db),
        item_in: schemas.TaskStudentCreate,
        current_user: models.TaskStudent = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new task.
    """
    item = await crud.task_student.create(db=db, obj_in=item_in)
    return item


# noinspection PyUnusedLocal
@router.put("/{id}", response_model=schemas.TaskStudent)
async def update_task_student_id(
        *,
        db: AsyncSession = Depends(deps.get_db),
        id: int,
        item_in: schemas.TaskStudentUpdate,
        current_user: models.TaskStudent = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an task.
    """
    item = await crud.task_student.get(db=db, id=id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    item = await crud.task_student.update(db=db, db_obj=item, obj_in=item_in)
    return item


# noinspection PyUnusedLocal
@router.get("/{id}", response_model=schemas.TaskStudent)
async def read_task_student_id(
        *,
        db: AsyncSession = Depends(deps.get_db),
        id: int,
        current_user: models.TaskStudent = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get task by ID.
    """
    item = await crud.task_student.get(db=db, id=id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


# noinspection PyUnusedLocal
@router.delete("/{id}", response_model=schemas.TaskStudent)
async def delete_task_student_id(
        *,
        db: AsyncSession = Depends(deps.get_db),
        id: int,
        current_user: models.TaskStudent = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an task.
    """
    item = await crud.task_student.get(db=db, id=id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    if item.status != 'completed':
        raise HTTPException(status_code=404, detail="Uncompleted task cannot be removed")
    item = await crud.task_student.remove(db=db, id=id)
    return item
