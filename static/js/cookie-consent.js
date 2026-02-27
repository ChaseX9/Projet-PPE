/**
 * Cookie Consent Banner Management
 * GDPR-compliant cookie consent with localStorage persistence
 */

(function () {
    'use strict';

    const CONSENT_KEY = 'capinvest_cookie_consent';
    const CONSENT_VERSION = '1.0';

    // Check if consent has already been given
    function hasConsent() {
        const consent = localStorage.getItem(CONSENT_KEY);
        if (!consent) return null;

        try {
            const parsed = JSON.parse(consent);
            return parsed.version === CONSENT_VERSION ? parsed : null;
        } catch {
            return null;
        }
    }

    // Save consent preferences
    function saveConsent(preferences) {
        const consentData = {
            version: CONSENT_VERSION,
            timestamp: new Date().toISOString(),
            essential: true,  // Always true, required for the app
            preferences: preferences.preferences || false,
            analytics: preferences.analytics || false,
        };

        localStorage.setItem(CONSENT_KEY, JSON.stringify(consentData));

        // Update backend if user is authenticated
        if (window.api && window.api.isAuthenticated()) {
            window.api.post('/api/user/consent', {
                cookies_consent: preferences.preferences || false
            }).catch(err => console.warn('Could not sync consent with backend:', err));
        }

        return consentData;
    }

    // Show cookie banner
    function showCookieBanner() {
        const banner = document.createElement('div');
        banner.id = 'cookie-consent-banner';
        banner.innerHTML = `
            <div style="
                position: fixed;
                bottom: 0;
                left: 0;
                right: 0;
                background: linear-gradient(135deg, #2c3e50 0%, #3498db 100%);
                color: white;
                padding: 1.5rem;
                box-shadow: 0 -2px 10px rgba(0,0,0,0.2);
                z-index: 9999;
                display: flex;
                align-items: center;
                justify-content: space-between;
                flex-wrap: wrap;
                gap: 1rem;
            ">
                <div style="flex: 1; min-width: 300px;">
                    <p style="margin: 0; font-size: 1rem; line-height: 1.5;">
                        🍪 <strong>Ce site utilise des cookies</strong><br>
                        Nous utilisons des cookies essentiels pour assurer le fonctionnement du site et des cookies optionnels pour améliorer votre expérience.
                        <a href="/politique_confidentialite.html" style="color: #ffd700; text-decoration: underline;">En savoir plus</a>
                    </p>
                </div>
                <div style="display: flex; gap: 1rem; flex-wrap: wrap;">
                    <button onclick="window.cookieConsent.acceptEssential()" style="
                        background: transparent;
                        border: 2px solid white;
                        color: white;
                        padding: 0.75rem 1.5rem;
                        border-radius: 4px;
                        cursor: pointer;
                        font-size: 1rem;
                        font-weight: 600;
                        transition: all 0.3s;
                    " onmouseover="this.style.background='rgba(255,255,255,0.1)'" onmouseout="this.style.background='transparent'">
                        Accepter uniquement les essentiels
                    </button>
                    <button onclick="window.cookieConsent.acceptAll()" style="
                        background: #27ae60;
                        border: none;
                        color: white;
                        padding: 0.75rem 1.5rem;
                        border-radius: 4px;
                        cursor: pointer;
                        font-size: 1rem;
                        font-weight: 600;
                        transition: all 0.3s;
                        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
                    " onmouseover="this.style.background='#2ecc71'" onmouseout="this.style.background='#27ae60'">
                        Accepter tous les cookies
                    </button>
                </div>
            </div>
        `;
        document.body.appendChild(banner);
    }

    // Hide banner
    function hideBanner() {
        const banner = document.getElementById('cookie-consent-banner');
        if (banner) {
            banner.style.transition = 'opacity 0.3s';
            banner.style.opacity = '0';
            setTimeout(() => banner.remove(), 300);
        }
    }

    // Public API
    window.cookieConsent = {
        init: function () {
            const consent = hasConsent();
            if (!consent) {
                // Show banner only if no consent exists
                setTimeout(showCookieBanner, 1000);  // Small delay for better UX
            }
        },

        acceptEssential: function () {
            saveConsent({ preferences: false, analytics: false });
            hideBanner();
        },

        acceptAll: function () {
            saveConsent({ preferences: true, analytics: true });
            hideBanner();
        },

        getConsent: function () {
            return hasConsent();
        },

        revoke: function () {
            localStorage.removeItem(CONSENT_KEY);
            showCookieBanner();
        }
    };

    // Auto-initialize on page load
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', window.cookieConsent.init);
    } else {
        window.cookieConsent.init();
    }
})();
