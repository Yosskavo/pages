### inverted

#       STILL UNDER DEVELOPMENT

Minimal CLI Text Editor Objectives
1. State and Mode Management

    Implement a system to toggle between Insert Mode (for typing text) and Command Mode (for navigation and control).

    Ensure the terminal behaves differently depending on the active mode.

2. Internal Data Buffer

    Store the document's content in a dedicated memory structure (e.g., strings or linked structures).

    Ensure the text exists independently of what is currently displayed on the terminal screen.

3. Coordinate Synchronization

    Map the physical cursor position on the screen to the logical index within your data buffer.

    Enforce boundaries to prevent the cursor from moving into invalid or non-existent text areas.

4. File Persistence (I/O)

    Enable the ability to load an existing file into the editor at startup.

    Implement a save mechanism that writes the current state of the memory buffer back to the disk.

5. Advanced Line Manipulation

    Line Merging: Handle backspacing at the start of a line so that the current content moves up and joins the previous line.

    Line Splitting: Handle the Enter key by breaking the current line into two and shifting subsequent text downward.

    Visual Integrity: Ensure the entire screen updates correctly when lines are added or removed, maintaining a clean UI without artifacts.
