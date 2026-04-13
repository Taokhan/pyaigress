from pydantic import BaseModel, field_validator

MODEL_MAP = {
    "mistral": "mistral-small3.1:24b",
    "nomic": "nomic-embed-text",
}

class AiTest(BaseModel):
    text: str
    model: str

    @field_validator("model")
    @classmethod
    def validate_model(cls, v):
        v = v.lower().strip()
        if v not in MODEL_MAP:
            raise ValueError(f"Invalid model. Choose from: {list(MODEL_MAP.keys())}")
        return v