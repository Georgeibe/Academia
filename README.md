# Ἀνάγνωσις: Ancient Greek, word by word

A small static website for reading Ancient Greek texts. Tap any word to see its dictionary form, meaning (English or Russian) and full parsing. Verbs are coloured by tense, and a translation can be shown under each section.

Texts:
- Plato, *Apology of Socrates* (Stephanus pages 17–42), with English and Russian translations.
- Xenophon, *Anabasis*, Books I–VII, with English translation.

## Publish on GitHub Pages
1. Create a new repository on GitHub and upload everything in this folder (keep the folder structure).
2. In the repository, go to **Settings → Pages**. Under "Build and deployment", choose **Deploy from a branch**, then branch `main` and folder `/ (root)`. Save.
3. After a minute the site is live at `https://<your-username>.github.io/<repository-name>/`.

The site is plain HTML, CSS and JavaScript with no build step. To try it on your own computer, run `python3 -m http.server` in this folder and open http://localhost:8000. Opening `index.html` directly from disk won't work, because browsers block loading the data file that way.

## Folders
- `index.html`, `css/`, `js/`: the website.
- `data/apology.json`, `data/anabasis-1.json`: each text with every word's parsing, the dictionary (English and Russian meanings) and the translations. Multi-book texts have one file per book.
- `tools/`: scripts that produce the data.
  - `build.py` converts a GLAUx text to a word database.
  - `export_site.py` turns that database into the website JSON.
  - `merge_gorman.py` replaces GLAUx's automatic parsing with Vanessa Gorman's hand-checked treebank where one exists (used for Anabasis I and III; the other books use GLAUx's automatic parsing).
  - `extract_perseus_sections.py` extracts a Perseus translation divided by book/chapter/section (Brownson's Anabasis).
  - `extract_fowler.py` extracts the English translation of the Apology, and `extract_solovyov.py` the Russian one (from a PDF of the plato.today page), both split by Stephanus section.
  - `glosses.tsv` and `glosses_ru.tsv` are the hand-written English and Russian meanings. Edit them to fix a meaning.
  - `apology.db` is the converted Apology. To fix a Russian meaning, edit `glosses_ru.tsv` and run:
    `python3 tools/export_site.py tools/apology.db tools/glosses_ru.tsv tools/eng_fowler_apology.json tools/rus_solovyov_apology.json data/apology.json apology stephanus tools/kat_berdzenishvili_apology.json`
    For Anabasis book N (1–7): `python3 tools/export_site.py tools/anabasisN.db tools/glosses_ru.tsv tools/eng_brownson_anabasisN.json - data/anabasis-N.json anabasis section` (for books with a file `tools/rus_anabasisN.json`, use it instead of `-`; it is an experimental translation made for this site)

## Adding a text
1. Run `tools/build.py` on a GLAUx XML file.
2. Write `glosses_ru.tsv` entries for any new words.
3. Run `tools/export_site.py` to make `data/<text>.json`.
4. Add the text to the `TEXTS` list at the top of `js/app.js`.

## Sources and licences
- Greek text, lemmas and parsing: [GLAUx](https://github.com/alekkeersmaekers/glaux) (A. Keersmaekers, KU Leuven), CC BY-SA 4.0. It is based on the [Perseus Digital Library](http://www.perseus.tufts.edu/). For the Apology, the annotation comes from Vanessa Gorman's hand-made treebank.
- Anabasis: Greek text from Perseus; parsing from GLAUx, corrected with [Vanessa Gorman's treebank](https://github.com/vgorman1/Greek-Dependency-Trees). English translation: C. L. Brownson (1922), Perseus, CC BY-SA.
- English translation of the Apology: H. N. Fowler, *Plato in Twelve Volumes* (1914), from [Perseus](https://github.com/PerseusDL/canonical-greekLit), CC BY-SA.
- Russian translation: M. S. Solovyov, *Творения Платона* (Moscow, 1899–1903), public domain; text as reprinted in Платон, Собр. соч. в 4 т., т. 1 (Moscow: Мысль, 1990), via plato.today. The editorial headings and A. A. Takho-Godi's notes are not included. Section breaks were placed automatically from the Stephanus margin marks and may be off by a phrase.
- Georgian translation: Levan Berdzenishvili, used with the translator's written permission (26 November 2026). This translation is **not** covered by the site's open licences; please ask the translator before reusing it. The notes and part headings are not included.
- English meanings: partly from the dictionary of the [Greek Study App](https://github.com/claypotfrog/GNTSP) by Jeff Jansen (GPL-3.0), partly written for this site.
- Russian meanings: written for this site.
- Code and data of this site: GPL-3.0 (see `LICENSE`). CC BY-SA 4.0 material can be included in GPL-3.0 works.

Corrections and suggestions are welcome as issues or pull requests.

---

# Ἀνάγνωσις: древнегреческий, слово за словом

Небольшой статический сайт для чтения древнегреческих текстов. Нажмите на любое слово, чтобы увидеть его словарную форму, значение (по-английски или по-русски) и полный разбор. Глаголы окрашены по времени, под каждым разделом можно показать перевод.


Публикация на GitHub Pages:
1. Загрузите эту папку в новый репозиторий.
2. Откройте **Settings → Pages**, выберите ветку `main` и папку `/ (root)`.
3. Через минуту сайт будет доступен по адресу `https://<имя>.github.io/<репозиторий>/`.

Чтобы исправить русское значение слова, отредактируйте `tools/glosses_ru.tsv` и выполните:
`python3 tools/export_site.py tools/apology.db tools/glosses_ru.tsv tools/eng_fowler_apology.json tools/rus_solovyov_apology.json data/apology.json`

## Noun declensions

`data/nouns.json` gives every noun its declension, gender and a full paradigm. It is built by `tools/noun_attest.py` (attested forms from GLAUx Attic prose: Xenophon, Plato, Thucydides, Lysias, Demosthenes, Isocrates) and `tools/noun_build.py` / `tools/noun_gen.py` (rule-based generation with accent placement). Attested forms take priority. Cells that are not attested are generated and shown in grey as reconstructed.

## Syntactic constructions

`tools/constructions.py treebank.xml data/<text>.json [book]` detects constructions in the dependency trees (Gorman/GLAUx) and writes `C` into the site data file. Run it after `export_site.py`, since the export overwrites the data file. Detected: accusative/nominative + infinitive, genitive/accusative absolute, supplementary participles (τυγχάνω, λανθάνω, φθάνω, διατελέω), participles after verbs of perception, future participle of purpose, articular infinitive, πρίν/ὥστε + infinitive, ὥστε + indicative, potential optative, contrary-to-fact, ἄν with infinitive/participle, oblique, iterative and final optatives, εἰ + optative, wishes with εἴθε.

## Experimental Georgian translation (Anabasis)

`tools/kat_anabasisN.json` holds an experimental Georgian translation by section, made for this site directly from the Greek. It is injected into `data/anabasis-N.json` as `tr.ka` (or pass it as the 8th argument of `export_site.py`). Book I is done so far.
