<!DOCTYPE HTML>
<!--
	Lens by Pixelarity
	pixelarity.com | hello@pixelarity.com
	License: pixelarity.com/license
-->
% setdefault('static_path', '/static/')

<html>
	<head>
		<title>Solar</title>
		<meta charset="utf-8" />
		<meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no" />
		<link rel="stylesheet" href="{{ static_path }}assets/css/main.css" />
		<noscript><link rel="stylesheet" href="{{ static_path }}assets/css/noscript.css" /></noscript>
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
						<h1 style="letter-spacing: 0.15em;"> S<span style="color: gold;">O</span>LAR </h1>
						<p> Solar is a framework for interoperable social media platforms with a single account. This system is invite-only, so you'll need to find me in meatspace if you want an account here.</p>
						<p>Also, since it's open source and decentralized, you're free to host it yourself and publish your posts from one system to another.</p>
						<p id="space"><b style="cursor: pointer" onclick={interstellar()}>Interstellar, man!</b></p>
						<ul class="icons">
							<li><a href="https://credenso.cafe" class="icon solid fa-home"><span class="label">Home</span></a></li>
							<li><a href="https://github.com/Credenso/solar" class="icon brands fa-github"><span class="label">Github</span></a></li>
							<li><a href="https://mastodon.social/@credenso" class="icon brands fa-mastodon"><span class="label">Mastodon</span></a></li>
							<li><a href="mailto:zen@credenso.cafe" class="icon fa-envelope"><span class="label">Email</span></a></li>
						</ul>
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

				<!-- Footer -->
					<footer id="footer">
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
