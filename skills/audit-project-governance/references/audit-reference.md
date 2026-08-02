# Référence d’audit et modèle de rapport

Lire ce fichier en entier avant de classifier les constats ou de produire le
rapport.

## Sommaire

1. [Inventaire minimal](#1-inventaire-minimal)
2. [Parcours représentatifs](#2-parcours-représentatifs)
3. [Anti-patterns à rechercher](#3-anti-patterns-à-rechercher)
4. [Taxonomie obligatoire des constats](#4-taxonomie-obligatoire-des-constats)
5. [Actions autorisées](#5-actions-autorisées)
6. [Invariants non contournables](#6-invariants-non-contournables)
7. [Capsule de tâche proposée](#7-capsule-de-tâche-proposée)
8. [Structure du rapport](#8-structure-du-rapport)
9. [Profondeur et contexte](#9-profondeur-et-contexte)
10. [Intégrité des tentatives et résultats](#10-intégrité-des-tentatives-et-résultats)

## 1. Inventaire minimal

Inclure au minimum les familles suivantes lorsqu’elles existent :

- `AGENTS.md` et autres instructions obligatoires ;
- index, cockpits et documents à lire ;
- politiques, ADR, contrats et schémas ;
- sources de vérité, projections et règles de métadonnées ;
- compatibilité et inventaires de surfaces ;
- gates CI, validations locales et hooks pré-écriture ;
- planification, roadmap, milestone et Definition of Done ;
- revues, approbations et rapports ;
- preuves matérielles, visuelles ou externes ;
- GitHub et autres miroirs ;
- exceptions, urgences, publication et release.

Pour chaque contrôle significatif, utiliser les champs suivants :

| Champ | Contenu attendu |
|---|---|
| Identifiant | Nom stable ou identifiant local |
| Source | Fichier, section, workflow, hook ou commande |
| Risque protégé | Défaillance que le contrôle cherche à empêcher |
| Propriétaire | Déclaré, constaté ou inconnu |
| Déclencheur | Événement, chemin, effet ou type de changement |
| Périmètre | Domaine et changements actuellement couverts |
| Mode | Automatique ou manuel |
| Effet | Bloquant ou informatif |
| Preuve | Artefact ou résultat produit |
| Commandes | Commandes réellement imposées |
| Lectures | Documents obligatoires |
| Mises à jour | Documents ou miroirs à synchroniser |
| Coût temporel | Valeur et statut de preuve |
| Coût de contexte | Taille observable et statut de preuve |
| Dépendances | OS, GPU, service, secret ou outil externe |
| Repli | Rollback ou fallback |
| Exception | Voie d’exception et expiration |
| Duplication | Contrôles recouvrant la même propriété |
| Faux blocage | Cause et vraisemblance sans métrique inventée |
| Valeur | Observée, supposée ou inconnue |

Qualifier les valeurs de coût uniquement comme :

- `mesuré` : chronométrage, logs ou métrique directement observés ;
- `estimé à partir d’éléments observables` : taille de fichier, nombre de
  commandes, graphe de dépendances ou autre proxy cité ;
- `inconnu` : preuve insuffisante.

## 2. Parcours représentatifs

Sélectionner les scénarios selon le profil d’audit. `TARGETED` ne retient que le
ou les parcours nécessaires, `STANDARD` en retient au moins trois dont le plus
critique applicable, et `DEEP` rejoue les six scénarios :

| Scénario | Exemple et frontière |
|---|---|
| A | Typo, lien cassé ou clarification documentaire sans effet normatif |
| B | Diagnostic, message d’erreur, panic ou bug interne local et réversible |
| C | Logique ou refactoring borné sans contrat public |
| D | CLI, API, schéma, comportement documenté, UI, MCP ou agent |
| E | Format, migration, source de vérité, ownership, compatibilité ou autorité |
| F | Secret, permission, publication, réseau, processus, destruction, unsafe/FFI, irréversibilité ou fallback de sécurité |

Pour chacun, reconstruire :

- fichiers et règles obligatoires ;
- plan et artefacts ;
- gates et conditions environnementales ;
- approbations et revues ;
- preuves et mises à jour documentaires ;
- synchronisations externes.

Qualifier chaque étape : `pertinent`, `excessif`, `manquant`, `différable`,
`automatisable`, `contrôle compensatoire possible` ou `non contournable`.

## 3. Anti-patterns à rechercher

### Gouvernance uniforme

- même processus pour tous les niveaux de risque ;
- validation complète pour chaque petit changement ;
- plan, ADR ou milestone exigé pour un bug local ;
- revue indépendante sans distinction de criticité ;
- preuve matérielle sans lien avec le changement.

### Dette de contexte

- `AGENTS.md` excessivement long ;
- règles répétées dans plusieurs documents ;
- lectures globales pour des règles propres à un domaine ;
- historique chargé comme règle active ;
- politiques recopiées dans les prompts ;
- absence de routage ou de chargement progressif.

### Conflits temporels et d’autorité

- état actuel contredit par un récit historique encore formulé comme normatif ;
- décision remplacée sans statut ni lien `superseded_by` ;
- plusieurs autorités incompatibles sans règle de préséance ;
- document récent ou spécifique supposé prioritaire sans autorité explicite ;
- issue, tableau de projet, prompt ou conversation utilisés comme source de vérité ;
- règle locale contournant silencieusement un invariant supérieur.

### Risques de raisonnement des agents

- conclusion généralisée depuis un seul test ou environnement ;
- absence d’échec assimilée à une preuve positive ;
- preuve CPU ou simulée assimilée à une preuve GPU, matérielle ou visuelle ;
- contrat ou oracle ajusté pour valider l’implémentation ;
- test qui recopie l’algorithme au lieu d’observer son comportement ;
- abstraction prématurée ou périmètre élargi sans besoin établi ;
- affirmation fondée sur une source périmée ;
- conformité documentaire substituée à la validité du résultat.

### Sur-extension organisationnelle

- RACI, comité, SLA ou séparation des fonctions sans équipe ni engagement réel ;
- CODEOWNERS sans propriété collective effective ;
- rôles fictifs remplaçables par des chapeaux cumulables du propriétaire ;
- processus professionnel recommandé sans événement déclencheur observable ;
- coût organisationnel supérieur au risque propre au contexte du projet.

### Dette documentaire

- nombreux documents modifiés sans changement de surface ;
- vérité copiée manuellement ;
- projection générée traitée comme autorité manuelle ;
- rapport redondant avec un test ciblé ;
- artefact procédural sans consommateur réel.

### Dette de validation

- suite complète avant test ciblé ;
- gate sans relation avec les chemins, concepts ou effets modifiés ;
- gates dupliqués ou propriété testée plusieurs fois ;
- indisponibilité environnementale classée comme échec ;
- absence de `PASS`, `FAIL`, `SKIP` et `UNAVAILABLE` ;
- validation lourde répétée au lieu de la frontière d’intégration.
- échec de préparation, d’orchestration ou d’environnement présenté comme un échec produit ;
- verdict produit dérivé du statut global du workflow sans preuve que le gate produit a été exécuté ;
- correction déclarée validée avant une tentative ultérieure ;
- historique de résultat réécrit au lieu d’un addendum append-only.

### Gouvernance sans cycle de vie

- règle sans propriétaire ni risque explicite ;
- règle post-incident jamais réévaluée ;
- prose remplaçable par un test exécutable ;
- exception permanente devenue norme implicite ;
- règle obsolète toujours chargée ;
- valeur du contrôle jamais mesurée.

### Absence de voie rapide gouvernée

- aucune distinction entre exploration, bugfix et changement critique ;
- aucune voie d’urgence ou exception expirante ;
- raccourcis hors système faute de voie officielle ;
- preuve impossible à différer honnêtement ;
- exception plus coûteuse que la procédure normale ;
- absence de rollback ou régularisation.

## 4. Taxonomie obligatoire des constats

Attribuer une catégorie principale à chaque constat :

- `strictness_is_justified`
- `necessary_but_expensive`
- `overbroad_scope`
- `duplicate_control`
- `obsolete_control`
- `manual_but_automatable`
- `context_debt`
- `documentation_debt`
- `validation_debt`
- `false_block_risk`
- `missing_fast_path`
- `missing_exception_path`
- `unsafe_to_relax`
- `candidate_for_compensating_control`
- `insufficient_evidence`
- `temporal_authority_conflict`
- `authority_precedence_gap`
- `agent_reasoning_risk`
- `organizational_overreach`

Documenter chaque constat avec :

- preuve exacte : fichier, section, commande ou workflow ;
- risque protégé ;
- coût constaté et statut de preuve ;
- fréquence probable, exprimée qualitativement si elle n’est pas mesurée ;
- conséquence d’un assouplissement ;
- conséquence du statu quo ;
- confiance : haute, moyenne ou faible, avec justification ;
- recommandation préliminaire.

## 5. Actions autorisées

Associer chaque contrôle à exactement une action principale :

- `keep_as_is`
- `keep_but_route_conditionally`
- `keep_but_move_to_integration_boundary`
- `keep_but_convert_to_warning`
- `automate`
- `replace_with_executable_test`
- `merge_with_other_control`
- `reduce_required_context`
- `add_compensating_control`
- `add_expiring_exception`
- `deprecate`
- `remove_after_evidence`
- `requires_more_measurement`

Pour chaque assouplissement, préciser :

- risque actuellement protégé ;
- nouveau déclencheur ;
- changement de périmètre ;
- contrôle compensatoire ;
- condition d’escalade ;
- rollback ;
- impact sur les statuts et preuves ;
- risque résiduel ;
- signal permettant de détecter une dégradation.

## 6. Invariants non contournables

Vérifier leur existence et leur applicabilité :

- vérité sur les commandes réellement exécutées ;
- distinction `PASS`, `FAIL`, `SKIP`, `UNAVAILABLE` ;
- source de vérité explicite ;
- aucune écriture, migration ou publication implicite ;
- aucune exposition de secret ;
- historique conservé ou migré explicitement ;
- provenance et permissions ;
- fallback ou rollback des opérations critiques ;
- conclusion limitée à la preuve réelle ;
- aucun échec produit sans gate produit exécuté et échoué ;
- verdict, classification et correction conservés dans une lignée append-only ;
- autorités architecturales du projet maintenues séparées.

## 7. Capsule de tâche proposée

Adapter ce schéma aux autorités réellement observées :

```yaml
task:
  objective: ""
  lane: EXPLORE|FAST|STANDARD|ASSURED
  emergency_overlay: false
  affected_domains: []
  affected_public_surfaces: []
  persistent_or_critical_effects: []
  relevant_authorities: []
  active_invariants: []
  required_gates: []
  deferred_gates: []
  required_evidence: []
  compensating_controls: []
  non_goals: []
  escalation_triggers: []
```

Ne pas proposer ce mécanisme par défaut si le dépôt ne présente pas de dette de
contexte, de routage ou de sélection de gates.

## 8. Structure du rapport

### Résumé exécutif

Présenter le verdict, les frontières dont la rigueur est justifiée, les coûts
disproportionnés les mieux prouvés et les principales inconnues.

### Périmètre, méthode et état des preuves

Inclure :

- commit, branche et état Git ;
- autorités consultées et références suivies ;
- commandes exécutées ;
- commandes seulement inspectées ;
- limites et dépendances indisponibles.

### Carte des autorités

Séparer autorités canoniques, projections générées, documents historiques,
fichiers opérationnels, caches et miroirs externes.

### Inventaire des contrôles

Utiliser les champs de la section 1. Scinder le tableau si sa largeur nuit à la
lisibilité, mais conserver tous les champs significatifs.

### Parcours A à F

Pour chaque scénario, présenter le parcours actuel, son coût observable, les
étapes pertinentes, excessives ou manquantes et les contrôles non contournables.

### Constats classifiés

Utiliser la taxonomie de la section 4 et ordonner les constats par impact,
confiance et réversibilité, pas seulement par sévérité rhétorique.

### Modèle adaptatif proposé

Définir `EXPLORE`, `FAST`, `STANDARD`, `ASSURED` et l’overlay `EMERGENCY`.
Fournir les déclencheurs, contrôles minimaux, escalades, preuves, rollbacks et
interdictions de chaque voie.

### Invariants

Présenter les invariants transversaux et leur source dans le dépôt.

### Matrice de disposition

Associer chaque contrôle à une action de la section 5, son contrôle
compensatoire, son risque résiduel et la mesure de non-régression.

### Optimisation du travail des agents IA

Ne retenir que les mécanismes répondant à des symptômes observés : routeur
`AGENTS.md`, règles spécialisées, références stables, capsule de tâche,
sélection de gates, validation progressive et séparation preuve/résumé.

### Plan incrémental et réversible

Ordonner les corrections. Pour chaque incrément, donner périmètre, précondition,
preuve attendue, rollback et critère d’arrêt. Ne rien implémenter.

### Première étape recommandée

Fournir exactement une étape. La rendre :

- bornée à une seule réforme ;
- réversible ;
- vérifiable par un signal défini ;
- sans modification silencieuse d’autorité ;
- assortie d’un rollback ;
- explicitement non exécutée.

### Limites et état final

Déclarer les inconnues, les preuves différées ou indisponibles, l’état Git final
et confirmer qu’aucune politique active, gate, workflow, validation, autorité ou
code de production n’a été réformé.

## 9. Profondeur et contexte

### Profils

| Profil | Couverture minimale | Livrable |
|---|---|---|
| `TARGETED` | Autorités et parcours nécessaires au problème nommé | Verdict, preuves, constats, correction bornée, limites |
| `STANDARD` | Échantillon représentatif et au moins trois parcours | Carte, contrôles principaux, friction, constats, plan |
| `DEEP` | Inventaire complet et parcours A à F | Structure exhaustive de la section 8 |

### Contextes de projet

| Contexte | Interprétation |
|---|---|
| `personal_agent_driven` | Un propriétaire peut cumuler les chapeaux ; éviter les institutions fictives |
| `collaborative` | Formaliser les responsabilités réellement partagées |
| `professional_operated` | Examiner exploitation, sécurité, publication et engagements applicables |
| `unknown` | Déclarer l’incertitude et éviter les prescriptions organisationnelles |

Chapeaux utilisables dans un projet personnel : `project_owner`,
`technical_owner`, `evidence_operator`, `release_authority`, `data_owner`.

### Résumé de friction

Inclure ce bloc lorsqu’un audit formel mesure suffisamment d’éléments :

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

Les nombres sont des comptes observés, jamais des estimations. Expliquer le
niveau de friction par les parcours et coûts constatés plutôt que par un seuil
universel.

## 10. Intégrité des tentatives et résultats

Lorsque cette dimension est applicable, lire
[attempt-outcome-integrity.md](attempt-outcome-integrity.md), relever la
progression des gates et produire une section **Attempt Outcome Integrity** avec
un verdict parmi `conformant`, `partially_conformant`, `non_conformant`,
`not_applicable` et `not_evaluable`.

Le rapport sépare l’échec opérationnel observé du verdict sur le produit, cite
le dernier gate réussi et le gate terminal, contrôle la lignée append-only et
évalue la matérialité avant de recommander une invalidation ou un rerun.
