from pydantic import BaseModel, Field, model_validator
from app.services.config_loader import load_policy


class Brakes(BaseModel):
    needs_review_band: list[float] = Field(min_length=2, max_length=2)
    suspect_conf_threshold: float = Field(ge=0, le=1)
    high_weight_threshold: float = Field(ge=0, le=1)
    fuzzy_ratio: float = Field(ge=0, le=1, default=0.85)


class Loop(BaseModel):
    max_steps: int = Field(ge=1)
    retries: int = Field(ge=0)


class Policy(BaseModel):
    version: str
    thresholds: dict[str, float]
    weights: dict[str, float]
    caps: dict[str, float]
    brakes: Brakes
    loop: Loop

    @model_validator(mode="after")
    def _constrain_probabilities(self) -> "Policy":
        for table in (self.thresholds, self.weights, self.caps):
            for value in table.values():
                if not 0 <= value <= 1:
                    raise ValueError(
                        "policy values must be within [0, 1], got {value}"
                    )
        return self


def load_policy_typed() -> Policy:
    return Policy(**load_policy())