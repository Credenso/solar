Lens by Pixelarity
pixelarity.com | hello@pixelarity
License: pixelarity.com/license


Instructions:

	Overview:

		Lens is made up of three primary components:

		- The "main wrapper": The skinny little column on the right. Home to what little
		  "regular" content you may have (header, footer, anything else you want to cram
		  in there), as well as ...

		- The "thumbnails" section: A grid of thumbnails pointing to their respective
		  full size images.

		- The "viewer": Basically the rest of the page, and basically where your full size
		  images will show up when a thumbnail is clicked.

		Note: Only the main wrapper and the thumbnails section are actually present in
		index.html. The viewer will be dynamically created on page load.

	How it works:

		Just add your thumbnails to the thumbnails section in the following format:

			<article>
				<a class="thumbnail" href="path/to/fullsize.jpg">
					<img src="path/to/thumbnail.jpg" alt="" />
				</a>
				<h2>Title</h2>
				<p>Description.</p>
			</article>

		And that's it. Lens will figure out the rest.

	The "data-position" attribute:

		As a full screen experience, the viewer will be subject to changes in its size and,
		consequently, its aspect ratio. Since your full size images are basically applied as
		backgrounds to the viewer itself, this means they'll probably (okay, definitely) get
		cropped. All is not lost, however, as you can use the optional "data-position" attribute
		to control how the full size image is positioned within the viewer. To do this, simply
		add it to your thumbnail's <a> element and set it to any valid "background-position"
		value. For example, this:

			<a class="thumbnail" href="path/to/fullsize.jpg" data-position="top left">...</a>

		... positions this particular full size image in the top left corner of the viewer (as
		opposed to its center, the default), effectively limiting cropping to everything but
		the top left corner.

	Keyboard shortcuts:

		Lens is set up to respond to the following keyboard shortcuts:

		- Left Arrow: Go to previous image.
		- Right Arrow: Go to next image.
		- Up Arrow: Go to image above the current one in the thumbnails section.
		- Down Arrow: Go to image below the current one in the thumbnails section.
		- Space: Go to next image.
		- Escape: Toggle the main wrapper.

		Note: All keyboard shortcuts are disabled when the "xsmall" breakpoint is active
		(since they don't really make a whole lot of sense there).

	Other stuff:

		- The main wrapper can be moved to the left by changing the "misc.main-side" variable
		  in assets/sass/libs/_vars.scss to "left" (and of course recompiling your CSS).

		- Additional tweakable settings can be found at the top of assets/js/main.js, but
		  be aware most of these need to sync with certain Sass variables (see comments
		  for details).