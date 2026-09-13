from __future__ import annotations

import random
from typing import Any

from noesis.adapters.base import UnsupportedRepresentationSite
from noesis.domain.models import AdapterCapabilities, CaptureRequest, CaptureResult, ModelIdentity


class HuggingFaceAdapter:
    """Reference adapter for open-weight Transformer models."""

    def __init__(self, model_id: str, revision: str = "main", device: str = "cpu") -> None:
        try:
            import torch
            import transformers
            from transformers import AutoModel, AutoTokenizer
        except ImportError as exc:  # pragma: no cover
            raise RuntimeError("Install noesis-latent[hf] to use HuggingFaceAdapter") from exc
        self._torch = torch
        self._transformers_version = transformers.__version__
        self._tokenizer = AutoTokenizer.from_pretrained(model_id, revision=revision)
        self._model = AutoModel.from_pretrained(model_id, revision=revision).to(device)
        self._model.eval()
        self._device = device
        self._identity = ModelIdentity(model_id=model_id, revision=revision, tokenizer_revision=revision)
        self._capabilities = AdapterCapabilities(frozenset({"embedding", "hidden_state"}))

    @property
    def identity(self) -> ModelIdentity:
        return self._identity

    @property
    def capabilities(self) -> AdapterCapabilities:
        return self._capabilities

    def _seed(self, seed: int) -> None:
        random.seed(seed)
        self._torch.manual_seed(seed)
        if self._torch.cuda.is_available():
            self._torch.cuda.manual_seed_all(seed)

    def capture(self, request: CaptureRequest) -> CaptureResult:
        if not self.capabilities.supports(request.site):
            raise UnsupportedRepresentationSite(request.site.key())
        self._seed(request.seed)
        encoded: dict[str, Any] = self._tokenizer(request.text, return_tensors="pt")
        encoded = {key: value.to(self._device) for key, value in encoded.items()}
        with self._torch.inference_mode():
            outputs = self._model(**encoded, output_hidden_states=True, return_dict=True)
        site = request.site
        if site.kind == "embedding":
            tensor = self._model.get_input_embeddings()(encoded["input_ids"])[0, site.token_index]
        elif site.kind == "hidden_state":
            hidden_states = outputs.hidden_states
            if hidden_states is None:
                raise RuntimeError("model did not return hidden states")
            try:
                tensor = hidden_states[site.layer][0, site.token_index]
            except (IndexError, TypeError) as exc:
                raise UnsupportedRepresentationSite(site.key()) from exc
        else:  # guarded above; retained fail closed
            raise UnsupportedRepresentationSite(site.key())
        vector = tuple(float(x) for x in tensor.detach().cpu().to(self._torch.float64).tolist())
        return CaptureResult(
            request=request,
            model=self.identity,
            vector=vector,
            runtime_metadata={
                "adapter": "huggingface",
                "device": self._device,
                "torch_version": self._torch.__version__,
                "transformers_version": self._transformers_version,
                "token_count": int(encoded["input_ids"].shape[-1]),
            },
        )
