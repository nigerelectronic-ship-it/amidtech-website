/* dc-lite — tiny runtime for AmidTech interactive demos.
   Renders a <template> using {{holes}}, <sc-for>, <sc-if> and onClick="{{fn}}",
   driven by a `Component` class (state / setState / lifecycle), and patches the
   DOM in place so CSS transitions and animations keep running between renders. */
(function () {
  'use strict';

  function lookup(scope, path) {
    path = path.trim();
    if (path === 'true') return true;
    if (path === 'false') return false;
    if (/^-?\d+(\.\d+)?$/.test(path)) return Number(path);
    var parts = path.split('.'), v = scope;
    for (var i = 0; i < parts.length; i++) {
      if (v == null) return undefined;
      v = v[parts[i]];
    }
    return v;
  }
  function esc(s) {
    return String(s == null ? '' : s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }
  var HOLE = /\{\{\s*([^}]+?)\s*\}\}/g;
  function interp(str, scope) {
    return str.replace(HOLE, function (_, p) { var v = lookup(scope, p); return v == null ? '' : String(v); });
  }
  var VOID = { area: 1, base: 1, br: 1, col: 1, embed: 1, hr: 1, img: 1, input: 1, link: 1, meta: 1, source: 1, track: 1, wbr: 1 };

  function DCLogic(props) { this.props = props || {}; this.state = {}; }
  DCLogic.prototype.setState = function (patch) {
    var p = typeof patch === 'function' ? patch(this.state) : patch;
    for (var k in p) if (Object.prototype.hasOwnProperty.call(p, k)) this.state[k] = p[k];
    if (this.__schedule) this.__schedule();
  };
  DCLogic.prototype.forceUpdate = function () { if (this.__schedule) this.__schedule(); };
  window.DCLogic = DCLogic;

  function mount(root, tpl, Component) {
    var comp = new Component({});
    if (!comp.state) comp.state = {};
    var handlers = [];
    var pending = false;

    function renderNode(node, scope, out) {
      if (node.nodeType === 3) { out.push(esc(interp(node.nodeValue, scope))); return; }
      if (node.nodeType !== 1) return;
      var tag = node.tagName.toLowerCase();
      if (tag === 'template' && node.hasAttribute('data-sc')) {
        var kind = node.getAttribute('data-sc');
        if (kind === 'for') {
          var lst = lookup(scope, (node.getAttribute('list') || '').replace(/[{}]/g, '')) || [];
          var nm = node.getAttribute('as') || 'item';
          for (var j = 0; j < lst.length; j++) { var sc = Object.create(scope); sc[nm] = lst[j]; sc.$index = j; renderChildren(node.content, sc, out); }
        } else if (lookup(scope, (node.getAttribute('value') || '').replace(/[{}]/g, ''))) {
          renderChildren(node.content, scope, out);
        }
        return;
      }
      if (tag === 'sc-for') {
        var list = lookup(scope, (node.getAttribute('list') || '').replace(/[{}]/g, '')) || [];
        var as = node.getAttribute('as') || 'item';
        for (var i = 0; i < list.length; i++) {
          var s = Object.create(scope); s[as] = list[i]; s.$index = i;
          renderChildren(node, s, out);
        }
        return;
      }
      if (tag === 'sc-if') {
        if (lookup(scope, (node.getAttribute('value') || '').replace(/[{}]/g, ''))) renderChildren(node, scope, out);
        return;
      }
      out.push('<' + tag);
      for (var a = 0; a < node.attributes.length; a++) {
        var at = node.attributes[a], name = at.name, val = at.value;
        if (name.indexOf('hint-') === 0) continue;
        if (/^on[a-z]+$/i.test(name)) {
          var fn = lookup(scope, val.replace(/[{}]/g, ''));
          if (typeof fn === 'function') { handlers.push(fn); out.push(' data-dc-' + name.slice(2).toLowerCase() + '="' + (handlers.length - 1) + '"'); }
          continue;
        }
        out.push(' ' + name + '="' + esc(interp(val, scope)) + '"');
      }
      out.push('>');
      if (VOID[tag]) return;
      renderChildren(tag === 'template' ? node.content : node, scope, out);
      out.push('</' + tag + '>');
    }
    function renderChildren(node, scope, out) {
      for (var c = node.firstChild; c; c = c.nextSibling) renderNode(c, scope, out);
    }

    function morph(from, to) {
      // children-level patch of `from` to match `to`
      var a = from.firstChild, b = to.firstChild;
      while (b) {
        var nextB = b.nextSibling;
        if (!a) { from.appendChild(b); b = nextB; continue; }
        var nextA = a.nextSibling;
        if (a.nodeType !== b.nodeType || (a.nodeType === 1 && (a.tagName !== b.tagName || (a.id || '') !== (b.id || '')))) {
          from.replaceChild(b, a);
        } else if (a.nodeType === 3) {
          if (a.nodeValue !== b.nodeValue) a.nodeValue = b.nodeValue;
        } else if (a.nodeType === 1) {
          var i, attr;
          for (i = a.attributes.length - 1; i >= 0; i--) { attr = a.attributes[i].name; if (!b.hasAttribute(attr)) a.removeAttribute(attr); }
          for (i = 0; i < b.attributes.length; i++) { attr = b.attributes[i]; if (a.getAttribute(attr.name) !== attr.value) a.setAttribute(attr.name, attr.value); }
          if (a.tagName === 'INPUT' || a.tagName === 'TEXTAREA') { if (b.hasAttribute('value') && a.value !== b.getAttribute('value')) a.value = b.getAttribute('value'); }
          morph(a, b);
        }
        a = nextA; b = nextB;
      }
      while (a) { var n = a.nextSibling; from.removeChild(a); a = n; }
    }

    function render() {
      pending = false;
      handlers = [];
      var vals = comp.renderVals ? comp.renderVals() : {};
      var out = [];
      renderChildren(tpl.content, vals, out);
      var tmp = document.createElement('div');
      tmp.innerHTML = out.join('');
      morph(root, tmp);
    }
    comp.__schedule = function () { if (!pending) { pending = true; requestAnimationFrame(render); } };

    ['click', 'input', 'change'].forEach(function (ev) {
      root.addEventListener(ev, function (e) {
        var el = e.target.closest('[data-dc-' + ev + ']');
        if (!el || !root.contains(el)) return;
        var fn = handlers[Number(el.getAttribute('data-dc-' + ev))];
        if (fn) fn(e);
      });
    });

    render();
    if (comp.componentDidMount) comp.componentDidMount();
    return comp;
  }

  window.dcLite = { mount: mount };
})();
