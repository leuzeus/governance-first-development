---
name: audit-project-governance
description: Auditer de manière contradictoire et fondée sur les preuves la gouvernance technique, informationnelle, documentaire, agentique et de livraison d’un dépôt, puis proposer des corrections proportionnelles au risque et au contexte du projet. Utiliser ce skill pour examiner AGENTS.md, politiques, ADR, autorités, gates CI, validations, revues, preuves, tentatives et verdicts produit, releases ou workflows d’agents; détecter contradictions temporelles, conflits d’autorité, dette de contexte, biais d’agents, faux blâme produit et surcharge organisationnelle; mesurer la friction; ou concevoir des voies EXPLORE, FAST, STANDARD, ASSURED et EMERGENCY.
---

# Auditer la gouvernance d’un projet

Version du skill : `0.2.0`

## Respecter le contrat

Évaluer simultanément la réduction du risque et le coût en temps, contexte,
tokens, validations, documentation et coordination. Ne pas confondre rigueur du
résultat et rigidité de la procédure.

Travailler en lecture seule sur les politiques, gates, workflows, scripts,
code et autorités. Ne créer que le livrable explicitement demandé. S’arrêter
avant toute réforme, sauf demande explicite d’implémentation.

Toujours :

- séparer faits, inférences et inconnues ;
- limiter toute conclusion aux preuves réellement obtenues ;
- distinguer `PASS`, `FAIL`, `SKIP` et `UNAVAILABLE` ;
- préserver secrets, compatibilité, provenance, rollback et autorités ;
- ne jamais traiter l’ancienneté, la complexité ou le coût comme une preuve de valeur ;
- ne jamais attribuer un échec au produit si aucun gate produit exécuté n’a observé cet échec ;
- ne jamais appliquer implicitement un modèle d’entreprise à un projet personnel.

## Calibrer l’audit

### Déterminer le contexte du projet

Classer le projet d’après les faits observables :

- `personal_agent_driven` : propriétaire principal unique, agents comme
  exécutants ou réviseurs ;
- `collaborative` : plusieurs contributeurs réguliers et responsabilités
  partagées ;
- `professional_operated` : utilisateurs, exploitation, engagements ou
  responsabilités organisationnelles établis ;
- `unknown` : preuves insuffisantes.

Ne recommander rôles séparés, CODEOWNERS, SLA, comité, politique d’incident ou
séparation des fonctions que si une frontière réelle le justifie. Dans un
projet personnel, préférer des **chapeaux d’autorité cumulables** :
`project_owner`, `technical_owner`, `evidence_operator`, `release_authority` et
`data_owner`.

### Choisir un profil

- `TARGETED` : question, contradiction, contrôle ou friction précis. Examiner
  seulement les autorités et parcours nécessaires.
- `STANDARD` : défaut. Échantillonner les domaines importants et au moins trois
  parcours représentatifs, dont le plus critique applicable.
- `DEEP` : demandé explicitement, préparation de réforme majeure, incident
  récurrent ou besoin d’assurance élevé. Faire l’inventaire complet et les six
  parcours A à F.

Choisir le profil minimal suffisant. Expliquer le choix. Ne jamais augmenter la
profondeur uniquement parce que des documents existent.

## Suivre le workflow

### 1. Établir l’état et la carte des autorités

Pour un dépôt Git, relever sans modifier :

```text
git status --short
git branch --show-current
git log -10 --oneline
```

Partir des routeurs et index. Suivre seulement les références nécessaires au
profil. Classer chaque source : autorité canonique, contrat ou schéma validé,
ADR, politique de domaine, plan/roadmap, document historique, projection,
fichier opérationnel, cache, miroir externe ou preuve environnementale.

Chercher une règle explicite de préséance. À défaut, signaler le manque sans
inventer une hiérarchie. Vérifier notamment :

- état actuel contredit par un historique voisin ;
- décision remplacée sans `superseded_by` ni statut non normatif ;
- deux autorités normatives incompatibles ;
- document plus récent supposé prioritaire sans règle ;
- issue, projet ou conversation traités comme source canonique ;
- règle spécialisée contournant un invariant supérieur.

En conflit non résolu, citer les deux sources et suspendre la conclusion
concernée.

### 2. Inventorier proportionnellement les contrôles

Pour chaque contrôle significatif retenu, relever : source, risque protégé,
déclencheur, périmètre, propriétaire ou chapeau, effet bloquant/informatif,
preuve, coût observable, dépendance externe, fallback/rollback, exception,
duplication, risque de faux blocage et valeur observée ou supposée.

Qualifier tout coût `mesuré`, `estimé à partir d’éléments observables` ou
`inconnu`. Ne jamais inventer temps, tokens, fréquence ou taux d’échec.

### 3. Rejouer les parcours utiles

Choisir parmi :

- A — documentation sans effet normatif ;
- B — bug local réversible ;
- C — changement fonctionnel interne ;
- D — surface publique ;
- E — persistance, compatibilité ou autorité ;
- F — sécurité, permission, publication, destruction, unsafe/FFI ou irréversibilité.

Pour chaque parcours sélectionné, relever lectures, gates, artefacts,
approbations, preuves, synchronisations et contraintes environnementales.
Qualifier chaque étape : pertinente, excessive, manquante, différable,
automatisable, compensable ou non contournable.

Inspecter les commandes avant exécution. Ne pas lancer une suite coûteuse pour
estimer son coût.

### 4. Examiner les risques propres aux agents

Rechercher avec une preuve concrète :

- généralisation depuis un seul test ou environnement ;
- absence d’échec présentée comme preuve de fonctionnement ;
- preuve CPU, simulée ou documentaire présentée comme preuve GPU, matérielle ou visuelle ;
- modification du contrat pour faire passer l’implémentation ;
- test reproduisant l’algorithme au lieu de vérifier le comportement ;
- abstraction sans second consommateur ni besoin établi ;
- élargissement silencieux du périmètre ;
- affirmation fondée sur une autorité périmée ;
- conformité procédurale utilisée comme substitut à la validité du résultat.

Ne pas signaler un biais théorique sans mécanisme ou exemple applicable au dépôt.

### 4.1 Auditer les tentatives et verdicts produit

Déclencher cette dimension lorsque le dépôt contient des manifests de tentative,
gates ordonnés, résultats de pipeline, classifications de panne, corrections,
retries, preuve invalidée, ou lorsqu’un échec opérationnel est présenté comme un
échec produit.

Lire alors [references/attempt-outcome-integrity.md](references/attempt-outcome-integrity.md)
en entier. Si les schémas GFD sont adoptés et disponibles, exécuter le validateur
en lecture seule :

```text
python -X utf8 scripts/audit_attempt_outcomes.py --root <repository> --records <record-root>
```

Sinon appliquer les mêmes règles sémantiques aux formats locaux et déclarer le
contrôle exécutable `UNAVAILABLE`. Ne pas imposer le schéma GFD à un projet qui ne
l’a pas adopté.

Séparer obligatoirement :

- statut d’exécution ;
- résultat et progression des gates ;
- statut de preuve `PASS|FAIL|SKIP|UNAVAILABLE` ;
- verdict produit `passed|failed|not_executed|not_applicable|inconclusive` ;
- classification `product_failure|operator_error|orchestration_error|environment_failure|unclassified`.

Un verdict produit `failed` exige un gate produit exécuté et échoué. Une
classification rétrospective ajoute un événement référant au résultat préservé ;
elle ne le réécrit pas. Une correction appliquée reste non validée jusqu’à une
tentative ultérieure probante. Avant d’invalider une preuve ou d’exiger un rerun,
vérifier la matérialité du changement et les gates réellement touchés.

### 5. Mesurer la friction

Rapporter lorsque observable :

```yaml
audit_profile: TARGETED|STANDARD|DEEP
project_context: personal_agent_driven|collaborative|professional_operated|unknown
authorities_loaded: 0
controls_examined: 0
governance_files_implicated: 0
useful_blocks_observed: 0
false_block_risks: 0
deferred_evidence: []
governance_friction: low|medium|high|unknown
evidence_quality: sufficient|partial|insufficient
```

Compter uniquement ce qui est effectivement observé. Justifier qualitativement
`governance_friction`; ne pas fabriquer de seuil universel.

### 6. Classifier et recommander

Lire [references/audit-reference.md](references/audit-reference.md) seulement
avant de classifier les constats ou de produire un rapport formel. Pour un
diagnostic bref sans classification, ne charger que les sections pertinentes.

Concevoir les corrections selon les effets réels :

- `EXPLORE` : diagnostic ou prototype isolé, sans prétention de livraison ;
- `FAST` : changement local, réversible et sans frontière critique ;
- `STANDARD` : comportement significatif ou surface publique additive ;
- `ASSURED` : persistance, migration, incompatibilité, secret, permission,
  publication, destruction, unsafe/FFI, autorité critique ou preuve matérielle indispensable ;
- `EMERGENCY` : overlay documenté avec contrôles compensatoires, expiration,
  rollback et régularisation.

Rendre les cérémonies adaptatives, jamais les invariants. Pour chaque
assouplissement, préciser contrôle compensatoire, escalade, rollback, risque
résiduel et signal de non-régression.

## Produire le livrable proportionné

- `TARGETED` : verdict, preuves, constat(s), risque, correction bornée et limites.
- `STANDARD` : ajouter carte des autorités, inventaire représentatif, parcours
  sélectionnés, métriques de friction et plan incrémental.
- `DEEP` : utiliser toute la structure de la référence et les six parcours.

Pour la dimension **Attempt Outcome Integrity**, donner exactement un verdict :
`conformant`, `partially_conformant`, `non_conformant`, `not_applicable` ou
`not_evaluable`. Ne pas transformer `not_applicable` ou `not_evaluable` en
réussite implicite.

Terminer par exactement une première étape seulement si l’utilisateur demande
un plan ou un audit formel. La rendre testable, réversible et non exécutée.

Avant de conclure, vérifier l’état Git si des artefacts ont été créés et
distinguer les changements préexistants. Indiquer explicitement si aucune
réforme n’a été appliquée.
