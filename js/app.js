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
    how_p: 'Underlined words are finite verbs; participles and infinitives have their own markings (bold italic and dotted underline by default — you can change them with the ⚙ button). The colour shows the tense; tap a colour to switch it off. Use the language switch at the top for English or Russian meanings.',
    decl: ['', '1st declension', '2nd declension', '3rd declension'], like: 'like', stem: 'stem in', gend: { m: 'masculine', f: 'feminine', n: 'neuter' }, par: 'Declension table', unpar: 'Hide table', cases: ['Nom.', 'Gen.', 'Dat.', 'Acc.', 'Voc.'], sg: 'Singular', pl: 'Plural', recon: 'Grey forms are not found in the corpus and are reconstructed from the pattern.',
    marks: 'Marking of participles and infinitives', ptc: 'Participles', inf: 'Infinitives', sty: { bi: 'bold italic', it: 'italic', dot: 'dotted underline', dash: 'dashed underline', wavy: 'wavy underline', dbl: 'double underline', over: 'line above', box: 'frame', strike: 'strikethrough' },
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
    how_p: 'Подчёркнуты личные формы глагола; у причастий и инфинитивов своё обозначение (по умолчанию жирный курсив и пунктирное подчёркивание — его можно поменять кнопкой ⚙). Цвет показывает время; нажмите на цвет, чтобы его отключить. Переключатель языка вверху меняет значения слов на английские или русские.',
    decl: ['', 'I склонение', 'II склонение', 'III склонение'], like: 'как', stem: 'основа на', gend: { m: 'муж. р.', f: 'жен. р.', n: 'ср. р.' }, par: 'Парадигма', unpar: 'Скрыть парадигму', cases: ['Им.', 'Род.', 'Дат.', 'Вин.', 'Зват.'], sg: 'Ед. ч.', pl: 'Мн. ч.', recon: 'Серым — формы, которых нет в корпусе; они восстановлены по образцу.',
    marks: 'Обозначение причастий и инфинитивов', ptc: 'Причастия', inf: 'Инфинитивы', sty: { bi: 'жирный курсив', it: 'курсив', dot: 'пунктир снизу', dash: 'штрихи снизу', wavy: 'волна снизу', dbl: 'двойная линия', over: 'линия сверху', box: 'рамка', strike: 'зачёркивание' },
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
    how_p: 'ხაზგასმულია ზმნის პირიანი ფორმები; მიმღეობებსა და ინფინიტივებს საკუთარი აღნიშვნა აქვთ (ნაგულისხმევად მუქი დახრილი და წერტილოვანი ხაზი — შეგიძლიათ შეცვალოთ ⚙ ღილაკით). ფერი დროს აჩვენებს; ფერზე დაჭერით მას გამორთავთ.',
    decl: ['', 'I ბრუნება', 'II ბრუნება', 'III ბრუნება'], like: 'როგორც', stem: 'ფუძე', gend: { m: 'მამრ.', f: 'მდედრ.', n: 'საშ.' }, par: 'პარადიგმა', unpar: 'პარადიგმის დამალვა', cases: ['სახ.', 'ნათ.', 'მიც.', 'ბრალდ.', 'წოდ.'], sg: 'მხ.', pl: 'მრ.', recon: 'ნაცრისფრად — კორპუსში დაუდასტურებელი, ნიმუშით აღდგენილი ფორმები.',
    marks: 'მიმღეობებისა და ინფინიტივების აღნიშვნა', ptc: 'მიმღეობები', inf: 'ინფინიტივები', sty: { bi: 'მუქი დახრილი', it: 'დახრილი', dot: 'წერტილოვანი ხაზი', dash: 'წყვეტილი ხაზი', wavy: 'ტალღოვანი ხაზი', dbl: 'ორმაგი ხაზი', over: 'ხაზი ზემოთ', box: 'ჩარჩო', strike: 'გადახაზვა' },
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
const STY = ['bi', 'it', 'dot', 'dash', 'wavy', 'dbl', 'over', 'box', 'strike'];
const TENSES = ['P', 'I', 'F', 'A', 'X', 'Y'];

// ---------- state ----------
const S = { lang: 'en', tr: 'none', on: { P: 1, I: 1, F: 1, A: 1, X: 1, Y: 1 }, vocab: false, last: {}, ptc: 'bi', inf: 'dot' };
try { Object.assign(S, JSON.parse(localStorage.getItem('anagnosis') || '{}')); } catch (e) {}
const save = () => { try { localStorage.setItem('anagnosis', JSON.stringify(S)); } catch (e) {} };
const cache = {};
let D = null, text = null, book = null, page = null, sel = null, sameLem = null;

const $ = id => document.getElementById(id);
const esc = s => String(s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
if (!T[S.lang]) S.lang = 'en';
if (!['bi','it','dot','dash','wavy','dbl','over','box','strike'].includes(S.ptc)) S.ptc = 'bi';
if (!['bi','it','dot','dash','wavy','dbl','over','box','strike'].includes(S.inf)) S.inf = 'dot';
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
    try { cache[file] = await (await fetch(file + '?v=20261128a')).json(); }
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
        <div class="key" role="group">${TENSES.map(k => `<button class="T${k}" data-t="${k}" aria-pressed="${!!S.on[k]}"><i></i>${esc(t().tense[k])}</button>`).join('')}<span class="gearw"><button class="gear" id="gear" aria-expanded="false" title="${esc(t().marks)}" aria-label="${esc(t().marks)}">⚙</button><div class="marks" id="marks" hidden><div><label for="mptc">${esc(t().ptc)}</label><select id="mptc">${STY.map(k => `<option value="${k}" ${S.ptc === k ? 'selected' : ''}>${esc(t().sty[k])}</option>`).join('')}</select></div><div><label for="minf">${esc(t().inf)}</label><select id="minf">${STY.map(k => `<option value="${k}" ${S.inf === k ? 'selected' : ''}>${esc(t().sty[k])}</option>`).join('')}</select></div></div></span></div>
        <div class="opts">
          <label for="tr">${esc(t().trans)}</label>
          <select id="tr"><option value="none">${esc(t().none)}</option><option value="en" ${hasEn ? '' : 'disabled'}>${esc(t().en)}</option>
            <option value="ru" ${hasRu ? '' : 'disabled'}>${esc(hasRu ? (x.ruLabel ? x.ruLabel[S.lang] : t().ru) : t().ru_soon)}</option>${hasKa ? `<option value="ka">${esc(t().ka)}</option>` : ''}</select>
          <button class="btn" id="vb" aria-pressed="${S.vocab}">${esc(t().vocab)}</button>
        </div>
      </div>
    </div></div>
    <main class="read wrap ptc-${S.ptc} inf-${S.inf}" id="text"></main>`;
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

// ---------- syntactic constructions ----------
const CXT = {
  ru: {
    head: 'Конструкция', mem: 'Связанные слова', gov: 'Зависит от', show: 'Показать конструкцию', hide: 'Скрыть конструкцию',
    auto: 'Определено автоматически по синтаксическому разбору; возможны ошибки.',
    c: {
      aci: ['Винительный с инфинитивом', 'accusativus cum infinitivo', 'Подлежащее инфинитива стоит в винительном падеже. Оборот зависит от глагола речи, мысли, желания или приказа и обычно переводится придаточным: «что…», «чтобы…».'],
      nci: ['Именительный с инфинитивом', 'nominativus cum infinitivo', 'Подлежащее инфинитива то же, что у управляющего глагола (δοκεῖ «кажется», λέγεται «говорят»), поэтому оно и именная часть стоят в именительном: «он, кажется, …», «говорят, что он …».'],
      gen_abs: ['Родительный самостоятельный', 'genitivus absolutus', 'Причастие и его подлежащее стоят в родительном и грамматически не связаны с остальным предложением. Переводится придаточным: «когда…», «так как…», «хотя…», «если…».'],
      acc_abs: ['Винительный самостоятельный', 'accusativus absolutus', 'Причастие безличного глагола в винительном ср. р. (ἐξόν «хотя можно», δέον «хотя нужно», δόξαν «когда решили»). Употребляется вместо родительного самостоятельного, когда подлежащего нет.'],
      tygx: ['Дополнительное причастие (τυγχάνω, λανθάνω, φθάνω)', 'participium coniunctum', 'Главный смысл несёт причастие, а глагол лишь добавляет оттенок: τυγχάνω + прич. «как раз, случайно …», λανθάνω + прич. «… незаметно», φθάνω + прич. «… раньше (кого-то)», διατελέω + прич. «постоянно …».'],
      perc: ['Причастие после глагола восприятия или знания', 'participium in oratione obliqua', 'После «видеть, слышать, знать, узнавать» причастие передаёт содержание восприятия: «увидел, что они приближаются». Переводится придаточным с «что» или «как».'],
      fut_ptc: ['Будущее причастие цели', 'participium futuri finale', 'Будущее причастие (часто с ὡς) выражает цель: «пришёл, чтобы сражаться». С ὡς цель подаётся как намерение действующего лица.'],
      art_inf: ['Субстантивированный инфинитив', 'infinitivus cum articulo', 'Инфинитив с артиклем ср. р. ведёт себя как существительное и склоняется через артикль: τὸ μάχεσθαι «сражение», τοῦ μάχεσθαι «сражения», διὰ τὸ εἶναι «из-за того, что был».'],
      prin: ['πρίν с инфинитивом', 'priusquam', 'После утвердительного главного предложения πρίν + инфинитив значит «прежде чем, до того как». Подлежащее инфинитива, если оно отличается, стоит в винительном.'],
      hoste_inf: ['ὥστε с инфинитивом', 'consecutio', 'Следствие, которое мыслится как возможное или естественное: «так, чтобы…», «настолько, что могли бы…».'],
      hoste_ind: ['ὥστε с изъявительным', 'consecutio', 'Действительно наступившее следствие: «так что (и на самом деле)…».'],
      pot_opt: ['Потенциальный оптатив', 'optativus potentialis', 'Оптатив с ἄν выражает возможность или вежливое утверждение: «мог бы», «пожалуй». С οὐ — «вряд ли», «не смог бы».'],
      unreal: ['Ирреальное условие', 'irrealis', 'Прошедшее время изъявительного наклонения с ἄν описывает то, чего на деле нет или не было: имперфект — «…бы» (сейчас), аорист — «…бы» (в прошлом).'],
      an_inf: ['ἄν при инфинитиве или причастии', 'potentialis in oratione obliqua', 'В косвенной речи ἄν при инфинитиве или причастии сохраняет значение возможности или нереальности, которое в прямой речи имел оптатив или изъявительное с ἄν.'],
      obl_opt: ['Оптатив косвенной речи', 'optativus obliquus', 'После прошедшего времени в главном предложении глагол придаточного (ὅτι, ὡς, косвенный вопрос) может стоять в оптативе. По-русски переводится обычным изъявительным: «сказал, что он ушёл».'],
      iter_opt: ['Повторяющееся действие в прошлом', 'optativus iterativus', 'Оптатив во временном или относительном придаточном (ἐπεί, ὁπότε, ὅστις) после прошедшего времени означает повторение: «всякий раз, когда…».'],
      final_opt: ['Придаточное цели или старания', 'optativus finalis', 'После прошедшего времени глагол в придаточном цели (ἵνα, ὅπως, ὡς) может стоять в оптативе вместо конъюнктива: «чтобы…».'],
      ei_opt: ['εἰ с оптативом', 'condicio potentialis / iterativa', 'Условие с εἰ + оптатив: либо «если бы (вдруг)…» о будущем (обычно с ἄν + оптатив в главном), либо «всякий раз, если…» о прошлом, либо косвенный вопрос «ли».'],
      wish_opt: ['Оптатив желания', 'optativus cupitivus', 'Оптатив без ἄν (часто с εἴθε, εἰ γάρ) выражает пожелание: «да будет…», «о если бы…».'],
    },
  },
  en: {
    head: 'Construction', mem: 'Related words', gov: 'Depends on', show: 'Show construction', hide: 'Hide construction',
    auto: 'Detected automatically from the syntactic parse; errors are possible.',
    c: {
      aci: ['Accusative and infinitive', 'accusativus cum infinitivo', 'The subject of the infinitive is in the accusative. It depends on a verb of saying, thinking, wishing or ordering and is usually translated with a clause: “that…”.'],
      nci: ['Nominative and infinitive', 'nominativus cum infinitivo', 'The infinitive has the same subject as the governing verb (δοκεῖ “seems”, λέγεται “is said”), so subject and predicate stay in the nominative: “he seems to be…”.'],
      gen_abs: ['Genitive absolute', 'genitivus absolutus', 'A participle and its subject in the genitive, grammatically independent of the rest of the sentence. Translate with a clause: “when…”, “since…”, “although…”, “if…”.'],
      acc_abs: ['Accusative absolute', 'accusativus absolutus', 'A neuter accusative participle of an impersonal verb (ἐξόν “although it was possible”, δέον “it being necessary”, δόξαν “when it was decided”), used instead of a genitive absolute when there is no subject.'],
      tygx: ['Supplementary participle (τυγχάνω, λανθάνω, φθάνω)', 'participium coniunctum', 'The participle carries the main idea; the verb adds a nuance: τυγχάνω + ptc. “happen to …”, λανθάνω + ptc. “… unnoticed”, φθάνω + ptc. “… first”, διατελέω + ptc. “keep on …”.'],
      perc: ['Participle after a verb of perceiving or knowing', 'participium in oratione obliqua', 'After “see, hear, know, learn” the participle gives the content of the perception: “saw that they were approaching”.'],
      fut_ptc: ['Future participle of purpose', 'participium futuri finale', 'A future participle (often with ὡς) expresses purpose: “came to fight”. With ὡς the purpose is presented as the subject’s intention.'],
      art_inf: ['Articular infinitive', 'infinitivus cum articulo', 'An infinitive with the neuter article works as a noun and is declined through the article: τὸ μάχεσθαι “fighting”, διὰ τὸ εἶναι “because of being”.'],
      prin: ['πρίν with infinitive', 'priusquam', 'After an affirmative main clause πρίν + infinitive means “before”. A different subject of the infinitive is in the accusative.'],
      hoste_inf: ['ὥστε with infinitive', 'consecutio', 'A result regarded as possible or natural: “so as to…”.'],
      hoste_ind: ['ὥστε with indicative', 'consecutio', 'A result that actually happened: “so that (in fact)…”.'],
      pot_opt: ['Potential optative', 'optativus potentialis', 'The optative with ἄν expresses possibility or a polite statement: “could”, “might”, “would”.'],
      unreal: ['Contrary-to-fact', 'irrealis', 'A past tense of the indicative with ἄν describes what is or was not so: imperfect “would (now)”, aorist “would have”.'],
      an_inf: ['ἄν with infinitive or participle', 'potentialis in oratione obliqua', 'In indirect speech ἄν with an infinitive or participle keeps the potential or unreal sense of an optative or indicative with ἄν in direct speech.'],
      obl_opt: ['Optative of indirect discourse', 'optativus obliquus', 'After a past tense in the main clause, the verb of a ὅτι/ὡς clause or indirect question may be put into the optative. Translate as an ordinary indicative.'],
      iter_opt: ['Repeated action in the past', 'optativus iterativus', 'An optative in a temporal or relative clause (ἐπεί, ὁπότε, ὅστις) after a past tense means repetition: “whenever…”.'],
      final_opt: ['Purpose or effort clause', 'optativus finalis', 'After a past tense the verb of a purpose clause (ἵνα, ὅπως, ὡς) may be in the optative instead of the subjunctive: “in order that…”.'],
      ei_opt: ['εἰ with optative', 'condicio potentialis / iterativa', 'A condition with εἰ + optative: “if (ever)… should” about the future, “whenever… if” about the past, or an indirect question “whether”.'],
      wish_opt: ['Optative of wish', 'optativus cupitivus', 'The optative without ἄν (often with εἴθε, εἰ γάρ) expresses a wish: “may…”, “if only…”.'],
    },
  },
  ka: {
    head: 'კონსტრუქცია', mem: 'დაკავშირებული სიტყვები', gov: 'დამოკიდებულია', show: 'კონსტრუქციის ჩვენება', hide: 'კონსტრუქციის დამალვა',
    auto: 'განსაზღვრულია ავტომატურად სინტაქსური ანალიზით; შეცდომები შესაძლებელია.',
  },
};
CXT.ka.c = CXT.en.c;
let cxOn = true, cxCur = [];
function cxMark(on) {
  document.querySelectorAll('.cx-me,.cx-m,.cx-g').forEach(e => e.classList.remove('cx-me', 'cx-m', 'cx-g'));
  if (!on) return;
  for (const [i, , m, g] of cxCur) {
    const q = k => document.querySelector(`[data-i="${k + 1}"]`);
    q(i)?.classList.add('cx-me'); m.forEach(k => q(k)?.classList.add('cx-m')); g.forEach(k => q(k)?.classList.add('cx-g'));
  }
}
function cxShow(id) {
  if (!D.CX) { D.CX = new Map(); for (const c of D.C || []) { if (!D.CX.has(c[0])) D.CX.set(c[0], []); D.CX.get(c[0]).push(c); } }
  cxCur = D.CX.get(id - 1) || [];
  const X = CXT[S.lang] || CXT.en, words = ks => ks.map(k => D.W[k][0]).join(' ');
  $('cx').innerHTML = cxCur.map(([, code, m, g]) => {
    const [name, lat, ex] = X.c[code];
    return `<div class="cxb"><div class="cxh">${esc(X.head)}</div><div class="cxn">${esc(name)} <span class="lat">· ${esc(lat)}</span></div>
      <div class="cxe">${esc(ex)}</div>${m.length ? `<div class="cxw">${esc(X.mem)}: <b>${esc(words(m))}</b></div>` : ''}${g.length ? `<div class="cxw">${esc(X.gov)}: <b>${esc(words(g))}</b></div>` : ''}</div>`;
  }).join('') + (cxCur.length ? `<p class="note">${esc(X.auto)}</p>` : '');
  $('cx').hidden = !cxCur.length; $('cxt').hidden = !cxCur.length;
  $('cxt').textContent = cxOn ? X.hide : X.show;
  cxMark(cxOn && cxCur.length);
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
  $('dc').hidden = true; $('pd').hidden = true; $('par').hidden = true; parOpen = false;
  if (L[2] === 'noun') nounInfo(L[0], w[0]);
  cxShow(id);
  $('card').classList.add('on');
  if (sel) sel.classList.remove('sel');
  sel = document.querySelector(`[data-i="${id}"]`);
  if (sel) sel.classList.add('sel');
}
let NOUNS = null, parOpen = false, curNoun = null;
const loadNouns = () => NOUNS || (NOUNS = fetch('data/nouns.json?v=20261128a').then(r => r.json()).catch(() => ({})));
const plainAcc = f => (f || '').normalize('NFD').replace(/\u0300/g, '\u0301').normalize('NFC').toLowerCase();
function nounInfo(lem, form) {
  loadNouns().then(N => {
    const n = N[lem];
    if (!n || !$('card').classList.contains('on')) return;
    const [d, typ, g] = n;
    let s = d ? t().decl[d] : '';
    if (typ && typ !== lem) s += typ.startsWith('-') ? ` (${t().stem} ${typ})` : ` (${t().like} ${typ})`;
    if (g && t().gend[g]) s += (s ? ', ' : '') + t().gend[g];
    $('dc').textContent = s; $('dc').hidden = !s;
    curNoun = { n, form };
    $('par').hidden = !n[3]; $('par').textContent = t().par;
  });
}
function paradigmHTML() {
  const { n, form } = curNoun; const F = n[3].split('|'), st = n[4], me = plainAcc(form);
  const hasPl = F.slice(5).some(Boolean);
  const cell = i => F[i] ? `<td class="${st[i] === 'g' ? 'rc' : ''}${plainAcc(F[i]) === me ? ' me' : ''}">${esc(F[i])}</td>` : '<td>—</td>';
  let h = `<table><tr><th></th><th>${esc(t().sg)}</th>${hasPl ? `<th>${esc(t().pl)}</th>` : ''}</tr>`;
  for (let c = 0; c < 5; c++) h += `<tr><th>${esc(t().cases[c])}</th>${cell(c)}${hasPl ? cell(c + 5) : ''}</tr>`;
  h += '</table>';
  if (st.includes('g')) h += `<p class="note">${esc(t().recon)}</p>`;
  return h;
}
function hide() { cxMark(false); $('card').classList.remove('on'); if (sel) sel.classList.remove('sel'); sel = null; }

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
  if (e.target.id === 'gear') { const m = $('marks'); m.hidden = !m.hidden; e.target.setAttribute('aria-expanded', !m.hidden); return; }
  if ($('marks') && !$('marks').hidden && !e.target.closest('.gearw')) { $('marks').hidden = true; $('gear').setAttribute('aria-expanded', 'false'); }
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
$('app').addEventListener('change', e => { if (e.target.id === 'tr') { S.tr = e.target.value; save(); renderText(); }
  if (e.target.id === 'mptc' || e.target.id === 'minf') { const k = e.target.id.slice(1); $('text').classList.remove(k + '-' + S[k]); S[k] = e.target.value; save(); $('text').classList.add(k + '-' + S[k]); } });
$('app').addEventListener('keydown', e => { if (e.key === 'Enter') { const w = e.target.closest('.w'); if (w) show(+w.dataset.i); } });
$('close').addEventListener('click', hide);
$('cxt').addEventListener('click', () => {
  cxOn = !cxOn; const X = CXT[S.lang] || CXT.en;
  $('cxt').textContent = cxOn ? X.hide : X.show; cxMark(cxOn);
});
$('par').addEventListener('click', () => {
  parOpen = !parOpen;
  if (parOpen) $('pd').innerHTML = paradigmHTML();
  $('pd').hidden = !parOpen; $('par').textContent = parOpen ? t().unpar : t().par;
});
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
