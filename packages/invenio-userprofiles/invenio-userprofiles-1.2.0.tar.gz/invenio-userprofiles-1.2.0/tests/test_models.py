# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015-2018 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Tests for user profile models."""

from __future__ import absolute_import, print_function

import pytest
from invenio_accounts.models import User
from invenio_db import db
from sqlalchemy.exc import IntegrityError
from test_validators import test_usernames

from invenio_userprofiles import InvenioUserProfiles, UserProfile


def test_userprofiles(app):
    """Test UserProfile model."""
    profile = UserProfile()

    # Check the username validator works on the model
    profile.username = test_usernames['valid']
    with pytest.raises(ValueError):
        profile.username = test_usernames['invalid_characters']
    with pytest.raises(ValueError):
        profile.username = test_usernames['invalid_begins_with_number']

    # Test non-validated attributes
    profile.first_name = 'Test'
    profile.last_name = 'User'
    assert profile.first_name == 'Test'
    assert profile.last_name == 'User'


def test_profile_updating(base_app):
    base_app.config.update(USERPROFILES_EXTEND_SECURITY_FORMS=True)
    InvenioUserProfiles(base_app)
    app = base_app

    with app.app_context():
        user = User(email='lollorosso', password='test_password')
        db.session.add(user)
        db.session.commit()

        assert user.profile is None

        profile = UserProfile(
            username='Test_User',
            full_name='Test T. User'
        )
        user.profile = profile
        user.profile.username = 'Different_Name'
        assert user.profile.username == 'Different_Name'
        assert profile.username == 'Different_Name'


def test_case_insensitive_username(app):
    """Test case-insensitive uniqueness."""
    with app.app_context():
        with db.session.begin_nested():
            u1 = User(email='test@example.org')
            u2 = User(email='test2@example.org')
            db.session.add(u1, u2)
        profile1 = UserProfile(user=u1, username="INFO")
        profile2 = UserProfile(user=u2, username="info")
        db.session.add(profile1)
        db.session.add(profile2)
        pytest.raises(IntegrityError, db.session.commit)


def test_case_preserving_username(app):
    """Test that username preserves the case."""
    with app.app_context():
        with db.session.begin_nested():
            u1 = User(email='test@example.org')
            db.session.add(u1)
        db.session.add(UserProfile(user=u1, username="InFo"))
        db.session.commit()
        profile = UserProfile.get_by_username('info')
        assert profile.username == 'InFo'


def test_delete_cascade(app):
    """Test that deletion of user, also removes profile."""
    with app.app_context():
        with db.session.begin_nested():
            u = User(email='test@example.org')
            db.session.add(u)
        p = UserProfile(user=u, username="InFo")
        db.session.add(p)
        db.session.commit()

        assert UserProfile.get_by_userid(u.id) is not None
        db.session.delete(u)
        db.session.commit()

        assert UserProfile.get_by_userid(u.id) is None


def test_create_profile(app):
    """Test that userprofile can be patched using UserAccount constructor."""
    with app.app_context():
        user = User(
            email='test@example.org',
        )
        db.session.add(user)
        db.session.commit()

        user_id = user.id
        patch_user = User(
            id=user_id,
            email='updated_test@example.org',
            profile={'full_name': 'updated_full_name'}
        )
        db.session.merge(patch_user)
        db.session.commit()

        patch_user = User(
            id=user_id,
            profile={'username': 'test_username'}
        )
        db.session.merge(patch_user)
        db.session.commit()

        user = User.query.filter(User.id == user_id).one()
        assert user.profile.full_name == 'updated_full_name'
        assert user.email == 'updated_test@example.org'
        assert user.profile.username == 'test_username'


def test_create_profile_with_null(app):
    """Test that creation with empty profile."""
    with app.app_context():
        user = User(
            email='test@example.org',
        )
        db.session.add(user)
        db.session.commit()

        assert user.profile is None
        user_id = user.id

        user = User(
            id=user_id,
            profile=None,
        )
        db.session.merge(user)
        db.session.commit()

        user = User.query.get(user_id)
        assert user.profile is None
