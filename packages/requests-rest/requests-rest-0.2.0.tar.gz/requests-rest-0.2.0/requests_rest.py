from functools import partial

import requests


def url_append(base_url, *args):
    url = base_url.rstrip('/')
    for a in args:
        a = str(a).strip('/')
        if a:
            url += '/' + a
    return url


def prefixed_request(prefix, f, method, url, *args, **kwargs):
    return f(method, url_append(prefix, url), *args, **kwargs)


class Resource(object):
    def __init__(self, base_url, resource_path, session=None, use_tail_slash=False):
        if session is None:
            session = requests.Session()

        self.base_url = base_url
        self.resource_path = resource_path
        self.prefix = url_append(base_url, resource_path)

        self.use_tail_slash = use_tail_slash

        session.request = partial(prefixed_request, self.prefix, session.request)
        self.client = session

    def _extract_response(self, response):
        pass

    def list(self, **kwargs):
        '''GET /xxx/'''
        return self.client.get('/' if self.use_tail_slash else '', **kwargs)

    def create(self, data=None, **kwargs):
        '''POST /xxx/'''
        return self.client.post('/' if self.use_tail_slash else '', data, **kwargs)

    def detail(self, id, **kwargs):
        '''GET /xxx/:id'''
        return self.client.get(id, **kwargs)

    def update(self, id, data=None, **kwargs):
        '''PUT /xxx/:id'''
        return self.client.put(id, data, **kwargs)

    def patch(self, id, data=None, **kwargs):
        '''PATCH /xxx/:id'''
        return self.client.patch(id, data, **kwargs)

    def delete(self, id, **kwargs):
        '''DELETE /xxx/:id'''
        return self.client.delete(id, **kwargs)


if __name__ == '__main__':
    # base_url = 'http://localhost:8001/'
    base_url = 'https://httpbin.org/'
    resource_path = 'anything'
    resource_user = Resource(base_url, resource_path)

    new_name = 'aponder'
    new_email = 'i@aponder.top'
    new_user = {
        'name': new_name,
        'email': new_email,
    }

    print(resource_user.list().json())
    print(resource_user.create(new_user).json())
    print(resource_user.update(1, new_user).json())
    print(resource_user.patch(1, new_name).json())
    print(resource_user.patch(1, new_email).json())
    print(resource_user.delete(1).json())
