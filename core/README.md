# Core App

This Django app handles the core functionality of the JET system, primarily focusing on user management, authentication, profiles, and departments.

## Features

- User authentication and registration
- User profile management
- Department hierarchy management
- Dashboard functionality
- User leaderboard

## Models

- `User`: Custom user model extending Django's AbstractUser
- `Department`: Represents organizational departments with hierarchical structure
- `Profile`: Extended profile information for users
- `Intern`: Information about interns in the organization
- `SMEdetails`: Details of Subject Matter Expert sessions

## Views

- Authentication views (login, register, logout)
- Dashboard views
- User management views (list, detail, update)
- Department management views

## Management Commands

- `create_superuser`: Creates a superuser and default department
- `migrate_old_app`: Migrates data from the old app structure to the new structure

## Usage

The core app is the central component of the JET system and serves as the foundation for the other apps.
