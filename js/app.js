{
// ---------- catalogue ----------
const TEXTS = [
  { id: 'apology', file: 'data/apology.json', gr: 'Ἀπολογία Σωκράτους',
    title: { en: 'Apology of Socrates', ru: 'Апология Сократа' }, author: { en: 'Plato', ru: 'Платон' },
    unit: { en: 'Stephanus page', ru: 'страница Стефана' }, ready: true },
  { id: 'anabasis', gr: 'Κύρου Ἀνάβασις', title: { en: 'Anabasis', ru: 'Анабасис' },
    author: { en: 'Xenophon', ru: 'Ксенофонт' }, ready: false },
];

// ---------- interface strings ----------
const T = {
  en: {
    tagline: 'Ancient Greek, word by word', lib_h: 'Read Ancient Greek, word by word',
    lib_p: 'Tap any word to see its dictionary form, meaning and full parsing. Verbs are coloured by tense. Translations can be shown under each section.',
    open: 'Read', soon: 'Coming soon', words: 'words', how_h: 'How to read',
    how_p: 'Underlined words are finite verbs, bold italic words are participles and struck-through words are infinitives. The colour shows the tense; tap a colour to switch it off. Use the language switch at the top for English or Russian meanings.',
    back: '← Library', tense: { P: 'Present', I: 'Imperfect', F: 'Future', A: 'Aorist', X: 'Perfect', Y: 'Pluperfect' },
    trans: 'Translation', none: 'None', en: 'English', ru: 'Russian', ru_soon: 'Russian (coming soon)',
    vocab: 'Page vocabulary', vocab_h: p => `Words on page ${p}`, vocab_n: 'in text',
    times: n => `${n}× in this text`, same: 'Mark all forms on this page', unsame: 'Clear marks',
    prev: '← Page', next: 'Page →', loading: 'Loading the text…', failed: 'The text could not be loaded.',
    legend: 'Text, lemmas and parsing: GLAUx corpus (A. Keersmaekers, CC BY-SA 4.0), based on the Perseus Digital Library. English translation: H. N. Fowler (1914), Perseus, CC BY-SA. Russian translation: M. S. Solovyov (1899–1903), public domain. Meanings: Greek Study App dictionary (J. Jansen, GPL-3.0) and written for this site.',
    foot: 'Open project. Corrections are welcome on GitHub.',
  },
  ru: {
    tagline: 'Древнегреческий, слово за словом', lib_h: 'Читайте по-древнегречески, слово за словом',
    lib_p: 'Нажмите на любое слово, чтобы увидеть его словарную форму, значение и полный разбор. Глаголы окрашены по времени. Перевод можно показать под каждым разделом.',
    open: 'Читать', soon: 'Скоро', words: 'слов', how_h: 'Как читать',
    how_p: 'Подчёркнуты личные формы глагола, жирным курсивом выделены причастия, зачёркнуты инфинитивы. Цвет показывает время; нажмите на цвет, чтобы его отключить. Переключатель языка вверху меняет значения слов на английские или русские.',
    back: '← Библиотека', tense: { P: 'Настоящее', I: 'Имперфект', F: 'Будущее', A: 'Аорист', X: 'Перфект', Y: 'Плюсквамперфект' },
    trans: 'Перевод', none: 'Нет', en: 'Английский', ru: 'Русский', ru_soon: 'Русский (скоро)',
    vocab: 'Слова страницы', vocab_h: p => `Слова на странице ${p}`, vocab_n: 'в тексте',
    times: n => `${n}× в этом тексте`, same: 'Отметить все формы на странице', unsame: 'Снять отметки',
    prev: '← Стр.', next: 'Стр. →', loading: 'Загрузка текста…', failed: 'Не удалось загрузить текст.',
    legend: 'Текст, леммы и разбор: корпус GLAUx (A. Keersmaekers, CC BY-SA 4.0) на основе Perseus Digital Library. Английский перевод: H. N. Fowler (1914), Perseus, CC BY-SA. Русский перевод: М. С. Соловьёв (1899–1903), общественное достояние. Значения: словарь Greek Study App (J. Jansen, GPL-3.0) и составленные для этого сайта.',
    foot: 'Открытый проект. Исправления приветствуются на GitHub.',
  },
};
const TENSES = ['P', 'I', 'F', 'A', 'X', 'Y'];

// ---------- state ----------
const S = { lang: 'en', tr: 'none', on: { P: 1, I: 1, F: 1, A: 1, X: 1, Y: 1 }, vocab: false, last: {} };
try { Object.assign(S, JSON.parse(localStorage.getItem('anagnosis') || '{}')); } catch (e) {}
const save = () => { try { localStorage.setItem('anagnosis', JSON.stringify(S)); } catch (e) {} };
const cache = {};
let D = null, text = null, page = null, sel = null, sameLem = null;

const $ = id => document.getElementById(id);
const esc = s => String(s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const t = () => T[S.lang];

// ---------- language ----------
function setLang(l) {
  S.lang = l; save();
  document.documentElement.lang = l;
  document.querySelectorAll('.lang button').forEach(b => b.setAttribute('aria-pressed', b.dataset.lang === l));
  $('tagline').textContent = t().tagline;
  $('foot').textContent = t().foot;
  hide(); route();
}

// ---------- library ----------
function library() {
  D = null; text = null;
  document.title = 'Anagnosis: Greek reader';
  $('app').innerHTML = `<div class="wrap">
    <section class="hero"><h1>${esc(t().lib_h)}</h1><p>${esc(t().lib_p)}</p></section>
    <div class="shelf">${TEXTS.map(x => `<a class="book${x.ready ? '' : ' soon'}" href="#${x.id}">
      <div class="gr">${esc(x.gr)}</div>
      <div class="au">${esc(x.author[S.lang])} · ${esc(x.title[S.lang])}</div>
      <span class="tag">${esc(x.ready ? t().open : t().soon)}</span></a>`).join('')}</div>
    <section class="howto"><h2>${esc(t().how_h)}</h2><p>${esc(t().how_p)}</p></section></div>`;
}

// ---------- reader ----------
async function reader(id, pg) {
  const x = TEXTS.find(a => a.id === id && a.ready);
  if (!x) { location.hash = ''; return; }
  if (!cache[id]) {
    $('app').innerHTML = `<p class="wrap empty">${esc(t().loading)}</p>`;
    try { cache[id] = await (await fetch(x.file)).json(); }
    catch (e) { $('app').innerHTML = `<p class="wrap empty">${esc(t().failed)}</p>`; return; }
  }
  D = cache[id]; text = x;
  const pages = D.pages.map(p => p[0]);
  page = pages.includes(pg) ? pg : (S.last[id] && pages.includes(S.last[id]) ? S.last[id] : pages[0]);
  S.last[id] = page; save();
  document.title = `${x.title[S.lang]} ${page} · Anagnosis`;
  const hasRu = Object.keys(D.tr.ru || {}).length > 0;
  $('app').innerHTML = `
    <div class="bar"><div class="wrap">
      <div class="title"><a href="#">${esc(t().back)}</a><h1>${esc(x.author[S.lang])}, ${esc(x.title[S.lang])}</h1></div>
      <nav class="pages" aria-label="${esc(x.unit[S.lang])}">${pages.map(p => `<button data-p="${p}" aria-current="${p === page}">${p}</button>`).join('')}</nav>
      <div class="ctrl">
        <div class="key" role="group">${TENSES.map(k => `<button class="T${k}" data-t="${k}" aria-pressed="${!!S.on[k]}"><i></i>${esc(t().tense[k])}</button>`).join('')}</div>
        <div class="opts">
          <label for="tr">${esc(t().trans)}</label>
          <select id="tr"><option value="none">${esc(t().none)}</option><option value="en">${esc(t().en)}</option>
            <option value="ru" ${hasRu ? '' : 'disabled'}>${esc(hasRu ? t().ru : t().ru_soon)}</option></select>
          <button class="btn" id="vb" aria-pressed="${S.vocab}">${esc(t().vocab)}</button>
        </div>
      </div>
    </div></div>
    <main class="read wrap" id="text"></main>`;
  $('tr').value = (S.tr === 'ru' && !hasRu) ? 'none' : S.tr;
  renderText();
  const cur = document.querySelector('.pages [aria-current=true]');
  if (cur) cur.scrollIntoView({ inline: 'center', block: 'nearest' });
}

function sectionHTML(txt, rng) {
  let out = '', cur = 0;
  for (let id = rng[0]; id <= rng[1]; id++) {
    const w = D.W[id - 1], f = w[0], i = txt.indexOf(f, cur);
    if (i < 0) continue;
    out += esc(txt.slice(cur, i));
    let cls = 'w';
    if (w[3]) {
      const tn = w[3] === 'Z' ? 'X' : w[3];
      cls += ` vb T${tn}${S.on[tn] ? '' : ' off'}${w[4] === 'P' ? ' ptc' : w[4] === 'N' ? ' inf' : ''}`;
    }
    if (sameLem !== null && w[1] === sameLem) cls += ' same';
    out += `<span class="${cls}" tabindex="0" data-i="${id}">${esc(f)}</span>`;
    cur = i + f.length;
  }
  return out + esc(txt.slice(cur));
}

function vocabHTML(p) {
  const seen = new Map();
  for (const [, , rng] of p[1]) for (let id = rng[0]; id <= rng[1]; id++) seen.set(D.W[id - 1][1], 1);
  const rows = [...seen.keys()].map(i => D.L[i]).filter(l => l[2] !== 'definite article').sort((a, b) => b[5] - a[5]);
  return `<section class="vocab"><h2>${esc(t().vocab_h(p[0]))}</h2><table><tbody>${rows.map(l =>
    `<tr><td class="g">${esc(l[1])}</td><td class="gl">${esc(S.lang === 'ru' ? l[4] || l[3] : l[3])}</td><td class="n">${l[5]}</td></tr>`).join('')}</tbody></table></section>`;
}

function renderText() {
  const p = D.pages.find(x => x[0] === page);
  const i = D.pages.indexOf(p), letters = 'abcde';
  const tr = S.tr !== 'none' ? (D.tr[S.tr] || {}) : null;
  $('text').innerHTML = (S.vocab ? vocabHTML(p) : '') + p[1].map(([vs, txt, rng], k) => {
    const key = page + letters[vs - 1];
    return `<div class="sec" id="s${key}"><span class="m">${k === 0 ? page : ''}${letters[vs - 1]}</span><p class="t">${sectionHTML(txt, rng)}</p>${tr && tr[key] ? `<p class="tr">${esc(tr[key].replace(/^¶\s*/, '').replace(/\s*¶\s*/g, ' '))}</p>` : ''}</div>`;
  }).join('') + `<div class="pager">
      ${i > 0 ? `<a class="btn" href="#${text.id}-${D.pages[i - 1][0]}">${esc(t().prev)} ${D.pages[i - 1][0]}</a>` : '<span></span>'}
      ${i < D.pages.length - 1 ? `<a class="btn" href="#${text.id}-${D.pages[i + 1][0]}">${esc(t().next.replace('→', ''))}${D.pages[i + 1][0]} →</a>` : ''}
    </div><p class="legend">${esc(t().legend)}</p>`;
}

// ---------- word card ----------
function show(id) {
  const w = D.W[id - 1], L = D.L[w[1]], P = D.P[w[2]];
  $('lem').textContent = L[1];
  $('cnt').textContent = t().times(L[5]);
  $('gl').textContent = S.lang === 'ru' ? (L[4] || L[3]) : L[3];
  $('ps').textContent = S.lang === 'ru' ? P[1] : P[0];
  $('same').textContent = sameLem === w[1] ? t().unsame : t().same;
  $('same').dataset.l = w[1];
  $('card').classList.add('on');
  if (sel) sel.classList.remove('sel');
  sel = document.querySelector(`[data-i="${id}"]`);
  if (sel) sel.classList.add('sel');
}
function hide() { $('card').classList.remove('on'); if (sel) sel.classList.remove('sel'); sel = null; }

// ---------- routing ----------
function route() {
  const h = location.hash.slice(1);
  const m = h.match(/^([a-z]+)(?:-(\d+))?$/);
  if (m && TEXTS.some(x => x.id === m[1])) reader(m[1], m[2] ? +m[2] : null);
  else library();
}

// ---------- events ----------
document.querySelector('.lang').addEventListener('click', e => { const b = e.target.closest('button'); if (b) setLang(b.dataset.lang); });
$('app').addEventListener('click', e => {
  const pb = e.target.closest('.pages button');
  if (pb) { location.hash = `${text.id}-${pb.dataset.p}`; return; }
  const kb = e.target.closest('.key button');
  if (kb) { const k = kb.dataset.t; S.on[k] = S.on[k] ? 0 : 1; save(); kb.setAttribute('aria-pressed', !!S.on[k]); renderText(); return; }
  if (e.target.id === 'vb') { S.vocab = !S.vocab; save(); e.target.setAttribute('aria-pressed', S.vocab); renderText(); return; }
  const w = e.target.closest('.w');
  if (w) show(+w.dataset.i);
});
$('app').addEventListener('change', e => { if (e.target.id === 'tr') { S.tr = e.target.value; save(); renderText(); } });
$('app').addEventListener('keydown', e => { if (e.key === 'Enter') { const w = e.target.closest('.w'); if (w) show(+w.dataset.i); } });
$('close').addEventListener('click', hide);
$('same').addEventListener('click', e => {
  const l = +e.target.dataset.l; sameLem = sameLem === l ? null : l;
  const id = sel ? +sel.dataset.i : null; renderText(); if (id) show(id);
});
document.addEventListener('keydown', e => {
  if (e.key === 'Escape') hide();
  if (!D || /input|select/i.test(e.target.tagName)) return;
  const i = D.pages.findIndex(p => p[0] === page);
  if (e.key === 'ArrowRight' && i < D.pages.length - 1) location.hash = `${text.id}-${D.pages[i + 1][0]}`;
  if (e.key === 'ArrowLeft' && i > 0) location.hash = `${text.id}-${D.pages[i - 1][0]}`;
});
window.addEventListener('hashchange', () => { hide(); sameLem = null; route(); window.scrollTo({ top: 0 }); });
setLang(S.lang);
}
