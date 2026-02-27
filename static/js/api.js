/**
 * Robo-Advisor API Client
 */
class RoboAPI {
    constructor(baseURL = '') {
        this.baseURL = baseURL;
        this.token = localStorage.getItem('robo_token');
    }

    setToken(token) {
        this.token = token;
        localStorage.setItem('robo_token', token);
    }

    clearToken() {
        this.token = null;
        localStorage.removeItem('robo_token');
    }

    logout() {
        this.clearToken();
        window.location.href = '/login.html';
    }

    isAuthenticated() {
        return !!this.token;
    }

    async fetchWithAuth(endpoint, options = {}) {
        const headers = options.headers || {};
        if (this.token) {
            headers['Authorization'] = `Bearer ${this.token}`;
        }

        const response = await fetch(`${this.baseURL}${endpoint}`, {
            ...options,
            headers
        });

        if (response.status === 401) {
            this.clearToken();
            if (window.location.pathname !== '/login.html') {
                window.location.href = '/login.html';
            }
        }

        return response;
    }

    async handleError(response) {
        let errorMsg = `Request failed with status ${response.status}`;
        try {
            const errorData = await response.json();
            if (errorData.detail) {
                if (Array.isArray(errorData.detail)) {
                    // FastAPI validation errors are often arrays of objects
                    errorMsg = errorData.detail.map(err => {
                        const loc = err.loc ? err.loc.join('.') : 'error';
                        return `${loc}: ${err.msg}`;
                    }).join(', ');
                } else if (typeof errorData.detail === 'string') {
                    errorMsg = errorData.detail;
                } else {
                    errorMsg = JSON.stringify(errorData.detail);
                }
            }
        } catch (e) {
            // Fallback if not JSON
        }
        throw new Error(errorMsg);
    }

    async get(endpoint) {
        const response = await this.fetchWithAuth(endpoint, { method: 'GET' });
        if (!response.ok) return await this.handleError(response);
        return await response.json();
    }

    async post(endpoint, data = null) {
        const options = {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' }
        };
        if (data) {
            options.body = JSON.stringify(data);
        }
        const response = await this.fetchWithAuth(endpoint, options);
        if (!response.ok) return await this.handleError(response);
        return await response.json();
    }

    async patch(endpoint, data = null) {
        const options = {
            method: 'PATCH',
            headers: { 'Content-Type': 'application/json' }
        };
        if (data) {
            options.body = JSON.stringify(data);
        }
        const response = await this.fetchWithAuth(endpoint, options);
        if (!response.ok) return await this.handleError(response);
        return await response.json();
    }

    async put(endpoint, data = null) {
        const options = {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' }
        };
        if (data) {
            options.body = JSON.stringify(data);
        }
        const response = await this.fetchWithAuth(endpoint, options);
        if (!response.ok) return await this.handleError(response);
        return await response.json();
    }

    async delete(endpoint, data = null) {
        const options = {
            method: 'DELETE',
            headers: { 'Content-Type': 'application/json' }
        };
        if (data) {
            options.body = JSON.stringify(data);
        }
        const response = await this.fetchWithAuth(endpoint, options);
        if (!response.ok) return await this.handleError(response);
        return await response.json();
    }

    // Auth
    async register(email, password, fullName = null) {
        const response = await fetch(`${this.baseURL}/auth/register`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password, full_name: fullName })
        });

        if (!response.ok) {
            const error = await response.json();
            let msg = error.detail || 'Registration failed';
            if (Array.isArray(msg)) {
                msg = msg.map(e => {
                    const field = e.loc[e.loc.length - 1];
                    return `${field}: ${e.msg}`;
                }).join('\n');
            }
            throw new Error(msg);
        }

        return await response.json();
    }

    async verifyEmail(token) {
        return await this.get(`/auth/verify?token=${token}`);
    }

    async resendVerification(email) {
        return await this.post('/auth/resend-verification', { email });
    }


    async login(email, password) {
        const response = await fetch(`${this.baseURL}/auth/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password })
        });

        if (!response.ok) {
            const error = await response.json();
            let msg = error.detail || 'Login failed';
            if (Array.isArray(msg)) {
                msg = msg.map(e => e.msg).join('\n');
            }
            throw new Error(msg);
        }

        const data = await response.json();
        this.setToken(data.access_token);
        return data;
    }

    async getMe() {
        const response = await this.fetchWithAuth('/auth/me');
        if (!response.ok) throw new Error('Failed to fetch user');
        return await response.json();
    }

    // Recommendations
    async getRecommendation(data) {
        const response = await this.fetchWithAuth('/api/recommandation', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to get recommendation');
        }

        return await response.json();
    }

    // Portfolios
    async getPortfolios() {
        const response = await this.fetchWithAuth('/api/portfolios/');
        if (!response.ok) throw new Error('Failed to fetch portfolios');
        return await response.json();
    }

    async getPortfolio(id) {
        const response = await this.fetchWithAuth(`/api/portfolios/${id}`);
        if (!response.ok) throw new Error('Failed to fetch portfolio');
        return await response.json();
    }

    async getExplorerAssets() {
        return await this.get('/api/explorer/assets');
    }
}

const api = new RoboAPI();
