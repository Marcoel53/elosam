import json
from urllib import error
from urllib import request


class LocalModelProvider:
    """
    Provider de modelo local do EloSam OS.

    Responsabilidades:
    - conectar o EloSam à API local do Ollama;
    - enviar prompts ao modelo;
    - receber respostas;
    - solicitar respostas estruturadas em JSON;
    - manter o EloSam desacoplado do runtime de IA.
    """

    VERSION = "1.0.0"

    def __init__(
        self,
        model="qwen2.5-coder:1.5b",
        base_url="http://127.0.0.1:11434",
        timeout=180,
    ):
        self.model = model
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def _post(
        self,
        endpoint,
        payload,
    ):
        url = (
            f"{self.base_url}"
            f"{endpoint}"
        )

        body = json.dumps(
            payload
        ).encode(
            "utf-8"
        )

        http_request = request.Request(
            url,
            data=body,
            headers={
                "Content-Type":
                    "application/json",
            },
            method="POST",
        )

        try:
            with request.urlopen(
                http_request,
                timeout=self.timeout,
            ) as response:
                content = response.read()

        except error.HTTPError as exc:
            detail = exc.read().decode(
                "utf-8",
                errors="replace",
            )

            raise RuntimeError(
                "Ollama retornou erro HTTP "
                f"{exc.code}: {detail}"
            ) from exc

        except error.URLError as exc:
            raise RuntimeError(
                "Não foi possível conectar "
                "ao Ollama em "
                f"{self.base_url}. "
                "Verifique se o Ollama "
                "está em execução."
            ) from exc

        return json.loads(
            content.decode("utf-8")
        )

    def generate(
        self,
        prompt,
        *,
        system=None,
        temperature=0.1,
    ):
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature":
                    temperature,
            },
        }

        if system:
            payload["system"] = system

        result = self._post(
            "/api/generate",
            payload,
        )

        return result.get(
            "response",
            "",
        ).strip()

    def generate_json(
        self,
        prompt,
        *,
        system=None,
        temperature=0.1,
    ):
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "format": "json",
            "options": {
                "temperature":
                    temperature,
            },
        }

        if system:
            payload["system"] = system

        result = self._post(
            "/api/generate",
            payload,
        )

        raw_response = result.get(
            "response",
            "",
        ).strip()

        if not raw_response:
            raise RuntimeError(
                "O modelo retornou "
                "uma resposta vazia."
            )

        try:
            return json.loads(
                raw_response
            )

        except json.JSONDecodeError as exc:
            raise RuntimeError(
                "O modelo não retornou "
                "JSON válido.\n\n"
                f"Resposta recebida:\n"
                f"{raw_response}"
            ) from exc

    def status(self):
        return {
            "version": self.VERSION,
            "provider": "ollama",
            "model": self.model,
            "base_url": self.base_url,
        }