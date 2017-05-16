import json

from barbicanclient import client as barbican_client

from MigrationTool import keystone


def get_secret(ctxt, secret_ref):
    session = keystone.create_keystone_session(ctxt)
    barbican = barbican_client.Client(session=session)
    return json.loads(barbican.secrets.get(secret_ref).payload)
