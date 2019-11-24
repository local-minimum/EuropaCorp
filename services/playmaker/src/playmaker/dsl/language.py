from ..models import Rule, Communication


class Zero(Rule):
    def __call__(self, _: Communication):
        return 0


class MailedTo(Rule):
    def __init__(self, reciever: str, success: float = 1, fail: float = 0):
        self.reciever = reciever
        self.success = success
        self.fail = fail

    def __call__(self, comm: Communication):
        return (
            self.success if comm.reciever == self.reciever else self.fail
        )


class BodyContains(Rule):
    def __init__(self, *phrases: str):
        self.phrases = phrases

    def __call__(self, comm: Communication):
        return len([phrase for phrase in self.phrases if phrase in comm.body])


class Sum(Rule):
    def __init__(self, *rules: Rule):
        self.rules = rules

    def __call__(self, comm: Communication):
        return sum(rule(comm) for rule in self.rules)


class Average(Rule):
    def __init__(self, *rules: Rule):
        self.rules = rules

    def __call__(self, comm: Communication):
        return sum(rule(comm) for rule in self.rules) / len(self.rules)


class Threshold(Rule):
    def __init__(
        self,
        threshold: float,
        rule: Rule,
        success: float = 1,
        fail: float = 0,
    ):
        self.threshold = threshold
        self.success = success
        self.fail = fail
        self.rule = rule

    def __call__(self, comm: Communication):
        return self.success if self.rule(comm) >= self.threshold else self.fail
