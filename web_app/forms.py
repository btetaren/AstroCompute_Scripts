
from flask_wtf import Form
from wtforms import StringField, BooleanField, FileField, PasswordField
from wtforms.validators import DataRequired

from folder_upload import FolderField


class InputForm(Form):
    filename = FolderField('File Name', validators=[DataRequired()])
    source_detect = BooleanField('Enable source detection', default=False)
    target_name = StringField('Name of target', validators=[DataRequired()])
    obsdate = StringField("Observation Date", validators=[DataRequired()])
    reffreq = StringField("Reference Frequency (with units!)",
                          validators=[DataRequired()])

    intervalSizeH = 0
    intervalSizeM = 0
    intervalSizeS = 2
    # visibility = 'v404_jun22_B_Cc7_bp.ms'
    # visibility_uv='v404_jun22_B_Cc7_bp.ms'
    imageSize = 6000
    numberIters = 5000
    cellSize = '0.02arcsec'
    taylorTerms = 1
    myStokes = 'I'
    thre ='10mJy'
    spw_choice ='0~7:5~58'
    ##only for Aegean_ObjDet.py
    seed = 134656956
    flood = 4
    tele = 'VLA'
    lat=''#only set if not on list in scope2lat func of aegean.py
    ##only for casa_timing_script.py
    runObj='T'
    ind=1#only set if doing OD
    targetBox='2982,2937,2997,2947'#only set if not doing OD
    annulus_rad_inner=10
    annulus_rad_outer=20
    cutout='T'
    pix_shift_cutout=20
    big_data='T'
    outlierFile=''
    runClean='T'
    fit_cutout='F'
    fix_pos='T'
    do_monte='F'
    nsim=100
    par_fix='xyabp'
    integ_fit='B'
    uv_fit='F'
    do_monte_uv='F'
    uv_fix='F'
    stokes_param='I'#for uv fit
    def_times='F'
    startTimeH=''#only set if def_times='T'
    startTimeM=''#only set if def_times='T'
    startTimeS=''#only set if def_times='T'
    endTimeH=''#only set if def_times='T'
    endTimeM=''#only set if def_times='T'
    endTimeS=''#only set if def_times='T'
    rem_int=5
    lc_scale_unit='m'
    lc_scale_time='M'
    opt_clean='F'


class LoginForm(Form):
    inputid = StringField('Input ID', validators=[DataRequired()])
    passwd = PasswordField("Password", validators=[DataRequired()])
