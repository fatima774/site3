/*
  lang-switcher.js
  Single reliable i18n loader for all pages.
  - Loads translation JSON from assets/lang/{fr,en,es}.json
  - Applies translations for elements with `data-i18n`
  - Supports placeholders, img alt, title and custom attribute via `data-i18n-attr`
  - Updates select options text (tries keys then fallback names)
  - Persists language in localStorage key `lfif-lang`
  - Avoids double-init when included multiple times
*/
(function () {
  if (window.__LFIF_I18N_INITIALIZED__) return;
  window.__LFIF_I18N_INITIALIZED__ = true;

  const LANG_KEY = 'lfif-lang';
  const DEFAULT = 'fr';
  const LANG_PATH = 'assets/lang/';
  const SUPPORTED = ['fr', 'en', 'es'];

  function fetchJson(lang) {
    return fetch(`${LANG_PATH}${lang}.json`, {cache: 'no-store'})
      .then(res => {
        if (!res.ok) throw new Error('Lang not found: ' + lang);
        return res.json();
      });
  }

  function getStored() {
    try { return localStorage.getItem(LANG_KEY) || DEFAULT; } catch (e) { return DEFAULT; }
  }

  function setStored(lang) {
    try { localStorage.setItem(LANG_KEY, lang); } catch (e) { /* ignore */ }
  }

  function applyText(el, text) {
    // store the original text/content the first time we touch the element so
    // we can fall back to it if the key is missing in the selected language.
    if (!el.dataset.i18nDefault) {
      // choose a reasonable default depending on element type
      const tagName = el.tagName && el.tagName.toUpperCase();
      if (tagName === 'INPUT' || tagName === 'TEXTAREA') {
        el.dataset.i18nDefault = el.placeholder || el.value || '';
      } else if (tagName === 'IMG') {
        el.dataset.i18nDefault = el.alt || '';
      } else {
        el.dataset.i18nDefault = el.textContent;
      }
    }

    // if the lookup returned null/undefined we fall back to the original
    // content stored above. this prevents leftover english/spanish strings
    // when the french JSON simply doesn't contain the key.
    if (text == null) {
      text = el.dataset.i18nDefault;
    }

    const tag = el.tagName && el.tagName.toUpperCase();
    const attr = el.getAttribute('data-i18n-attr');
    const asHtml = el.getAttribute('data-i18n-html') === 'true';

    if (attr) {
      el.setAttribute(attr, text);
      return;
    }

    if (tag === 'INPUT' || tag === 'TEXTAREA') {
      // placeholder if present, otherwise value
      if (el.hasAttribute('placeholder') || el.type === 'text') el.placeholder = text;
      else el.value = text;
      return;
    }

    if (tag === 'IMG') { el.alt = text; return; }

    // for option elements we update the textContent
    if (tag === 'OPTION') { el.textContent = text; return; }

    if (asHtml) el.innerHTML = text; else el.textContent = text;
  }

  function applyTranslations(map) {
    // elements with data-i18n
    document.querySelectorAll('[data-i18n]').forEach(el => {
      // do not replace the inner HTML of a <select> element: that would remove its <option>s
      if (el.tagName && el.tagName.toUpperCase() === 'SELECT') return;
      const key = el.getAttribute('data-i18n');
      const text = lookup(map, key);
      applyText(el, text);
    });

    // some elements may use data-i18n-title or similar convenience attrs
    document.querySelectorAll('[data-i18n-title]').forEach(el => {
      const key = el.getAttribute('data-i18n-title');
      const text = lookup(map, key);
      if (text != null) el.title = text;
    });
  }

  function lookup(map, key) {
    if (!key) return null;
    // support nested keys with dots
    if (map.hasOwnProperty(key)) return map[key];
    const parts = key.split('.');
    let cur = map;
    for (let p of parts) {
      if (cur && typeof cur === 'object' && (p in cur)) cur = cur[p]; else { cur = null; break; }
    }
    return (typeof cur === 'string') ? cur : cur == null ? null : JSON.stringify(cur);
  }

  function updateLangSelect(select, map) {
    if (!select) return;

    // If options have data-i18n, they'll be handled by applyTranslations; otherwise try common key names
    const fallbackKeys = (value) => [
      `lang.${value}`, `language.${value}`, `lang_${value}`, `language_${value}`, `lang-${value}`
    ];

    Array.from(select.options).forEach(opt => {
      const key = opt.getAttribute('data-i18n');
      if (key) {
        const t = lookup(map, key);
        if (t) opt.textContent = t;
        return;
      }

      // try fallback keys
      const val = (opt.value || '').trim();
      if (SUPPORTED.includes(val)) {
        let found = null;
        for (const k of fallbackKeys(val)) { if (lookup(map, k)) { found = lookup(map, k); break; } }
        if (found) opt.textContent = found; else {
          // default fallback names
          const defaultNames = { fr: 'Français', en: 'English', es: 'Español' };
          opt.textContent = defaultNames[val] || opt.textContent;
        }
      }
    });
  }

  // main loader
  async function loadLang(lang) {
    if (!SUPPORTED.includes(lang)) lang = DEFAULT;
    try {
      const map = await fetchJson(lang);
      applyTranslations(map);
      // update select labels
      const select = document.getElementById('lang-select');
      updateLangSelect(select, map);
      // make sure the <select> reflects the language we just loaded
      if (select) select.value = lang;
      // set lang attribute on html
      document.documentElement.lang = lang;
      setStored(lang);
    } catch (e) {
      console.error('i18n load failed', e);
    }
  }

  function init() {
    const stored = getStored();
    const select = document.getElementById('lang-select');

    // ensure we control the select: remove inline onchange if any
    if (select) {
      try { select.onchange = null; } catch (e) { /* ignore */ }
      // when user changes language
      select.addEventListener('change', function (ev) {
        const v = (this.value || DEFAULT).trim();
        loadLang(v);
      });
    }

    // initial load
    loadLang(stored);
  }

  // DOM ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else init();

})();
