from pathlib import Path

from js import Blob, ace, document, window
from pyodide.ffi.wrappers import add_event_listener

from main import simplify_python  # type: ignore[attr-defined]

editor_input = ace.edit("editor-input")
editor_input.setOption("maxLines", float("inf"))
editor_output = ace.edit("editor-output")
editor_output.setOption("maxLines", float("inf"))
editor_output.setReadOnly(True)


def on_keyup_editor_input(_: None) -> None:
    input_ = editor_input.getValue()
    try:
        output = simplify_python(input_.encode("utf-8"))
        editor_output.setValue(output.decode())
    except Exception as exception:  # noqa: BLE001
        editor_output.setValue(exception)


async def on_change_file_input(e) -> None:  # type: ignore[no-untyped-def] # noqa: ANN001
    file_list = e.target.files
    first_item = file_list.item(0)
    editor_input.setValue(await first_item.text())
    on_keyup_editor_input(None)


def on_download_output(_: None) -> None:
    content = editor_output.getValue()
    a = document.createElement("a")
    document.body.appendChild(a)
    a.style = "display: none"
    blob = Blob.new([content])
    url = window.URL.createObjectURL(blob)
    a.href = url
    a.download = "main.py"
    a.click()
    window.URL.revokeObjectURL(url)


def main() -> None:
    with Path("before.py").open() as file:
        editor_input.setValue(file.read())
    on_keyup_editor_input(None)
    add_event_listener(
        document.getElementById("editor-input"),
        "keyup",
        on_keyup_editor_input,
    )
    add_event_listener(
        document.getElementById("download-output"),
        "click",
        on_download_output,
    )
    add_event_listener(
        document.getElementById("file-input"),
        "change",
        on_change_file_input,
    )


if __name__ == "__main__":
    main()
