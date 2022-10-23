class ParserData:
    @staticmethod
    def parse_input_data(data: str):
        """
        function parse users requests
        :param data: get str with requests
        :return: return dict with data
        """
        result_data = {}
        if data:
            parameters = data.split('&')
            for items in parameters:
                key, value = items.split('=')
                result_data[key] = value
        return result_data

class GetRequest(ParserData):

    @staticmethod
    def get_request_param(environ):
    # get requests parameters
        query_string = environ["QUERY_STRING"]
    # create dict from str with parser
        request_parameters = GetRequest.parse_input_data(query_string)
        return request_parameters

class PostRequest(ParserData):

    @staticmethod
    def get_wsgi_input_data(env) -> bytes:
        get_content_data_length = env.get('CONTENT_LENGTH')
        content_length = int(get_content_data_length) if get_content_data_length else 0
        data = env['wsgi.input'].read(content_length) if content_length > 0 else b''
        return data

    def parse_wsgi_input_data(self, data: bytes) -> dict:
        result = {}
        if data:
            data_string = data.decode(encoding='utf-8')
            print(f'str after decode: {data_string}')
            result = self.parse_input_data(data_string)
            print(result)
        return result

    def get_request_parameters(self, environ):
        data = self.get_wsgi_input_data(environ)
        data = self.parse_wsgi_input_data(data)
        return data


