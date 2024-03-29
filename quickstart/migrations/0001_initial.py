# Generated by Django 4.0.5 on 2022-06-08 21:05

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='QuestionImage',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('path', models.ImageField(upload_to='question_images')),
                ('data_base64_string', models.TextField(editable=False)),
            ],
        ),
        migrations.CreateModel(
            name='StateIcon',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('path', models.ImageField(upload_to='state_icons')),
                ('data_base64_string', models.TextField(editable=False)),
            ],
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.TextField(max_length=30)),
                ('code', models.TextField(max_length=2, unique=True, validators=[django.core.validators.RegexValidator('^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')])),
                ('added', models.DateTimeField(default=django.utils.timezone.now)),
                ('icon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quickstart.stateicon')),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('text', models.TextField()),
                ('image', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='quickstart.questionimage')),
                ('state', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='quickstart.state')),
            ],
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('text', models.TextField()),
                ('is_correct', models.BooleanField(default=False)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quickstart.question')),
            ],
        ),
    ]
