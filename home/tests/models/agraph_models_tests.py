# type: ignore
from unittest import TestCase

from home.agraph.agraph_models import GraphUser
from home.agraph.agraph_models import InstanceWithLabel
from home.agraph.agraph_models import URI


class TestGraphUser(TestCase):
    def setUp(self):
        self.valid_data = {
            "user_id": "12345",
            "email": "user@example.com",
            "givenName": "John",
            "job_title": "Developer",
            "seniority": "Senior",
            "worksFor": {"uri": "TechCompany"},
            "phdAwardedBy": URI(uri="MIT"),
            "career_stage": {"uri": "Mid"},
            "hasSkill": "Python",
            "hasExpertiseIn": "AI",
        }

    def test_graph_user_creation(self):
        """Test that a GraphUser object is created correctly with all fields."""
        user = GraphUser(**self.valid_data)

        self.assertEqual(user.user_id, "12345")
        self.assertEqual(user.email, "user@example.com")
        self.assertEqual(user.givenName, "John")
        self.assertEqual(user.job_title, "Developer")
        self.assertEqual(user.seniority, "Senior")
        self.assertIsInstance(user.worksFor, URI)
        self.assertEqual(user.worksFor.uri, "TechCompany")
        self.assertIsInstance(user.phdAwardedBy, URI)
        self.assertEqual(user.phdAwardedBy.uri, "MIT")
        self.assertIsInstance(user.career_stage, URI)
        self.assertEqual(user.career_stage.uri, "Mid")
        self.assertEqual(user.hasSkill, "Python")
        self.assertEqual(user.hasExpertiseIn, "AI")
        self.assertDictEqual(
            user.model_dump(exclude_unset=True),
            {
                "user_id": "12345",
                "email": "user@example.com",
                "givenName": "John",
                "job_title": "Developer",
                "seniority": "Senior",
                "worksFor": {"uri": "TechCompany"},
                "phdAwardedBy": {"uri": "MIT"},
                "career_stage": {"uri": "Mid"},
                "hasSkill": "Python",
                "hasExpertiseIn": "AI",
            },
        )

    def test_graph_user_creation_with_missing_fields(self):
        """Test that a GraphUser object handles missing fields gracefully."""
        partial_data = {
            "user_id": "12345",
            "email": "user@example.com",
            "givenName": "John",
            "worksFor": {"uri": "TechCompany"},
        }
        user = GraphUser(**partial_data)
        self.assertEqual(user.user_id, "12345")
        self.assertEqual(user.email, "user@example.com")
        self.assertEqual(user.givenName, "John")
        self.assertIsInstance(user.worksFor, URI)
        self.assertEqual(user.worksFor.uri, "TechCompany")
        self.assertEqual(user.job_title, None)
        self.assertEqual(user.seniority, None)
        self.assertDictEqual(user.model_dump(exclude_unset=True), partial_data)

    def test_graph_user_from_dict(self):
        """Test that a GraphUser object can be created from a dictionary."""
        valid_data = {
            "user_id": "12345",
            "email": "user@example.com",
            "givenName": "John",
            "job_title": "Developer",
            "seniority": "Senior",
            "worksFor": {"uri": "TechCompany"},
            "phdAwardedBy": URI(uri="MIT"),
            "career_stage": "This Field Will Be Converted To URI",
            "hasSkill": "Python",
            "hasExpertiseIn": "AI",
        }

        user = GraphUser.from_dict(valid_data)

        self.assertEqual(user.user_id, "12345")
        self.assertEqual(user.email, "user@example.com")
        self.assertEqual(user.givenName, "John")
        self.assertEqual(user.job_title, "Developer")
        self.assertEqual(user.seniority, "Senior")
        self.assertIsInstance(user.worksFor, URI)
        self.assertEqual(user.worksFor.uri, "TechCompany")
        self.assertIsInstance(user.phdAwardedBy, URI)
        self.assertEqual(user.phdAwardedBy.uri, "MIT")
        self.assertIsInstance(user.career_stage, URI)
        self.assertEqual(user.career_stage.uri, "This Field Will Be Converted To URI")
        self.assertEqual(user.hasSkill, "Python")
        self.assertEqual(user.hasExpertiseIn, "AI")
        self.assertDictEqual(
            user.model_dump(exclude_unset=True),
            {
                "user_id": "12345",
                "email": "user@example.com",
                "givenName": "John",
                "job_title": "Developer",
                "seniority": "Senior",
                "worksFor": {"uri": "TechCompany"},
                "phdAwardedBy": {"uri": "MIT"},
                "career_stage": {"uri": "This Field Will Be Converted To URI"},
                "hasSkill": "Python",
                "hasExpertiseIn": "AI",
            },
        )


class TestURI(TestCase):
    def setUp(self):
        self.valid_data = {
            "uri": "valid_uri_string",
        }

    def test_uri_creation(self):
        """Test that a URI object is created correctly with all fields."""
        uri = URI(**self.valid_data)

        self.assertEqual(uri.uri, "valid_uri_string")
        self.assertDictEqual(uri.model_dump(exclude_unset=True), self.valid_data)


class TestInstanceWithLabel(TestCase):
    def setUp(self):
        self.valid_data = {
            "id": "12345",
            "label": "A Readable Name",
        }

    def test_instance_with_label_creation(self):
        """Test that an InstanceWithLabel object is created correctly with all fields."""
        instance = InstanceWithLabel(**self.valid_data)

        self.assertEqual(instance.id, "12345")
        self.assertEqual(instance.label, "A Readable Name")
        self.assertDictEqual(instance.model_dump(exclude_unset=True), self.valid_data)
