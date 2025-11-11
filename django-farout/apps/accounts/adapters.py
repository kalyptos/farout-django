"""
Custom social account adapter for Discord OAuth.
Handles Discord user data and creates/updates User model.
"""
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.utils import timezone


class DiscordAccountAdapter(DefaultSocialAccountAdapter):
    """
    Custom adapter for Discord OAuth provider.
    Updates user model with Discord-specific fields.
    """

    def pre_social_login(self, request, sociallogin):
        """
        Invoked just after a user successfully authenticates via a social provider,
        but before the login is actually processed.
        """
        if sociallogin.is_existing:
            # Update last login time for existing users
            user = sociallogin.user
            user.update_last_login()

    def populate_user(self, request, sociallogin, data):
        """
        Populate user model with data from Discord.
        """
        user = super().populate_user(request, sociallogin, data)

        # Extract Discord data
        discord_data = sociallogin.account.extra_data

        # Set Discord-specific fields
        user.discord_id = str(discord_data.get('id', ''))
        user.avatar = discord_data.get('avatar', '')
        user.discriminator = discord_data.get('discriminator', '')

        # Set username from Discord username if not set
        if not user.username:
            user.username = discord_data.get('username', f'user_{user.discord_id}')

        # Set email if provided by Discord
        if not user.email and discord_data.get('email'):
            user.email = discord_data.get('email')

        return user

    def save_user(self, request, sociallogin, form=None):
        """
        Save the user after social login.
        """
        user = super().save_user(request, sociallogin, form)

        # Update Discord fields from social account data
        discord_data = sociallogin.account.extra_data

        user.discord_id = str(discord_data.get('id', ''))
        user.avatar = discord_data.get('avatar', '')
        user.discriminator = discord_data.get('discriminator', '')
        user.update_last_login()

        user.save()

        return user
