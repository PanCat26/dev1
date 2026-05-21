from __future__ import annotations

import os

_DEEPEVAL_IMPORT_ERROR: ImportError | None = None

try:
    from deepeval.metrics import AnswerRelevancyMetric, FaithfulnessMetric
    from deepeval.test_case import LLMTestCase
except ImportError as exc:  # pragma: no cover
    AnswerRelevancyMetric = FaithfulnessMetric = LLMTestCase = None  # type: ignore
    _DEEPEVAL_IMPORT_ERROR = exc


def deepeval_installed() -> bool:
    return AnswerRelevancyMetric is not None and FaithfulnessMetric is not None and LLMTestCase is not None


def deepeval_import_error_text() -> str | None:
    if _DEEPEVAL_IMPORT_ERROR is None:
        return None
    return (
        "DeepEval is not installed (`pip install -r requirements.txt`). "
        f"Underlying error: {_DEEPEVAL_IMPORT_ERROR}"
    )


def _openrouter_key() -> str:
    return (os.getenv("OPENROUTER_API_KEY") or "").strip()


DEFAULT_OPENROUTER_JUDGE_MODEL = "deepseek/deepseek-v4-flash:free"


def _openrouter_generation_kwargs() -> dict:
    """OpenRouter reasoning (Python OpenAI client uses extra_body). Disable via OPENROUTER_JUDGE_REASONING=0."""
    raw = (os.getenv("OPENROUTER_JUDGE_REASONING") or "1").strip().lower()
    if raw in ("0", "false", "no", "off"):
        return {}
    return {"extra_body": {"reasoning": {"enabled": True}}}


def deepeval_judge_model_from_env():
    """Return OpenRouter-backed judge when OPENROUTER_API_KEY is set; else None (DeepEval OpenAI-style default)."""

    router_key = _openrouter_key()
    if not router_key:
        return None

    try:
        from deepeval.models import OpenRouterModel
    except ImportError:
        return None

    base = (os.getenv("OPENROUTER_BASE_URL") or "https://openrouter.ai/api/v1").strip()
    model_id = (
        os.getenv("OPENROUTER_JUDGE_MODEL") or DEFAULT_OPENROUTER_JUDGE_MODEL
    ).strip()
    temp_raw = os.getenv("OPENROUTER_JUDGE_TEMPERATURE")
    temp = float(temp_raw) if temp_raw not in ("", None) else None

    kwargs: dict = {
        "model": model_id,
        "api_key": router_key,
        "base_url": base,
    }
    gen_kw = _openrouter_generation_kwargs()
    if gen_kw:
        kwargs["generation_kwargs"] = gen_kw
    if temp is not None:
        kwargs["temperature"] = temp

    try:
        return OpenRouterModel(**kwargs)
    except TypeError:
        kwargs.pop("temperature", None)
        kwargs.pop("generation_kwargs", None)
        return OpenRouterModel(**kwargs)


def summarize_judge_requirements_hint() -> str:
    if _openrouter_key():
        mid = (
            os.getenv("OPENROUTER_JUDGE_MODEL") or DEFAULT_OPENROUTER_JUDGE_MODEL
        ).strip()
        base = (os.getenv("OPENROUTER_BASE_URL") or "https://openrouter.ai/api/v1").strip()
        return (
            f"OpenRouter judge configured (model={mid!r}, base_url={base!r}). "
            "Check key balance and model availability on openrouter.ai."
        )

    if os.getenv("OPENAI_API_KEY"):
        return (
            "No OPENROUTER_API_KEY; DeepEval falls back to default OpenAI-compatible judge "
            "(OPENAI_API_KEY / OPENAI_BASE_URL)."
        )

    return (
        "Set OPENROUTER_API_KEY (recommended) or OPENAI_API_KEY so DeepEval judges can call an API."
    )


def normalize_retrieval_section(file_path: str, symbol_name: str, text: str) -> str:
    header = f"# {file_path} :: {symbol_name}\n\n"
    max_body = min(9000, max(512, len(text)))
    trimmed = text if len(text) <= max_body else text[:max_body]
    return header + trimmed


def score_answer_quality(
    *,
    question: str,
    answer_text: str,
    retrieval_context_sections: list[str],
) -> tuple[float | None, float | None, str | None, str | None, list[str]]:
    """Compute AnswerRelevancy + Faithfulness or return explanatory errors."""

    errors: list[str] = []

    if not deepeval_installed():
        errors.append(deepeval_import_error_text() or "DeepEval unavailable.")
        return None, None, None, None, errors

    trimmed_answer = answer_text.strip()
    if not trimmed_answer:
        errors.append("Empty model answer; skipping DeepEval metrics.")
        return None, None, None, None, errors

    judge = deepeval_judge_model_from_env()

    metric_kw: dict = {"include_reason": True, "async_mode": False, "verbose_mode": False}
    if judge is not None:
        metric_kw["model"] = judge

    relevancy_score = None
    relevancy_reason = None
    faithfulness_score = None
    faithfulness_reason = None

    rr_metric = AnswerRelevancyMetric(**metric_kw)
    rr_case = LLMTestCase(
        input=question,
        actual_output=trimmed_answer,
    )

    try:
        rr_metric.measure(rr_case)
        relevancy_score = float(rr_metric.score)
        if getattr(rr_metric, "reason", None):
            relevancy_reason = str(rr_metric.reason)
    except Exception as exc:  # noqa: BLE001
        errors.append(
            f"AnswerRelevancyMetric failed: {exc}. {summarize_judge_requirements_hint()}"
        )

    faith_sections = retrieval_context_sections or []
    if not faith_sections:
        errors.append(
            "FaithfulnessMetric skipped because retrieval_context was empty; "
            "ensure Qdrant indexes return evidence snippets for those manual prompts."
        )
    else:
        faith_metric = FaithfulnessMetric(**metric_kw)
        f_case = LLMTestCase(
            input=question,
            actual_output=trimmed_answer,
            retrieval_context=faith_sections,
        )
        try:
            faith_metric.measure(f_case)
            faithfulness_score = float(faith_metric.score)
            if getattr(faith_metric, "reason", None):
                faithfulness_reason = str(faith_metric.reason)
        except Exception as exc:  # noqa: BLE001
            errors.append(
                f"FaithfulnessMetric failed: {exc}. {summarize_judge_requirements_hint()}"
            )

    return (
        relevancy_score,
        faithfulness_score,
        relevancy_reason,
        faithfulness_reason,
        errors,
    )
