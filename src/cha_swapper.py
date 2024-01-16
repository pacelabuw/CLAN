from utils.setup import setup_filesystem, get_cha_files
from utils.swapper import swap_file


def main():
    try:
        setup_filesystem()
    except:
        print("Created input folder, please and .cha files to be swapped.")
        input("Press enter to exit...")
        exit(0)

    files = get_cha_files()

    for file in files:
        swap_file(file)

    input("Press enter to exit...")


if __name__ == "__main__":
    main()
