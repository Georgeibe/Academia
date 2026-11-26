# Ἀνάγνωσις: Ancient Greek, word by word

A small static website for reading Ancient Greek texts. Tap any word to see its dictionary form, meaning (English or Russian) and full parsing. Verbs are coloured by tense, and a translation can be shown under each section.

First text: Plato, *Apology of Socrates* (Stephanus pages 17–42).

## Publish on GitHub Pages
1. Create a new repository on GitHub and upload everything in this folder (keep the folder structure).
2. In the repository, go to **Settings → Pages**. Under "Build and deployment", choose **Deploy from a branch**, then branch `main` and folder `/ (root)`. Save.
3. After a minute the site is live at `https://<your-username>.github.io/<repository-name>/`.

The site is plain HTML, CSS and JavaScript with no build step. To try it on your own computer, run `python3 -m http.server` in this folder and open http://localhost:8000. Opening `index.html` directly from disk won't work, because browsers block loading the data file that way.

## Folders
- `index.html`, `css/`, `js/`: the website.
- `data/apology.json`: the text, every word's parsing, the dictionary (English and Russian meanings) and the English translation.
- `tools/`: scripts that produce the data.
  - `build.py` converts a GLAUx text to a word database.
  - `export_site.py` turns that database into the website JSON.
  - `extract_fowler.py` extracts the English translation, and `extract_solovyov.py` the Russian one (from a PDF of the plato.today page), both split by Stephanus section.
  - `glosses.tsv` and `glosses_ru.tsv` are the hand-written English and Russian meanings. Edit them to fix a meaning.
  - `apology.db` is the converted Apology. To fix a Russian meaning, edit `glosses_ru.tsv` and run:
    `python3 tools/export_site.py tools/apology.db tools/glosses_ru.tsv tools/eng_fowler_apology.json tools/rus_solovyov_apology.json data/apology.json`

## Adding a text
1. Run `tools/build.py` on a GLAUx XML file.
2. Write `glosses_ru.tsv` entries for any new words.
3. Run `tools/export_site.py` to make `data/<text>.json`.
4. Add the text to the `TEXTS` list at the top of `js/app.js`.

## Sources and licences
- Greek text, lemmas and parsing: [GLAUx](https://github.com/alekkeersmaekers/glaux) (A. Keersmaekers, KU Leuven), CC BY-SA 4.0. It is based on the [Perseus Digital Library](http://www.perseus.tufts.edu/). For the Apology, the annotation comes from Vanessa Gorman's hand-made treebank.
- English translation: H. N. Fowler, *Plato in Twelve Volumes* (1914), from [Perseus](https://github.com/PerseusDL/canonical-greekLit), CC BY-SA.
- Russian translation: M. S. Solovyov, *Творения Платона* (Moscow, 1899–1903), public domain; text as reprinted in Платон, Собр. соч. в 4 т., т. 1 (Moscow: Мысль, 1990), via plato.today. The editorial headings and A. A. Takho-Godi's notes are not included. Section breaks were placed automatically from the Stephanus margin marks and may be off by a phrase.
- English meanings: partly from the dictionary of the [Greek Study App](https://github.com/claypotfrog/GNTSP) by Jeff Jansen (GPL-3.0), partly written for this site.
- Russian meanings: written for this site.
- Code and data of this site: GPL-3.0 (see `LICENSE`). CC BY-SA 4.0 material can be included in GPL-3.0 works.

Corrections and suggestions are welcome as issues or pull requests.

---

# Ἀνάγνωσις: древнегреческий, слово за словом

Небольшой статический сайт для чтения древнегреческих текстов. Нажмите на любое слово, чтобы увидеть его словарную форму, значение (по-английски или по-русски) и полный разбор. Глаголы окрашены по времени, под каждым разделом можно показать перевод.

Первый текст: Платон, «Апология Сократа» (страницы Стефана 17–42), с английским переводом Фаулера и русским переводом М. С. Соловьёва.

Публикация на GitHub Pages:
1. Загрузите эту папку в новый репозиторий.
2. Откройте **Settings → Pages**, выберите ветку `main` и папку `/ (root)`.
3. Через минуту сайт будет доступен по адресу `https://<имя>.github.io/<репозиторий>/`.

Чтобы исправить русское значение слова, отредактируйте `tools/glosses_ru.tsv` и выполните:
`python3 tools/export_site.py tools/apology.db tools/glosses_ru.tsv tools/eng_fowler_apology.json tools/rus_solovyov_apology.json data/apology.json`
