document.addEventListener('DOMContentLoaded', async () => {
    try {
        const response = await fetch('/.auth/me');
        if (!response.ok) return;

        const payload = await response.json();
        const clientPrincipal = payload.clientPrincipal;
        
        if (clientPrincipal && clientPrincipal.userDetails) {
            const email = clientPrincipal.userDetails; // e.g. david.benitez@milicic.com.ar
            const namePart = email.split('@')[0];
            const name = namePart.split('.').map(part => part.charAt(0).toUpperCase() + part.slice(1)).join(' ');
            
            const greetingEl = document.getElementById('userGreeting');
            if (greetingEl) {
                greetingEl.textContent = 'Bienvenido, ' + name;
            }
        }
    } catch (error) {
        console.error('Error fetching user info:', error);
    }
});
