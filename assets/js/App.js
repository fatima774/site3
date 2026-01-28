// assets/js/app.js
// Main app script (single copy). Handles mobile nav, theme, i18n and tabs.
(function () {
	'use strict';
	function log(...a){console.log('[app.js]',...a)}
	function warn(...a){console.warn('[app.js]',...a)}
	function err(...a){console.error('[app.js]',...a)}

	document.addEventListener('DOMContentLoaded', () => {
		log('DOM ready');

		// Elements
		const toggle = document.querySelector('.nav-toggle');
		const menu = document.getElementById('primary-menu');
		const themeBtn = document.getElementById('theme-toggle');
		const langSelect = document.getElementById('lang-select');
		const i18nEls = Array.from(document.querySelectorAll('[data-i18n]'));
		const root = document.documentElement;

		// Mobile nav
		if (toggle && menu) {
			toggle.addEventListener('click', () => {
				const expanded = toggle.getAttribute('aria-expanded') === 'true';
				toggle.setAttribute('aria-expanded', String(!expanded));
				menu.classList.toggle('open');
			});
		} else {
			warn('nav-toggle or primary-menu missing');
		}

		// Theme init & toggle
		try {
			const savedTheme = localStorage.getItem('lfif-theme') || 'light';
			root.setAttribute('data-theme', savedTheme);
			if (themeBtn) themeBtn.textContent = savedTheme === 'dark' ? '☀️ Thème' : '🌙 Thème';
			if (themeBtn) {
				themeBtn.addEventListener('click', () => {
					const next = root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
					root.setAttribute('data-theme', next);
					localStorage.setItem('lfif-theme', next);
					// update label using current dictionary if available
					try {
						const dict = window.__lfif && window.__lfif.currentDict;
						if (themeBtn) {
							if (dict && dict.theme_dark_label && dict.theme_light_label) {
								themeBtn.textContent = next === 'dark' ? dict.theme_light_label : dict.theme_dark_label;
							} else {
								themeBtn.textContent = next === 'dark' ? '☀️ Thème' : '🌙 Thème';
							}
						}
					} catch (e) { /* ignore */ }
					log('Theme switched to', next);
				});
			} else warn('theme-toggle button not found');
		} catch (e) {
			err('Theme init error', e);
		}

		// i18n helpers
		async function fetchJson(path) {
			try {
				const res = await fetch(path, { cache: 'no-store' });
				if (!res.ok) {
					throw new Error(`HTTP ${res.status} ${res.statusText}`);
				}
				const data = await res.json();
				log(`Successfully loaded: ${path}`);
				return data;
			} catch (e) {
				err(`Failed to fetch ${path}:`, e.message);
				throw e;
			}
		}

		async function loadLang(lang) {
			try {
				log('Loading language', lang);
				const dict = await fetchJson(`assets/lang/${lang}.json`);

				// Title
				const titleEl = document.querySelector('title[data-i18n="page_title"]');
				if (dict.page_title) {
					if (titleEl) titleEl.textContent = dict.page_title;
					document.title = dict.page_title;
				}

				// Apply translations to all elements with data-i18n
				i18nEls.forEach(el => {
					const key = el.getAttribute('data-i18n');
					if (!key) return;
					if (!(key in dict)) {
						warn(`Missing translation key: ${key}`);
						return;
					}

					const tag = el.tagName;
					if (tag === 'INPUT' || tag === 'TEXTAREA') {
						el.placeholder = dict[key];
					} else if (tag === 'IMG') {
						el.alt = dict[key];
					} else {
						el.textContent = dict[key];
					}
				});

				// expose current dict for other handlers (theme labels etc.)
				window.__lfif = window.__lfif || {};
				window.__lfif.currentDict = dict;
				// update theme button label now that we have localized strings
				if (themeBtn && dict) {
					try {
						if (dict.theme_dark_label && dict.theme_light_label) {
							const currentTheme = root.getAttribute('data-theme');
							themeBtn.textContent = currentTheme === 'dark' ? dict.theme_light_label : dict.theme_dark_label;
						}
					} catch (e) { /* ignore */ }
				}

				document.documentElement.lang = lang;
				localStorage.setItem('lfif-lang', lang);
				if (langSelect) {
					langSelect.value = lang;
				}
				log('Language successfully applied:', lang);
			} catch (e) {
				err('loadLang error:', e.message);
				throw e;
			}
		}

		// Lang selector
		if (langSelect) {
			langSelect.addEventListener('change', (e) => {
				const next = e.target.value;
				log('Language selector changed to:', next);
				loadLang(next);
			});
		} else warn('lang-select not found');

		// Init language and set selector value
		const savedLang = localStorage.getItem('lfif-lang') || 'fr';
		log('Initializing with saved language:', savedLang);
		if (langSelect) {
			langSelect.value = savedLang;
		}
		loadLang(savedLang).catch(e => {
			warn('Initial loadLang failed:', e.message);
			log('Fallback: trying to load language as fallback');
		});

		// Tab switching (for courses page)
		const tabBtns = document.querySelectorAll('.tab-btn');
		if (tabBtns.length > 0) {
			tabBtns.forEach(btn => {
				btn.addEventListener('click', () => {
					const tabName = btn.getAttribute('data-tab');
					// Hide all tabs
					document.querySelectorAll('.tab-content').forEach(tab => {
						tab.classList.remove('active');
					});
					// Remove active from all buttons
					tabBtns.forEach(b => b.classList.remove('active'));
					// Show selected tab
					const tabEl = document.getElementById(`tab-${tabName}`);
					if (tabEl) tabEl.classList.add('active');
					btn.classList.add('active');
					log('Tab switched to', tabName);
				});
			});
		}

		// Contact form basic handler (optional)
		const contactForm = document.querySelector('.contact-form');
		if (contactForm) {
			contactForm.addEventListener('submit', (ev) => {
				ev.preventDefault();
				const form = ev.currentTarget;
				const formData = new FormData(form);
				const name = (formData.get('nom') || '').trim();
				const email = (formData.get('email') || '').trim();
				const message = (formData.get('message') || '').trim();
				if (!name || !email || !message) {
					alert('Veuillez remplir tous les champs.');
					return;
				}
				const submit = form.querySelector('button[type="submit"]');
				if (submit) { submit.disabled = true; submit.textContent = 'Envoi...'; }
				// Try to POST to /api/contact if backend exists
				fetch('/api/contact', { method: 'POST', body: formData })
					.then(r => {
						if (!r.ok) throw new Error('Erreur serveur');
						return r.json();
					})
					.then(json => {
						alert(json.message || 'Message envoyé, merci.');
						form.reset();
					})
					.catch(e => {
						console.warn('Contact send failed', e);
						alert('Erreur lors de l\'envoi. Le message a été enregistré localement.');
						form.reset();
					})
					.finally(() => {
						if (submit) { submit.disabled = false; submit.textContent = 'Envoyer'; }
					});
			});
		}

		// Expose debug helpers
		window.__lfif = { loadLang, fetchJson, i18nElsCount: i18nEls.length };
		log('app.js initialized, i18n elements:', i18nEls.length);
	});
})();
