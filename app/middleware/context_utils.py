from contextvars import ContextVar

request_id_var = ContextVar("request_id")


def set_request_id(id: str) -> None:
    request_id_var.set(id)

def get_request_id() -> str:
    return request_id_var.get()
