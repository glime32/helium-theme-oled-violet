# OLED Violet pour Helium

Noir OLED + violet `#61008A`, repris du thème KDE « OLED Violet ».

| Dossier | Extension | ID |
|---|---|---|
| `theme/` | **OLED Violet** — thème du navigateur (barres, onglets, champ d'adresse) | `ijefijobeglhilaepdlidhoccidilkjj` |
| `pages/` | **OLED Violet – pages internes** — `helium://settings`, extensions, historique, téléchargements, flags… | `gedllacmkafonphbnjkaebplipiiaogi` |

## Mise à jour automatique

Chaque push sur `main` lance l'action **Publier** : elle signe les deux extensions,
écrit `updates.xml` et publie sur <https://glime32.github.io/helium-theme-oled-violet/>.
Helium lit `update_url` dans les manifestes et installe la nouvelle version tout seul
(quelques heures max, ou tout de suite avec « Mettre à jour » dans `helium://extensions`,
mode développeur activé).

Pour changer une couleur : modifier `theme/manifest.json` ou `pages/oled.css`, puis push.

## Installation (une fois)

1. `helium://flags/#extensions-on-chrome-urls` → **Enabled**, puis relancer Helium
   (nécessaire pour `pages/`, sinon l'extension refuse de se charger).
2. Télécharger les deux `.crx` depuis la page GitHub Pages.
3. `helium://extensions` → mode développeur → glisser-déposer chaque `.crx` dans la page.

## Clés

Les clés de signature (`keys/*.pem`) fixent l'ID des extensions. Elles sont dans les
secrets du dépôt (`THEME_KEY`, `PAGES_KEY`) et en local dans `keys/` (ignoré par git).
Les perdre = nouvel ID = réinstaller à la main.

## Construire en local

```sh
pip install cryptography
python scripts/build.py 1.0.0 https://glime32.github.io/helium-theme-oled-violet   # → dist/
```
