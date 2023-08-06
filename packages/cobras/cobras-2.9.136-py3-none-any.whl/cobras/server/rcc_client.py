'''rcc redis client

Copyright (c) 2020 Machine Zone, Inc. All rights reserved.
'''

from urllib.parse import urlparse
from hashlib import sha1

from rcc.client import RedisClient


class RedisClientRcc(object):
    def __init__(self, url, password, cluster):
        self.url = url
        self.password = password
        self.cluster = cluster

        netloc = urlparse(url).netloc
        host, _, port = netloc.partition(':')
        if port:
            port = int(port)
        else:
            port = 6379

        self.redis = RedisClient(self.url, self.password)

        self.host = host

    async def getClientIdForKey(self, key):
        return await self.redis.send('CLIENT', 'ID', key=key)

    async def getHostForKey(self, key):
        # Check whether redis is running in cluster mode or not
        try:
            info = await self.redis.send('INFO')
        except Exception:
            return f'{self.redis.host}:{self.redis.port}'

        if info.get('cluster_enabled') == '0':
            return f'{self.redis.host}:{self.redis.port}'

        # Redis is running in cluster mode.
        # 1. get the slot for a key
        slot = await self.redis.send('CLUSTER', 'KEYSLOT', key)

        # 2. find which node is handling a slot
        slots = await self.redis.send('CLUSTER', 'SLOTS')

        for slotInfo in slots:
            if slotInfo[0] <= slot <= slotInfo[1]:
                host = slotInfo[2][0].decode()
                port = slotInfo[2][1]
                return f'{host}:{port}'

        # this should not happen, unless the cluster is being reconfigured
        return 'unknown-host'

    async def ping(self):
        return await self.redis.send('PING')

    async def xadd(self, stream, field, data, maxLen):
        return await self.redis.send(
            'XADD',
            stream,
            'MAXLEN',
            '~',
            maxLen,
            b'*',
            field,
            data,
            b'sha1',
            sha1(data.encode()).hexdigest(),
        )

    async def xaddRaw(self, stream, maxLen, *args):
        return await self.redis.send('XADD', stream, 'MAXLEN', '~', maxLen, b'*', *args)

    async def exists(self, key):
        return await self.redis.send('EXISTS', key)

    async def xread(self, stream, streamId):
        return await self.redis.send(
            'XREAD', 'BLOCK', b'0', b'STREAMS', stream, streamId
        )

    async def delete(self, key):
        return await self.redis.send('DEL', key)

    async def xrevrange(self, stream, start, end, count):
        return await self.redis.send('XREVRANGE', stream, start, end, b'COUNT', count)
