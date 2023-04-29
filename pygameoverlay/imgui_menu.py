import imgui


def menu():
    imgui.set_next_window_size(250, 250)
    # imgui.set_next_window_position(50, 50)
    imgui.begin(
        "Hello World",
        # imgui.WINDOW_NO_MOVE
        flags=imgui.WINDOW_NO_RESIZE | imgui.WINDOW_NO_SAVED_SETTINGS)
    imgui.text("Welcome to Hell")

    if imgui.button("Click me!"):
        print("Click")

    # if imgui.checkbox

    imgui.end()
