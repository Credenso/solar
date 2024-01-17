<!DOCTYPE HTML>
<!--
	Lens by Pixelarity
	pixelarity.com | hello@pixelarity.com
	License: pixelarity.com/license
-->
% setdefault('static_path', '/static/')
% setdefault('member', None)

<html>
	<head>
		<title>Solar</title>
		<meta charset="utf-8" />
		<meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no" />
		<link rel="stylesheet" href="{{ static_path }}assets/css/main.css" />
		<link rel="icon" href="{{ static_path }}images/solar_icon.png" />
		<noscript><link rel="stylesheet" href="{{ static_path }}assets/css/noscript.css" /></noscript>
		<script>
			//// Persist into localStorage
			//const cookies = document.cookie.split('=')
			//if (cookies[0] === "secret_key") {
			//	window.localStorage.setItem('nsec', cookies[1])
			//}
		</script>
		<style>
		.hiddenLink {
			display: none;
		}

		 @keyframes space {
			100% { transform: rotate3d(1,1,1,360deg); }
		}
		</style>
	</head>
	<body class="is-preload-0 is-preload-1 is-preload-2">

		<!-- Main -->
			<div id="main">
				<!-- Header -->
					<header id="header">
						<a href="/"><h1 style="letter-spacing: 0.15em;"> S<span style="color: gold; text-shadow: 0 0 1em;">O</span>LAR </h1></a>
			% if defined('base'):
				{{ !base }}
			% else:
					% if member:
						<h3>You are signed in as {{ member.get('name') }}. <a href="/logout">Sign out</a></h3>
						<hr>
						<h2>Hi {{ member.get('display_name') or member.get('name') }}!</h2>
						% if member.get('links'):
						<p>Here are some links to other features that come with your account.</p>
							% for link in member.get('links'):
								<a target="_blank" href="{{ link[1] }}">{{ link[0] }}</a><br>
							% end
						<hr/>
						% end
							<p>Select one of the available apps below, and then press Enter or tap the main image to continue.</p>
					% else:
						<p><a href="/login">Sign In</a></p>
						<p> Solar is a framework for interoperable social media platforms with a single account. This system is invite-only, so you'll need to find me in meatspace if you want an account here.</p>
						<p>Also, since it's open source and decentralized, you're free to host it yourself and publish your posts from one system to another.</p>
						<p id="space"><b style="cursor: pointer" onclick={interstellar()}>Interstellar, man!</b></p>
					% end
					</header>

				<!-- Thumbnail -->
					<section id="thumbnails">
						% if (len(potions) > 0):
							% for potion in potions:
								<article>
									<a class="thumbnail" href="{{ potion['image_full'] }}"><img src="{{ potion['image_thumb'] }}" alt="" /></a>
									<h2>{{ potion['name'] }}</h2>
									<p>{{ potion['description'] }}</p>
									<a class="hiddenLink" href={{ potion['path'] }}></a>
								</article>
							% end
						% else:
							<article>
								<a class="thumbnail" href="{{ static_path }}images/fulls/01.jpg" data-position="left center"><img src="{{ static_path }}images/thumbs/01.jpg" alt="" /></a>
								<h2>Diam tempus accumsan</h2>
								<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit.</p>
							</article>
						% end

					</section>
			% end

				<!-- Footer -->
					<footer id="footer">
						<ul class="icons">
							<li><a href="https://credenso.cafe" class="icon solid fa-home"><span class="label">Home</span></a></li>
							<li><a href="https://github.com/Credenso/solar" class="icon brands fa-github"><span class="label">Github</span></a></li>
							<li><a href="https://mastodon.social/@credenso" class="icon brands fa-mastodon"><span class="label">Mastodon</span></a></li>
							<li><a href="mailto:zen@credenso.cafe" class="icon fa-envelope"><span class="label">Email</span></a></li>
						</ul>
						<ul class="copyright">
							<li><a href="https://credenso.cafe">&copy;redenso</a></li>
						</ul>
					</footer>

			</div>
			<script>
				let clicked = false
				const interstellar = async () => {
					document.querySelector('#space').style.visibility = "hidden"
					if (clicked) return;
					clicked = true;
					document.querySelector('html').style.backgroundImage = "url('{{ static_path }}images/tesseract.jpg')"
					//let clickbox = document.createElement('div')
					//clickbox.style="width: 4em; height: 4em; position: absolute; top: 50%; left: 50%; transform: translate(-12em, 12em); background-color: blue;"
					//document.body.appendChild(clickbox)
					const audio = new Audio("{{ static_path }}assets/audio/Time.mp3")
					audio.onloadedmetadata = () => {
						const main = document.querySelector('div#main')
						const image = document.querySelector('div.image')
						const nav = document.querySelector('div.inner')
						const caption = document.querySelector('div.caption')

						main.style.animation = `space ${audio.duration}s ease-in-out`
						if (image) {
							image.style.animation = `space ${audio.duration}s ease-in`
						}

						if (nav) {
							nav.style.animation = `space ${audio.duration}s linear`
						}

						if (caption) {
							caption.style.animation = `space ${audio.duration}s backwards`
						}

						audio.play()
					}
				}
			</script>

		<!-- Scripts -->
			<script src="{{ static_path }}assets/js/jquery.min.js"></script>
			<script src="{{ static_path }}assets/js/browser.min.js"></script>
			<script src="{{ static_path }}assets/js/breakpoints.min.js"></script>
			<script src="{{ static_path }}assets/js/main.js"></script>

	</body>
</html>
