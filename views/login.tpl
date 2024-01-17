% rebase('index.tpl')
% setdefault('static_path', '/static/')
% setdefault('error', None)
% setdefault('redir', None)


% if error:
	<div class="error box"> {{ error }} </div>
% end

<div class="box">
	<form method="POST">
		<label for="name">Name:</label>
		<input type="text" id="name" name="name">
		<br/>
		<label for="name">Password:</label>
		<input type="password" id="password" name="password">
		<input type="hidden" id="redirect" name="redirect" value="{{ redir }}">
		<br/>
		<button>Log In</button>
	</form>
</div>
<section id="thumbnails">
	<article>
		<a class="thumbnail" href="{{ static_path }}images/dawn.jpg" data-position="center center"><img src="{{ static_path }}images/thumbs/01.jpg" alt="" /></a>
		<h2>Login Page</h2>
		<p>Are you really who you say you are?</p>
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
	const redirect = document.getElementById('redirect').value
	
	if (redirect === "") {
		if (document.referrer === window.location.href) {
			document.getElementById('redirect').value = "/"
		} else {
			document.getElementById('redirect').value = document.referrer
		}
	}
</script>
