// Authentication helpers

function getAuthHeaders() {
    const token = localStorage.getItem('access_token');
    if (token) {
        return { 'Authorization': `Bearer ${token}` };
    }
    return {};
}

function isAuthenticated() {
    return !!localStorage.getItem('access_token');
}

function getCurrentUser() {
    const userStr = localStorage.getItem('user');
    return userStr ? JSON.parse(userStr) : null;
}

function logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('user');
    window.location.href = 'index.html';
}

function requireAuth() {
    if (!isAuthenticated()) {
        window.location.href = 'index.html';
        return false;
    }
    return true;
}
