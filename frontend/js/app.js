/* ============================================
   AutoElite — Shared JavaScript
   ============================================ */

const API_BASE_URL = 'http://localhost:5000/api';

/* ---------- Page Loader ---------- */
window.addEventListener('load', function() {
    const loader = document.querySelector('.page-loader');
    if (loader) {
        setTimeout(function() {
            loader.classList.add('loaded');
        }, 600);
    }
});

/* ---------- Navbar Scroll ---------- */
document.addEventListener('DOMContentLoaded', function() {
    const navbar = document.querySelector('.navbar');

    function handleNavScroll() {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    }

    window.addEventListener('scroll', handleNavScroll, { passive: true });
    handleNavScroll();

    /* ---------- Mobile Nav Toggle ---------- */
    const toggle = document.querySelector('.nav-toggle');
    const navLinks = document.querySelector('.nav-links');

    if (toggle && navLinks) {
        toggle.addEventListener('click', function() {
            toggle.classList.toggle('active');
            navLinks.classList.toggle('open');
            document.body.style.overflow = navLinks.classList.contains('open') ? 'hidden' : '';
        });

        navLinks.querySelectorAll('a').forEach(function(link) {
            link.addEventListener('click', function() {
                toggle.classList.remove('active');
                navLinks.classList.remove('open');
                document.body.style.overflow = '';
            });
        });
    }

    /* ---------- Scroll Reveal (Intersection Observer) ---------- */
    const revealElements = document.querySelectorAll('.reveal, .reveal-left, .reveal-right');

    if (revealElements.length > 0) {
        const observer = new IntersectionObserver(function(entries) {
            entries.forEach(function(entry) {
                if (entry.isIntersecting) {
                    entry.target.classList.add('visible');
                    observer.unobserve(entry.target);
                }
            });
        }, {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        });

        revealElements.forEach(function(el) {
            observer.observe(el);
        });
    }

    /* ---------- Active Nav Link ---------- */
    const currentPage = window.location.pathname.split('/').pop() || 'index.html';
    document.querySelectorAll('.nav-links a').forEach(function(link) {
        const href = link.getAttribute('href');
        if (href === currentPage) {
            link.classList.add('active');
        }
    });
});

/* ---------- Auth ---------- */
function getAuthData() {
    const token = localStorage.getItem('authToken');
    const userData = localStorage.getItem('user');
    if (token && userData) {
        return { token: token, user: JSON.parse(userData) };
    }
    return null;
}

function logout() {
    localStorage.removeItem('authToken');
    localStorage.removeItem('user');
    window.location.href = 'index.html';
}

function updateNavAuth() {
    const auth = getAuthData();
    const userEl = document.querySelector('.nav-user');
    const logoutEl = document.querySelector('.nav-logout');
    const authLinks = document.querySelector('.nav-auth-links');

    if (auth) {
        if (userEl) {
            userEl.classList.remove('hidden');
            userEl.querySelector('span').textContent = auth.user.firstName;
        }
        if (logoutEl) logoutEl.classList.remove('hidden');
        if (authLinks) authLinks.classList.add('hidden');
    } else {
        if (userEl) userEl.classList.add('hidden');
        if (logoutEl) logoutEl.classList.add('hidden');
        if (authLinks) authLinks.classList.remove('hidden');
    }
}

document.addEventListener('DOMContentLoaded', updateNavAuth);

/* ---------- Toast Notifications ---------- */
function showToast(message, type) {
    type = type || 'success';
    let container = document.querySelector('.toast-container');
    if (!container) {
        container = document.createElement('div');
        container.className = 'toast-container';
        document.body.appendChild(container);
    }

    var icon = type === 'success' ? 'fa-check-circle' : 'fa-exclamation-circle';
    var toastClass = 'toast toast-' + type;

    var toast = document.createElement('div');
    toast.className = toastClass;
    toast.innerHTML = '<i class="fas ' + icon + '"></i><span class="toast-message">' + message + '</span>';

    container.appendChild(toast);

    setTimeout(function() {
        if (toast.parentNode) toast.parentNode.removeChild(toast);
    }, 3000);
}

/* ---------- Stat Counter Animation ---------- */
function animateCounter(element, target, duration, suffix) {
    suffix = suffix || '';
    var start = 0;
    var startTime = null;

    function step(timestamp) {
        if (!startTime) startTime = timestamp;
        var progress = Math.min((timestamp - startTime) / duration, 1);
        var value = Math.floor(progress * (target - start) + start);
        element.textContent = value.toLocaleString() + suffix;
        if (progress < 1) {
            requestAnimationFrame(step);
        }
    }

    requestAnimationFrame(step);
}

function initStatCounters() {
    var statNumbers = document.querySelectorAll('.stat-number[data-target]');
    if (statNumbers.length === 0) return;

    var observer = new IntersectionObserver(function(entries) {
        entries.forEach(function(entry) {
            if (entry.isIntersecting) {
                var el = entry.target;
                var target = parseInt(el.getAttribute('data-target'));
                var suffix = el.getAttribute('data-suffix') || '';
                animateCounter(el, target, 2000, suffix);
                observer.unobserve(el);
            }
        });
    }, { threshold: 0.5 });

    statNumbers.forEach(function(el) {
        observer.observe(el);
    });
}

document.addEventListener('DOMContentLoaded', initStatCounters);

/* ---------- Utility ---------- */
function formatPrice(price) {
    return 'ZMW ' + parseInt(price).toLocaleString();
}

function getFuelDisplay(car) {
    if (car.fuel_type === 'Electric') {
        return (car.mileage || 396) + ' mi range';
    }
    return car.fuel_type || 'Gasoline';
}

function getCarBadge(car) {
    if (car.fuel_type === 'Electric') return 'Electric';
    if (car.horsepower > 500) return 'Performance';
    if (car.type === 'SUV') return 'Premium SUV';
    return 'Premium';
}
