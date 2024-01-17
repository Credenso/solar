from ingredients.bottle import Bottle, run, request, response, redirect, template, abort, static_file
from ingredients.schnorr import sha256, schnorr_verify, schnorr_sign, pubkey_gen_from_hex
from ingredients.files import load_dir, make_file, update_file
from ingredients import members
import os
import json
import hashlib
import secrets
from urllib import request as url_request
import configparser
from datetime import datetime

# Constants - might put these in a config file
config = configparser.ConfigParser()
config.read('.env')
station = config['SOLAR']['STATION']
port = config['SOLAR']['PORT']

# Application Setup
app = Bottle()

on_the_menu = []
from potions.blog import app as blog
from potions.ao import app as ao
from potions.greenspots import app as greenspots
from potions.vibes import app as vibes
on_the_menu.append(blog)
on_the_menu.append(ao)
on_the_menu.append(greenspots)
on_the_menu.append(vibes)

# We rack the potions one by one so that the menu
# can easily be modified by a shell script.
potion_rack = []
for potion in on_the_menu:
    app.mount(potion.path, potion.app)
    potion_rack.append({
        'name': potion.name,
        'path': potion.path,
        'description': potion.description,
        'image_full': potion.image_full,
        'image_thumb': potion.image_thumb
        })


nonces = {}

# LNBits registration - should maybe be put elsewhere
def lnbits_registration(name):
    # Do not leak admin_id or the api key
    data = {
            'admin_id': 'e4b2428e32a14539b19f4422b07f49b3', 
            'wallet_name': f"{name.capitalize()}'s Wallet", 
            'user_name': name
            }

    headers = {
            'Content-Type': 'application/json',
            'X-Api-Key': '3c658537d952491e8060da84176d19be'
            }

    req = url_request.Request('https://ln.credenso.cafe/usermanager/api/v1/users',
                           json.dumps(data).encode(),
                           headers)

    urlopen = url_request.urlopen(req)
    data = json.loads(urlopen.read())
    wallet_url = f'https://ln.credenso.cafe/wallet?usr={data.get("id")}'
    return wallet_url

# TODO - Integrate https://github.com/rndusr/torf
def newFileEvent(pubkey, name, file):

    if file.content_type.startswith('image'):
        path = f'u/{name}/images'
        # Create the blurhash here

    elif file.content_type.startswith('audio'):
        path = f'u/{name}/audio'
    elif file.content_type.startswith('markdown'):
        path = f'u/{name}/posts'
    else:
        path = f'u/{name}/assets'

    try:
        os.makedirs("data/" + path, exist_ok=True)
        file.save("data/" + path)
    except IOError as e:
        print('error: ', e)
        pass

    e = {
        'content': file.filename,
        'pubkey': pubkey,
        'kind': 1063,
        'created_at': round(datetime.now().timestamp()),
        'tags': [
            ['url',f'https://{station}/{path}/{file.filename}'],
            ['m',file.content_type],
            ['x', sha256(file.file.read()).hex()]
        ]
    }

    return e;

active_members = members.MembersList('data/members/active')
sessions = {}

# This function returns True if the pubkey has an
# existing session that matches the key, and False 
# otherwise. It also refreshes the validated session, 
# and cleans any that have been inactive for more 
# than a day

def validate_session(pubkey, session_key):
    now = datetime.now()

    # Clean up sessions older than 10 hours
    for existing_session in sessions.items():
        if (now - existing_session[1]['created']).seconds > 36000:
            del sessions[existing_session[0]]

    member = active_members.get(pubkey)
    session = sessions.get(member.get('name'))

    if session is None:
        return False

    if session['key'] == session_key:
        session['created'] = now
        return True
    else:
        return False

@app.get('/register')
def register_get():
    return template("register.tpl")

@app.post('/register')
def register_post():
    name = request.forms.get('name')
    email = request.forms.get('email')
    nsec = request.forms.get('nsec')
    wallet_url = lnbits_registration(name)

    member_data = {
        "name": name,
        "email": email,
        "secret_key": nsec or None,
        "realms": ["private"],
        "links": [
            ["Credenso Wallet", wallet_url]
        ]
    }

    active_members.new(member_data, name)

    # Log a user in when they register
    nsec = active_members.login(name, name)
    key = secrets.token_hex(24)
    sessions[name] = { "key": key, "created": datetime.now() }
    response.set_cookie('nsec', nsec, maxage=36000, path="/")
    response.set_cookie('npub', pubkey_gen_from_hex(nsec).hex(), maxage=36000, path="/")
    response.set_cookie('session', key, maxage=36000, path="/")

    return redirect('/')


    
@app.get('/login')
def login_get():
    return template("login.tpl")

@app.post('/login')
def login_post():
    name = request.forms.get('name')
    password = request.forms.get('password')
    result = active_members.login(name, password)
    print('name', name)
    redir = request.forms.get('redirect')
    if result:
        key = secrets.token_hex(24)
        sessions[name] = { "key": key, "created": datetime.now() }
        response.set_cookie('nsec', result, maxage=36000, path="/")
        response.set_cookie('npub', pubkey_gen_from_hex(result).hex(), maxage=36000, path="/")
        response.set_cookie('session', key, maxage=36000, path="/")

        prev = request.forms.get('redirect')
        return redirect(prev)

    return template("login.tpl", error="Login Failed", redir=redir)

@app.get('/logout')
def logout():
    response.delete_cookie('nsec', path="/")
    response.delete_cookie('npub', path="/")
    response.delete_cookie('session', path="/")
    return redirect('/')

# TODO: Deprecate this in favor of sessions
@app.get('/nonce')
def invite_get():
    name = request.query.name
    nonce = secrets.token_hex(24)
    nonces[name] = nonce
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

#@app.post('/register')
#def register_post():
#    name = request.query.name
#    memberList = json.loads(members())
#    if memberList['names'].get(name) is not None:
#        abort(401, "Name in use")
#
#    body = json.loads(request.body.getvalue())
#    invite_code = body.get('invite').get('code')
#    inv_bytes = sha256(invite_code.encode())
#    sig_bytes = bytes.fromhex(body.get('hexSig'))
#    pubkey_bytes = bytes.fromhex(body.get('pubKey'))
#    verified = schnorr_verify(inv_bytes, pubkey_bytes, sig_bytes)
#
#    if not verified:
#        abort(400, "Invalid Signature")
#
#    invites = load_dir('invites')
#
#    invite = None
#    for invite_file in invites:
#        if (invite_file.metadata.get('invite_code') == invite_code):
#            invite = invite_file
#
#    if invite is None:
#        abort(500, "Invite not found")
#
#    filename = invite.metadata['filename']
#    update_file({ 'member': name }, f'invites/{filename}')
#    os.rename(f'invites/{filename}', f'invites/completed/{filename}')
#
#    os.makedirs(f'u/{name}', exist_ok=True)
#
#    # Eventually, registering a user on the Solar system will give
#    # them a basic account on the server, from which they can gain
#    # shell access and host a page.
#
#    # I'll probably leverage Alchemy to make that happen. For now,
#    # This uses 'sup' -- https://sup.dyne.org/ to make the user, but
#    # the account would be disabled until given a password.
#
#    # subprocess.run(['sup', 'useradd', '-m', name])
#
#    # This is for registering with a wallet on lnbits
#    url = "https://ln.credenso.cafe/usermanager/api/v1/users"
#
#    data = {
#            'admin_id': 'e4b2428e32a14539b19f4422b07f49b3', 
#            'wallet_name': "Test User's Wallet", 
#            'user_name': 'test'
#            }
#
#    headers = {
#            'X-Api-Key': '3c658537d952491e8060da84176d19be', 
#            'Content-Type': 'application/json'
#            }
#
#
#    req = urllib.request.Request(url,
#                           json.dumps(data).encode(),
#                           headers)
#
#    urlopen = urllib.request.urlopen(req)
#    response = urlopen.read()
#
#    member = {
#        "name": name,
#        "public_key": body.get('pubKey'),
#        "joined": round(datetime.now().timestamp()),
#        "class": "member",
#        "station": station
#    }
#
#    make_file(member, f'This file represents the membership of {name} at {station}', f'data/members/{name}')
#
#    return json.dumps(member)

@app.post('/new_upload')
def invite_post():
    npub = request.get_cookie('npub')
    if npub:
        member = active_members.get(npub)

        if member is None:
            abort(401, "Member not found")

    else:
        abort(401, "Verification failed")

    #session_key = request.get_cookie('session')
    #if validate_session(npub, session_key) is False:
    #    abort(401, "Session Invalid")

    #logo = request.files.get('logo')
    #print('logo', logo)
    events = []

    for key in request.files.keys():
        files = request.files.getall(key)

        for file in files:
            events.append(newFileEvent(npub, member.get('name'), file))

    return json.dumps(events)

    #name = request.query.name
    #nonce = nonces.pop(name)
    #if (nonce is None):
    #    abort(500, "Nonce not found")

    #nonce_bytes = sha256(nonce.encode())
    #pubkey = request.forms.get('public_key')
    #pubkey_bytes = bytes.fromhex(pubkey)
    #sig_bytes = bytes.fromhex(request.forms.get('sig'))
    #verified = schnorr_verify(nonce_bytes, pubkey_bytes, sig_bytes)

    #if not verified:
    #    abort(401, "Verification failed")

    #events = []

    ## Processing the image
    #image = request.files.get('icon')
    #if image:
    #    events.append(newFileEvent(pubkey, name, image))

    #for key in request.files.keys():
    #    files = request.files.getall(key)

    #    for file in files:
    #        events.append(newFileEvent(pubkey, name, file))

    #return json.dumps(events)

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

    for key in request.files.keys():
        files = request.files.getall(key)

        for file in files:
            events.append(newFileEvent(pubkey, name, file))

    return json.dumps(events)

@app.get('/.well-known/nostr.json')
def list_members():
    member_cards = load_dir('data/members/active')
    memberDictionary = {
        'names': {},
        'admins': []
    }

    for card in member_cards:
        memberDictionary['names'][card.metadata['name']] = card.metadata.get('public_key')

        if "admin" in card.get('realms'):
            memberDictionary['admins'].append(card.metadata.get('public_key'))

    return json.dumps(memberDictionary)

# This handles all the static files in the given system...
# Until we get NGINX to take care of it.
@app.route('/u/<filepath:path>')
def static(filepath):
        return static_file(filepath, root=f'{os.getcwd()}/data/u')

@app.route('/static/<filepath:path>')
def static(filepath):
        return static_file(filepath, root=f'{os.getcwd()}/static')

@app.route('/ao/<filepath:path>')
def static(filepath):
        return static_file(filepath, root=f'/home/zen/Development/ao/dist/')

@app.route('/')
def index():
    npub = request.get_cookie('npub')
    if npub:
        member = active_members.get(npub)
        session_key = request.get_cookie('session')
        validate_session(npub, session_key)
    else:
        member = None


    return template("index.tpl",  potions=potion_rack, member=member)

# Display the art as the server loads
with open('assets/art.txt', 'r') as art:
    for line in art.readlines():
        print(line, end="")

# Make sure the relevant directories exist
os.makedirs('data/members', exist_ok=True)
os.makedirs('data/invites/completed', exist_ok=True)

# Run the server!
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=port, debug=True)
