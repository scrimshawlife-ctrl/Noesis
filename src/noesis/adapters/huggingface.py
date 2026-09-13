from __future__ import annotations

import random
from typing import Any

from noesis.domain.models import CaptureRequest, CaptureResult, ModelIdentity


class HuggingFaceAdapter:
    """Reference adapter for open-weight Transformer models.

    Heavy dependencies are imported lazily so the base package remains usable in CI
    without torch/transformers or a model download.
    """

    def __init__(self, model_id: str, revision: str = "main", device: str = "cpu") -> None:
        try:
            import torch
            from transformers import AutoModel, AutoTokenizer
        except ImportError as exc:  # pragma: no cover - environment dependent
            raise RuntimeError("Install noesis-latent[hf] to use HuggingFaceAdapter") from exc

        self._torch = torch
        self._tokenizer = AutoTokenizer.from_pretrained(model_id, revision=revision)
        self._model = AutoModel.from_pretrained(model_id, revision=revision).to(device)
        self._model.eval()
        self._device = device
        self._identity = ModelIdentity(
            model_id=model_id,
            revision=revision,
            tokenizer_revision=revision,
        )

    @property
    def identity(self) -> ModelIdentity:
        return self._identity

    def _seed(self, seed: int) -> None:
        random.seed(seed)
        self._torch.manual_seed(seed)
        if self._torch.cuda.is_available():
            self._torch.cuda.manual_seed_all(seed)

    def capture(self, request: CaptureRequest) -> CaptureResult:
        self._seed(request.seed)
        encoded: dict[str, Any] = self._tokenizer(request.text, return_tensors="pt")
        encoded = {key: value.to(self._device) for key, value in encoded.items()}

        with self._torch.inference_mode():
            outputs = self._model(**encoded, output_hidden_states=True, return_dict=True)

        site = request.site
        token_index = site.token_index
        if site.kind == "embedding":
            tensor = self._model.get_input_embeddings()(encoded["input_ids"])[0, token_index]
        elif site.kind == "hidden_state":
            if site.layer is None:
                raise ValueError("hidden_state capture requires a layer")
            hidden_states = outputs.hidden_states
            if hidden_states is None:
                raise RuntimeError("model did not return hidden states")
            try:
                tensor = hidden_states[site.layer][0, token_index]
            except IndexError as exc:
                raise ValueError(f"invalid representation site: {site.key()}") from exc
        else:
            raise ValueError(f"unsupported representation kind: {site.kind}")

        vector = tuple(float(x) for x in tensor.detach().cpu().to(self._torch.float64).tolist())
        return CaptureResult(
            request=request,
            model=self.identity,
            vector=vector,
            runtime_metadata={
                "adapter": "huggingface",
                "device": self._device,
                "torch_version": self._torch.__version__,
                "token_count": int(encoded["input_ids"].shape[-1]),
            },
        )
