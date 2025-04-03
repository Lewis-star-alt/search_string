from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
import string
from random import choice
import re
import logging

logging.basicConfig(level=logging.INFO)

class UserString(BaseModel):
    arr_length: int = Field(..., gt=0, le=10_000)
    arr_mode: int = Field(..., le=4, ge=1)
    ustring: str = Field(...)
    search_mode: int = Field(..., le=2, ge=1)
    regex: Optional[str] = Field(None)

app = FastAPI()

@app.post("/enter")
def get_string(ustr: UserString):
    try:
        if ustr.arr_mode == 1:
            letters = string.ascii_lowercase
        elif ustr.arr_mode == 2:
            letters = string.ascii_uppercase
        elif ustr.arr_mode == 3:
            letters = string.ascii_letters
        else:
            letters = string.ascii_letters + string.digits

        if not letters:
            raise HTTPException(status_code=500, detail="Invalid arr_mode")

        generated_str = ''.join(choice(letters) for _ in range(ustr.arr_length))

        if ustr.search_mode == 1:
            if not ustr.ustring:
                raise HTTPException(status_code=400, detail="Search string cannot be empty")
            count = generated_str.count(ustr.ustring)
        else:
            if not ustr.regex:
                raise HTTPException(status_code=400, detail="Regex is required")
            try:
                matches = re.findall(ustr.regex, generated_str)
                count = len(matches)
            except re.error as e:
                raise HTTPException(status_code=400, detail=f"Invalid regex: {str(e)}")

        stat = count / ustr.arr_length
        return {"stat": stat}

    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")
