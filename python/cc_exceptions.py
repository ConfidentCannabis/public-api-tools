import attr


class InvalidAuthError(Exception):
    pass


@attr.s
class InvalidRequestError(Exception):
    msg = attr.ib()
    error_code = attr.ib(default=None)
    error_field = attr.ib(default=None)
    error_category = attr.ib(default=None)

    def __str__(self):
        return 'InvalidRequestError {} {} ({}: {})'.format(
            self.error_code,
            self.msg,
            self.error_category,
            self.error_field
        )
