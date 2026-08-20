// Restores the hero scroll-zoom effect from Ippodo's original bundle.js, adapted to be
// safe for any source image aspect ratio.
//
// bundle.js's original handler animates raw background-size percentages on TWO layer
// types at different speeds: .p-top-hero__item--main grows by 100+scrollTop/50 (slow),
// .p-top-hero__item--front grows by 100+scrollTop/3 (fast, ~17x the main layer's rate).
// The front layers are background-images anchored at their own outer edge, so growing
// their background-size makes the illustrated content expand PAST that edge and out of
// the hero box's overflow:hidden clipping — visually: grows bigger while sliding off
// toward the edge, until it's entirely outside the box (reads as "disappears"), not
// "grows toward the center." That only looks right when the source is a WIDE image
// (confirmed against the pristine ippodo_clone: a full illustrated street scene, with
// the two front layers being separate transparent PNGs of figures drawn only on the
// left/right edges — full writeup in zen-fixes.css). Our replacement hero image
// (m240130.jpg) was a 812x1426 PORTRAIT photo — the original formula inflated it to ~4x
// the container height, so only its top sliver showed, i.e. the hero rendered as an
// empty white box.
//
// Fix, in two parts:
// - .p-top-hero__item--main: zen-fixes.css sets background-size:cover as the permanent
//   baseline (correct for any aspect ratio), and this handler animates a CSS
//   transform:scale on top of that instead of touching background-size — composes
//   safely with cover regardless of the source image's shape.
// - .p-top-hero__item--front-left/-right (the six drink illustrations): these are
//   discrete <img> elements, not one zoomable background-image, so "grows and slides
//   past the edge until gone" is reproduced directly with three animated properties
//   instead of relying on the background-size illusion: scale up, translateX AWAY from
//   center (toward whichever edge that layer sits on), and opacity down to 0 — capped
//   at FRONT_FADE_DISTANCE of scroll so they're fully gone well before the hero itself
//   scrolls out of view, rather than continuing to animate indefinitely.
//
// Runs on window "load" (not immediately) because this <script> tag is not deferred
// while jquery-3.6.3.min.js is: if this ran at parse time, jQuery would not exist yet
// and the binding would silently fail to register.
window.addEventListener('load', function () {
  var MAIN_MAX_SCALE = 1.3;
  var MAIN_SCALE_DISTANCE = 4000;

  // FRONT_MAX_SCALE was 1.6: at that scale a drink cluster's own box (already 46% of
  // the hero's height) grows past the hero's own top edge — with position:absolute +
  // bottom:0, the scaled-up box's TOP edge shoots upward faster than its opacity fades,
  // so mid-scroll the (still mostly-opaque) top portion of the cluster ends up poking
  // out above the hero, overlapping the fixed header — reported as the drinks
  // "jumping" to the top corners while scrolling. Unlike the real bundle.js effect
  // (a background-image zoom clipped by its own box, which can never escape its
  // container), these are real <img> elements whose transform:scale grows their actual
  // box, so it has to stay modest enough to stay visually within the hero while it's
  // still visible. Lower max scale + faster fade (shorter distance) means the cluster
  // is mostly transparent well before it grows tall enough to reach the header.
  var FRONT_MAX_SCALE = 1.15;
  var FRONT_MAX_TRANSLATE_PX = 160;
  var FRONT_FADE_DISTANCE = 320;

  function applyHeroZoom() {
    var scrollTop = jQuery(window).scrollTop();

    var mainScale = Math.min(MAIN_MAX_SCALE, 1 + scrollTop / MAIN_SCALE_DISTANCE);
    jQuery('.p-top-hero__item--main').css({
      transform: 'scale(' + mainScale + ')'
    });

    var t = Math.min(1, scrollTop / FRONT_FADE_DISTANCE);
    var frontScale = 1 + t * (FRONT_MAX_SCALE - 1);
    var translate = t * FRONT_MAX_TRANSLATE_PX;
    var opacity = 1 - t;

    jQuery('.p-top-hero__item--front-left').css({
      transform: 'scale(' + frontScale + ') translateX(-' + translate + 'px)',
      opacity: opacity
    });
    jQuery('.p-top-hero__item--front-right').css({
      transform: 'scale(' + frontScale + ') translateX(' + translate + 'px)',
      opacity: opacity
    });
  }

  jQuery(window).on('scroll', applyHeroZoom);
  applyHeroZoom();
});
