import os

choice = input("push or pull?\nPUSH/PULL: ").strip().upper()
if choice == "PUSH":
    os.system("git add .")
    changes = input("please describe your changes: ")
    os.system(f'git commit -m "{changes}"')
    os.system("git push")
elif choice == "PULL":
    os.system("git pull")
else:
    print("STOP WITH YOUR TYPOS.")
