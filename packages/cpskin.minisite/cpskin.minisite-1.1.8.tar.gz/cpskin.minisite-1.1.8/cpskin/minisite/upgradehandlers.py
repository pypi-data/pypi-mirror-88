# -*- coding: utf-8 -*-
PROFILE_ID = 'profile-cpskin.minisite:default'


def upgrade_viewlets(context):
    context.runImportStepFromProfile(PROFILE_ID, 'viewlets')


def move_cpskin_actions(context):
    context.runImportStepFromProfile(
        'profile-cpskin.minisite:to0003',
        'actions'
    )
    context.runImportStepFromProfile(PROFILE_ID, 'actions')


def add_minisite_menu(context):
    context.runImportStepFromProfile(PROFILE_ID, 'viewlets')
    context.runImportStepFromProfile(PROFILE_ID, 'actions')
