/* ============================================
   Site Laços - JavaScript Principal
   ============================================
   Funcionalidades:
   - Toggle do menu mobile
   - Toggle do submenu Clubes no mobile
   - Atualização automática do ano no footer
*/

document.addEventListener('DOMContentLoaded', function() {

    // ===== MENU MOBILE =====
    const menuButton = document.getElementById('mobile-menu-button');
    const mobileMenu = document.getElementById('mobile-menu');
    const iconOpen = document.getElementById('icon-open');
    const iconClose = document.getElementById('icon-close');

    if (menuButton && mobileMenu) {
        menuButton.addEventListener('click', function() {
            mobileMenu.classList.toggle('hidden');
            iconOpen.classList.toggle('hidden');
            iconClose.classList.toggle('hidden');
        });
    }

    // ===== SUBMENU CLUBES NO MOBILE =====
    const clubesButton = document.getElementById('mobile-clubes-button');
    const clubesSubmenu = document.getElementById('mobile-clubes-submenu');
    const clubesIcon = document.getElementById('mobile-clubes-icon');

    if (clubesButton && clubesSubmenu) {
        clubesButton.addEventListener('click', function() {
            clubesSubmenu.classList.toggle('hidden');
            clubesIcon.classList.toggle('rotate-180');
        });
    }

    // ===== ANO ATUAL NO FOOTER =====
    const yearSpan = document.getElementById('year');
    if (yearSpan) {
        yearSpan.textContent = new Date().getFullYear();
    }

    // ===== FECHAR MENU MOBILE AO CLICAR EM LINK =====
    const mobileLinks = document.querySelectorAll('#mobile-menu a');
    mobileLinks.forEach(link => {
        link.addEventListener('click', function() {
            // Só fecha se não for um botão de submenu
            if (!link.closest('#mobile-clubes-submenu') === false) {
                mobileMenu.classList.add('hidden');
                iconOpen.classList.remove('hidden');
                iconClose.classList.add('hidden');
            }
        });
    });
});