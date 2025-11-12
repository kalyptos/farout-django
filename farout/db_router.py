"""
Database router for directing models to appropriate databases.

Main Database (default):
- Core organization data (users, ships, fleet, squadron, etc.)

Communications Database (communications):
- Internal messaging
- Contact form submissions
- Isolated for performance and scaling
"""


class CommunicationsRouter:
    """
    Router for communications app models (messages, contact forms).

    Routes to 'communications' database for better isolation and scaling.
    """

    route_app_labels = {'communications'}

    def db_for_read(self, model, **hints):
        """
        Attempts to read communications models go to communications DB.
        """
        if model._meta.app_label in self.route_app_labels:
            return 'communications'
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write communications models go to communications DB.
        """
        if model._meta.app_label in self.route_app_labels:
            return 'communications'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if both models are in the communications app.
        Prevent relations between communications and other apps.
        """
        if (
            obj1._meta.app_label in self.route_app_labels or
            obj2._meta.app_label in self.route_app_labels
        ):
            # Both must be in communications app
            return (
                obj1._meta.app_label in self.route_app_labels and
                obj2._meta.app_label in self.route_app_labels
            )
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Ensure communications app only migrates on communications DB.
        """
        if app_label in self.route_app_labels:
            return db == 'communications'
        return None
