import graphene
from graphql import GraphQLError

from ..models import AdminAppToken as AdminAppTokenModel
from ..misc import githubauth

from ..db.sa import sa

##__________________________________________________________________||
class OAuthAppInfo(graphene.ObjectType):
    client_id = graphene.String()
    authorize_url = graphene.String()
    token_url = graphene.String()
    redirect_uri = graphene.String()

##__________________________________________________________________||
class GitHubUser(graphene.ObjectType):
    login = graphene.String()
    name = graphene.String()
    avatarUrl = graphene.String() # Camel case so can easily be instantiated

##__________________________________________________________________||
class AuthPayload(graphene.ObjectType):
    token = graphene.String()

##__________________________________________________________________||
class GitHubAuth(graphene.Mutation):
    class Arguments:
        code = graphene.String(required=True)

    authPayload = graphene.Field(lambda: AuthPayload)

    def mutate(root, info, code):
        token = githubauth.get_token(code)
        if not token:
            raise GraphQLError('Unsuccessful to obtain the token')
        admin_token = AdminAppTokenModel.query.one()
        if not githubauth.is_member(user_token=token, admin_token=admin_token.token):
            raise GraphQLError('The user is not a member.')
        authPayload = AuthPayload(token=token)
        return GitHubAuth(authPayload=authPayload)

##__________________________________________________________________||
class StoreAdminAppToken(graphene.Mutation):
    class Arguments:
        code = graphene.String(required=True)

    ok = graphene.Boolean()

    def mutate(root, info, code):
        token = githubauth.get_token(code, admin=True)

        row = AdminAppTokenModel.query.one_or_none()
        if row:
            row.token = token
        else:
            row = AdminAppTokenModel(token=token)
            sa.session.add(row)
        sa.session.commit()
        ok = True
        return StoreAdminAppToken(ok=ok)