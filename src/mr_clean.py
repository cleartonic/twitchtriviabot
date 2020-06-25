class Mr:
    def clean(message):
        lower_case = Mr.lower(message)
        letters_only = filter(str.isalpha, lower_case)
        return "".join(letters_only)

    def lower(message):
        return message.lower()
