def menu(files):
    while True:
        print("Available images:")
        for i, file in enumerate(files, start=1):
            print(f"{i}. {file}")
        print("0. exit")
        try:
            choice = int(input("Select the image number to decompress: "))
            if choice == 0:
                print(f"=======================================")
                print("👋 See you soon!!!")
                return 0
            elif choice < 1 or choice > len(files):
                print("❌ Invalid option. Try again.")
                continue
            return choice
        except ValueError:
            print("❌ Please enter a number.")
