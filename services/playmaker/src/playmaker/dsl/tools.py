from typing import Dict, Any, Optional, List

from . import language as lang
from ..models import Link, Communication, Rule
from ..exceptions import DSLParsingError


def get_supplied_optionals(
    data: Dict[str, Any],
    optionals=List[str],
) -> Dict[str, Any]:
    return {k: data[k] for k in data if k in optionals}


def build_rule(data: Optional[Dict[str, Any]]) -> Rule:
    if data is None:
        return lang.Zero()

    try:
        rule = data['rule'].upper().replace("_", "")
    except TypeError:
        raise DSLParsingError("Rule expected to be a dictionary but was {}".format(
            type(data),
        ))
    if rule == 'MAILEDTO':
        return lang.MailedTo(
            data['reciever'],
            **get_supplied_optionals(data, ['success', 'fail']),
        )
    elif rule == 'BODYCONTAINS':
        return lang.BodyContains(*data['contains'])
    elif rule == 'SUM':
        return lang.Sum(*(build_rule(rule) for rule in data['rules']))
    elif rule == 'AVERAGE':
        return lang.Average(*(build_rule(rule) for rule in data['rules']))
    elif rule == 'THRESHOLD':
        return lang.Threshold(
            data['threshold'],
            build_rule(data['rule']),
            **get_supplied_optionals(data, ['success', 'fail'])
        )
    elif rule == 'BODYMENTIONS':
        return lang.Threshold(
            data.get('threshold', 1),
            lang.BodyContains(*data['options']),
            **get_supplied_optionals(data, ['success', 'fail'])
        )
    raise DSLParsingError("Rule {} not understood".format(rule))


def should_execute(link: Link, comm: Communication) -> bool:
    return link.rule(comm) >= link.execute_threshold
