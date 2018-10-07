from pagination import paginate_data
from settings import DEFAULT_PAGE_SIZE


class TestPagination:
    def test_pagination_without_params(self):
        params = {}
        data = range(40)
        result = paginate_data(data, params)

        assert result.get('count', None) == len(data)
        assert result.get('size', None) == DEFAULT_PAGE_SIZE
        assert len(result.get('data', None)) == DEFAULT_PAGE_SIZE
        assert result.get('page', None) == 1

    def test_pagination_with_size(self):
        params = {'size': 2}
        data = range(40)
        result = paginate_data(data, params)

        assert result.get('count', None) == len(data)
        assert result.get('size', None) == params['size']
        assert len(result.get('data', None)) == params['size']
        assert result.get('page', None) == 1

    def test_pagination_with_page(self):
        params = {'page': 2}
        data = range(40)
        result = paginate_data(data, params)

        assert result.get('count', None) == len(data)
        assert result.get('size', None) == DEFAULT_PAGE_SIZE
        assert len(result.get('data', None)) == DEFAULT_PAGE_SIZE
        assert result.get('page', None) == params['page']

    def test_pagination_with_page_and_size(self):
        params = {'page': 2, 'size': 4}
        data = range(40)
        result = paginate_data(data, params)

        assert result.get('count', None) == len(data)
        assert result.get('size', None) == params['size']
        assert len(result.get('data', None)) == params['size']
        assert result.get('page', None) == params['page']
