from ingredients.bottle import Bottle, run, request, abort
from ingredients.schnorr import sha256, schnorr_verify, schnorr_sign
from ingredients.files import load_dir, make_file, update_file
import os
import json
import secrets
from datetime import datetime

# Constants - might put these in a config file
STATION = "solar.credenso.cafe"
PORT = 1618

# Application Setup
app = Bottle()
nonces = {}

# TODO - Integrate https://github.com/rndusr/torf
def newFileEvent(pubkey, name, file):

    if file.content_type.startswith('image'):
        path = f'u/{name}/images'
    elif file.content_type.startswith('audio'):
        path = f'u/{name}/audio'
    else:
        path = f'u/{name}/assets'

    try:
        os.makedirs(path, exist_ok=True)
        file.save(path)
    except IOError:
        pass

    e = {
        'content': file.filename,
        'pubkey': pubkey,
        'kind': 1063,
        'created_at': round(datetime.now().timestamp()),
        'tags': [
            ['url',f'http://{STATION}/{path}/{file.filename}'],
            ['m',file.content_type],
            ['x', sha256(file.file.read()).hex()]
        ]
    }

    return e;
    

@app.get('/nonce')
def invite_get():
    name = request.query.name
    nonce = secrets.token_hex(24)
    nonces[name] = nonce
    print(nonces)
    return nonce

@app.post('/invite')
def invite_post():
    name = request.query.name
    nonce = nonces.pop(name)
    if (nonce is None):
        abort(500, "Nonce not found")

    nonce_bytes = sha256(nonce.encode())

    body = json.loads(request.body.getvalue())
    sig_bytes = bytes.fromhex(body.get('hexSig'))
    pubkey_bytes = bytes.fromhex(body.get('pubKey'))
    verified = schnorr_verify(nonce_bytes, pubkey_bytes, sig_bytes)

    if (not verified):
        abort(400, "Invalid Signature")

    invite = {
        'invite_code': secrets.token_hex(24),
        'public_key': body.get('pubKey'),
        'timestamp': round(datetime.now().timestamp()),
        'member': None
    }

    file_name = f'{name}_{invite.get("timestamp")}'

    make_file(invite, f'Invitation from {name}', f'invites/{file_name}')

    return invite.get('invite_code')

@app.post('/register')
def register_post():
    name = request.query.name
    memberList = json.loads(members())
    print(memberList)
    if memberList['names'].get(name) is not None:
        abort(401, "Name in use")

    body = json.loads(request.body.getvalue())
    invite_code = body.get('invite').get('code')
    inv_bytes = sha256(invite_code.encode())
    sig_bytes = bytes.fromhex(body.get('hexSig'))
    pubkey_bytes = bytes.fromhex(body.get('pubKey'))
    verified = schnorr_verify(inv_bytes, pubkey_bytes, sig_bytes)

    if not verified:
        abort(400, "Invalid Signature")

    invites = load_dir('invites')

    invite = None
    for invite_file in invites:
        if (invite_file.metadata.get('invite_code') == invite_code):
            invite = invite_file

    if invite is None:
        abort(500, "Invite not found")

    filename = invite.metadata['filename']
    update_file({ 'member': name }, f'invites/{filename}')
    os.rename(f'invites/{filename}', f'invites/completed/{filename}')

    os.makedirs(f'u/{name}', exist_ok=True)

    # Eventually, registering a user on the Solar system will give
    # them a basic account on the server, from which they can gain
    # shell access and host a page.

    # I'll probably leverage Alchemy to make that happen. For now,
    # This uses 'sup' -- https://sup.dyne.org/ to make the user, but
    # the account would be disabled until given a password.

    # subprocess.run(['sup', 'useradd', '-m', name])

    member = {
        "name": name,
        "public_key": body.get('pubKey'),
        "joined": round(datetime.now().timestamp()),
        "class": "member",
        "station": STATION
    }

    make_file(member, f'This file represents the membership of {name} at {STATION}', f'members/{name}')

    return json.dumps(member)

@app.post('/upload')
def invite_post():
    name = request.query.name
    nonce = nonces.pop(name)
    if (nonce is None):
        abort(500, "Nonce not found")

    nonce_bytes = sha256(nonce.encode())
    pubkey = request.forms.get('public_key')
    pubkey_bytes = bytes.fromhex(pubkey)
    sig_bytes = bytes.fromhex(request.forms.get('sig'))
    verified = schnorr_verify(nonce_bytes, pubkey_bytes, sig_bytes)

    if not verified:
        abort(401, "Verification failed")

    events = []

    # Processing the image
    image = request.files.get('icon')
    if image:
        events.append(newFileEvent(pubkey, name, image))
    
    print(request.forms.keys())
    hasLyrics = request.forms.get('hasLyrics')
    if hasLyrics is not None:
        lyrics = request.forms.getall('formLyrics')

    for key in request.files.keys():
        files = request.files.getall(key)

        for file in files:
            events.append(newFileEvent(pubkey, name, file))
            #if hasLyrics is not None:
            #    # Might include these in the event post
            #    print('lyrics', lyrics[i])

    return json.dumps(events)

@app.get('/.well-known/nostr.json')
def members():
    member_cards = load_dir('members')
    memberDictionary = {
        'names': {},
        'admins': []
    }

    for card in member_cards:
        memberDictionary['names'][card.metadata['name']] = card.metadata.get('public_key')

        if card.metadata['class'] == "admin":
            memberDictionary['admins'].append(card.metadata.get('public_key'))

    return json.dumps(memberDictionary)

# Display the art as the server loads
with open('assets/art.txt', 'r') as art:
    for line in art.readlines():
        print(line, end="")

# Make sure the members/ dir exists
os.makedirs('members', exist_ok=True)

# Run the server!
app.run(host='localhost', port=PORT, debug=True)
