from django.core.validators import RegexValidator


class TitleValidator(RegexValidator):
    regex = r"^[,.:;?!A-zА-я0-9-\s]+$"
    message = ("В имени котёнка допустимы: "
               "кириллица и латинские символы, "
               "арабские цифры, пробел, а также дефис.")


class TextValidator(TitleValidator):
    message = ("В текстовом описании допустимы: "
               "кириллица и латинские символы, "
               "арабские цифры, пробел, а также дефис.")
