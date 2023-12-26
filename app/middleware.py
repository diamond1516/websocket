from channels.middleware import BaseMiddleware
from channels.db import database_sync_to_async
from django.contrib.auth.models import User, AnonymousUser


class AuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        user = await self.get_user(scope)
        scope['user'] = user

        await super().__call__(scope, receive, send)

    @database_sync_to_async
    def get_user_from_db(self, user_id):
        if user_id:
            obj = User.objects.filter(id=user_id).first()
            if obj:
                return obj
        return AnonymousUser()

    async def get_user(self, scope):
        headers = dict(scope['headers'])
        user_id = headers.get(b'id', b'').decode('utf-8')
        return await self.get_user_from_db(user_id)
