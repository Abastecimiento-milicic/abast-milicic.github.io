document.addEventListener('DOMContentLoaded', async () => {
    // Lista de usuarios con acceso a la pestaña de envío de informe
    const authorizedEmails = [
        'david.benitez@milicic.com.ar',
        'ventas@milicic.com'
    ];

    try {
        const isLocalhost = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';
        
        if (isLocalhost) {
            const tabEnvio = document.getElementById('tab-envio');
            if (tabEnvio) tabEnvio.style.display = 'inline-block';
            return;
        }

        const response = await fetch('/.auth/me');
        if (!response.ok) {
            return;
        }

        const payload = await response.json();
        const clientPrincipal = payload.clientPrincipal;
        
        if (clientPrincipal && clientPrincipal.userDetails) {
            const email = clientPrincipal.userDetails.toLowerCase(); // e.g. david.benitez@milicic.com.ar
            window.userEmail = email; // Exponer para otros scripts

            const namePart = email.split('@')[0];
            const name = namePart.split('.').map(part => part.charAt(0).toUpperCase() + part.slice(1)).join(' ');
            
            const greetingEl = document.getElementById('userGreeting');
            if (greetingEl) {
                greetingEl.textContent = 'Bienvenido, ' + name;
            }

            // Validar si el usuario puede ver la pestaña "ENVIAR INFORME"
            if (authorizedEmails.includes(email) || isLocalhost) {
                const tabEnvio = document.getElementById('tab-envio');
                if (tabEnvio) {
                    tabEnvio.style.display = 'inline-block';
                }
            }
        }
    } catch (error) {
        console.error('Error fetching user info:', error);
        // Fallback local
        if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
            const tabEnvio = document.getElementById('tab-envio');
            if (tabEnvio) tabEnvio.style.display = 'inline-block';
        }
    }
});
