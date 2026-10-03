(function () {
  'use strict';
  var storageKey = 'uas-text-size';
  var sizes = [{ id: 'default', label: 'Default', scale: '1' }, { id: 'large', label: 'Larger', scale: '1.15' }, { id: 'xlarge', label: 'Extra large', scale: '1.3' }];
  var selected = 'default';
  var controls = [];
  var style = document.createElement('style');
  style.textContent = 'html{--uas-text-scale:1}@supports(zoom:1){html[data-uas-text-size] body{zoom:var(--uas-text-scale);min-width:0}html[data-uas-text-size] #uas-analytics-consent{max-width:calc(100vw / var(--uas-text-scale) - 24px)}}@supports not(zoom:1){html[data-uas-text-size="large"]{font-size:115%}html[data-uas-text-size="xlarge"]{font-size:130%}}.uas-text-size-panel{position:fixed;z-index:10000;width:200px;max-width:calc(100vw - 24px);padding:12px;background:#151512;border:1px solid #68685b;border-radius:8px;color:#e8e2d6;font:14px/1.5 system-ui,sans-serif}.uas-text-size-panel[hidden]{display:none}.uas-text-size-panel fieldset{margin:0;padding:0;border:0}.uas-text-size-panel legend{margin-bottom:8px;font-weight:700}.uas-text-size-panel label{display:flex;align-items:center;gap:8px;padding:6px 0;cursor:pointer}.uas-text-size-panel input{accent-color:var(--uas-accent,#83dded)}.uas-text-size-panel button{margin-top:8px;padding:6px 10px;background:#242420;color:#f5f0e8;border:1px solid #68685b;border-radius:4px;cursor:pointer}.uas-text-size-panel :focus-visible{outline:2px solid var(--uas-accent,#83dded);outline-offset:3px}';
  document.head.appendChild(style);
  try { selected = localStorage.getItem(storageKey) || selected; } catch (_) {}
  function apply(id) {
    var size = sizes.find(function (item) { return item.id === id; }) || sizes[0];
    selected = size.id;
    document.documentElement.dataset.uasTextSize = selected;
    document.documentElement.style.setProperty('--uas-text-scale', size.scale);
    try { localStorage.setItem(storageKey, selected); } catch (_) {}
    controls.forEach(function (control) { control.render(); });
  }
  function init() {
    document.querySelectorAll('[data-text-size-control]').forEach(function (button, index) {
      if (button.dataset.textSizeReady) return;
      button.dataset.textSizeReady = 'true';
      var panel = document.createElement('div');
      panel.id = 'uas-text-size-panel-' + index;
      panel.className = 'uas-text-size-panel';
      panel.hidden = true;
      panel.setAttribute('role', 'dialog');
      panel.setAttribute('aria-label', 'Text size');
      panel.innerHTML = '<fieldset><legend>Choose a reading size</legend>' + sizes.map(function (size) {
        return '<label><input type="radio" name="uas-size-' + index + '" value="' + size.id + '">' + size.label + ' (' + Math.round(Number(size.scale) * 100) + '%)</label>';
      }).join('') + '</fieldset><button type="button">Close text size</button>';
      document.body.appendChild(panel);
      button.setAttribute('aria-haspopup', 'dialog');
      button.setAttribute('aria-controls', panel.id);
      button.setAttribute('aria-expanded', 'false');
      function render() {
        panel.querySelectorAll('input').forEach(function (input) { input.checked = input.value === selected; });
        var size = sizes.find(function (item) { return item.id === selected; });
        button.setAttribute('aria-label', 'Text size: ' + size.label);
        button.title = 'Text size: ' + size.label;
      }
      function place() {
        var rect = button.getBoundingClientRect();
        var scale = parseFloat(getComputedStyle(document.body).zoom) || 1;
        var panelRect = panel.getBoundingClientRect();
        panel.style.top = Math.max(12, Math.min(window.innerHeight - panelRect.height - 12, rect.bottom + 8)) / scale + 'px';
        panel.style.left = Math.max(12, Math.min(window.innerWidth - panelRect.width - 12, rect.right - panelRect.width)) / scale + 'px';
      }
      function close(restore) {
        panel.hidden = true;
        button.setAttribute('aria-expanded', 'false');
        if (restore) button.focus();
      }
      button.addEventListener('click', function () {
        if (!panel.hidden) return close(true);
        controls.forEach(function (control) { control.close(false); });
        render(); panel.hidden = false; place();
        button.setAttribute('aria-expanded', 'true');
        panel.querySelector('input:checked').focus();
      });
      panel.addEventListener('change', function (event) {
        if (event.target.matches('input[type=radio]')) { apply(event.target.value); place(); requestAnimationFrame(place); }
      });
      panel.querySelector('button').addEventListener('click', function () { close(true); });
      document.addEventListener('click', function (event) {
        if (!panel.hidden && !panel.contains(event.target) && !button.contains(event.target)) close(false);
      });
      document.addEventListener('keydown', function (event) {
        if (panel.hidden) return;
        if (event.key === 'Escape') { event.preventDefault(); event.stopImmediatePropagation(); close(true); }
      }, true);
      panel.addEventListener('keydown', function (event) {
        if (event.key !== 'Tab') return;
        var last = event.shiftKey ? panel.querySelector('input:checked') : panel.querySelector('button');
        if (document.activeElement === last) { event.preventDefault(); close(true); }
      });
      window.addEventListener('resize', function () { if (!panel.hidden) place(); });
      window.addEventListener('scroll', function () { if (!panel.hidden) place(); }, true);
      controls.push({ render: render, close: close });
      render();
    });
  }
  apply(selected);
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
