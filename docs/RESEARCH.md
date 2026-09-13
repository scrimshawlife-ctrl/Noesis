# Research Baseline

Last reviewed: 2026-09-13

Noesis uses the following literature as an evidence baseline. Publication status and limitations are recorded because the field is moving quickly.

## R-001 — Continuous latent reasoning

**Hao et al. (2024), _Training Large Language Models to Reason in a Continuous Latent Space_ (Coconut).** Preprint: arXiv:2412.06769.

Relevance: demonstrates a method that feeds the model's last hidden state back as subsequent input embeddings rather than decoding every intermediate state into text.

Use in Noesis: supports feasibility of controlled latent-reasoning experiments.

Limitation: does not establish that the latent state is a faithful or human-interpretable reasoning transcript.

## R-002 — Direct inter-agent latent communication

**Du et al. (2026), _Enabling Agents to Communicate Entirely in Latent Space_. ACL 2026. DOI: 10.18653/v1/2026.acl-long.1248.**

Relevance: Interlat uses continuous last hidden states for direct communication and reports experiments including heterogeneous models plus a learned compression process.

Use in Noesis: supports feasibility of EXP-002 after earlier capability gates.

Limitation: feasibility/task utility is not proof of a universal shared semantic language.

## R-003 — SAE reasoning-feature evidence

**Galichin et al. (2026), _I Have Covered All the Bases Here: Interpreting Reasoning Features in Large Language Models via Sparse Autoencoders_. AAAI 2026. DOI: 10.1609/aaai.v40i36.40334.**

Relevance: reports SAE features associated with uncertainty, exploratory thinking, and reflection, with steering experiments.

Use in Noesis: motivates sparse-feature and intervention tooling.

Limitation: feature interpretation requires independent falsification; association with reasoning vocabulary can be confounded.

## R-004 — Adversarial falsification of SAE reasoning features

**Ma et al. (2026), _Do Sparse Autoencoders Identify Reasoning Features in Language Models?_ arXiv:2601.05679.**

Relevance: reports that features selected as reasoning-related under standard contrastive methods are often driven by token-level/lexical correlates and fail stronger falsification criteria.

Use in Noesis: directly motivates `WF-004` lexical-trigger controls, negative examples, adversarial falsification, and conservative settlements.

Status: preprint; treat conclusions as important but not final consensus.

## R-005 — SAE feature consistency

**Song et al. (2026), _Mechanistic Interpretability Should Prioritize Feature Consistency in Sparse Autoencoders_. ACL 2026. DOI: 10.18653/v1/2026.acl-long.99.**

Relevance: shows SAE feature dictionaries can vary across runs and proposes pairwise dictionary mean correlation coefficient (PW-MCC) as a consistency metric.

Use in Noesis: run-to-run feature consistency is a required evaluation axis before feature promotion.

## R-006 — Causal CoT feature analysis

**Chen, Plaat, and van Stein (2026), _How Does Chain of Thought Think? Mechanistic Interpretability of Chain-of-Thought Reasoning with Sparse Autoencoding_. AAAI 2026. DOI: 10.1609/aaai.v40i36.40281.**

Relevance: combines sparse autoencoding with activation patching and reports causal differences by model scale.

Use in Noesis: supports combining feature discovery with intervention rather than relying on interpretation alone.

## R-007 — SAE steering

**Fang et al. (2026), _Controllable LLM Reasoning via Sparse Autoencoder-Based Steering_. ACL 2026.**

Relevance: provides evidence that identified SAE feature sets can be used for controlled steering in some reasoning settings.

Use in Noesis: informs causal-intervention methods and the need to separate control effectiveness from semantic interpretation.

## R-008 — Caution on latent-token faithfulness

**Zhang et al. (2025), _Do Latent Tokens Think? A Causal and Adversarial Analysis of Chain-of-Continuous-Thought_. arXiv:2512.21711.**

Relevance: questions whether continuous latent tokens faithfully encode reasoning and reports shortcut behavior in tested settings.

Use in Noesis: reinforces the rule that latent utility and latent interpretability are separate propositions.

## Evidence policy

Research citations justify experiment design, not project claims. Noesis results must be independently measured and settled under repository contracts. Conflicting literature is preserved rather than harmonized into false certainty.
