from src.setup import setup_filesystem, get_cha_files
from src.swapper import swap_file


def main():
    try:
        setup_filesystem()
    except:
        print("Created input folder, please add .cha files to be swapped")
        input("Press enter to exit...")
        exit(0)

    files = get_cha_files()

    for file in files:
        try:
            swap_file(file)
        except Exception as e:
            print(f"Error: {e}")
        print()

    input("Press enter to exit...")


if __name__ == "__main__":
    main()
