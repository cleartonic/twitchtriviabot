try:
    from main import main
    
    if __name__ == '__main__':
        main()
except:
    import traceback
    traceback.print_exc()
    x = input("Press enter to close...")