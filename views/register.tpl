% rebase('index.tpl')
% setdefault('static_path', '/static/')
% setdefault('error', None)
% setdefault('redir', None)

<style>
 	#main {
		width: 30em;
		max-width: 100vw;
	}

	h1 {
		text-align: center;
	}
	
	#info, #registration {
		text-align: left;
	}

	.hidden {
		display: none;
	}

	#bad_name {
		font-size: 0.7em;
		color: red;
	}

	.invalid {
		border: 2px solid red !important;
	}
</style>


% if error:
	<div class="error box"> {{ error }} </div>
% end

<hr>
<div id="info">
<p><b>Welcome to Solar!</b> You're currently at the registration page for
the first iteration of a truly <i title="free, as in 'freedom'" style="cursor: pointer">free</i> social media platform. This project
is very important to me, and I've invested a lot of time into getting everything to a
place where I feel ready to put something out there. That said, the project is still
just a baby. I have <i>a lot</i> of work to do before any of this is ready for
an official release. I've decided that the best way to figure out how to
prioritize the work I do next is to get other people on the platform and start
asking for feedback.</p>

<p>If you want a feature, let me know and I'll do my best to
add it as soon as I can. But first - <b>let's get your account activated!</b></p>

<p>Before we continue, there's a couple of guidelines for your time here:</p> 

<ul>
<li><p><b>Be yourself!</b> Like, actually though. This isn't meant to be an
anonymous platform. If I don't recognize your name, I'll probably email you to
say "hi who are you". I don't want to have anyone on this site that I can't
personally vouch for. Pseudonyms and personas are cool, so long as there's
somewhere in your bio that makes it clear who that persona actually belongs
to.</p>

<li><p><b>Don't lose your password.</b> Your account gives you posting access to all
social media sites on the system. I don't store the password anywhere, so if
you lose it then you lose access to your account.</p>

<li><p><b>Don't abuse your posting privileges.</b> I am personally responsible for
everything that gets posted here. I don't want to tell people what they can or
can't say, but if you're being hateful or spammy then I'll probably take issue
with it.</p> 

<li><p><b>Self-promotion is shameless.</b> If you're an artist, freelancer, 
community organizer, or something similar: please use this site to share
information about what you're doing! I want to support you.</p> 
</ul>
<p>You can learn more about the philosophy behind what I'm building by 
<a href="/blog/post/solar" target="_blank">reading this post.</a>
</p> 

<input id="continue" type="checkbox" style="float: unset" name="continue">
<label for="continue">I get it, let's do the account thing!</label>
</div>

<div id="registration" class="box hidden">
	<h2>Registration</h2>
	<p>When you first make your account, <b>your password will be the same as your username</b>. To update your information: visit The Bus, open the side menu, and click on My Account - you might need to log in first.</p>
	
	<form method="POST">
		<label for="name">Account Name:</label>
		<input type="text" id="name" name="name" placeholder="your account identifier" required />
		<small id="bad_name" class="hidden">Name already taken</small>
		<br/>
		<label for="email">Email:</label>
		<input type="text" id="email" name="email" placeholder="optional, but helpful" />
		<br/>
		<details>
		<summary>Advanced</summary>
		<label for="nsec">Nostr Private Key:</label>
		<input type="text" id="nsec" name="nsec" placeholder="optional, but helpful" />
		</details>
		<br/>
		<button id="register">Register</button>
	</form>
</div>
<section id="thumbnails">
	<article>
		<a class="thumbnail" href="{{ static_path }}images/dawn.jpg" data-position="center center"><img src="{{ static_path }}images/thumbs/01.jpg" alt="" /></a>
		<h2>Solar Registration Page</h2>
		<p>This is the start of something big - I promise.</p>
	</article>
</section>

<style>
	.error {
		background-color: #FFDDDD;
		margin: 1em;
		border-radius: 0.25em;
		padding: 0.5em;
	}

	#thumbnails {
		display: none;
	}
</style>

<script>
	let existing_accounts = {}

	fetch('/.well-known/nostr.json').then(res => res.json().then(accounts => existing_accounts = accounts))

	const cont = () => {
		document.querySelector('#info').classList.add('hidden')
		document.querySelector('#registration').classList.remove('hidden')
	}

	const validate_name = () => {
		const name = document.querySelector('#name').value.toLowerCase().replace(/[^a-z0-9._]/, "")
		document.querySelector('#name').value = name

		console.log('name', name)
		const existing = existing_accounts.names[name] !== undefined

		if (existing) {
			document.querySelector('#name').classList.add('invalid')
			document.querySelector('#bad_name').classList.remove('hidden')
			document.querySelector('#register').disabled = true
		} else {
			document.querySelector('#name').classList.remove('invalid')
			document.querySelector('#bad_name').classList.add('hidden')
			document.querySelector('#register').disabled = false
		}
	}

	document.querySelector('#continue').checked = false
	document.querySelector('#continue').addEventListener('change', cont)

	document.querySelector('#name').addEventListener('input', validate_name)
</script>
