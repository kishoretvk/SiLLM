import pathlib
import json
import dataclasses
import logging

import mlx.core as mx
import mlx.nn as nn

@dataclasses.dataclass
class ModelArgs:
    """
    Model arguments.
    """
    model_type: str
    dim: int
    n_layers: int
    head_dim: int
    hidden_dim: int
    n_heads: int
    n_kv_heads: int
    norm_eps: float
    vocab_size: int
    rope_theta: float = 10000.0
    rope_traditional: bool = True
    rope_scaling: dict = None
    moe: dict = None

    def __repr__(self):
        return json.dumps(dataclasses.asdict(self), indent=4)

    @staticmethod
    def load(config_path):
        """
        Load model config from JSON file.
        Args:
            config_path: Path to config file.
        Returns:
            ModelArgs instance.
        """
        assert pathlib.Path(config_path).exists(), config_path

        with open(config_path, "r") as f:
            config = json.loads(f.read())
        config = {k:v for k, v in config.items() if k in ModelArgs.__annotations__}
        args = ModelArgs(**config)

        logging.info(f"Loaded model config from {config_path}")
        for k, v in dataclasses.asdict(args).items():
            logging.debug(f"Config {k}: {v}")

        return args

class Model(nn.Module):
    """
    Base class for LLM models.
    """
    def __init__(self, args: ModelArgs):
        super().__init__()
    
    def __call__(self, inputs: mx.array, cache=None):
        raise NotImplementedError(f"Class model.Model is used for inheritance only")