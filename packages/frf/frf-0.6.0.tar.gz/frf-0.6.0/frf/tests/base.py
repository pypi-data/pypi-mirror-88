# pylint: skip-file
import frf


class ProtectedResource(frf.Resource):

    async def list(self):
        return {}

    @frf.action(name='me')
    async def current_user(self, subject=frf.CurrentSubject):
        return subject.id
