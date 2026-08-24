# Ecliptys Forge

## 💡 Overview

Forge, from Ecliptys, is a **local-first repository intelligence and context engine for AI coding agents**.

Its goal is to help AI-powered programming agents understand software repositories before attempting to modify them. Forge analyzes the structure, code, dependencies, relationships, conventions, and other relevant project information to help agents retrieve the context they actually need for a given task.

Forge is designed to be **model-provider independent** and usable with both local and cloud-based AI models, while prioritizing local execution, privacy, and control.

> **Forge gives AI coding agents the ability to understand a repository before attempting to change it.**

---

## The Problem

AI coding agents can generate and modify code remarkably well, but their effectiveness depends heavily on the quality and relevance of the context they receive.

As software repositories grow, understanding a task may require information scattered across many files, modules, configurations, dependencies, tests, documentation, and external integrations.

Providing the entire repository to an AI model is inefficient and often unnecessary. It increases context consumption, can introduce irrelevant information, and may make it harder for the model to identify the relationships that actually matter to the task.

This problem affects both cloud-based and locally running models.

Forge aims to address this by helping agents **retrieve relevant repository context instead of blindly consuming more of it**.

Better context can lead to:

* Lower token consumption and cost.
* Better use of available context windows.
* More reliable code generation and modification.
* Better results from smaller and less expensive models.
* More practical local AI coding workflows.

---

## The Vision

Forge is built around a simple principle:

> **Understand before modifying.**

Before an AI coding agent changes a repository, it should have enough understanding of the relevant parts of that repository to make an informed decision.

Forge aims to provide that understanding through a structured representation of the project, including concepts such as:

* Repository structure.
* Programming languages and technologies.
* Modules and components.
* Dependencies.
* Classes, interfaces, functions, and other symbols.
* Relationships between code elements.
* Architectural patterns and conventions.
* Tests and validation mechanisms.
* External services and infrastructure.
* Configuration and resource dependencies.
* Project specifications and documentation.

The long-term vision is to make high-quality AI-assisted development practical even when using **smaller local models and affordable hardware**, while giving developers greater control over their code and data.

---

## Goals

Forge aims to:

* Analyze software repositories locally.
* Build a structured representation of a repository.
* Understand relationships between code elements and project components.
* Identify architectural patterns, conventions, and relevant project information.
* Retrieve context relevant to a specific development task.
* Provide repository intelligence to external AI coding agents.
* Integrate with AI agents through open and interoperable interfaces such as MCP.
* Remain independent of any specific AI model or model provider.
* Prioritize local-first execution, privacy, and developer control.
* Support both local and cloud-based models when desired.
* Be extensible through providers, adapters, and plugins.

---

## Non-Goals

Forge is not intended to:

* Be an IDE.
* Replace VS Code, Cursor, or other development environments.
* Train or provide its own foundation AI model.
* Replace Git or other version-control systems.
* Be a deployment platform.
* Be a generic unrestricted "vibe coding" tool.
* Execute arbitrary commands autonomously without appropriate controls.
* Support every programming language from day one.

Forge may eventually include agent capabilities, but its primary purpose is to provide **repository intelligence and context** that agents can use.

---

## How It Works

At a high level, Forge aims to transform a software repository into structured knowledge that can be queried according to a development task.

```text
             SOFTWARE REPOSITORY
                      │
                      ▼
                 ┌─────────┐
                 │ Analyze │
                 └────┬────┘
                      │
                      ▼
          ┌──────────────────────┐
          │ Repository           │
          │ Intelligence         │
          │                      │
          │ Structure            │
          │ Symbols              │
          │ Dependencies         │
          │ Relationships        │
          │ Architecture         │
          │ Conventions          │
          │ Specifications       │
          └──────────┬───────────┘
                     │
                     ▼
                   TASK
                     │
                     ▼
          ┌──────────────────────┐
          │ Relevant Context     │
          └──────────┬───────────┘
                     │
                     ▼
             AI CODING AGENT
                     │
                     ▼
            Plan → Modify → Validate
```

The goal is not to provide an AI model with more information.

The goal is to provide it with **better information**.

---

## Why Forge?

Traditional retrieval approaches can help an AI model find code that appears relevant to a query.

Forge aims to go further by understanding the **relationships between the relevant elements and the broader structure of the repository**.

For example, a task involving authentication may require more than finding files containing the word `authentication`.

The relevant context could involve a chain such as:

```text
AuthController
      │
      ▼
  AuthService
      │
      ├──────────────► LDAP Client
      │
      ▼
UserRepository
      │
      ▼
    User
      │
      ▼
 PostgreSQL
```

Understanding these relationships can help an AI coding agent determine not only **which files are relevant**, but also **why they are relevant and how they interact**.

Forge therefore focuses on **repository intelligence**, rather than treating the codebase as an undifferentiated collection of text.

---

## Project Status

🚧 **Early development**

Forge is currently in the design and initial development stage.

The architecture, APIs, supported languages, storage mechanisms, and agent integrations are expected to evolve as the project develops.

The project is intentionally being built incrementally, with an emphasis on understanding the underlying engineering concepts and maintaining a simple, extensible architecture.

---

## License

Apache License 2.0
