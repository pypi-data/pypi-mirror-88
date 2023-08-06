from django.middleware.common import CommonMiddleware

__all__ = ("AppendSlashMiddleware",)


class AppendSlashMiddleware(CommonMiddleware):
    """
    If there is no '/' at the end of the request URL,
    it is forcibly attached.
    """

    def process_request(self, request):
        if not request.path.endswith("/"):
            request.path += "/"
        if not request.path_info.endswith("/"):
            request.path_info += "/"
