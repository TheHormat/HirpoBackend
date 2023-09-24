import random
import string


def code_slug_generator1(size=12, chars=string.ascii_letters):
    return "".join(random.choice(chars) for _ in range(size))


def create_slug_shortcode(size, model_):
    new_code = code_slug_generator1(size=size)
    qs_exists = model_.objects.filter(slug=new_code).exists()
    return create_slug_shortcode(size, model_) if qs_exists else new_code


def code_slug_generator2(size=6, chars=string.digits):
    return "".join(random.choice(chars) for _ in range(size))


def create_activation_code(size, model_):
    new_code = code_slug_generator2(size=size)
    qs_exists = model_.objects.filter(activation_code=new_code).exists()
    return create_activation_code(size, model_) if qs_exists else new_code


def code_slug_generator3(size=10, chars=string.digits):
    return "".join(random.choice(chars) for _ in range(size))


def create_password_reset_code(size, model_):
    new_code = code_slug_generator3(size=size)
    qs_exists = model_.objects.filter(activation_code=new_code).exists()
    return create_password_reset_code(size, model_) if qs_exists else new_code
