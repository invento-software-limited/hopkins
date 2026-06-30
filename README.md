# 🏠 Hopkins

A Frappe v16 website builder application for **Hopkins Blinds** — a blinds and window covering company based in the UK 🇬🇧. Built with [Frappe Builder](https://github.com/frappe/builder) 🏗️ and integrated with [ERPNext](https://github.com/frappe/erpnext).

> **Publisher:** Invento Software Limited  
> **Contact:** hello@invento.com.bd

---

## 📖 Table of Contents

- [Features](#features)
- [DocTypes](#doctypes)
- [API Endpoints](#api-endpoints)
- [Builder Pages & Components](#builder-pages--components)
- [Client Scripts](#client-scripts)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Development](#development)
- [CI/CD](#cicd)
- [Changelog](#changelog)
- [License](#license)

---

## ✨ Features

### 🌐 Marketing Website
A fully functional, responsive marketing website built with Frappe Builder, comprising:

| Page | Route | Description |
|------|-------|-------------|
| **Home** 🏡 | `/home` | Hero section with tagline "Solving the unsolvable in blinds — since 1753", services overview, animated logo carousel 🖼️ (trusted clients), testimonial slider 💬, and product showcase |
| **About Us** 👥 | `/about-us` | Company heritage and background, team/values presentation |
| **Products** 🛍️ | `/products` | Product catalogue with dynamic listing, category filtering, search, and pagination via ERPNext Item integration |
| **Heritage** 📜 | `/heritage` | Chronological timeline of the company's history since 1753 |
| **Contact Us** 📬 | `/contact-us` | Contact form with inquiry submission (creates CRM Leads) |

### 🤝 Customer Engagement
- 📧 **Newsletter subscription** — email capture with duplicate detection and automated Email Group management
- 📋 **Inquiry/Contact form** — creates **Lead** records in ERPNext with enquiry type classification
- ⭐ **Client testimonials** — auto-rotating slider with hover-pause
- 🏢 **Trusted client logos** — seamless infinite-scroll carousel

### ⚙️ Technical Features
- 🔍 **SEO-ready** — Case Studies with custom meta title, description, and OG image per entry
- 🍪 **Cookie consent banner** — customisable cookie categories (essential, analytics, marketing)
- 📊 **Google Analytics 4** integration (G-7K696X9R05)
- 🔔 **Toastify notifications** for real-time user feedback
- 📱 **Mobile-responsive** layout with responsive breakpoints
- 🎭 **3D fade-in animations** on page load with scroll-triggered transitions
- 🔐 **CSRF-protected** API calls from frontend forms

---

## 📦 DocTypes

### 📰 Case Study
- **Naming:** By fieldname (title)
- **Permissions:** System Manager (full), Guest (read)
- **Fields:** title, route, image, short_description, content, published + SEO metadata (meta_title, meta_description, meta_image)
- **Features:** Automatic route slugification from title, SEO context for rendering, guest-accessible (website published)

### 💬 Client Testimonial
- **Naming:** Hash (auto)
- **Permissions:** System Manager (full), Guest (read)
- **Fields:** person_name, trusted_client (link), description, publish_to_website
- **Features:** Linked to Trusted Client for branding context

### 🤝 Trusted Client
- **Naming:** By fieldname (client_name)
- **Permissions:** System Manager (full), Guest (read)
- **Fields:** client_name, logo (image), website_url

---

## 🔌 API Endpoints

All endpoints are `allow_guest=True` and whitelisted.

### 📬 `hopkins.api.submit_inquiry`
Submit a contact form enquiry. Creates a **Lead** document in ERPNext with an internal comment containing the enquiry type and message.

**Parameters:** `name`, `email`, `company`, `enquiry_type`, `country`, `message`

### 📧 `hopkins.api.subscribe_newsletter`
Subscribe an email to the "Newsletter" Email Group. Auto-creates the Email Group if it doesn't exist and prevents duplicate subscriptions.

**Parameters:** `email`, `first_name` (optional)

### 🛍️ `hopkins.api.get_products`
Retrieve paginated products from ERPNext via the `invento_webshop` ProductQuery engine.

**Parameters:** `page` (default: 1), `page_length` (default: 8), `search` (optional), `category` (optional)

**Returns:** Products with item_code, item_name, image, description, price (£ GBP formatted), stock code, pagination metadata.

---

## 🧱 Builder Pages & Components

### ♻️ Reusable Components
| Component | Description |
|-----------|-------------|
| **HOPKINS Navbar** 🧭 | Fixed-position transparent navigation bar that becomes opaque on scroll, with mobile hamburger menu |
| **HOPKINS Hero** 🦸 | Full-width hero section with tagline, heading, CTA button, and "What we do best" callout card |
| **HOPKINS Footer Section** 🦶 | Site footer with newsletter subscription form and links |
| **HOPKINS Yellow Top Corner** 💛 | Decorative yellow corner accent element |
| **HOPKINS Blue Bottom Corner** 💙 | Decorative blue corner accent element |
| **Cart Container** 🛒 | Mini-cart/shopping cart drawer |
| **Product Card** 🃏 | Individual product display card for catalogue grid |
| **Search Dropdown** 🔍 | Product search with dropdown suggestions |

### 🌍 Global Assets
- 🎨 **CSS** — Logo slider (infinite scroll), testimonial slider layout, slide transitions
- ⚡ **JavaScript** — Contact form submission handler (AJAX + Toastify feedback), logo carousel + testimonial slider logic with auto-advance and hover-pause

---

## 📜 Client Scripts

| Type | ID | Purpose |
|------|----|---------|
| 🎨 CSS | `CSS-c1e44` | Logo slider and testimonial carousel styles |
| 📜 JavaScript | `JavaScript-0bd33` | Contact form submission (AJAX POST to `submit_inquiry` with CSRF token, Toastify feedback) |
| 📜 JavaScript | `JavaScript-cdbe6` | Logo/track infinite scroll animation, testimonial slider with auto-advance (5s), hover pause, prev/next controls |

---

## 🛠️ Tech Stack

- 🐍 **Frappe** v16 (Python 3.14)
- 🏗️ **Frappe Builder** v1.24.7 — drag-and-drop website builder
- 🏪 **ERPNext** v16 — product catalogue & CRM (Lead management)
- 🟢 **Node.js** 24 — frontend asset pipeline
- 🗄️ **MariaDB** 10.6 — database
- 🔄 **Redis** — caching & queues
- 🐍 **Python** 3.14 — server-side runtime
- ✅ **Pre-commit** — code quality (ruff, prettier, eslint, semgrep)

---

## 🚀 Installation

Using the [bench](https://github.com/frappe/bench) CLI:

```bash
# Clone the bench and Frappe
bench init frappe-bench --frappe-branch version-16
cd frappe-bench

# Get required apps
bench get-app erpnext --branch version-16
bench get-app builder --branch v1.24.7

# Get Hopkins
bench get-app https://github.com/inventosoftware/Hopkins --branch develop

# Create site and install
bench new-site site1.local
bench --site site1.local install-app erpnext
bench --site site1.local install-app builder
bench --site site1.local install-app hopkins

# Build assets
bench build
```

---

## 💻 Development

### 📋 Prerequisites
- 🐍 Python 3.14+
- 🟢 Node.js 24+
- 🗄️ MariaDB 10.6+
- 🔄 Redis

### ✅ Code Quality

This app uses `pre-commit` for code formatting and linting:

```bash
cd apps/hopkins
pre-commit install
```

Pre-commit is configured to use:

| Tool | Purpose |
|------|---------|
| **ruff** 🦀 | Python linting, import sorting, and formatting |
| **eslint** 🧹 | JavaScript linting |
| **prettier** 💅 | JavaScript/Vue/SCSS formatting |
| **pre-commit-hooks** 🪝 | Trailing whitespace, merge conflict checks, AST validation |
| **semgrep** 🔍 | Frappe-specific security pattern scanning |

### 🧪 Running Tests

```bash
bench --site site1.local run-tests --app hopkins
```

---

## 🔄 CI/CD

Three GitHub Actions workflows are configured 🚀:

### 🧪 CI (`ci.yml`)
Triggers on push/PR to `version-16`. Runs full test suite:
- Sets up MariaDB, Redis, Python 3.14, Node.js 24
- Installs Frappe, ERPNext, Builder
- Installs Hopkins and runs all doctype unit tests

### 🔍 Linters (`linter.yml`)
Triggers on PRs. Runs:
- Pre-commit hooks (ruff, eslint, prettier, semgrep)
- `pip-audit` vulnerability check on Python dependencies

### 🏷️ Auto Tag and Release (`tag_and_release.yml`)
Triggers on PR merge to `version-16`. Automatically:
- Reads version from `hopkins/__init__.py`
- Looks up the corresponding changelog in `hopkins/change_log/v{major}/v{version}.md`
- Creates a Git tag and publishes a GitHub Release with changelog content

---

## 📝 Changelog

The full changelog is maintained in [changelog/changelog.md](changelog/changelog.md) following [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) format and [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

Individual release notes live in `hopkins/change_log/v0/` and are automatically consumed by the release pipeline.

**Current version:** v0.0.8

---

## 📄 License

MIT
