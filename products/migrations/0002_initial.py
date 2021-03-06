# Generated by Django 4.0 on 2021-12-20 03:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='like',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.user'),
        ),
        migrations.AddField(
            model_name='coursestat',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.course'),
        ),
        migrations.AddField(
            model_name='coursestat',
            name='stat',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.stat'),
        ),
        migrations.AddField(
            model_name='course',
            name='course_status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.coursestatus'),
        ),
        migrations.AddField(
            model_name='course',
            name='level',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='products.level'),
        ),
        migrations.AddField(
            model_name='course',
            name='sub_category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='products.subcategory'),
        ),
        migrations.AddField(
            model_name='course',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.user'),
        ),
        migrations.AddField(
            model_name='comment',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.course'),
        ),
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.user'),
        ),
        migrations.AddConstraint(
            model_name='like',
            constraint=models.UniqueConstraint(fields=('user', 'course'), name='unique likes'),
        ),
        migrations.AddConstraint(
            model_name='coursestat',
            constraint=models.UniqueConstraint(fields=('course', 'stat'), name='unique course_stats'),
        ),
    ]
