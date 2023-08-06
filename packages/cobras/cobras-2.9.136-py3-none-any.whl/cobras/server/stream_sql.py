'''Stream SQL processor, to filter and transform messages when subcribing.

Copyright (c) 2018-2019 Machine Zone, Inc. All rights reserved.
'''

import collections
import fnmatch
import logging

from cobras.common.algorithm import extractAttributeFromDict

StreamSQLExpression = collections.namedtuple(
    'StreamSQLExpression',
    [
        'components',
        'val',
        'length',
        'equalExpression',
        'likeExpression',
        'differentExpression',
        'largerThanExpression',
        'lowerThanExpression',
    ],
)


class InvalidStreamSQLError(Exception):
    pass


class StreamSqlFilter:
    def __init__(self, sql_filter):
        '''
        Support expression on strings, bool, int
        Support AND and OR expressions

        No parenthesis support
        '''

        self.emptyFilter = False
        self.channel = None

        if sql_filter is None:
            raise InvalidStreamSQLError()

        # Basic validation
        tokens = [token.strip() for token in sql_filter.split()]

        try:
            selectIdx = tokens.index('SELECT')
        except ValueError:
            try:
                selectIdx = tokens.index('select')
            except ValueError:
                raise InvalidStreamSQLError()

        if selectIdx != 0:
            raise InvalidStreamSQLError()

        try:
            fromIdx = tokens.index('FROM')
        except ValueError:
            try:
                fromIdx = tokens.index('from')
            except ValueError:
                raise InvalidStreamSQLError()

        # Parse glob
        if tokens[1] == '*':
            self.fields = None
        else:
            fields = ' '.join(tokens[1:fromIdx])
            fields = fields.split(',')
            self.fields = []
            for field in fields:
                field = field.strip()
                field, delim, alias = field.partition(' AS ')
                if not alias:
                    alias = field
                self.fields.append((field, alias))

        # Parse channel name
        channelIdx = fromIdx + 1
        self.channel = tokens[channelIdx].replace('`', '')

        try:
            whereIdx = tokens.index('WHERE')
        except ValueError:
            try:
                whereIdx = tokens.index('where')
            except ValueError:
                self.emptyFilter = True
                return

        conditionStart = whereIdx + 1
        sql_filter = ' '.join(tokens[conditionStart:])
        sql_filter = sql_filter.replace('\n', ' ')

        # Since we don't have a legit lexer, we need spaces around our
        # OR and AND ...
        # FIXME: we should figure out how to use ply, or sqlparse
        self.andExpr = True
        if ' AND ' in sql_filter or ' OR ' in sql_filter:
            if ' AND ' in sql_filter:
                exprs = sql_filter.split(' AND ')
            elif ' OR ' in sql_filter:
                exprs = sql_filter.split(' OR ')
                self.andExpr = False

            exprs = [expr.strip() for expr in exprs]
            self.expressions = [self.buildExpression(expr) for expr in exprs]
        else:
            self.expressions = [self.buildExpression(sql_filter)]

    def buildExpression(self, text):
        '''
        FIXME: support lower than and greater than for ints
               support float ?
        '''

        equalExpression = False
        likeExpression = False
        differentExpression = False
        largerThanExpression = False
        lowerThanExpression = False

        if ' LIKE ' in text:
            jsonExpr, _, val = text.partition(' LIKE ')
            likeExpression = True
        elif ' != ' in text:
            jsonExpr, _, val = text.partition(' != ')
            differentExpression = True
        elif ' = ' in text:
            jsonExpr, _, val = text.partition('=')
            equalExpression = True
        elif ' > ' in text:
            jsonExpr, _, val = text.partition('>')
            largerThanExpression = True
        elif ' < ' in text:
            jsonExpr, _, val = text.partition('<')
            lowerThanExpression = True
        else:
            raise InvalidStreamSQLError('Invalid operand')

        self.jsonExpr = jsonExpr.strip()

        val = val.strip()
        if val.startswith("'") and val.endswith("'"):
            val = val.replace("'", '')
            if likeExpression:
                val = val.replace('%', '*')
                val = val.replace('_', '?')
        elif val in ('true', 'false'):
            val = val == 'true'
        else:
            try:
                val = int(val)
            except ValueError:
                raise InvalidStreamSQLError()

        components = self.jsonExpr.split('.')
        return StreamSQLExpression(
            components,
            val,
            len(components),
            equalExpression,
            likeExpression,
            differentExpression,
            largerThanExpression,
            lowerThanExpression,
        )

    def matchExpression(self, msg, expression):
        if expression.length == 2:
            val = msg.get(expression.components[0], {}).get(
                expression.components[1]
            )  # noqa
            return self.matchOperand(val, expression)
        elif expression.length == 1:
            val = msg.get(expression.components[0])
            return self.matchOperand(val, expression)
        else:
            msgCopy = dict(msg)

            for component in expression.components:
                msgCopy = msgCopy.get(component, {})

            return self.matchOperand(msgCopy, expression)

    def matchOperand(self, val, expression):
        if expression.equalExpression:
            return expression.val == val
        elif expression.likeExpression:
            return fnmatch.fnmatch(val, expression.val)
        elif expression.differentExpression:
            return expression.val != val
        elif expression.largerThanExpression:
            return val > expression.val
        elif expression.lowerThanExpression:
            return val < expression.val
        else:
            assert False, 'unexpected expression'

    def match(self, msg):
        if self.emptyFilter:
            return self.transform(msg)

        if isinstance(msg, list):
            if len(msg) == 0:
                logging.error('Bad type for {}, expecting non empty list'.format(msg))
                return False
            else:
                msg = msg[0]

        if not isinstance(msg, dict):
            logging.error('Bad type for {}, expecting dictionary'.format(msg))
            return False

        if self.andExpr:
            if not all(
                self.matchExpression(msg, expression) for expression in self.expressions
            ):  # noqa
                return False
            else:
                return self.transform(msg)
        else:
            if not any(
                self.matchExpression(msg, expression) for expression in self.expressions
            ):  # noqa
                return False
            else:
                return self.transform(msg)

    def transform(self, msg):
        '''extract a subfield'''

        if self.fields is None:
            return msg

        ret = {}
        for field, alias in self.fields:
            subtree = extractAttributeFromDict(dict(msg), field)
            ret.update({alias: subtree})

        return ret


def match_stream_sql_filter(sql_filter, msg):
    try:
        f = StreamSqlFilter(sql_filter)
        return f.match(msg)
    except InvalidStreamSQLError:
        return False
