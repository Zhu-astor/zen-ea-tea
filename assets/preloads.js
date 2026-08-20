
    (function() {
      var preconnectOrigins = ["https://cdn.shopify.com","https://extensions.shopifycdn.com"];
      var scripts = ["/cdn/shopifycloud/checkout-web/assets/c1/polyfills.Cwf7UO8Y.js","/cdn/shopifycloud/checkout-web/assets/c1/app.CkuaWA3J.js","/cdn/shopifycloud/checkout-web/assets/c1/esnext-vendor.BPUAVeAN.js","/cdn/shopifycloud/checkout-web/assets/c1/context-browser.HVFGwVvz.js","/cdn/shopifycloud/checkout-web/assets/c1/shipping-methods-grouping.Bpt9aC_O.js","/cdn/shopifycloud/checkout-web/assets/c1/receipt-mapper-load-recovery.DsVvt3T1.js","/cdn/shopifycloud/checkout-web/assets/c1/receipt-eager-mappers.faXL0gUd.js","/cdn/shopifycloud/checkout-web/assets/c1/utilities-errors.DFxGWs1k.js","/cdn/shopifycloud/checkout-web/assets/c1/checkout-proposal.CQvPMZjG.js","/cdn/shopifycloud/checkout-web/assets/c1/helpers-installmentsNotSupportedForAddress.CxMlnEzG.js","/cdn/shopifycloud/checkout-web/assets/c1/consent-manager-shared.DeRe-msU.js","/cdn/shopifycloud/checkout-web/assets/c1/utilities-extension-execution-errors.myo5KOK2.js","/cdn/shopifycloud/checkout-web/assets/c1/extensions-rpc.BSUrRrcQ.js","/cdn/shopifycloud/checkout-web/assets/c1/error-logger-report-graphql-error.CZRVsArp.js","/cdn/shopifycloud/checkout-web/assets/c1/shop-pay-normalizeBuyerDetails.DhQSn8aF.js","/cdn/shopifycloud/checkout-web/assets/c1/NotFound.CiMC9qcZ.js","/cdn/shopifycloud/checkout-web/assets/c1/hydrate.BGxPyctO.js","/cdn/shopifycloud/checkout-web/assets/c1/utilities-browser.hHA6yQnJ.js","/cdn/shopifycloud/checkout-web/assets/c1/utilities-shopCashMoney.D9wfJ1nI.js","/cdn/shopifycloud/checkout-web/assets/c1/color-contrast-colorContrast.CGuYazWI.js","/cdn/shopifycloud/checkout-web/assets/c1/locale-en.CFcOtHmB.js","/cdn/shopifycloud/checkout-web/assets/c1/OnePage.BG9rzQOj.js","/cdn/shopifycloud/checkout-web/assets/c1/hooks-useUnauthenticatedErrorModal.CDeQ3SpH.js","/cdn/shopifycloud/checkout-web/assets/c1/hooks-usePostPurchase.SQIL6DXk.js","/cdn/shopifycloud/checkout-web/assets/c1/components-DeliveryTransition.DrnsGPCk.js","/cdn/shopifycloud/checkout-web/assets/c1/hooks-useShowShopPayOptin.6TREHNe-.js","/cdn/shopifycloud/checkout-web/assets/c1/remember-me-hooks.C9Yqjj20.js","/cdn/shopifycloud/checkout-web/assets/c1/ChangeCompanyLocationLink.BTaYBjNm.js","/cdn/shopifycloud/checkout-web/assets/c1/BillingAddressForm.BvB0thxQ.js","/cdn/shopifycloud/checkout-web/assets/c1/PhoneField.CsYYBxqK.js","/cdn/shopifycloud/checkout-web/assets/c1/ImpressionEventCapture.1WiqtpF2.js","/cdn/shopifycloud/checkout-web/assets/c1/components-RedirectionNotice.module.B6HCeC__.js","/cdn/shopifycloud/checkout-web/assets/c1/Popover.DG_QiAiE.js","/cdn/shopifycloud/checkout-web/assets/c1/Choice.BSv0sxjj.js","/cdn/shopifycloud/checkout-web/assets/c1/Interaction-tracker.DrcX39lu.js","/cdn/shopifycloud/checkout-web/assets/c1/Checkbox.ZgDZAIrA.js","/cdn/shopifycloud/checkout-web/assets/c1/hooks-useForceShopPayUrl.Q0odMXGB.js","/cdn/shopifycloud/checkout-web/assets/c1/hooks-useEcpSpiDebugLog.DSFGZDeG.js","/cdn/shopifycloud/checkout-web/assets/c1/ShopPayLogo.Sy-snVIJ.js","/cdn/shopifycloud/checkout-web/assets/c1/Monorail-monorailMetric-wallets.Dt0y145E.js","/cdn/shopifycloud/checkout-web/assets/c1/cross-border-hooks.BXj7kBgE.js","/cdn/shopifycloud/checkout-web/assets/c1/EmptyState.BLyiTDqs.js","/cdn/shopifycloud/checkout-web/assets/c1/AutocompleteField-hooks.CTSi5owY.js","/cdn/shopifycloud/checkout-web/assets/c1/PendingShipping.D6IV2rKo.js","/cdn/shopifycloud/checkout-web/assets/c1/components-useVaultedMsiInstallments.DWjyD6oh.js","/cdn/shopifycloud/checkout-web/assets/c1/PaymentIcon.Cten2hZZ.js","/cdn/shopifycloud/checkout-web/assets/c1/shop-cash-context.B8Sog8lu.js","/cdn/shopifycloud/checkout-web/assets/c1/hooks-useGeneralPaymentErrorMessage.BIaLHB7j.js","/cdn/shopifycloud/checkout-web/assets/c1/PaymentLine.DKUfro6v.js","/cdn/shopifycloud/checkout-web/assets/c1/useShopPayButtonClassName.Cm2BR4c-.js","/cdn/shopifycloud/checkout-web/assets/c1/cvv-cvvBridge.vWnAzooy.js","/cdn/shopifycloud/checkout-web/assets/c1/hooks-useFilteredShopPayAvailablePaymentMethods.DQIY9qYJ.js","/cdn/shopifycloud/checkout-web/assets/c1/Section.CR8kKeHv.js","/cdn/shopifycloud/checkout-web/assets/c1/MobileOrderSummary.CjRxJB_k.js","/cdn/shopifycloud/checkout-web/assets/c1/useShopPaySessionTokenStorage.Cra2avCH.js","/cdn/shopifycloud/checkout-web/assets/c1/hooks-useOnePageFormSubmit.jNa0uK4E.js","/cdn/shopifycloud/checkout-web/assets/c1/PaymentButtons.BGluQumR.js","/cdn/shopifycloud/checkout-web/assets/c1/shop-pay-installments-types.DSeSDEMS.js","/cdn/shopifycloud/checkout-web/assets/c1/IncentiveBadge.Bsw5_0gG.js","/cdn/shopifycloud/checkout-web/assets/c1/utils-useViolationsHandler.Dmrr19Wu.js","/cdn/shopifycloud/checkout-web/assets/c1/negotiated-findSelectedDeliveryMethod.D5QWkBNx.js","/cdn/shopifycloud/checkout-web/assets/c1/hooks-payment-button.bcbAjuKb.js","/cdn/shopifycloud/checkout-web/assets/c1/hooks-useStableHostMethodsReferences.Cn6SIHel.js","/cdn/shopifycloud/checkout-web/assets/c1/shop-cash-monorail.CR6NDOrS.js","/cdn/shopifycloud/checkout-web/assets/c1/BillingAddressSelector.DdQpyypE.js","/cdn/shopifycloud/checkout-web/assets/c1/PaymentErrorBanner.Bu_OMWpC.js","/cdn/shopifycloud/checkout-web/assets/c1/Section-SectionStyleOverride.Ai085JEn.js","/cdn/shopifycloud/checkout-web/assets/c1/Switch.DNucle1o.js","/cdn/shopifycloud/checkout-web/assets/c1/hooks-useAvailableShopPromotionDiscounts.BCofz-6V.js","/cdn/shopifycloud/checkout-web/assets/c1/checkout-as-guest-amazon-pay.CVmFSgHT.js","/cdn/shopifycloud/checkout-web/assets/c1/Middot.CXkhIszI.js","/cdn/shopifycloud/checkout-web/assets/c1/EstimatedDeliveryContent.B7pl_dJs.js","/cdn/shopifycloud/checkout-web/assets/c1/ShippingMethodRateLabel.8CS-QCpD.js","/cdn/shopifycloud/checkout-web/assets/c1/shipping-methods-consolidated-included.suOZKFvB.js","/cdn/shopifycloud/checkout-web/assets/c1/ShippingLines.Bhd3hKfh.js","/cdn/shopifycloud/checkout-web/assets/c1/ShipmentBreakdown.BZOPEdBt.js","/cdn/shopifycloud/checkout-web/assets/c1/MerchandiseModal.CbflpZQJ.js","/cdn/shopifycloud/checkout-web/assets/c1/ShippingMethodSelector.-6X33YAt.js","/cdn/shopifycloud/checkout-web/assets/c1/TextArea.B8lMDGJ6.js","/cdn/shopifycloud/checkout-web/assets/c1/SubscriptionPriceBreakdown.BaLChE49.js","/cdn/shopifycloud/checkout-web/assets/c1/StockProblems-StockProblemsLineItemList.BqIl_uCY.js","/cdn/shopifycloud/checkout-web/assets/c1/extensibility-browser-engine.BVIK9Sg4.js","/cdn/shopifycloud/checkout-web/assets/c1/component-RuntimeExtension.CrlV7tjf.js","/cdn/shopifycloud/checkout-web/assets/c1/AnnouncementRuntimeExtensions.BvqsM4Ac.js","/cdn/shopifycloud/checkout-web/assets/c1/QRCode.C6YpDzpm.js","/cdn/shopifycloud/checkout-web/assets/c1/utilities-dates.ChO2GdxN.js","/cdn/shopifycloud/checkout-web/assets/c1/NumberField.Cut7VP83.js","/cdn/shopifycloud/checkout-web/assets/c1/extensions-remote-dom.4HiQnZlH.js","/cdn/shopifycloud/checkout-web/assets/c1/EmailField.jBbi2b1a.js","/cdn/shopifycloud/checkout-web/assets/c1/Sheet.2PGvssMk.js","/cdn/shopifycloud/checkout-web/assets/c1/extension-targets-rendering-extension-targets.BH_7sKvw.js","/cdn/shopifycloud/checkout-web/assets/c1/dist-v4.EwEgHOG0.js","/cdn/shopifycloud/checkout-web/assets/c1/ExtensionsInner.B-9PmgUK.js","/cdn/shopifycloud/checkout-web/assets/c1/adapter-host.DZY-mwce.js","/cdn/shopifycloud/checkout-web/assets/c1/sandbox.C6K77SV1.worker.js","/cdn/shopifycloud/checkout-web/assets/c1/sandbox-2025-07.DpzA6bL0.worker.js","https://extensions.shopifycdn.com/shopifycloud/checkout-web/assets/c1/polyfills-entry-modern.oWckgtZS.worker.js"];
      var styles = ["/cdn/shopifycloud/checkout-web/assets/c1/assets/app.BYT6yYGe.css","/cdn/shopifycloud/checkout-web/assets/c1/assets/grouping.Cray4R9V.css","/cdn/shopifycloud/checkout-web/assets/c1/assets/previous.l6vaLTDB.css","/cdn/shopifycloud/checkout-web/assets/c1/assets/OnePage.BDn7-hvu.css","/cdn/shopifycloud/checkout-web/assets/c1/assets/DeliveryTransition.DhbMYMIx.css","/cdn/shopifycloud/checkout-web/assets/c1/assets/useVaultedMsiInstallments.dhevUZ1f.css","/cdn/shopifycloud/checkout-web/assets/c1/assets/MobileOrderSummary.2B5x30PG.css","/cdn/shopifycloud/checkout-web/assets/c1/assets/useOnePageFormSubmit.tSP6pJcp.css","/cdn/shopifycloud/checkout-web/assets/c1/assets/cvvBridge.CIy8uDiZ.css","/cdn/shopifycloud/checkout-web/assets/c1/assets/Choice.jvH8TQL4.css","/cdn/shopifycloud/checkout-web/assets/c1/assets/RedirectionNotice.B8v_QGNW.css","/cdn/shopifycloud/checkout-web/assets/c1/assets/EmptyState.BEvzDDvy.css","/cdn/shopifycloud/checkout-web/assets/c1/assets/Section.CU18S7Ap.css","/cdn/shopifycloud/checkout-web/assets/c1/assets/PaymentLine.0ZuT82rY.css","/cdn/shopifycloud/checkout-web/assets/c1/assets/Switch.Dq_6Ius6.css","/cdn/shopifycloud/checkout-web/assets/c1/assets/PaymentIcon.CLVwzp6i.css","/cdn/shopifycloud/checkout-web/assets/c1/assets/IncentiveBadge.C5mVOEBf.css","/cdn/shopifycloud/checkout-web/assets/c1/assets/BillingAddressForm.BdwN7V1K.css","/cdn/shopifycloud/checkout-web/assets/c1/assets/useShowShopPayOptin.87JMHPUK.css","/cdn/shopifycloud/checkout-web/assets/c1/assets/PhoneField.uZEuHncj.css","/cdn/shopifycloud/checkout-web/assets/c1/assets/Middot.D7Ujmshx.css","/cdn/shopifycloud/checkout-web/assets/c1/assets/ShippingLines.LcqrKXE1.css","/cdn/shopifycloud/checkout-web/assets/c1/assets/MerchandiseModal.D6OuIVjc.css","/cdn/shopifycloud/checkout-web/assets/c1/assets/EstimatedDeliveryContent.B_THySFF.css","/cdn/shopifycloud/checkout-web/assets/c1/assets/PaymentButtons.BbF1yV61.css","/cdn/shopifycloud/checkout-web/assets/c1/assets/RuntimeExtension.DWkDBM73.css","/cdn/shopifycloud/checkout-web/assets/c1/assets/AnnouncementRuntimeExtensions.DWE5rRxz.css","/cdn/shopifycloud/checkout-web/assets/c1/assets/QRCode.BZ_m5G5a.css","/cdn/shopifycloud/checkout-web/assets/c1/assets/Checkbox.CfwUdlpL.css","/cdn/shopifycloud/checkout-web/assets/c1/assets/Popover.C8uylY0y.css","/cdn/shopifycloud/checkout-web/assets/c1/assets/NumberField.CRpcZnVJ.css","/cdn/shopifycloud/checkout-web/assets/c1/assets/Sheet.BiQjEGaX.css","/cdn/shopifycloud/checkout-web/assets/c1/assets/useShopPaySessionTokenStorage.DfWUBaTh.css"];
      var fontPreconnectUrls = [];
      var fontPrefetchUrls = [];
      var imgPrefetchUrls = ["https://cdn.shopify.com/s/files/1/0531/8718/2743/files/logo_ippodo-en_x320.jpg?v=1627554223"];

      function preconnect(url, callback) {
        var link = document.createElement('link');
        link.rel = 'dns-prefetch preconnect';
        link.href = url;
        link.crossOrigin = '';
        link.onload = link.onerror = callback;
        document.head.appendChild(link);
      }

      function preconnectAssets() {
        var resources = preconnectOrigins.concat(fontPreconnectUrls);
        var index = 0;
        (function next() {
          var res = resources[index++];
          if (res) preconnect(res, next);
        })();
      }

      function prefetch(url, as, callback) {
        var link = document.createElement('link');
        if (link.relList.supports('prefetch')) {
          link.rel = 'prefetch';
          link.fetchPriority = 'low';
          link.as = as;
          if (as === 'font') link.type = 'font/woff2';
          link.href = url;
          link.crossOrigin = '';
          link.onload = link.onerror = callback;
          document.head.appendChild(link);
        } else {
          var xhr = new XMLHttpRequest();
          xhr.open('GET', url, true);
          xhr.onloadend = callback;
          xhr.send();
        }
      }

      function prefetchAssets() {
        var resources = [].concat(
          scripts.map(function(url) { return [url, 'script']; }),
          styles.map(function(url) { return [url, 'style']; }),
          fontPrefetchUrls.map(function(url) { return [url, 'font']; }),
          imgPrefetchUrls.map(function(url) { return [url, 'image']; })
        );
        var index = 0;
        function run() {
          var res = resources[index++];
          if (res) prefetch(res[0], res[1], next);
        }
        var next = (self.requestIdleCallback || setTimeout).bind(self, run);
        next();
      }

      function onLoaded() {
        try {
          if (parseFloat(navigator.connection.effectiveType) > 2 && !navigator.connection.saveData) {
            preconnectAssets();
            prefetchAssets();
          }
        } catch (e) {}
      }

      if (document.readyState === 'complete') {
        onLoaded();
      } else {
        addEventListener('load', onLoaded);
      }
    })();
  