# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015-2018 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Tests for user profile views."""

from __future__ import absolute_import, print_function

from flask import url_for
from flask_security import url_for_security
from helpers import login, sign_up
from invenio_accounts.models import User
from invenio_db import db
from test_validators import test_usernames

from invenio_userprofiles import InvenioUserProfiles
from invenio_userprofiles.models import UserProfile
from invenio_userprofiles.views import blueprint_ui_init, userprofile


def prefix(name, data):
    """Prefix all keys with value."""
    data = {"{0}-{1}".format(name, k): v for (k, v) in data.items()}
    data['submit'] = name
    return data


def test_profile_in_registration(base_app):
    """Test accounts registration form."""
    base_app.config.update(USERPROFILES_EXTEND_SECURITY_FORMS=True)
    InvenioUserProfiles(base_app)
    base_app.register_blueprint(blueprint_ui_init)
    app = base_app

    with app.test_request_context():
        register_url = url_for_security('register')

    with app.test_client() as client:
        resp = client.get(register_url)
        assert 'profile.username' in resp.get_data(as_text=True)
        assert 'profile.full_name' in resp.get_data(as_text=True)

        data = {
            'email': 'test_user@example.com',
            'password': 'test_password',
            'profile.username': 'TestUser',
            'profile.full_name': 'Test C. User',
        }
        resp = client.post(register_url, data=data, follow_redirects=True)

    with app.test_request_context():
        user = User.query.filter_by(email='test_user@example.com').one()
        assert user.profile.username == 'TestUser'
        assert user.profile.full_name == 'Test C. User'

    with app.test_client() as client:
        resp = client.get(register_url)
        data = {
            'email': 'newuser@example.com',
            'password': 'test_password',
            'profile.username': 'TestUser',
            'profile.full_name': 'Same Username',
        }
        resp = client.post(register_url, data=data)
        assert resp.status_code == 200
        assert 'profile.username' in resp.get_data(as_text=True)


def test_template_filter(app):
    """Test template filter."""
    with app.app_context():
        user = User(email='test@example.com', password='test_password')
        db.session.add(user)
        db.session.commit()
        user.profile = UserProfile(username='test_username', full_name='name')
        db.session.commit()

        assert userprofile(user.profile.user_id) == user.profile


def test_profile_view_not_accessible_without_login(app):
    """Test the user can't access profile settings page without logging in."""
    with app.test_request_context():
        profile_url = url_for('invenio_userprofiles.profile')

    with app.test_client() as client:
        resp = client.get(profile_url, follow_redirects=True)
        assert resp.status_code == 200
        assert 'name="login_user_form"' in str(resp.data)


def test_profile_view(app):
    """Test the profile view."""
    app.config['USERPROFILES_EMAIL_ENABLED'] = False
    with app.test_request_context():
        profile_url = url_for('invenio_userprofiles.profile')

    with app.test_client() as client:
        sign_up(app, client)
        login(app, client)
        resp = client.get(profile_url)
        assert resp.status_code == 200
        assert 'name="profile_form"' in str(resp.data)

        # Valid submission should work
        resp = client.post(profile_url, data=prefix('profile', dict(
            username=test_usernames['valid'],
            full_name='Valid Name', )))

        assert resp.status_code == 200
        data = resp.get_data(as_text=True)
        assert test_usernames['valid'] in data
        assert 'Valid' in data
        assert 'Name' in data

        # Invalid submission should not save data
        resp = client.post(profile_url, data=prefix('profile', dict(
            username=test_usernames['invalid_characters'],
            full_name='Valid Name', )))

        assert resp.status_code == 200
        assert test_usernames['invalid_characters'] in \
            resp.get_data(as_text=True)

        resp = client.get(profile_url)
        assert resp.status_code == 200
        assert test_usernames['valid'] in resp.get_data(as_text=True)

        # Whitespace should be trimmed
        client.post(profile_url, data=prefix('profile', dict(
            username='{0} '.format(test_usernames['valid']),
            full_name='Valid Name ', )))
        resp = client.get(profile_url)

        assert resp.status_code == 200
        data = resp.get_data(as_text=True)
        assert test_usernames['valid'] in data
        assert 'Valid Name ' not in data


def test_profile_name_exists(app):
    """Test the profile view."""
    app.config['USERPROFILES_EMAIL_ENABLED'] = False
    error_msg = 'Username already exists.'

    with app.app_context():
        profile_url = url_for('invenio_userprofiles.profile')

    # Create an existing user
    email1 = 'exiting@example.org'
    password1 = '123456'
    with app.test_client() as client:
        sign_up(app, client, email=email1, password=password1)
        login(app, client, email=email1, password=password1)
        assert client.get(profile_url).status_code == 200
        resp = client.post(profile_url, data=prefix('profile', dict(
            username='existingname', full_name='Valid Name',)))
        assert error_msg not in resp.get_data(as_text=True)

    # Create another user and try setting username to same as above user.
    with app.test_client() as client:
        sign_up(app, client)
        login(app, client)
        resp = client.get(profile_url)
        assert resp.status_code == 200

        resp = client.post(profile_url, data=prefix('profile', dict(
            username='existingname', full_name='Another name',
        )))
        assert resp.status_code == 200
        assert error_msg in resp.get_data(as_text=True)


def test_profile_case_change(app):
    """Test the profile view."""
    app.config['USERPROFILES_EMAIL_ENABLED'] = False
    error_msg = 'Username already exists.'

    with app.app_context():
        profile_url = url_for('invenio_userprofiles.profile')

    with app.test_client() as client:
        # Create a user
        sign_up(app, client)
        login(app, client)
        resp = client.get(profile_url)
        assert resp.status_code == 200

        data = prefix('profile', dict(
            username='valid', full_name='Another name', ))

        # Set the name first time
        resp = client.post(profile_url, data=data)
        assert resp.status_code == 200
        assert error_msg not in resp.get_data(as_text=True)

        # Set the name second time
        resp = client.post(profile_url, data=data)
        assert resp.status_code == 200
        assert error_msg not in resp.get_data(as_text=True)

        # Change case of the username
        data = prefix('profile', dict(
            username='Valid', full_name='Another name', ))

        resp = client.post(profile_url, data=data)
        assert resp.status_code == 200
        assert error_msg not in resp.get_data(as_text=True)


def test_send_verification_form(app):
    """Test send verification form."""
    mail = app.extensions['mail']

    with app.test_request_context():
        profile_url = url_for('invenio_userprofiles.profile')

    with app.test_client() as client:
        sign_up(app, client)
        login(app, client)
        resp = client.get(profile_url)
        assert resp.status_code == 200
        assert 'You have not yet verified your email address' in \
            resp.get_data(as_text=True)

        with mail.record_messages() as outbox:
            assert len(outbox) == 0
            resp = client.post(profile_url, data=prefix('verification', dict(
                send_verification_email='Title'
            )))
            assert len(outbox) == 1


def test_change_email(app):
    """Test send verification form."""
    mail = app.extensions['mail']
    error_msg = 'Username already exists.'

    with app.test_request_context():
        profile_url = url_for('invenio_userprofiles.profile')

    # Create an existing user
    email1 = 'exiting@example.org'
    password1 = '123456'
    with app.test_client() as client:
        sign_up(app, client, email=email1, password=password1)
        login(app, client, email=email1, password=password1)
        assert client.get(profile_url).status_code == 200

    with app.test_client() as client:
        sign_up(app, client)
        login(app, client)
        resp = client.get(profile_url)
        assert resp.status_code == 200

        data = prefix('profile', dict(
            username='test',
            full_name='Test User',
            email=app.config['TEST_USER_EMAIL'],
            email_repeat=app.config['TEST_USER_EMAIL'],
        ))

        # Test existing email of another user.
        data['profile-email_repeat'] = data['profile-email'] = email1
        resp = client.post(profile_url, data=data)
        assert 'exiting@example.org is already associated with an account.' \
            in resp.get_data(as_text=True)

        # Test empty email
        data['profile-email_repeat'] = data['profile-email'] = ''
        resp = client.post(profile_url, data=data)
        assert "Email not provided" in resp.get_data(as_text=True)

        # Test not an email
        data['profile-email_repeat'] = data['profile-email'] = 'sadfsdfs'
        resp = client.post(profile_url, data=data)
        assert "Invalid email address" in resp.get_data(as_text=True)

        # Test different emails
        data['profile-email_repeat'] = 'typo@example.org'
        data['profile-email'] = 'new@example.org'
        resp = client.post(profile_url, data=data)
        assert 'Email addresses do not match.' in resp.get_data(as_text=True)


def test_change_email_whitespace(app):
    """Test send verification form."""
    mail = app.extensions['mail']

    with app.test_request_context():
        profile_url = url_for('invenio_userprofiles.profile')

    with app.test_client() as client:
        sign_up(app, client)
        login(app, client)
        resp = client.get(profile_url)
        assert resp.status_code == 200

        data = prefix('profile', dict(
            username='test',
            full_name='Test User',
            email=app.config['TEST_USER_EMAIL'],
            email_repeat=app.config['TEST_USER_EMAIL'],
        ))

        with mail.record_messages() as outbox:
            assert len(outbox) == 0
            data['profile-email_repeat'] = data['profile-email'] = 'new@ex.org'
            resp = client.post(profile_url, data=data)
            assert 'Invalid email address' not in resp.get_data(as_text=True)
            # Email was sent for email address confirmation.
            assert len(outbox) == 1
