document.addEventListener("DOMContentLoaded", function() {
    // These selectors account for the varied ways in which themes are implemented
    const SELECTORS = {
        addToCart: [
            '[data-amp-add-to-cart]',
            'form[action*="/cart/add"] [type="submit"]',
            'button[name="add"]',
            '.product-form__cart-submit',
            '.add-to-cart'
        ],
        variant: [
            'select[name="id"]',
            'input[name="id"]:checked',
            'input[name="id"][type="hidden"]'
        ],
        buyNowBtn: [
            '.shopify-payment-button',
            '.shopify-payment-button__button',
            'button[name="checkout"]',
            '.dynamic-checkout__button',
        ],
        subscriptionsContainer: [ // Shopify lumps together preorder/subscriptions/try-before-you-buy into Purchase Options
            'product-subscriptions',
            'product-subscriptions__button',
        ]
    };

    function findElement(selectors) {
        return selectors.reduce((found, selector) =>
            found || document.querySelector(selector), null);
    }

    function getInitialVariant() {
        const variantElement = findElement(SELECTORS.variant);
        const form = document.querySelector('form[action*="/cart/add"]');
        return variantElement?.value || form?.dataset?.variantId;
    }

    function waitForConfig(callback, maxAttempts = 100) {
        let attempts = 0;
        function checkConfig() {
            if (typeof AppPreOrdersConfig !== 'undefined' && typeof LiquidPreOrdersConfig !== 'undefined') {
                callback();
            } else if (attempts < maxAttempts) {
                attempts++;
                setTimeout(checkConfig, 250);
            }
        }
        checkConfig();
    }

    function updateOnVariantSelection(variantId) {

        waitForConfig(() => {
            if (!AppPreOrdersConfig?.purchases_enabled) {
                return;
            }

            if (AppPreOrdersConfig?.visibility === 'tagged' &&
                !LiquidPreOrdersConfig?.product_tags?.map(tag => tag.toLowerCase())
                    .includes('preorder-enabled'.toLowerCase())) {
                return;
            }

            const addToCartBtn = findElement(SELECTORS.addToCart);
            const buyNowBtn = findElement(SELECTORS.buyNowBtn);
            const subscriptionsContainer = findElement(SELECTORS.subscriptionsContainer);
            const variant = LiquidPreOrdersConfig?.variants?.[variantId];
            const customPreordersButtonText = AppPreOrdersConfig?.custom_button_copy;
            let preorderComment = document.getElementById('preorder-comment');

            if (!variant || !customPreordersButtonText || !addToCartBtn) {
                return;
            }

            if (subscriptionsContainer) {
                // Always hide the selling plan radio buttons when selling plans are assigned, even when stock level >0
                subscriptionsContainer.style.display = "none";
            }

            const isPreorder = variant.oos &&
                variant.inventory_policy === 'continue';

            if (isPreorder) {
                addToCartBtn.dataset.preorderModified = 'true';
                (addToCartBtn.querySelector('span') || addToCartBtn).textContent = customPreordersButtonText;
                if (buyNowBtn) {
                    buyNowBtn.style.display = "none";
                }
                if (!preorderComment) {
                    preorderComment = document.createElement("div");
                }
                Object.assign(preorderComment, {
                    id: "preorder-comment",
                    style: { textAlign: "center" },
                    innerHTML: `<p>${AppPreOrdersConfig?.product_page_copy || ''}</p>`
                });

                addToCartBtn.insertAdjacentElement('afterend', preorderComment);
            } else if (addToCartBtn.dataset.preorderModified === 'true') {
                addToCartBtn.dataset.preorderModified = 'false';
                (addToCartBtn.querySelector('span') || addToCartBtn).textContent = addToCartBtn.dataset.originalText || "Add to cart";
                if (buyNowBtn) {
                    buyNowBtn.style.display = "block";
                }
                preorderComment?.remove();
            }
        });
    }

    function observeAddToCartButton() {
        const addToCartBtn = findElement(SELECTORS.addToCart);
        if (!addToCartBtn) return;

        const observer = new MutationObserver(() => {
            const currentVariantId = getInitialVariant();
            if (currentVariantId) {
                observer.disconnect();
                updateOnVariantSelection(currentVariantId);
                observer.observe(addToCartBtn, { childList: true, subtree: true, characterData: true });
            }
        });

        observer.observe(addToCartBtn, { childList: true, subtree: true, characterData: true });
    }

    const addToCartBtn = findElement(SELECTORS.addToCart);
    if (addToCartBtn) {
        addToCartBtn.dataset.originalText = addToCartBtn.textContent;

        const initialVariantId = getInitialVariant();
        if (initialVariantId) {
            updateOnVariantSelection(initialVariantId);
        }

        document.addEventListener('change', function(event) {
            const variantSelector = event.target.closest('select[name="id"], input[name="id"]');
            if (variantSelector) {
                updateOnVariantSelection(variantSelector.value);
            }
        });

        observeAddToCartButton();
    }
});