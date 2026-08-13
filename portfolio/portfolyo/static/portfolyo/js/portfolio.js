document.addEventListener('DOMContentLoaded', () => {
    const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    // Typewriter
    const txtElement = document.querySelector('.typewriter-text');
    if (txtElement && !reduceMotion) {
        const words = JSON.parse(txtElement.getAttribute('data-words') || '[]');
        const wait = parseInt(txtElement.getAttribute('data-wait') || '3000', 10);
        let wordIndex = 0;
        let isDeleting = false;
        let txt = '';

        function type() {
            const fullTxt = words[wordIndex % words.length] || '';

            txt = isDeleting
                ? fullTxt.substring(0, txt.length - 1)
                : fullTxt.substring(0, txt.length + 1);

            txtElement.innerHTML = `<span>${txt}</span><span class="cursor" style="border-right:2px solid var(--accent);margin-left:2px;animation:blink .7s infinite"></span>`;

            let typeSpeed = isDeleting ? 50 : 100;

            if (!isDeleting && txt === fullTxt) {
                typeSpeed = wait;
                isDeleting = true;
            } else if (isDeleting && txt === '') {
                isDeleting = false;
                wordIndex++;
                typeSpeed = 400;
            }

            setTimeout(type, typeSpeed);
        }

        setTimeout(type, 700);
    } else if (txtElement) {
        const words = JSON.parse(txtElement.getAttribute('data-words') || '[]');
        txtElement.textContent = words[0] || '';
    }

    // Contact form
    const contactForm = document.getElementById('contact-form');
    const formFeedback = document.getElementById('form-feedback');

    if (contactForm && formFeedback) {
        contactForm.addEventListener('submit', function (e) {
            e.preventDefault();
            const endpoint = (contactForm.getAttribute('data-endpoint') || '').trim();
            if (!endpoint.startsWith('http')) {
                formFeedback.style.display = 'block';
                formFeedback.style.background = '#fdecea';
                formFeedback.style.color = '#a33';
                formFeedback.innerText = 'İletişim formu henüz bağlanmadı.';
                return;
            }

            const formData = new FormData(this);

            formFeedback.style.display = 'block';
            formFeedback.style.background = 'var(--accent-tint)';
            formFeedback.style.color = 'var(--accent)';
            formFeedback.innerText = 'Gönderiliyor...';

            fetch(endpoint, {
                method: 'POST',
                body: formData,
                headers: { 'Accept': 'application/json' }
            })
                .then(async (response) => {
                    const text = await response.text();
                    let data = {};
                    try {
                        data = JSON.parse(text);
                    } catch {
                        data = {};
                    }
                    return { ok: response.ok, data };
                })
                .then(({ ok, data }) => {
                    if (ok) {
                        formFeedback.style.background = 'var(--accent-tint)';
                        formFeedback.style.color = 'var(--accent-hover)';
                        formFeedback.innerText = 'Mesajınız gönderildi. Teşekkürler.';
                        contactForm.reset();
                    } else {
                        formFeedback.style.background = '#fdecea';
                        formFeedback.style.color = '#a33';
                        formFeedback.innerText = (data && data.error)
                            ? data.error
                            : 'Mesaj gönderilemedi. Lütfen tekrar deneyin.';
                    }
                })
                .catch(() => {
                    formFeedback.style.background = '#fdecea';
                    formFeedback.style.color = '#a33';
                    formFeedback.innerText = 'Mesajınız gönderilemedi. Lütfen tüm alanları doğru doldurun.';
                });
        });
    }

    // Scroll reveal + stagger
    const reveals = document.querySelectorAll('.reveal');
    const revealObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach((entry) => {
            if (!entry.isIntersecting) return;

            const section = entry.target;
            section.classList.add('active');

            const items = section.querySelectorAll('.reveal-item');
            items.forEach((item, index) => {
                setTimeout(() => item.classList.add('is-visible'), reduceMotion ? 0 : 80 + index * 90);
            });

            observer.unobserve(section);
        });
    }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });

    reveals.forEach((el) => revealObserver.observe(el));

    // Navbar + scroll top
    const navbar = document.getElementById('navbar');
    const navToggle = document.getElementById('navToggle');
    const navMenu = document.getElementById('navMenu');
    const scrollBtn = document.getElementById('scrollTopBtn');
    const heroVisual = document.getElementById('heroVisual');

    const onScroll = () => {
        const y = window.scrollY;
        if (navbar) navbar.classList.toggle('is-scrolled', y > 12);
        if (scrollBtn) scrollBtn.classList.toggle('visible', y > 400);

        // Soft parallax on hero photo
        if (heroVisual && !reduceMotion && y < window.innerHeight) {
            heroVisual.style.transform = `translateY(${y * 0.08}px)`;
        }
    };

    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();

    if (navToggle && navMenu) {
        navToggle.addEventListener('click', () => navMenu.classList.toggle('open'));
        navMenu.querySelectorAll('a').forEach((link) => {
            link.addEventListener('click', () => navMenu.classList.remove('open'));
        });
    }

    // Active nav link
    const sections = document.querySelectorAll('section[id]');
    const navLinks = document.querySelectorAll('.nav-menu a');

    window.addEventListener('scroll', () => {
        let current = 'home';
        sections.forEach((section) => {
            if (window.scrollY >= section.offsetTop - 120) {
                current = section.id;
            }
        });
        navLinks.forEach((link) => {
            link.classList.toggle('active', link.getAttribute('href') === `#${current}`);
        });
    }, { passive: true });

    if (scrollBtn) {
        scrollBtn.addEventListener('click', () => {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
    }

    // Preloader
    window.addEventListener('load', () => {
        setTimeout(() => {
            const preloader = document.getElementById('preloader');
            if (preloader) preloader.classList.add('hidden');
            document.body.classList.add('is-ready');
        }, 280);
    });
});

const style = document.createElement('style');
style.textContent = `
@keyframes blink {
    0%, 100% { opacity: 1; }
    50% { opacity: 0; }
}`;
document.head.appendChild(style);
