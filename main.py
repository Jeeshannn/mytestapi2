from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="User Identity API - Mocked ")

# -------------------------
# Mock Database
# -------------------------
IDENTITIES = []
CURRENT_USER = {"id": 1, "type": "user"}  # Simulated authenticated user
id_counter = 1

# -------------------------
# Models
# -------------------------
class UserIdentityCreate(BaseModel):
    document_name: str

class UserIdentityResponse(BaseModel):
    id: int
    user_id: int
    document_name: str
    file_name: Optional[str] = None

# -------------------------
# Endpoints
# -------------------------

@app.get("/")
def root():
    return {"message": "Mocked User Identity API running!"}

@app.post("/", response_model=UserIdentityResponse)
async def upload_identity_document(
    file: UploadFile = File(...),
    document_name: str = Form(...),
):
    global id_counter
    identity = {
        "id": id_counter,
        "user_id": CURRENT_USER["id"],
        "document_name": document_name,
        "file_name": file.filename,
    }
    id_counter += 1
    IDENTITIES.append(identity)
    return identity

@app.put("/{identity_id}", response_model=UserIdentityResponse)
async def update_identity_with_file(
    identity_id: int,
    document_name: str = Form(...),
    file: UploadFile = File(None),
):
    for identity in IDENTITIES:
        if identity["id"] == identity_id and identity["user_id"] == CURRENT_USER["id"]:
            identity["document_name"] = document_name
            if file:
                identity["file_name"] = file.filename
            return identity
    raise HTTPException(status_code=404, detail="Identity record not found")

@app.get("/{identity_id}", response_model=UserIdentityResponse)
def get_identity(identity_id: int):
    for identity in IDENTITIES:
        if identity["id"] == identity_id and identity["user_id"] == CURRENT_USER["id"]:
            return identity
    raise HTTPException(status_code=404, detail="Identity record not found")

@app.delete("/{identity_id}")
def delete_identity(identity_id: int):
    global IDENTITIES
    before = len(IDENTITIES)
    IDENTITIES = [i for i in IDENTITIES if not (i["id"] == identity_id and i["user_id"] == CURRENT_USER["id"])]
    if len(IDENTITIES) == before:
        raise HTTPException(status_code=404, detail="Identity record not found")
    return {"message": "Identity record deleted"}
