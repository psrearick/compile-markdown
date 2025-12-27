import os
import argparse
import re

def rename_path(path, dry_run):
    """
    Renames a file or directory by removing special characters.
    Returns the new filename (not the full path).
    """
    directory, filename = os.path.split(path)

    # Keep only alphanumeric characters, dots, underscores, and hyphens
    new_filename = re.sub(r'[^a-zA-Z0-9._-]', '', filename)

    # Ensure the filename is not empty after stripping
    if not new_filename:
        new_filename = "renamed_item"

    full_new_path = os.path.join(directory, new_filename)

    # Perform rename if names differ and not in dry_run mode
    if filename != new_filename:
        if not dry_run:
            try:
                os.rename(path, full_new_path)
            except OSError as e:
                print(f"Error renaming {path}: {e}")
                return filename

    return new_filename

def process_folder(path, recursive, dry_run, absolute):

    if not os.path.exists(path):
        return ""

    # output_string accumulates the log of changes
    output_string = ""

    # List directory contents
    try:
        items = os.listdir(path)
    except OSError as e:
        print(f"Error reading directory {path}: {e}")
        return ""

    for item in items:
        item_path = os.path.join(path, item)

        # Get the new cleaned filename
        new_filename = rename_path(item_path, dry_run=dry_run)

        # Construct the full path for the new name
        new_full_path = os.path.join(path, new_filename)

        # Prepare strings for logging
        display_old = os.path.abspath(item_path) if absolute else item_path
        display_new = os.path.abspath(new_full_path) if absolute else new_full_path

        log_entry = f"{display_old} -> {display_new}"
        output_string = "\n".join([output_string, log_entry]) if output_string else log_entry

        # Recursion logic
        # Must check if the *new* path is a directory, as the old path may no longer exist
        target_for_recursion = new_full_path if not dry_run else item_path

        if recursive and os.path.isdir(target_for_recursion):
            # If we renamed the directory, we must recurse into the new name
            child_list = process_folder(target_for_recursion, recursive=recursive, dry_run=dry_run, absolute=absolute)

            if child_list:
                output_string = f"{output_string}\n{child_list}"

    return output_string

def main():
    parser = argparse.ArgumentParser(description="Rename files and directories to remove special characters.")
    parser.add_argument("-a", "--absolute", action="store_true", help="Print absolute paths")
    parser.add_argument("-r", "--recursive", action="store_true", help="Rename files and directories recursively")
    parser.add_argument("-o", "--output", help="Output changes to file (default: ./renamed.txt)")
    parser.add_argument("-t", "--target", help="Path to the target directory (default: current directory)")
    parser.add_argument("-d", "--dry-run", action="store_true", help="Print changes without saving")
    parser.add_argument("-s", "--skip-write", action="store_true", help="Do not write changes to file")

    args = parser.parse_args()

    # Set defaults if None
    target = os.getcwd() if args.target is None else args.target
    recursive = args.recursive
    absolute = args.absolute
    skip_write = args.skip_write
    dry_run = args.dry_run
    output_file = "renamed.txt" if args.output is None else args.output

    changes = process_folder(target, recursive=recursive, dry_run=dry_run, absolute=absolute)

    if changes:
        print(changes)
    else:
        print("No items found or no changes needed.")

    if skip_write:
        return

    # Handle output file path logic
    if not os.path.exists(output_file):
        # If output is just a filename or doesn't exist, put it in cwd or use as is
        if not os.path.dirname(output_file):
            output_file = os.path.join(os.getcwd(), output_file)
    elif os.path.isdir(output_file):
        # If output is a directory, append default filename
        output_file = os.path.join(output_file, "renamed.txt")

    output_file = os.path.abspath(output_file)

    if changes:
        try:
            with open(output_file, 'w') as f:
                f.write(changes)
            print(f"\nLog saved to: {output_file}")
        except IOError as e:
            print(f"Error writing to log file: {e}")

if __name__ == "__main__":
    main()
