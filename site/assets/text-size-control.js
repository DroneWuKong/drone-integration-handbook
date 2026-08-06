(function () {
  'use strict';

  var storageKey = 'uas-text-size';
  var sizes = [
    { id: 'default', label: 'Default', scale: '1' },
    { id: 'large', label: 'Larger', scale: '1.15' },
    { id: 'xlarge', label: 'Extra large', scale: '1.3' }
  ];

  var style = document.createElement('style');
  style.textContent = [
    'html{--uas-text-scale:1}',
    '@supports (zoom:1){html[data-uas-text-size] body{zoom:var(--uas-text-scale)}}',
    '@supports not (zoom:1){html[data-uas-text-size="large"]{font-size:115%}html[data-uas-text-size="xlarge"]{font-size:130%}}',
    '.uas-text-size-panel{position:fixed;z-index:10000;width:190px;padding:8px;background:#151512;border:1px solid #3e3e34;border-radius:8px;box-shadow:0 12px 30px rgba(0,0,0,.35);font:600 12px system-ui,sans-serif;color:#e8e2d6}',
    '.uas-text-size-panel[hidden]{display:none}.uas-text-size-panel p{margin:3px 6px 7px;color:#b8b0a0;font-size:11px}.uas-text-size-option{display:flex;align-items:center;justify-content:space-between;width:100%;padding:8px;border:0;border-radius:5px;background:transparent;color:inherit;font:inherit;text-align:left;cursor:pointer}.uas-text-size-option:hover,.uas-text-size-option:focus-visible{background:rgba(245,158,11,.12);outline:0}.uas-text-size-option[aria-checked="true"]{color:#f59e0b}.uas-text-size-option span:last-child{font-family:ui-monospace,monospace;font-size:10px}'
  ].join('');
  document.head.appendChild(style);

  function getSize() {
    try { return localStorage.getItem(storageKey) || 'default'; } catch (_) { return 'default'; }
  }

  function apply(id) {
    var selected = sizes.find(function (size) { return size.id === id; }) || sizes[0];
    document.documentElement.dataset.uasTextSize = selected.id;
    document.documentElement.style.setProperty('--uas-text-scale', selected.scale);
    try { localStorage.setItem(storageKey, selected.id); } catch (_) {}
    return selected;
  }

  function buildControl(button) {
    if (button.dataset.textSizeReady) return;
    button.dataset.textSizeReady = 'true';
    button.setAttribute('aria-haspopup', 'menu');
    button.setAttribute('aria-expanded', 'false');

    var panel = document.createElement('div');
    panel.className = 'uas-text-size-panel';
    panel.hidden = true;
    panel.setAttribute('role', 'menu');
    panel.setAttribute('aria-label', 'Text size');
    panel.innerHTML = '<p>Choose a reading size</p>' + sizes.map(function (size) {
      return '<button type="button" class="uas-text-size-option" role="menuitemradio" data-size="' + size.id + '" aria-checked="false"><span>' + size.label + '</span><span>' + (size.id === 'default' ? '100%' : Math.round(Number(size.scale) * 100) + '%') + '</span></button>';
    }).join('');
    document.body.appendChild(panel);

    function placePanel() {
      var rect = button.getBoundingClientRect();
      panel.style.top = Math.min(window.innerHeight - panel.offsetHeight - 12, rect.bottom + 8) + 'px';
      panel.style.left = Math.max(12, Math.min(window.innerWidth - panel.offsetWidth - 12, rect.right - panel.offsetWidth)) + 'px';
    }

    function render() {
      var selected = getSize();
      panel.querySelectorAll('[data-size]').forEach(function (option) {
        option.setAttribute('aria-checked', String(option.dataset.size === selected));
      });
      var current = sizes.find(function (size) { return size.id === selected; }) || sizes[0];
      button.setAttribute('aria-label', 'Text size: ' + current.label);
      button.title = 'Text size: ' + current.label;
    }

    function close() {
      panel.hidden = true;
      button.setAttribute('aria-expanded', 'false');
    }

    button.addEventListener('click', function () {
      if (panel.hidden) {
        render();
        panel.hidden = false;
        placePanel();
        button.setAttribute('aria-expanded', 'true');
        panel.querySelector('[aria-checked="true"]').focus();
      } else close();
    });

    panel.addEventListener('click', function (event) {
      var option = event.target.closest('[data-size]');
      if (!option) return;
      apply(option.dataset.size);
      render();
      close();
      button.focus();
    });

    document.addEventListener('click', function (event) {
      if (!panel.hidden && !panel.contains(event.target) && event.target !== button) close();
    });
    document.addEventListener('keydown', function (event) {
      if (event.key === 'Escape' && !panel.hidden) { close(); button.focus(); }
    });
    window.addEventListener('resize', function () { if (!panel.hidden) placePanel(); });
    window.addEventListener('scroll', function () { if (!panel.hidden) placePanel(); }, true);
    render();
  }

  apply(getSize());
  function init() { document.querySelectorAll('[data-text-size-control]').forEach(buildControl); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
