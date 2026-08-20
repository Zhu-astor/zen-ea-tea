// Wishlist entry point. app-embed.liquid loads this file and nothing else; the button
// and the app proxy client are its dependencies, not the theme's.
//
// The server decides whether anything renders. A shop that is switched off answers
// `active: false`, and the client renders nothing rather than guessing.

import { loadWishlist } from "./wishlist-api.js";
import { mount, setCount, resolveAppearance } from "./wishlist-button.js";
import { mountModal } from "./wishlist-modal.js";
import { mountPdpButton } from "./wishlist-pdp-button.js";
import { createStore } from "./wishlist-store.js";

async function init() {
  const wishlist = await loadWishlist();

  if (!wishlist) return;

  const store = createStore(wishlist.items);
  const appearance = resolveAppearance(wishlist.appearance);
  const floating = mount(wishlist.appearance);

  store.subscribe(() => setCount(floating, store.size()));
  setCount(floating, store.size());

  const modal = mountModal(store, appearance, wishlist.attribution_token);
  floating.addEventListener("click", modal.open);

  mountPdpButton(store, appearance);
}

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", init);
} else {
  init();
}
