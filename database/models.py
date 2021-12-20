"""
@author: chuanchao.peng
@date: 2021/12/20 18:19
@file models.py
@desc:
"""

from peewee import Model, CharField, DateField, FloatField, PrimaryKeyField, TimeField

from database.engine import db


class Instrument(Model):
    instrument_id = CharField(max_length=20)


class DailyQuote(Model):
    id = PrimaryKeyField()
    instrument_id = CharField(max_length=20, verbose_name="品种ID", index=True)
    date = DateField(verbose_name='交易日期', index=True)
    open = FloatField(verbose_name='开盘价')
    high = FloatField(verbose_name='最高价')
    low = FloatField(verbose_name='最低价')
    close = FloatField(verbose_name='收盘价')

    class Meta:
        database = db


class HourlyQuote(Model):
    id = PrimaryKeyField()
    instrument_id = CharField(max_length=20, verbose_name="品种ID", index=True)
    date = DateField(verbose_name='交易日期', index=True)
    time = TimeField(verbose_name='交易时间')
    open = FloatField(verbose_name='开盘价')
    high = FloatField(verbose_name='最高价')
    low = FloatField(verbose_name='最低价')
    close = FloatField(verbose_name='收盘价')

    class Meta:
        database = db


def create_tables():
    db.create_tables([DailyQuote, HourlyQuote])
