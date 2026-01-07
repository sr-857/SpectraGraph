from pydantic import BaseModel
import hashlib
import json


class FingerprintBase(BaseModel):
    """
    Base class for entities that require deterministic fingerprinting.
    """

    def _fingerprint_payload(self) -> dict:
        """
        Override in child classes to control fingerprint inputs.
        """
        return self.model_dump(exclude_none=True)

    def fingerprint(self) -> str:
        payload = self._fingerprint_payload()
        canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(canonical.encode("utf-8")).hexdigest()