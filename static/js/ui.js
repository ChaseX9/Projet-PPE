/**
 * CapInvest UI System
 * High-end custom Modals and Toasts
 */

const UI = {
    // Current resolve function for active confirm modal
    _confirmResolve: null,

    /**
     * Initialize UI elements in DOM
     */
    init() {
        if (!document.getElementById('modal-overlay')) {
            const overlay = document.createElement('div');
            overlay.id = 'modal-overlay';
            overlay.className = 'modal-overlay';
            overlay.innerHTML = `
                <div class="custom-modal">
                    <div class="modal-icon" id="modal-icon"></div>
                    <h3 class="modal-title" id="modal-title"></h3>
                    <p class="modal-message" id="modal-message"></p>
                    <div class="modal-footer" id="modal-footer"></div>
                </div>
            `;
            document.body.appendChild(overlay);
        }

        if (!document.getElementById('toast-container')) {
            const container = document.createElement('div');
            container.id = 'toast-container';
            container.className = 'toast-container';
            document.body.appendChild(container);
        }

        // Initialize Legal Widget
        this._initLegalWidget();

        // Global override for window.alert (non-blocking)
        window.alert = (msg) => this.alert(msg);
    },

    /**
     * Initialize the floating legal widget
     * @private
     */
    _initLegalWidget() {
        if (document.getElementById('legal-widget')) return;

        // Skip legal widget on login/registration page (DOM-based detection is most reliable)
        if (document.getElementById('login-card') || document.getElementById('register-card')) {
            return;
        }

        const widget = document.createElement('div');
        widget.id = 'legal-widget';
        widget.className = 'legal-widget-container';
        widget.innerHTML = `
            <div class="legal-widget-popup">
                <span class="legal-widget-title">Informations Légales</span>
                <div class="legal-widget-links">
                    <a href="/mentions_legales.html" class="legal-widget-link">
                        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line><polyline points="10 9 9 9 8 9"></polyline></svg>
                        Mentions Légales
                    </a>
                    <a href="/politique_confidentialite.html" class="legal-widget-link">
                        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect><path d="M7 11V7a5 5 0 0 1 10 0v4"></path></svg>
                        Confidentialité
                    </a>
                </div>
                <div class="legal-widget-footer">
                    CapInvest © ${new Date().getFullYear()}. Plateforme de conseil.
                </div>
            </div>
            <div class="legal-widget-trigger" title="Infos Légales">
                <img src="/static/images/capinvest_logo.png" alt="CapInvest Logo">
            </div>
        `;
        document.body.appendChild(widget);

        // Toggle on click for mobile
        const trigger = widget.querySelector('.legal-widget-trigger');
        trigger.addEventListener('click', (e) => {
            if (window.innerWidth <= 768) {
                widget.classList.toggle('active');
                e.stopPropagation();
            }
        });

        document.addEventListener('click', () => {
            widget.classList.remove('active');
        });
    },

    /**
     * Show a custom alert modal
     */
    alert(message, title = "CapInvest", type = "info") {
        return new Promise((resolve) => {
            this.init();
            const overlay = document.getElementById('modal-overlay');
            const iconEl = document.getElementById('modal-icon');
            const titleEl = document.getElementById('modal-title');
            const msgEl = document.getElementById('modal-message');
            const footerEl = document.getElementById('modal-footer');

            // Set Icon based on type
            let iconColor = "var(--primary)";
            let svg = "";
            if (type === "success") {
                iconColor = "var(--success)";
                svg = `<svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="${iconColor}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>`;
            } else if (type === "error") {
                iconColor = "var(--danger)";
                svg = `<svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="${iconColor}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><line x1="15" y1="9" x2="9" y2="15"></line><line x1="9" y1="9" x2="15" y2="15"></line></svg>`;
            } else {
                svg = `<svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="${iconColor}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="16" x2="12" y2="12"></line><line x1="12" y1="8" x2="12.01" y2="8"></line></svg>`;
            }

            iconEl.innerHTML = svg;
            iconEl.style.background = `rgba(${type === 'error' ? '200, 75, 75' : (type === 'success' ? '107, 155, 110' : '74, 144, 164')}, 0.1)`;
            titleEl.textContent = title;
            msgEl.textContent = message;
            footerEl.innerHTML = `<button class="modal-btn modal-btn-confirm">D'accord</button>`;

            overlay.classList.add('active');

            footerEl.querySelector('.modal-btn-confirm').onclick = () => {
                overlay.classList.remove('active');
                resolve();
            };
        });
    },

    /**
     * Show a custom confirm modal
     */
    confirm(message, title = "Confirmation", dangerous = false) {
        return new Promise((resolve) => {
            this.init();
            const overlay = document.getElementById('modal-overlay');
            const iconEl = document.getElementById('modal-icon');
            const titleEl = document.getElementById('modal-title');
            const msgEl = document.getElementById('modal-message');
            const footerEl = document.getElementById('modal-footer');

            const iconColor = dangerous ? "var(--danger)" : "var(--primary)";
            const svg = dangerous
                ? `<svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="${iconColor}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path><line x1="12" y1="9" x2="12" y2="13"></line><line x1="12" y1="17" x2="12.01" y2="17"></line></svg>`
                : `<svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="${iconColor}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"></path><line x1="12" y1="17" x2="12.01" y2="17"></line></svg>`;

            iconEl.innerHTML = svg;
            iconEl.style.background = dangerous ? 'rgba(200, 75, 75, 0.1)' : 'rgba(74, 144, 164, 0.1)';
            titleEl.textContent = title;
            msgEl.textContent = message;

            footerEl.innerHTML = `
                <button class="modal-btn modal-btn-cancel">Annuler</button>
                <button class="modal-btn ${dangerous ? 'modal-btn-danger' : 'modal-btn-confirm'}">${dangerous ? 'Supprimer' : 'Confirmer'}</button>
            `;

            overlay.classList.add('active');

            footerEl.querySelector('.modal-btn-cancel').onclick = () => {
                overlay.classList.remove('active');
                resolve(false);
            };

            footerEl.querySelector(dangerous ? '.modal-btn-danger' : '.modal-btn-confirm').onclick = () => {
                overlay.classList.remove('active');
                resolve(true);
            };
        });
    },

    /**
     * Show a temporary toast notification
     */
    toast(message, type = "success", duration = 4000) {
        this.init();
        const container = document.getElementById('toast-container');
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;

        let icon = "";
        if (type === "success") icon = `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="var(--success)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>`;
        else if (type === "error") icon = `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="var(--danger)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><line x1="15" y1="9" x2="9" y2="15"></line><line x1="9" y1="9" x2="15" y2="15"></line></svg>`;
        else if (type === "warning") icon = `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="var(--warning)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="16" x2="12" y2="12"></line><line x1="12" y1="8" x2="12.01" y2="8"></line></svg>`;
        else icon = `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="var(--primary)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="16" x2="12" y2="12"></line><line x1="12" y1="8" x2="12.01" y2="8"></line></svg>`;

        toast.innerHTML = `
            ${icon}
            <span>${message}</span>
        `;

        container.appendChild(toast);

        setTimeout(() => {
            toast.classList.add('hiding');
            setTimeout(() => toast.remove(), 400);
        }, duration);
    }
};

// Auto-init on script load
document.addEventListener('DOMContentLoaded', () => UI.init());
// Also export for immediate use if needed before DOMContentLoaded (though UI.init() handles it)
window.UI = UI;
