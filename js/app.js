{
// ---------- catalogue ----------
// A text has either one data file (file) or several books (books: number -> file).
const TEXTS = [
  { id: 'apology', file: 'data/apology.json', gr: 'Ἀπολογία Σωκράτους',
    title: { en: 'Apology of Socrates', ru: 'Апология Сократа', ka: 'სოკრატეს აპოლოგია' }, author: { en: 'Plato', ru: 'Платон', ka: 'პლატონი' },
    unit: { en: 'Stephanus page', ru: 'страница Стефана', ka: 'სტეფანუსის გვერდი' } },
  { id: 'anabasis', gr: 'Κύρου Ἀνάβασις', title: { en: 'Anabasis', ru: 'Анабасис', ka: 'ანაბასისი' },
    author: { en: 'Xenophon', ru: 'Ксенофонт', ka: 'ქსენოფონტი' },
    ruLabel: { en: 'Russian (experimental)', ru: 'Русский (экспериментальный)', ka: 'რუსული (ექსპერიმენტული)' }, unit: { en: 'Chapter', ru: 'Глава', ka: 'თავი' },
    books: { 1: 'data/anabasis-1.json', 2: 'data/anabasis-2.json', 3: 'data/anabasis-3.json', 4: 'data/anabasis-4.json', 5: 'data/anabasis-5.json', 6: 'data/anabasis-6.json', 7: 'data/anabasis-7.json' }, nbooks: 7 },
];
const ROMAN = ['', 'I', 'II', 'III', 'IV', 'V', 'VI', 'VII'];

// ---------- interface strings ----------
const T = {
  en: {
    tagline: 'Ancient Greek, word by word', lib_h: 'Read Ancient Greek, word by word',
    lib_p: 'Tap any word to see its dictionary form, meaning and full parsing. Verbs are coloured by tense. Translations can be shown under each section.',
    open: 'Read', soon: 'Coming soon', how_h: 'How to read',
    how_p: 'Underlined words are finite verbs, bold italic words are participles and struck-through words are infinitives. The colour shows the tense; tap a colour to switch it off. Use the language switch at the top for English or Russian meanings.',
    back: '← Library', tense: { P: 'Present', I: 'Imperfect', F: 'Future', A: 'Aorist', X: 'Perfect', Y: 'Pluperfect' },
    trans: 'Translation', none: 'None', en: 'English', ru: 'Russian', ka: 'Georgian', ru_soon: 'Russian (coming soon)',
    vocab: 'Page vocabulary', vocab_h: p => `Words on this page (${p})`,
    times: n => `${n}× in this text`, same: 'Mark all forms on this page', unsame: 'Clear marks',
    prev: '←', next: '→', loading: 'Loading the text…', failed: 'The text could not be loaded.',
    book: 'Book', books_ready: n => `Book${n > 1 ? 's' : ''} ${n === 1 ? 'I' : 'I–' + ROMAN[n]} available`,
    legend: {
      apology: 'Text, lemmas and parsing: GLAUx corpus (A. Keersmaekers, CC BY-SA 4.0), based on the Perseus Digital Library. English translation: H. N. Fowler (1914), Perseus, CC BY-SA. Russian translation: M. S. Solovyov (1899–1903), public domain. Georgian translation: Levan Berdzenishvili, used with the translator’s permission. Meanings: Greek Study App dictionary (J. Jansen) and written for this site.',
      anabasis: 'Text: Perseus Digital Library. Lemmas and parsing: GLAUx corpus (A. Keersmaekers, CC BY-SA 4.0), corrected with V. Gorman\'s hand-checked treebank. English translation: C. L. Brownson (1922), Perseus, CC BY-SA. Russian translation: experimental, made for this site directly from the Greek; it may contain errors. Meanings: Greek Study App dictionary (J. Jansen) and written for this site.',
    },
    foot: 'Open project. Corrections are welcome on GitHub.',
  },
  ru: {
    tagline: 'Древнегреческий, слово за словом', lib_h: 'Читайте по-древнегречески, слово за словом',
    lib_p: 'Нажмите на любое слово, чтобы увидеть его словарную форму, значение и полный разбор. Глаголы окрашены по времени. Перевод можно показать под каждым разделом.',
    open: 'Читать', soon: 'Скоро', how_h: 'Как читать',
    how_p: 'Подчёркнуты личные формы глагола, жирным курсивом выделены причастия, зачёркнуты инфинитивы. Цвет показывает время; нажмите на цвет, чтобы его отключить. Переключатель языка вверху меняет значения слов на английские или русские.',
    back: '← Библиотека', tense: { P: 'Настоящее', I: 'Имперфект', F: 'Будущее', A: 'Аорист', X: 'Перфект', Y: 'Плюсквамперфект' },
    trans: 'Перевод', none: 'Нет', en: 'Английский', ru: 'Русский', ka: 'Грузинский', ru_soon: 'Русский (скоро)',
    vocab: 'Слова страницы', vocab_h: p => `Слова на этой странице (${p})`,
    times: n => `${n}× в этом тексте`, same: 'Отметить все формы на странице', unsame: 'Снять отметки',
    prev: '←', next: '→', loading: 'Загрузка текста…', failed: 'Не удалось загрузить текст.',
    book: 'Книга', books_ready: n => n === 1 ? 'Доступна книга I' : `Доступны книги I–${ROMAN[n]}`,
    legend: {
      apology: 'Текст, леммы и разбор: корпус GLAUx (A. Keersmaekers, CC BY-SA 4.0) на основе Perseus Digital Library. Английский перевод: H. N. Fowler (1914), Perseus, CC BY-SA. Русский перевод: М. С. Соловьёв (1899–1903), общественное достояние. Грузинский перевод: Леван Бердзенишвили, публикуется с разрешения переводчика. Значения: словарь Greek Study App (J. Jansen) и составленные для этого сайта.',
      anabasis: 'Текст: Perseus Digital Library. Леммы и разбор: корпус GLAUx (A. Keersmaekers, CC BY-SA 4.0), исправленный по размеченному вручную корпусу В. Горман. Английский перевод: C. L. Brownson (1922), Perseus, CC BY-SA. Русский перевод: экспериментальный, выполнен для этого сайта непосредственно с греческого; возможны ошибки. Значения: словарь Greek Study App (J. Jansen) и составленные для этого сайта.',
    },
    foot: 'Открытый проект. Исправления приветствуются на GitHub.',
  },
  ka: {
    tagline: 'ძველი ბერძნული, სიტყვა-სიტყვით', lib_h: 'იკითხეთ ძველბერძნულად, სიტყვა-სიტყვით',
    lib_p: 'დააჭირეთ ნებისმიერ სიტყვას და ნახავთ მის ლექსიკონურ ფორმას, მნიშვნელობასა და სრულ გრამატიკულ ანალიზს. ზმნები დროების მიხედვით არის გაფერადებული. ყოველი მონაკვეთის ქვეშ შეგიძლიათ თარგმანის ჩვენება.',
    open: 'კითხვა', soon: 'მალე', how_h: 'როგორ ვიკითხოთ',
    how_p: 'ხაზგასმულია ზმნის პირიანი ფორმები, მუქი დახრილით — მიმღეობები, გადახაზულია ინფინიტივები. ფერი დროს აჩვენებს; ფერზე დაჭერით მას გამორთავთ. სიტყვების მნიშვნელობა და ანალიზი ჯერჯერობით ინგლისურადაა; ზედა გადამრთველით შეგიძლიათ რუსულზე გადართვა.',
    back: '← ბიბლიოთეკა', tense: { P: 'აწმყო', I: 'იმპერფექტი', F: 'მყოფადი', A: 'აორისტი', X: 'პერფექტი', Y: 'პლუსკვამპერფექტი' },
    trans: 'თარგმანი', none: 'არა', en: 'ინგლისური', ru: 'რუსული', ka: 'ქართული', ru_soon: 'რუსული (მალე)',
    vocab: 'გვერდის ლექსიკა', vocab_h: p => `ამ გვერდის სიტყვები (${p})`,
    times: n => `${n}-ჯერ ამ ტექსტში`, same: 'ამ გვერდზე ყველა ფორმის მონიშვნა', unsame: 'მონიშვნის მოხსნა',
    prev: '←', next: '→', loading: 'ტექსტი იტვირთება…', failed: 'ტექსტის ჩატვირთვა ვერ მოხერხდა.',
    book: 'წიგნი', books_ready: n => n === 1 ? 'ხელმისაწვდომია I წიგნი' : `ხელმისაწვდომია I–${ROMAN[n]} წიგნები`,
    legend: {
      apology: 'ტექსტი, ლემები და ანალიზი: კორპუსი GLAUx (A. Keersmaekers, CC BY-SA 4.0), Perseus Digital Library-ის საფუძველზე. ინგლისური თარგმანი: H. N. Fowler (1914), Perseus, CC BY-SA. რუსული თარგმანი: მ. ს. სოლოვიოვი (1899–1903), საზოგადოებრივი საკუთრება. ქართული თარგმანი: ლევან ბერძენიშვილი, ქვეყნდება მთარგმნელის ნებართვით. მნიშვნელობები: Greek Study App-ის ლექსიკონი (J. Jansen) და ამ საიტისთვის შედგენილი.',
      anabasis: 'ტექსტი: Perseus Digital Library. ლემები და ანალიზი: კორპუსი GLAUx (A. Keersmaekers, CC BY-SA 4.0), შესწორებული ვ. გორმანის ხელით შემოწმებული კორპუსით. ინგლისური თარგმანი: C. L. Brownson (1922), Perseus, CC BY-SA. რუსული თარგმანი: ექსპერიმენტული, შესრულებულია ამ საიტისთვის უშუალოდ ბერძნულიდან; შესაძლოა შეიცავდეს შეცდომებს. მნიშვნელობები: Greek Study App-ის ლექსიკონი (J. Jansen) და ამ საიტისთვის შედგენილი.',
    },
    foot: 'ღია პროექტი. შესწორებებს სიამოვნებით მივიღებთ GitHub-ზე.',
  },
};
const TENSES = ['P', 'I', 'F', 'A', 'X', 'Y'];

// ---------- state ----------
const S = { lang: 'en', tr: 'none', on: { P: 1, I: 1, F: 1, A: 1, X: 1, Y: 1 }, vocab: false, last: {} };
try { Object.assign(S, JSON.parse(localStorage.getItem('anagnosis') || '{}')); } catch (e) {}
const save = () => { try { localStorage.setItem('anagnosis', JSON.stringify(S)); } catch (e) {} };
const cache = {};
let D = null, text = null, book = null, page = null, sel = null, sameLem = null;

const $ = id => document.getElementById(id);
const esc = s => String(s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
if (!T[S.lang]) S.lang = 'en';
const t = () => T[S.lang] || T.en;
const ready = x => !!(x.file || x.books);
const nBooks = x => x.books ? Object.keys(x.books).length : 0;
// hash for a place in a text: #apology-17, #anabasis-1-3
const href = (x, b, p) => '#' + x.id + (x.books ? `-${b}` : '') + (p ? `-${p}` : '');
const STEPH = () => D.scheme !== 'section';
const secKey = (p, vs) => STEPH() ? p + 'abcde'[vs - 1] : `${p}.${vs}`;

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
    <div class="shelf">${TEXTS.map(x => `<a class="book${ready(x) ? '' : ' soon'}" href="${href(x, 1)}">
      <div class="gr">${esc(x.gr)}</div>
      <div class="au">${esc(x.author[S.lang])} · ${esc(x.title[S.lang])}</div>
      ${x.books ? `<div class="meta">${esc(t().books_ready(nBooks(x)))}</div>` : ''}
      <span class="tag">${esc(ready(x) ? t().open : t().soon)}</span></a>`).join('')}</div>
    <section class="howto"><h2>${esc(t().how_h)}</h2><p>${esc(t().how_p)}</p></section></div>`;
}

// ---------- reader ----------
async function reader(id, b, pg) {
  const x = TEXTS.find(a => a.id === id && ready(a));
  if (!x) { location.hash = ''; return; }
  const last = S.last[id] || {};
  if (x.books) {
    if (!x.books[b]) b = x.books[last.book] ? last.book : +Object.keys(x.books)[0];
  } else b = null;
  const file = x.books ? x.books[b] : x.file;
  if (!cache[file]) {
    $('app').innerHTML = `<p class="wrap empty">${esc(t().loading)}</p>`;
    try { cache[file] = await (await fetch(file + '?v=20261126i')).json(); }
    catch (e) { $('app').innerHTML = `<p class="wrap empty">${esc(t().failed)}</p>`; return; }
  }
  D = cache[file]; text = x; book = b;
  const pages = D.pages.map(p => p[0]);
  page = pages.includes(pg) ? pg : (last.book === b && pages.includes(last.page) ? last.page : pages[0]);
  S.last[id] = { book: b, page }; save();
  const where = x.books ? `${ROMAN[b]}.${page}` : `${page}`;
  document.title = `${x.title[S.lang]} ${where} · Anagnosis`;
  const hasRu = Object.keys(D.tr.ru || {}).length > 0, hasEn = Object.keys(D.tr.en || {}).length > 0, hasKa = Object.keys(D.tr.ka || {}).length > 0;
  const bookNav = x.books ? `<nav class="pages books" aria-label="${esc(t().book)}">${Array.from({ length: x.nbooks }, (_, i) => i + 1)
    .map(n => `<button data-b="${n}" aria-current="${n === b}" ${x.books[n] ? '' : 'disabled'}>${esc(t().book)} ${ROMAN[n]}</button>`).join('')}</nav>` : '';
  $('app').innerHTML = `
    <div class="bar"><div class="wrap">
      <div class="title"><a href="#">${esc(t().back)}</a><h1>${esc(x.author[S.lang])}, ${esc(x.title[S.lang])}${x.books ? ' ' + ROMAN[b] : ''}</h1></div>
      ${bookNav}
      <nav class="pages" aria-label="${esc(x.unit[S.lang])}">${pages.map(p => `<button data-p="${p}" aria-current="${p === page}">${p}</button>`).join('')}</nav>
      <div class="ctrl">
        <div class="key" role="group">${TENSES.map(k => `<button class="T${k}" data-t="${k}" aria-pressed="${!!S.on[k]}"><i></i>${esc(t().tense[k])}</button>`).join('')}</div>
        <div class="opts">
          <label for="tr">${esc(t().trans)}</label>
          <select id="tr"><option value="none">${esc(t().none)}</option><option value="en" ${hasEn ? '' : 'disabled'}>${esc(t().en)}</option>
            <option value="ru" ${hasRu ? '' : 'disabled'}>${esc(hasRu ? (x.ruLabel ? x.ruLabel[S.lang] : t().ru) : t().ru_soon)}</option>${hasKa ? `<option value="ka">${esc(t().ka)}</option>` : ''}</select>
          <button class="btn" id="vb" aria-pressed="${S.vocab}">${esc(t().vocab)}</button>
        </div>
      </div>
    </div></div>
    <main class="read wrap" id="text"></main>`;
  $('tr').value = (S.tr === 'ru' && !hasRu) || (S.tr === 'en' && !hasEn) || (S.tr === 'ka' && !hasKa) ? 'none' : S.tr;
  renderText();
  document.querySelectorAll('.pages [aria-current=true]').forEach(c => c.scrollIntoView({ inline: 'center', block: 'nearest' }));
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
  const where = text.books ? `${ROMAN[book]}.${p[0]}` : p[0];
  return `<section class="vocab"><h2>${esc(t().vocab_h(where))}</h2><table><tbody>${rows.map(l =>
    `<tr><td class="g">${esc(l[1])}</td><td class="gl">${esc(S.lang === 'ru' ? l[4] || l[3] : l[3])}</td><td class="n">${l[5]}</td></tr>`).join('')}</tbody></table></section>`;
}

function renderText() {
  const p = D.pages.find(x => x[0] === page);
  const i = D.pages.indexOf(p);
  const tr = S.tr !== 'none' ? (D.tr[S.tr] || {}) : null;
  $('text').innerHTML = (S.vocab ? vocabHTML(p) : '') + p[1].map(([vs, txt, rng], k) => {
    const key = secKey(page, vs);
    const label = STEPH() ? (k === 0 ? page : '') + 'abcde'[vs - 1] : (k === 0 ? `${page}.${vs}` : vs);
    return `<div class="sec" id="s${key}"><span class="m">${label}</span><p class="t">${sectionHTML(txt, rng)}</p>${tr && tr[key] ? `<p class="tr">${esc(tr[key].replace(/^¶\s*/, '').replace(/\s*¶\s*/g, ' '))}</p>` : ''}</div>`;
  }).join('') + `<div class="pager">
      ${i > 0 ? `<a class="btn" href="${href(text, book, D.pages[i - 1][0])}">${esc(t().prev)} ${D.pages[i - 1][0]}</a>` : '<span></span>'}
      ${i < D.pages.length - 1 ? `<a class="btn" href="${href(text, book, D.pages[i + 1][0])}">${D.pages[i + 1][0]} ${esc(t().next)}</a>` : ''}
    </div><p class="legend">${esc(t().legend[text.id] || '')}</p>`;
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
  const m = location.hash.slice(1).match(/^([a-z]+)(?:-(\d+))?(?:-(\d+))?$/);
  const x = m && TEXTS.find(a => a.id === m[1]);
  if (!x) return library();
  if (x.books) reader(x.id, m[2] ? +m[2] : null, m[3] ? +m[3] : null);
  else reader(x.id, null, m[2] ? +m[2] : null);
}

// ---------- events ----------
document.querySelector('.lang').addEventListener('click', e => { const b = e.target.closest('button'); if (b) setLang(b.dataset.lang); });
$('app').addEventListener('click', e => {
  const bb = e.target.closest('.books button');
  if (bb) { location.hash = href(text, +bb.dataset.b); return; }
  const pb = e.target.closest('.pages button');
  if (pb) { location.hash = href(text, book, pb.dataset.p); return; }
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
  if (e.key === 'ArrowRight' && i < D.pages.length - 1) location.hash = href(text, book, D.pages[i + 1][0]);
  if (e.key === 'ArrowLeft' && i > 0) location.hash = href(text, book, D.pages[i - 1][0]);
});
window.addEventListener('hashchange', () => { hide(); sameLem = null; route(); window.scrollTo({ top: 0 }); });
setLang(S.lang);
}
