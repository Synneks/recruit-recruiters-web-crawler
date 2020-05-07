import stringcase


def check_page_number(page_number):
    if page_number is not None:
        try:
            page_number = int(page_number) if int(page_number) > 0 else None
        except ValueError:
            page_number = None
    return page_number


def to_json(o):
    return {stringcase.camelcase(k): v for k, v in vars(o).items()}
