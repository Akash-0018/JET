# JET System Migration Plan

This repository contains the JET application, which has been restructured from a single monolithic 'app' into multiple domain-specific Django apps.

## New Structure

The application has been divided into the following apps:

1. **core** - User management, authentication, profiles, departments
2. **learning** - Courses, certifications, enrollments, metrics
3. **communication** - Email functionality, templates, AI-generated content
4. **games** - All game-related functionality

## How to Complete the Migration

Follow these steps to complete the migration from the old structure to the new structure:

### 1. Apply Migrations

Migrations have been created for the new app structure. Apply them with:

```bash
python manage.py migrate
```

### 2. Create Default Department and Superuser

A management command has been created to set up the initial data:

```bash
python manage.py create_superuser
```

### 3. Migrate Data from Old App

A custom management command has been created to migrate data from the old app to the new structure:

```bash
python manage.py migrate_old_app
```

This command will copy all data from the old app tables to the corresponding new app tables.

### 4. Test the New Structure

After migrating the data, thoroughly test all functionality:

- Login and user management
- Email functionality
- Course and certification features
- Games and activities
- Metrics reporting

### 5. Clean Up

Once everything is working correctly:

1. Remove 'app' from INSTALLED_APPS in settings.py
2. Delete the old app directory
3. Update any remaining references to the old app in the codebase

## Troubleshooting

If you encounter issues during the migration:

1. Check the database tables to ensure data was properly migrated
2. Review server logs for any errors
3. If necessary, restore from the backup database (`db.sqlite3.backup`)

## Development Workflow

Going forward, new features should be added to the appropriate app based on functionality:

- User-related features: core app
- Learning and metrics features: learning app
- Email and AI features: communication app
- Games and activities: games app

Ensure that cross-app dependencies are properly managed with appropriate imports.
