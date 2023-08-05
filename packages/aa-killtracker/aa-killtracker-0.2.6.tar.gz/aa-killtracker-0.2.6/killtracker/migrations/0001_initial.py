# Generated by Django 2.2.13 on 2020-07-23 22:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("eveuniverse", "0002_load_eveunit"),
        ("eveonline", "0012_index_additions"),
    ]

    operations = [
        migrations.CreateModel(
            name="EveKillmail",
            fields=[
                ("id", models.BigIntegerField(primary_key=True, serialize=False)),
                (
                    "time",
                    models.DateTimeField(
                        blank=True, db_index=True, default=None, null=True
                    ),
                ),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "solar_system",
                    models.ForeignKey(
                        blank=True,
                        default=None,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="eveuniverse.EveEntity",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Webhook",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        help_text="short name to identify this webhook",
                        max_length=64,
                        unique=True,
                    ),
                ),
                (
                    "webhook_type",
                    models.IntegerField(
                        choices=[(1, "Discord Webhook")],
                        default=1,
                        help_text="type of this webhook",
                    ),
                ),
                (
                    "url",
                    models.CharField(
                        help_text="URL of this webhook, e.g. https://discordapp.com/api/webhooks/123456/abcdef",
                        max_length=255,
                        unique=True,
                    ),
                ),
                (
                    "notes",
                    models.TextField(
                        blank=True,
                        default=None,
                        help_text="you can add notes about this webhook here if you want",
                        null=True,
                    ),
                ),
                (
                    "is_enabled",
                    models.BooleanField(
                        db_index=True,
                        default=True,
                        help_text="whether notifications are currently sent to this webhook",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="EveKillmailPosition",
            fields=[
                (
                    "killmail",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        primary_key=True,
                        related_name="position",
                        serialize=False,
                        to="killtracker.EveKillmail",
                    ),
                ),
                ("x", models.FloatField(blank=True, default=None, null=True)),
                ("y", models.FloatField(blank=True, default=None, null=True)),
                ("z", models.FloatField(blank=True, default=None, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="EveKillmailZkb",
            fields=[
                (
                    "killmail",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        primary_key=True,
                        related_name="zkb",
                        serialize=False,
                        to="killtracker.EveKillmail",
                    ),
                ),
                (
                    "location_id",
                    models.PositiveIntegerField(
                        blank=True, db_index=True, default=None, null=True
                    ),
                ),
                ("hash", models.CharField(blank=True, default="", max_length=64)),
                (
                    "fitted_value",
                    models.FloatField(blank=True, default=None, null=True),
                ),
                (
                    "total_value",
                    models.FloatField(
                        blank=True, db_index=True, default=None, null=True
                    ),
                ),
                (
                    "points",
                    models.PositiveIntegerField(
                        blank=True, db_index=True, default=None, null=True
                    ),
                ),
                (
                    "is_npc",
                    models.BooleanField(
                        blank=True, db_index=True, default=None, null=True
                    ),
                ),
                (
                    "is_solo",
                    models.BooleanField(
                        blank=True, db_index=True, default=None, null=True
                    ),
                ),
                (
                    "is_awox",
                    models.BooleanField(
                        blank=True, db_index=True, default=None, null=True
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Tracker",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        help_text="name to identify tracker. Will be shown on alerts posts.",
                        max_length=100,
                        unique=True,
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        blank=True,
                        default="",
                        help_text="Brief description what this tracker is for. Will not be shown on alerts.",
                    ),
                ),
                (
                    "require_max_jumps",
                    models.PositiveIntegerField(
                        blank=True,
                        default=None,
                        help_text="Require all killmails to be max x jumps away from origin solar system",
                        null=True,
                    ),
                ),
                (
                    "require_max_distance",
                    models.FloatField(
                        blank=True,
                        default=None,
                        help_text="Require all killmails to be max x LY away from origin solar system",
                        null=True,
                    ),
                ),
                (
                    "identify_fleets",
                    models.BooleanField(
                        default=False,
                        help_text="when true: kills are interpreted and shown as fleet kills",
                    ),
                ),
                (
                    "exclude_blue_attackers",
                    models.BooleanField(
                        default=False, help_text="exclude killmails with blue attackers"
                    ),
                ),
                (
                    "require_blue_victim",
                    models.BooleanField(
                        default=False,
                        help_text="only include killmails where the victim has standing with our group",
                    ),
                ),
                (
                    "require_min_attackers",
                    models.PositiveIntegerField(
                        blank=True,
                        default=None,
                        help_text="Require killmails to have at least given number of attackers",
                        null=True,
                    ),
                ),
                (
                    "require_max_attackers",
                    models.PositiveIntegerField(
                        blank=True,
                        default=None,
                        help_text="Require killmails to have no more than max number of attackers",
                        null=True,
                    ),
                ),
                (
                    "exclude_high_sec",
                    models.BooleanField(
                        default=False,
                        help_text="exclude killmails from high sec. Also exclude high sec systems in route finder for jumps from origin.",
                    ),
                ),
                (
                    "exclude_low_sec",
                    models.BooleanField(
                        default=False, help_text="exclude killmails from low sec"
                    ),
                ),
                (
                    "exclude_null_sec",
                    models.BooleanField(
                        default=False, help_text="exclude killmails from null sec"
                    ),
                ),
                (
                    "exclude_w_space",
                    models.BooleanField(
                        default=False, help_text="exclude killmails from WH space"
                    ),
                ),
                (
                    "require_min_value",
                    models.PositiveIntegerField(
                        blank=True,
                        default=None,
                        help_text="Require killmail's value to be greater or equal to the given value in M ISK",
                        null=True,
                    ),
                ),
                (
                    "exclude_npc_kills",
                    models.BooleanField(default=False, help_text="exclude npc kills"),
                ),
                (
                    "require_npc_kills",
                    models.BooleanField(
                        default=False,
                        help_text="only include killmails that are npc kills",
                    ),
                ),
                (
                    "ping_type",
                    models.CharField(
                        choices=[
                            ("PN", "(no ping)"),
                            ("PH", "@here"),
                            ("PE", "@everybody"),
                        ],
                        default="PN",
                        help_text="Options for pinging on every matching killmail",
                        max_length=2,
                    ),
                ),
                (
                    "is_posting_name",
                    models.BooleanField(
                        default=True,
                        help_text="whether posted messages include the tracker's name",
                    ),
                ),
                (
                    "is_enabled",
                    models.BooleanField(
                        db_index=True,
                        default=True,
                        help_text="toogle for activating or deactivating a tracker",
                    ),
                ),
                (
                    "exclude_attacker_alliances",
                    models.ManyToManyField(
                        blank=True,
                        default=None,
                        help_text="exclude killmails with attackers from one of these alliances",
                        related_name="tracker_exclude_attacker_alliances_set",
                        to="eveonline.EveAllianceInfo",
                    ),
                ),
                (
                    "exclude_attacker_corporations",
                    models.ManyToManyField(
                        blank=True,
                        default=None,
                        help_text="exclude killmails with attackers from one of these corporations",
                        related_name="tracker_exclude_attacker_corporations_set",
                        to="eveonline.EveCorporationInfo",
                    ),
                ),
                (
                    "origin_solar_system",
                    models.ForeignKey(
                        blank=True,
                        default=None,
                        help_text="Solar system to calculate distance and jumps from. When provided distance and jumps will be shown on killmail messages",
                        null=True,
                        on_delete=django.db.models.deletion.SET_DEFAULT,
                        related_name="tracker_origin_solar_systems_set",
                        to="eveuniverse.EveSolarSystem",
                    ),
                ),
                (
                    "require_attacker_alliances",
                    models.ManyToManyField(
                        blank=True,
                        default=None,
                        help_text="only include killmails with attackers from one of these alliances",
                        related_name="tracker_required_attacker_alliances_set",
                        to="eveonline.EveAllianceInfo",
                    ),
                ),
                (
                    "require_attacker_corporations",
                    models.ManyToManyField(
                        blank=True,
                        default=None,
                        help_text="only include killmails with attackers from one of these corporations",
                        related_name="tracker_required_attacker_corporations_set",
                        to="eveonline.EveCorporationInfo",
                    ),
                ),
                (
                    "require_attackers_ship_groups",
                    models.ManyToManyField(
                        blank=True,
                        default=None,
                        help_text="Only include killmails where at least one attacker is flying one of these ship groups",
                        limit_choices_to=models.Q(
                            models.Q(
                                ("eve_category_id", 65),
                                ("eve_category_id", 6),
                                _connector="OR",
                            ),
                            ("published", True),
                        ),
                        related_name="tracker_require_attackers_ship_groups_set",
                        to="eveuniverse.EveGroup",
                    ),
                ),
                (
                    "require_attackers_ship_types",
                    models.ManyToManyField(
                        blank=True,
                        default=None,
                        help_text="Only include killmails where at least one attacker is flying one of these ship types",
                        limit_choices_to=models.Q(
                            models.Q(
                                ("eve_group__eve_category_id", 65),
                                ("eve_group__eve_category_id", 6),
                                _connector="OR",
                            ),
                            ("published", True),
                        ),
                        related_name="tracker_require_attackers_ship_groups_set",
                        to="eveuniverse.EveType",
                    ),
                ),
                (
                    "require_constellations",
                    models.ManyToManyField(
                        blank=True,
                        default=None,
                        help_text="Only include killmails that occurred in one of these regions",
                        to="eveuniverse.EveConstellation",
                    ),
                ),
                (
                    "require_regions",
                    models.ManyToManyField(
                        blank=True,
                        default=None,
                        help_text="Only include killmails that occurred in one of these regions",
                        to="eveuniverse.EveRegion",
                    ),
                ),
                (
                    "require_solar_systems",
                    models.ManyToManyField(
                        blank=True,
                        default=None,
                        help_text="Only include killmails that occurred in one of these regions",
                        related_name="tracker_require_solar_systems_set",
                        to="eveuniverse.EveSolarSystem",
                    ),
                ),
                (
                    "require_victim_alliances",
                    models.ManyToManyField(
                        blank=True,
                        default=None,
                        help_text="only include killmails where the victim belongs to one of these alliances",
                        related_name="tracker_require_victim_alliances_set",
                        to="eveonline.EveAllianceInfo",
                    ),
                ),
                (
                    "require_victim_corporations",
                    models.ManyToManyField(
                        blank=True,
                        default=None,
                        help_text="only include killmails where the victim belongs to one of these corporations",
                        related_name="tracker_require_victim_corporations_set",
                        to="eveonline.EveCorporationInfo",
                    ),
                ),
                (
                    "require_victim_ship_groups",
                    models.ManyToManyField(
                        blank=True,
                        default=None,
                        help_text="Only include killmails where victim is flying one of these ship groups",
                        limit_choices_to=models.Q(
                            models.Q(
                                ("eve_category_id", 65),
                                ("eve_category_id", 6),
                                _connector="OR",
                            ),
                            ("published", True),
                        ),
                        related_name="tracker_require_victim_ship_groups_set",
                        to="eveuniverse.EveGroup",
                    ),
                ),
                (
                    "webhook",
                    models.ForeignKey(
                        help_text="Webhook URL for a channel on Discord to sent all alerts to",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="killtracker.Webhook",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="EveKillmailAttacker",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "damage_done",
                    models.BigIntegerField(blank=True, default=None, null=True),
                ),
                (
                    "is_final_blow",
                    models.BooleanField(
                        blank=True, db_index=True, default=None, null=True
                    ),
                ),
                (
                    "security_status",
                    models.FloatField(blank=True, default=None, null=True),
                ),
                (
                    "alliance",
                    models.ForeignKey(
                        blank=True,
                        default=None,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="evekillmailattacker_alliances_set",
                        to="eveuniverse.EveEntity",
                    ),
                ),
                (
                    "character",
                    models.ForeignKey(
                        blank=True,
                        default=None,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="evekillmailattacker_characters_set",
                        to="eveuniverse.EveEntity",
                    ),
                ),
                (
                    "corporation",
                    models.ForeignKey(
                        blank=True,
                        default=None,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="evekillmailattacker_corporations_set",
                        to="eveuniverse.EveEntity",
                    ),
                ),
                (
                    "faction",
                    models.ForeignKey(
                        blank=True,
                        default=None,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="evekillmailattacker_factions_set",
                        to="eveuniverse.EveEntity",
                    ),
                ),
                (
                    "killmail",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="attackers",
                        to="killtracker.EveKillmail",
                    ),
                ),
                (
                    "ship_type",
                    models.ForeignKey(
                        blank=True,
                        default=None,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="evekillmailattacker_shiptypes_set",
                        to="eveuniverse.EveEntity",
                    ),
                ),
                (
                    "weapon_type",
                    models.ForeignKey(
                        blank=True,
                        default=None,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="eveuniverse.EveEntity",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="EveKillmailVictim",
            fields=[
                (
                    "killmail",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        primary_key=True,
                        related_name="victim",
                        serialize=False,
                        to="killtracker.EveKillmail",
                    ),
                ),
                (
                    "damage_taken",
                    models.BigIntegerField(blank=True, default=None, null=True),
                ),
                (
                    "alliance",
                    models.ForeignKey(
                        blank=True,
                        default=None,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="evekillmailvictim_alliances_set",
                        to="eveuniverse.EveEntity",
                    ),
                ),
                (
                    "character",
                    models.ForeignKey(
                        blank=True,
                        default=None,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="evekillmailvictim_characters_set",
                        to="eveuniverse.EveEntity",
                    ),
                ),
                (
                    "corporation",
                    models.ForeignKey(
                        blank=True,
                        default=None,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="evekillmailvictim_corporations_set",
                        to="eveuniverse.EveEntity",
                    ),
                ),
                (
                    "faction",
                    models.ForeignKey(
                        blank=True,
                        default=None,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="evekillmailvictim_factions_set",
                        to="eveuniverse.EveEntity",
                    ),
                ),
                (
                    "ship_type",
                    models.ForeignKey(
                        blank=True,
                        default=None,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="evekillmailvictim_shiptypes_set",
                        to="eveuniverse.EveEntity",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
