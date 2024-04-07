import json
import os
from typing import Optional, List

from fastapi import FastAPI, Body, HTTPException, status, Request
# from fastapi.responses import Response
from pydantic import ConfigDict, BaseModel, Field
from pydantic.functional_validators import BeforeValidator

from typing_extensions import Annotated

from bson import ObjectId
import motor.motor_asyncio
from pymongo import ReturnDocument
from uuid import uuid4

app = FastAPI(
    title="Student Course API",
    summary="A sample application showing how to use FastAPI to add a ReST API to a MongoDB collection.",
)
client = motor.motor_asyncio.AsyncIOMotorClient(
    "mongodb+srv://aman:test123@cluster0.fuocuqz.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

db = client.library
student_collection = db.get_collection("students")

PyObjectId = Annotated[str, BeforeValidator(str)]


class Address(BaseModel):
    city: str
    country: Optional[str]


class StudentModel(BaseModel):
    """
    SStructure for a single student record.
    """
    id: str = uuid4().hex
    name: str = Field(...)
    age: int = Field(...)
    address: Optional[Address] = None
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "name": "Aman",
                "age": 25,
                "address": {
                    "city": "Jaipur",
                    "country": "India"
                }
            }
        },
    )


class UpdateStudentModel(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    address: Optional[dict] = None
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        json_schema_extra={
            "example": {
                "name": "Aman",
                "age": 25,
                "address": {
                    "city": "Jaipur",
                    "country": "India"
                }
            }
        },
    )


class StudentCollection(BaseModel):
    students: List[StudentModel]


@app.post(
    "/students/",
    response_description="Add new student",
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
async def create_student(student: StudentModel = Body(...)):
    """
    Inserting a new student record if it does not exist.
    A unique `id` will be created and provided in the response.
    """
    stud_detail = await student_collection.find_one(
        {"name": student.name}
    )
    response = dict()
    print("stud_detail : ", stud_detail)
    if stud_detail:
        response["response"] = "Record already exist"
    else:
        new_student = await student_collection.insert_one(
            student.model_dump(by_alias=True, exclude=["_id"])
        )
        projection = {"_id": 0}
        print("new_student.inserted_id : ", new_student.inserted_id)
        print("new_student.inserted_id : ", type(student.id))
        created_student = await student_collection.find_one(
            {"id": student.id}, projection=projection
        )
        print("created_student : ", created_student)
        if created_student:
            response["response"] = student.id
        else:
            response["response"] = "Record not created successfully"
    return response


@app.get(
    "/students/",
    response_description="List all students",
    response_model_by_alias=False,
)
async def list_students(request: Request):
    headers = request.headers
    country = headers.get("country")
    age = headers.get("age")
    projection = {"_id": 0}
    student_list = await student_collection.find(projection=projection).to_list(1000)
    if country:
        student_list = [student for student in student_list if student["address"]["city"] == country]
    if age is not None:
        student_list = [student for student in student_list if int(student["age"]) >= int(age)]

    response = {"response": student_list}
    return response


@app.get(
    "/students/{id}",
    response_description="Get a single student",
    response_model=StudentModel,
    response_model_by_alias=False,
)
async def show_student(id: str):
    if (
            student := await student_collection.find_one({"id": id})
    ) is not None:
        return student

    raise HTTPException(status_code=404, detail=f"Student {id} not found")


@app.patch(
    "/students/{id}",
    response_description="Update a student",
    response_model_by_alias=False,
)
async def update_student(id: str, student: UpdateStudentModel = Body(...)):
    """
    Update individual fields of an existing student record.

    Only the provided fields will be updated.
    Any missing or `null` fields will be ignored.
    """
    filtered_data = {}

    # filtered_data = {}
    for key, value in student.model_dump(by_alias=True).items():
        if value is not None:
            if key == "address":
                for k, v in value.items():
                    if k == "city":
                        filtered_data["address.city"] = v
                    if k == "country":
                        filtered_data["address.country"] = v
            else:
                filtered_data[key] = value

    if len(filtered_data) >= 1:
        update_result = await student_collection.find_one_and_update(
            {"id": id},
            {"$set": filtered_data},
            projection={"_id": 0},
            return_document=ReturnDocument.AFTER,
        )
        print("update_result ", update_result)
        if update_result is not None:
            return update_result
        else:
            raise HTTPException(status_code=404, detail=f"Student {id} not found")

    # The update is empty, but we should still return the matching document:
    if (existing_student := await student_collection.find_one({"id": id})) is not None:
        return existing_student

    raise HTTPException(status_code=404, detail=f"Student {id} not found")


@app.delete("/students/{id}", response_description="Delete a student")
async def delete_student(id: str):
    """
    Remove a single student record from the database.
    """
    delete_result = await student_collection.delete_one({"id": id})

    if delete_result.deleted_count == 1:
        return {}

    raise HTTPException(status_code=404, detail=f"Student {id} not found")