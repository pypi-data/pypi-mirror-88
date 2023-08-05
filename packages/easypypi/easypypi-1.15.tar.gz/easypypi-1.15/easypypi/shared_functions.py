"""
Functions shared by easypypi.py and licenses.py
Check: Separate file required to avoid circular import?
"""

import os


def create_file(filepath, content, **kwargs):
    """
    Create a backup if required, then create new file using writelines
    Returns "file exists" if filepath already exists and overwrite = False
    """
    if type(content) == str:
        content = content.splitlines(True)  # keep line breaks
    if filepath.is_file():
        if kwargs.get("overwrite"):
            backup = filepath.with_name(filepath.stem + " - old.py")
            if backup.is_file():
                os.remove(backup)
            filepath.rename(backup)
            print(f"\n✓ Renamed {filepath.name} to:\n  {backup.name}")
            filepath.touch()  # Create empty file to append lines to
        else:
            print(f"\nⓘ Existing file preserved:\n  {filepath}")
            return "file exists"
    with open(filepath, "a") as file:
        file.writelines(content)
        print(f"\n✓ Created new file:\n  {filepath}")


def update_line(script_lines, old_line_starts, new_value):
    """ Updates and returns script_lines, ready for writing to setup.py """
    for index, line in enumerate(script_lines.copy()):
        if line.lstrip().startswith(old_line_starts):
            try:
                if not new_value.startswith("["):
                    new_value = f'"{new_value}"'  # Add quotation marks unless list
                script_lines[index] = old_line_starts + new_value.rstrip() + "\n"
                print(
                    f"\n✓ Updated script line {index+1}:\n{script_lines[index].rstrip()[:400]}"
                )
                break  # only update first occurrence
            except:
                print(new_value, type(new_value))
    return script_lines
