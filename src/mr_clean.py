class Mr:
    def clean(message):
        lower_case = message.lower()
        letters_only = filter(str.isalpha, lower_case)
        return "".join(letters_only)
