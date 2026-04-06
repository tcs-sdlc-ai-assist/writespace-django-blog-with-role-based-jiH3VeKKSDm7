# Changelog

All notable changes to the WriteSpace project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [1.0.0] - 2024-12-01

### Added

- **Public Landing Page** — Hero section with gradient design, feature highlights, and latest posts preview accessible to all visitors.
- **Authentication System** — Login and registration with Django's built-in auth, session management via signed cookies, and role-based redirects for admin and regular users.
- **Blog CRUD** — Full create, read, update, and delete functionality for blog posts with UUID primary keys, ownership enforcement, and staff override permissions.
- **Admin Dashboard** — Staff-only dashboard displaying platform statistics (total posts, total users, admin count, recent posts in last 30 days) and quick action links.
- **User Management** — Staff-only user management panel with the ability to create new users with assigned roles (user/admin) and delete non-default, non-self users.
- **Default Admin Seeding** — Custom management command `create_default_admin` to bootstrap the initial superuser from environment variables.
- **Avatar System** — Custom template tag `render_avatar` displaying emoji-based avatars with role-differentiated styling (crown for admins, book for users).
- **Responsive UI** — Fully responsive design using Tailwind CSS CDN with mobile hamburger menus, card-based layouts, and gradient banners.
- **Static Files** — Whitenoise integration for serving static files with compressed manifest storage.
- **Vercel Deployment** — Vercel configuration with Python 3.12 runtime targeting the WSGI application.
- **Neon PostgreSQL** — Database configuration via `dj-database-url` supporting Neon PostgreSQL in production with SQLite fallback for local development.
- **Error Pages** — Custom 404 and 500 error pages with consistent gradient styling.