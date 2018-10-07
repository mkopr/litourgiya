from settings import DEFAULT_PAGE_SIZE


def paginate_data(data: list, params: dict) -> dict:
    page = 1 if not params.get('page', None) else params['page']
    size = DEFAULT_PAGE_SIZE if not params.get('size', None) else params['size']
    return {'count': len(data), 'size': size, 'page': page, 'data': data[size*(page-1):size*page]}
