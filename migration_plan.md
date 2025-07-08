# Migration Plan: From Single 'app' to Multiple Django Apps

This document outlines the steps to migrate from the current single app structure to a more modular structure with multiple specialized Django apps.

## New Structure

1. **core** - User management, authentication, profiles, departments
2. **learning** - Courses, certifications, enrollments, metrics
3. **communication** - Email functionality, templates, AI-generated content
4. **games** - All game-related functionality

## Migration Steps

1. **Create new apps** ✓
   - Create the core, learning, communication, and games apps using `python manage.py startapp`

2. **Set up model structure** ✓
   - Distribute models from the original app to appropriate new apps
   - Update all imports and dependencies

3. **Update settings.py** ✓
   - Add the new apps to INSTALLED_APPS
   - Change AUTH_USER_MODEL from 'app.User' to 'core.User'

4. **Update urls.py** ✓
   - Update main project urls.py to include URLs from each app
   - Create urls.py in each app with appropriate URL patterns

5. **Move views and forms** ✓
   - Distribute views and forms from the original app to the appropriate new apps
   - Update all imports and dependencies

6. **Create migrations** ✓
   - Generate migrations for the new apps

7. **Data Migration**
   - Option 1: Export to JSON fixtures and import into new structure
   - Option 2: Use a custom management command to copy data from old tables to new tables
   - Option 3: SQL migration scripts

8. **Testing**
   - Test admin interface
   - Test all views and functionality
   - Verify data integrity

9. **Cleanup**
   - Remove the old 'app' from INSTALLED_APPS
   - Remove any references to the old app in the codebase
   - If everything is working, the old app can be removed

## Current Progress

- ✓ New app structure created
- ✓ Models, views, forms, and URLs properly distributed
- ✓ Settings and configuration updated
- ✓ Migrations created
- ✓ Admin interfaces set up
- ✓ Basic superuser created
- ❌ Data migration - TO BE DONE
- ❌ Testing - TO BE DONE
- ❌ Cleanup - TO BE DONE

## Next Steps

1. Create a custom management command to migrate data from the old app to the new apps
2. Test all functionality to ensure it works with the new structure
3. Once everything is working, clean up by removing the old 'app'
