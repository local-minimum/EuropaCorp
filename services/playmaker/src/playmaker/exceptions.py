class UnknownMailerError(Exception):
    pass


class StoryParsingError(Exception):
    pass


class DSLParsingError(StoryParsingError):
    pass
